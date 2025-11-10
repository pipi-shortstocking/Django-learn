from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate # Django의 기본 authenticate 함수, 우리가 설정한 DefaultAuthBackend인 TokenAuth 방식으로 유저 인증

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from .models import Profile

class RegisterSerializer(serializers.ModelSerializer): # 회원가입 시리얼라이저
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())] # 이메일에 대한 중복 검증
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password] # 비밀번호에 대한 검증
    )
    password2 = serializers.CharField(write_only=True, required=True) #비밀번호 확인을 위한 필드

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, data): # 추가적으로 비밀번호 일치 여부 확인
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didnt match."})

        return data

    def create(self, validated_data):
        # CREATE 요청에 대해 create 메소드를 오버라이딩, 유저를 생성하고 토큰을 생성하게 함
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    # write_only 옵션을 통해 클라이언트 -> 서버 방향의 역직렬화 가능, 서버 -> 클라이언트 방향의 직렬화 불가능

    def validate(self, data):
        # **은 파이썬에서 딕셔너리의 key-value 쌍을 함수의 키워드 인자로 풀어서 전달한다는 의미
        # 즉, data 딕셔너리의 값을 username=..., password=... 이런 식으로 authenticate 함수에 넘김
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user) # 토큰에서 유저를 찾아서 응답
            return token
        raise serializers.ValidationError({"error": "Unable to log in with provided credentials."})

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('nickname', 'position', 'subjects', 'image')