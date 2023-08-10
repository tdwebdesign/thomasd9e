from django.http import HttpResponsePermanentRedirect


class SecureMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.is_secure():
            return HttpResponsePermanentRedirect(
                "https://" + request.get_host() + request.get_full_path()
            )
        return self.get_response(request)
