from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ExpenseIncome
from .serializers import ExpenseIncomeSerializer
from .permissions import IsOwnerOrSuperuser
from django.shortcuts import render


class ExpenseIncomeViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseIncomeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ExpenseIncome.objects.all().order_by('-created_at')
        return ExpenseIncome.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

def api_home(request):
    return render(request, 'expenses/api_home.html')
