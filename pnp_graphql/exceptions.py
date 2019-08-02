from pnp_graphql import status_code
from django.utils.translation import ugettext_lazy as _


class APIBaseException(Exception):
    status = status_code.HTTP_500_INTERNAL_SERVER_ERROR
    message = _('Internal Server Error.')
    error_key = 'error'

    def __init__(self, message=None, status=None):
        if status is not None:
            self.status = status
        if message is not None:
            self.message = message


class APIAuthenticationError(APIBaseException):
    status = status_code.HTTP_400_BAD_REQUEST
    message = _('Error while authenticating.')
    error_key = 'error'


class AuthenticationFailed(APIBaseException):
    status = status_code.HTTP_401_UNAUTHORIZED
    message = _('Incorrect authentication credentials.')
    error_key = 'authentication_failed'


class NotAuthenticated(APIBaseException):
    status = status_code.HTTP_401_UNAUTHORIZED
    message = _('Authentication credentials were not provided.')
    error_key = 'not_authenticated'


class PermissionDenied(APIBaseException):
    status = status_code.HTTP_403_FORBIDDEN
    message = _('You do not have permission to perform this action.')
    error_key = 'permission_denied'
