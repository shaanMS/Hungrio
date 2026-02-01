from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


class CaptchaAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        key = CaptchaStore.generate_key()
        relative_image_url = captcha_image_url(key)  # yeh /captcha/image/xxx/ deta hai
        full_image_url = request.build_absolute_uri(relative_image_url)
        return Response({
            "captcha_key": key,
            "captcha_image": full_image_url,
        })
