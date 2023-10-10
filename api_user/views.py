from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse_lazy

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.permissions import IsAuthenticated, AllowAny


from .serializers import LoginSerializer, UserListSerializer, UserRegistrationSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from .permissions import IsOwnerOrSuperUser, IsSuperUser


User = get_user_model()


class UserListAPIView(generics.ListAPIView):
    # ユーザーリスト
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsSuperUser]


class UserDetailAPIView(generics.RetrieveAPIView):
    # 詳細画面
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsOwnerOrSuperUser]
    lookup_field = 'id'


class UserRegistrationAPIView(generics.GenericAPIView):
    # ユーザー登録
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # JWTトークンの生成
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    # ログイン
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # JWTトークンの生成
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    # ログアウト
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response("refresh_token is required", status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            # もしすでに存在するトークンがあればブラックリストに追加
            outstanding_token = OutstandingToken.objects.filter(
                token=refresh_token).first()
            if outstanding_token:
                blacklisted_token = BlacklistedToken(token=outstanding_token)
                blacklisted_token.save()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(generics.GenericAPIView):
    # パスワード再設定
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                # メール送信処理
                current_site = get_current_site(request)
                mail_subject = 'パスワード再設定用メール'
                message = f'''
パスワードを再設定するには、以下のリンクをクリックしてください。

http://{current_site.domain}/api/password_reset/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}/

もし心当たりがない場合は、このメールを無視してください。
'''
                send_mail(mail_subject, message, None, [user.email])
                return Response({"status": "パスワード再設定用のメールが送信されました"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(generics.GenericAPIView):
    # パスワード再設定確認
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(id=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({"status": "パスワードが正常に変更されました"}, status=status.HTTP_200_OK)

            return Response({"status": "パスワードリセットトークンが無効です"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
