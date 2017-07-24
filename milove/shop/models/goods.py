import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from imagekit import ImageSpec
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Brand(models.Model):
    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')

    name = models.CharField(max_length=200, verbose_name=_('name'))

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    name = models.CharField(max_length=50, verbose_name=_('name'))
    super_category = models.ForeignKey('self', blank=True, null=True,
                                       on_delete=models.CASCADE,
                                       verbose_name=_('super category'))

    def __str__(self):
        if not self.super_category:
            return self.name
        return str(self.super_category) + ' - ' + str(self.name)


class Attachment(models.Model):
    class Meta:
        verbose_name = _('attachment')
        verbose_name_plural = _('attachments')

    name = models.CharField(max_length=50, verbose_name=_('name'))

    def __str__(self):
        return self.name


_prod_image_path = 'products'
_prod_image_placeholder_path = os.path.join(_prod_image_path,
                                            'placeholder-120x120.png')


class _Thumbnail(ImageSpec):
    processors = [ResizeToFill(120, 120)]
    format = 'JPEG'
    options = {'quality': 80}


class ProductImage(models.Model):
    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')

    image = models.ImageField(upload_to=_prod_image_path,
                              verbose_name=_('image'))
    image_thumb = ImageSpecField(source='image', spec=_Thumbnail)
    product = models.ForeignKey('Product', on_delete=models.CASCADE,
                                related_name='images',
                                verbose_name=_('product'))

    def __str__(self):
        return str(self.image)


class Product(models.Model):
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    publish_dt = models.DateTimeField(default=timezone.now, verbose_name=_(
        'Product|publish datetime'))

    sold = models.BooleanField(default=False, verbose_name=_('Product|sold'))
    sold_dt = models.DateTimeField(null=True, blank=True,
                                   verbose_name=_('Product|sold datetime'))

    @staticmethod
    def sold_changed(_, new_obj):
        if new_obj.sold is True:
            new_obj.sold_dt = timezone.now()
        else:
            new_obj.sold_dt = None

    brand = models.ForeignKey('Brand', on_delete=models.CASCADE,
                              related_name='products',
                              verbose_name=_('Product|brand'))
    name = models.CharField(max_length=200, blank=True,
                            verbose_name=_('Product|name'))
    style = models.CharField(max_length=200, verbose_name=_('Product|style'))
    size = models.CharField(max_length=20, blank=True,
                            verbose_name=_('Product|size'))

    CONDITION_S = 'S'
    CONDITION_A_PLUS = 'A+'
    CONDITION_A = 'A'
    CONDITION_B = 'B'
    CONDITION_C = 'C'
    CONDITION_D = 'D'

    CONDITIONS = (
        (CONDITION_S, _('ProductCondition|S')),
        (CONDITION_A_PLUS, _('ProductCondition|A+')),
        (CONDITION_A, _('ProductCondition|A')),
        (CONDITION_B, _('ProductCondition|B')),
        (CONDITION_C, _('ProductCondition|C')),
        (CONDITION_D, _('ProductCondition|D')),
    )

    condition = models.CharField(max_length=2, choices=CONDITIONS,
                                 verbose_name=_('Product|condition'))

    categories = models.ManyToManyField('Category', related_name='products',
                                        verbose_name=_('Product|categories'))
    attachments = models.ManyToManyField('Attachment', blank=True,
                                         verbose_name=_('Product|attachments'))
    description = models.TextField(verbose_name=_('Product|description'))
    original_price = models.FloatField(verbose_name=_('Product|original price'))
    price = models.FloatField(verbose_name=_('Product|price'))

    main_image = models.ImageField(default=_prod_image_placeholder_path,
                                   upload_to=_prod_image_path,
                                   verbose_name=_('Product|main image'))
    main_image_thumb = ImageSpecField(source='main_image', spec=_Thumbnail)

    def __str__(self):
        return ('#%s ' % self.pk) + self.brand.name \
               + (' ' + str(self.name) if self.name else '')
