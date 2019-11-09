from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings
from .serializer import UserLoginSerializer, TokenSerializer, RawReceiptSerializer, ProcessedReceiptSerializer
from receiptreader.models import RawReceipt, ProcessedReceipt

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(jwt_payload_handler(user))
            })
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


# receipt model
class RawReceiptListCreateView(generics.ListCreateAPIView):
    queryset = RawReceipt.objects.all()
    serializer_class = RawReceiptSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)

class RawReceiptDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET rawreceipt/:id/
    PUT rawreceipt/:id/
    DELETE rawreceipt/:id/
    """

    queryset = RawReceipt.objects.all()
    serializer_class = RawReceiptSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            raw_receipt = self.queryset.get(pk=kwargs['pk'])
            return Response(RawReceiptSerializer(raw_receipt).data)
            pass
        except RawReceipt.DoesNotExist:
            return Response({
                "message": "Raw Receipt with id: {} does not exist".format(kwargs['pk'])
            }, status.HTTP_404_NOT_FOUND)

class ProcessedReceiptListCreateView(generics.ListCreateAPIView):
    queryset = ProcessedReceipt.objects.all()
    serializer_class = ProcessedReceiptSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)

class ProcessedReceiptDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET rawreceipt/:id/
    PUT rawreceipt/:id/
    DELETE rawreceipt/:id/
    """

    queryset = ProcessedReceipt.objects.all()
    serializer_class = ProcessedReceiptSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            raw_receipt = self.queryset.get(pk=kwargs['pk'])
            return Response(ProcessedReceiptSerializer(raw_receipt).data)
            pass
        except RawReceipt.DoesNotExist:
            return Response({
                "message": "Raw Processed Receipt with id: {} does not exist".format(kwargs['pk'])
            }, status.HTTP_404_NOT_FOUND)
