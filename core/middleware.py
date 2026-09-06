from django.urls import Resolver404, resolve, reverse
from django.utils import translation


class InterfaceLanguageMiddleware:
    """Choose language by interface, not by the visitor's staff status."""

    admin_views = {
        "core:feedback_list", "core:feedback_detail", "core:feedback_reply",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = "ja"
        try:
            match = resolve(request.path_info)
        except Resolver404:
            match = None
        if request.path_info.startswith(reverse("admin:index")) or (
            match and match.view_name in self.admin_views
        ):
            language = "en-us"
        request.LANGUAGE_CODE = language
        with translation.override(language):
            response = self.get_response(request)
            # Keep deferred template rendering inside the selected locale.
            if hasattr(response, "render") and not response.is_rendered:
                response.render()
            response.setdefault("Content-Language", language)
            return response
