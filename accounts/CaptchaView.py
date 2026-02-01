from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.CaptchaSerializer import CaptchaJWTSerializer




class CaptchaTokenView(TokenObtainPairView):
    serializer_class = CaptchaJWTSerializer
