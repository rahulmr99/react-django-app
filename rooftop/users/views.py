from django.shortcuts import render

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView, RetrieveUpdateAPIView, get_object_or_404, ListCreateAPIView
)
# Create your views here.
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from users.models import User
from users.serializers import UserCreateSerializer, UserLoginSerializer
from rest_framework.response import Response


class UserCreateAPIView(CreateAPIView):
    """
    User Register APIView
    """
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    # def post(self, request, *args, **kwargs):
    #     request.data.update({"type": "2"})
    #     print(request.data, "MMMMMMMMMMMMMM")
    #     return self.create(request, *args, **kwargs)

class UserLoginAPIView(CreateAPIView):
    """
    User login APIView
    """
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)