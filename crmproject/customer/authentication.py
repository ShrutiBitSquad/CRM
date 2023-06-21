from django.contrib.auth.backends import ModelBackend
class LowercaseEmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get('email')
        if email is not None:
            email = email.lower()
        return super().authenticate(request, email, password, **kwargs)