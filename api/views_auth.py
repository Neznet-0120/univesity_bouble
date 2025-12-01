from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'role': user.role,
            'first_name': user.first_name or '',
            'last_name': user.last_name or '',
            'group_id': user.group.id if user.group else None,
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'detail': 'Успешно вышел'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Ошибка при выходе'}, status=status.HTTP_400_BAD_REQUEST)
        