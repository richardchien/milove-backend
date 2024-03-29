from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django import forms
from django.core import exceptions

from ..models.order import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('get_product_main_image_preview', 'product', 'price')
    # order item should not be edited
    readonly_fields = ('get_product_main_image_preview', 'product', 'price')
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.initial and 'status' in self.initial:
            choice_set = set(get_direct_dst_statuses(self.initial['status']))
            if self.should_hide_not_allowed_statuses():
                self.fields['status'].choices = filter(
                    lambda choice: choice[0] in choice_set,
                    Order.STATUSES
                )
            else:
                self.fields['status'].choices = map(
                    lambda choice: (choice[0], '√ %s' % choice[1])
                    if choice[0] in choice_set
                    else (choice[0], '× %s' % choice[1]),
                    Order.STATUSES
                )

    def should_hide_not_allowed_statuses(self):
        return self.request and not self.request.user.has_perm(
            'shop.randomly_switch_order_status')

    def clean(self):
        super().clean()
        if self.should_hide_not_allowed_statuses() \
                and self.initial \
                and 'status' in self.initial \
                and self.initial['status'] != self.cleaned_data['status']:
            # the current user cannot has no permission to
            # randomly switch order status,
            # so we restrict them
            if self.cleaned_data['status'] not in get_direct_dst_statuses(
                    self.initial['status']):
                raise exceptions.ValidationError(
                    _('Order status cannot be switched to %(dst_status)s '
                      'from %(src_status)s.') % {
                        'src_status': self.initial['status'],
                        'dst_status': self.cleaned_data['status']
                    }
                )
        return self.cleaned_data


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'discount_amount',
                    'paid_amount', 'comment', 'status', 'tracking_number')
    list_display_links = ('id', 'user')
    list_filter = ('status',)
    inlines = (OrderItemInline, ShippingAddressInline)
    ordering = ('-created_dt',)
    search_fields = ('id', 'user__username', 'user__email',
                     'comment', 'tracking_number')

    form = OrderForm
    fields = ('id', 'created_dt', 'user', 'total_price', 'discount_amount',
              'paid_amount', 'comment', 'status', 'last_status',
              'express_company', 'tracking_number')
    readonly_fields = ('id', 'created_dt', 'user', 'total_price',
                       'paid_amount', 'comment', 'last_status')

    def has_add_permission(self, request):
        # only users can create orders
        if request.user.is_superuser:
            # except superuser
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        # no one can delete orders
        if request.user.is_superuser:
            # except superuser
            return True
        return False

    def get_form(self, request, obj=None, **kwargs):
        # inject "request" object to form
        # https://stackoverflow.com/questions/2683689/django-access-request-object-from-admins-form-clean

        AdminForm = super().get_form(request, obj, **kwargs)

        class AdminFormWithRequest(AdminForm):
            def __new__(cls, *a, **kw):
                kw['request'] = request
                return AdminForm(*a, **kw)

        return AdminFormWithRequest


admin.site.register(Order, OrderAdmin)
