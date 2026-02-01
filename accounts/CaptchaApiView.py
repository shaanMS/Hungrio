from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


class CaptchaAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        key = CaptchaStore.generate_key()

        return Response({
            "captcha_key": key,
            "captcha_image": captcha_image_url(key),
        })
