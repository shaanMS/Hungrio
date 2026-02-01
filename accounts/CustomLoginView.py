# from django.views.generic import TemplateView
# from captcha.models import CaptchaStore
# from captcha.helpers import captcha_image_url

# class LoginPageView(TemplateView):
#     template_name = "login.html"

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         key = CaptchaStore.generate_key()
#         # ctx["captcha_key"] = key
#         # ctx["captcha_image"] = captcha_image_url(key)
#         ctx["form"] = LoginForm()
#         return ctx



from django.views.generic import TemplateView
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

class LoginPageView(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        key = CaptchaStore.generate_key()
        ctx["captcha_key"] = key
        ctx["captcha_image"] = captcha_image_url(key)

        return ctx
