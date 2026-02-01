from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.CaptchaSerializer import CaptchaSerializer




class CaptchaTokenView(TokenObtainPairView):
    serializer_class = CaptchaSerializer
