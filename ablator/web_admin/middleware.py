from ablator.version import __version__


class VersioningMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.ablator_version = __version__
        response = self.get_response(request)
        return response
