from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .models import User
from .serializers import UserSerializer, UserCreateSerializer


class UserList(APIView):

    """List all users, or create a new user"""

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """User retrieve, update or delete"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    no_authorization_errors = "No Authorizations"

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        user = self.get_object(pk)

        if user != request.user:
            return Response(
                {"errors": self.no_authorization_errors},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        if user != request.user:
            return Response(
                {"errors": self.no_authorization_errors},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
