from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import User
from .serializers import UserSerializer, UserSerializerInfo


class UserCreateView(APIView):
    """View para criação de novos usuários."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Usuário criado com sucesso.", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"detail": "Erro ao criar usuario", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserInfoView(APIView):
    """View para obter informações do usuário autenticado ou por UUID."""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        if user_id:
            if not request.user.is_staff and str(request.user.id) != user_id:
                return Response(
                    {"detail": "Acesso não autorizado."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            user = get_object_or_404(User, id=user_id)
        else:
            user = request.user

        serializer = UserSerializerInfo(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListView(APIView):
    """Lista todos os usuários ou apenas as informações do usuário logado."""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == "admin":
            users = User.objects.all()
            serializer = UserSerializerInfo(users, many=True)
        else:
            serializer = UserSerializerInfo(user)
        return Response(
            {"detail": "Dados retornados com sucesso.", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class UserUpdateView(UpdateAPIView):
    """View para atualizar dados de um usuário específico."""

    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"

    def get_object(self):
        """
        Permite que administradores editem qualquer usuário e restringe usuários comuns a editarem apenas seus próprios dados.
        """
        obj = super().get_object()

        if not self.request.user.is_staff and obj != self.request.user:
            raise PermissionDenied(
                {"detail": "Você não tem permissão para editar este usuário."}
            )
        return obj

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Usuário atualizado com sucesso.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Erro ao atualizar o usuário.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserDeleteView(DestroyAPIView):
    """View para deletar um usuário específico."""

    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = "id"

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        self.perform_destroy(user)
        return Response(
            {"detail": "Usuário deletado com sucesso."},
            status=status.HTTP_204_NO_CONTENT,
        )
