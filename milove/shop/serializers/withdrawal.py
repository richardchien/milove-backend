from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models.withdrawal import *

__all__ = ['WithdrawalAddSerializer']


class WithdrawalAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        exclude = ('user',)
        read_only_fields = ('created_dt', 'processed_amount', 'status')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        with transaction.atomic():
            withdrawal = super().create(validated_data)
            user.info.decrease_balance(withdrawal.amount)
        return withdrawal

    def validate(self, attrs):
        if attrs['amount'] < 0.0 \
                or attrs['amount'] > self.context['request'].user.info.balance:
            raise ValidationError(_('Amount is not valid.'))
        return super().validate(attrs)
