# from rest_framework import serializers
# from captcha.models import CaptchaStore
# from captcha.helpers import captcha_image_url
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# class CaptchaJWTSerializer(TokenObtainPairSerializer):
#     captcha_key = serializers.CharField()
#     captcha_value = serializers.CharField()

#     def validate(self, attrs):
#         captcha_key = attrs.pop('captcha_key')
#         captcha_value = attrs.pop('captcha_value')

#         # captcha verify
#         if not CaptchaStore.objects.filter(
#             hashkey=captcha_key,
#             response=captcha_value
#         ).exists():
#             raise serializers.ValidationError("Invalid captcha")

#         return super().validate(attrs)




from rest_framework import serializers
from captcha.models import CaptchaStore
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CaptchaJWTSerializer(TokenObtainPairSerializer):
    captcha_key = serializers.CharField()
    captcha_value = serializers.CharField()

    def validate(self, attrs):
        captcha_key = attrs.pop("captcha_key")
        captcha_value = attrs.pop("captcha_value")

        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_key)
        except CaptchaStore.DoesNotExist:
            raise serializers.ValidationError("Captcha expired")

        if captcha.response.lower() != captcha_value.lower():
            raise serializers.ValidationError("Invalid captcha")

        captcha.delete()  # 🔥 IMPORTANT (one-time use)

        return super().validate(attrs)
