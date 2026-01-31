from rest_framework_simplejwt.views import TokenObtainPairView
from accounts import CaptchaSerializer




class CaptchaTokenView(TokenObtainPairView):
    serializer_class = CaptchaSerializer
