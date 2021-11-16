from .models import PrivacyLog


class ConsentExpiredMiddleware(object):
    """
    Check if the user consent log is expired,
    sets a context boolean so developer can decide what to do
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response):
        assert hasattr(request, "user")
        if request.user.is_authenticated:
            if PrivacyLog.objects.get_privacy_logs_for_object(request.user).is_expired:
                response.context_data["consents_expired"] = True
        return response
