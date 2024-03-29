from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django.dispatch import receiver
from django.conf import settings
from jsonfield import JSONField

from .payment_method import PaymentMethod
from .order import Order
from .address import AbstractAddress

__all__ = ['BillingAddress', 'Payment']


class BillingAddress(AbstractAddress):
    class Meta:
        verbose_name = _('billing address')
        verbose_name_plural = _('billing addresses')

    payment = models.OneToOneField('Payment', on_delete=models.CASCADE,
                                   related_name='billing_address',
                                   verbose_name=_('payment'))


class Payment(models.Model):
    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')

    created_dt = models.DateTimeField(_('created datetime'), auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             related_name='payments',
                             on_delete=models.SET_NULL, verbose_name=_('user'))
    # "order" being null means the payment is of a recharge, but not an order
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='payments', verbose_name=_('order'),
                              blank=True, null=True)
    amount = models.FloatField(_('Payment|amount'))

    TYPE_STANDARD = 'standard'
    TYPE_RECHARGE = 'recharge'
    TYPES = (
        (TYPE_STANDARD, _('PaymentType|standard')),
        (TYPE_RECHARGE, _('PaymentType|recharge')),
    )

    type = models.CharField(_('type'), max_length=20,
                            choices=TYPES, default=TYPE_STANDARD)

    recharged = models.BooleanField(_('Payment|recharged'), default=False)

    use_balance = models.BooleanField(_('Payment|use balance'))
    # amount that need to be paid from balance
    amount_from_balance = models.FloatField(_('Payment|amount from balance'),
                                            default=0.0)
    # amount that actually have been paid from balance
    paid_amount_from_balance = models.FloatField(
        _('Payment|paid amount from balance'), default=0.0)

    use_point = models.BooleanField(_('Payment|use point'))
    # amount that need to be paid from point
    amount_from_point = models.FloatField(_('Payment|amount from point'),
                                          default=0.0)
    # point that actually have been paid
    paid_point = models.IntegerField(_('Payment|paid point'), default=0)

    METHODS = (
        (PaymentMethod.PAYPAL, _('PayPal')),
        (PaymentMethod.CREDIT_CARD, _('credit card'))
    )

    method = models.CharField(_('Payment|method'), null=True, blank=True,
                              max_length=20, choices=METHODS)
    vendor_payment_id = models.CharField(_('Payment|vendor payment ID'),
                                         null=True, blank=True, max_length=100)
    extra_info = JSONField(_('extra information'), default={}, blank=True)

    STATUS_PENDING = 'pending'
    STATUS_CLOSED = 'closed'
    STATUS_FAILED = 'failed'
    STATUS_SUCCEEDED = 'succeeded'

    STATUSES = (
        (STATUS_PENDING, _('PaymentStatus|pending')),
        (STATUS_CLOSED, _('PaymentStatus|closed')),
        (STATUS_FAILED, _('PaymentStatus|failed')),
        (STATUS_SUCCEEDED, _('PaymentStatus|succeeded')),
    )

    status = models.CharField(_('status'), max_length=20, choices=STATUSES,
                              default=STATUS_PENDING)

    @staticmethod
    def status_changed(old_obj, new_obj):
        if new_obj.type == Payment.TYPE_STANDARD \
                and new_obj.status in (Payment.STATUS_CLOSED,
                                       Payment.STATUS_FAILED):
            # payment closed or failed, refund paid balance and point
            new_obj.user.info.increase_point(new_obj.paid_point)
            new_obj.user.info.increase_balance(
                new_obj.paid_amount_from_balance)

            # clean payment object, in case of duplicated refund
            new_obj.paid_point = 0
            new_obj.paid_amount_from_balance = 0.0

        if new_obj.type == Payment.TYPE_RECHARGE \
                and new_obj.status == Payment.STATUS_SUCCEEDED \
                and not new_obj.recharged:
            # payment succeeded, increase the balance
            new_obj.user.info.increase_balance(new_obj.amount)
            new_obj.recharged = True

    def __str__(self):
        return _('Payment #%(pk)s') % {'pk': self.pk}


@receiver(signals.pre_save, sender=Payment)
def payment_pre_save(instance, **kwargs):
    old_instance = None
    if instance.pk:
        old_instance = Payment.objects.get(pk=instance.pk)

    if old_instance and old_instance.status != instance.status:
        instance.status_changed(old_instance, instance)


@receiver(signals.post_save, sender=Payment)
def payment_post_save(instance, **kwargs):
    # put this code in post_save is because that
    # the order should notify user and staffs after becoming "paid",
    # and that notification needs the payment object related to the order,
    # which means the payment with status "succeeded" must be save first
    if instance.type == Payment.TYPE_STANDARD \
            and instance.status == Payment.STATUS_SUCCEEDED \
            and instance.order.status == Order.STATUS_UNPAID:
        # payment succeeded, mark the order as paid
        instance.order.status = Order.STATUS_PAID
        instance.order.paid_amount = instance.amount
        instance.order.save()
