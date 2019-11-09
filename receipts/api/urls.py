from django.urls import path
from .views import LoginView, RawReceiptListCreateView, RawReceiptDetailView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('receipt/rawreceipt/', RawReceiptListCreateView.as_view(), name='receipt-list'),
    path('receipt/rawreceipt/<int:pk>', RawReceiptDetailView.as_view(), name='receipt-details'),
]
