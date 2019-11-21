from django.urls import path
from .views import LoginView, RawReceiptListCreateView, RawReceiptDetailView, ProcessedReceiptListCreateView, ProcessedReceiptDetailView, ProcessedReceiptVerifyView

urlpatterns = [
    path('auth/login', LoginView.as_view(), name='auth-login'),
    path('receipt/raw', RawReceiptListCreateView.as_view(), name='raw-receipt-list'),
    path('receipt/raw/<int:pk>', RawReceiptDetailView.as_view(), name='raw-receipt-details'),
    path('receipt/processed', ProcessedReceiptListCreateView.as_view(), name='processed-receipt-list'),
    path('receipt/processed/<int:pk>', ProcessedReceiptDetailView.as_view(), name='processed-receipt-details'),

    path('receipt/processed/<int:pk>/verify', ProcessedReceiptVerifyView.as_view(), name='processed-receipt-verify'),
]
