from rest_framework import serializers
from .models import ExpenseIncome

class ExpenseIncomeSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ExpenseIncome
        fields = [
            'id', 'title', 'description', 'amount', 'transaction_type',
            'tax', 'tax_type', 'total', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total', 'created_at', 'updated_at']

    def get_total(self, obj):
        return obj.total
