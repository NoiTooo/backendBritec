
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import Organization

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name',
                  'last_name', 'is_active', 'is_staff', 'date_joined', 'organizations']


class UserRegistrationSerializer(serializers.ModelSerializer):
    # User登録
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name',
                  'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'})

        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    # Userログイン
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get(
                'request'), username=email, password=password)

            if not user:
                raise serializers.ValidationError('Invalid email or password.')

        else:
            raise serializers.ValidationError(
                'Both email and password fields are required.')

        data['user'] = user
        return data


class PasswordResetSerializer(serializers.Serializer):
    # パスワード再設定
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Emailが登録されていません")
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        user = User.objects.get(email=email)
        # トークン生成処理（実際にはメール送信などを行う）
        return user


class PasswordResetConfirmSerializer(serializers.Serializer):
    # パスワード再設定確認
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("パスワードが一致しません")
        return data
