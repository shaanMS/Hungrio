from rest_framework import serializers
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CaptchaJWTSerializer(TokenObtainPairSerializer):
    captcha_key = serializers.CharField()
    captcha_value = serializers.CharField()

    def validate(self, attrs):
        captcha_key = attrs.pop('captcha_key')
        captcha_value = attrs.pop('captcha_value')

        # captcha verify
        if not CaptchaStore.objects.filter(
            hashkey=captcha_key,
            response=captcha_value
        ).exists():
            raise serializers.ValidationError("Invalid captcha")

        return super().validate(attrs)
