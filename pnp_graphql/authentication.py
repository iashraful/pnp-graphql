from django.utils.translation import ugettext_lazy as _
from six import text_type

from pnp_graphql import exceptions


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, text_type):
        # Work around django test client oddness
        auth = auth.encode('iso-8859-1')
    return auth


class TokenAuthentication(object):
    """
    This class(TokenAuthentication) is inspired from Django REST Framework Authentication class
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """
    keyword = 'Token'
    model = None

    def get_model(self):
        """
           A custom token model may be used, but must have the following properties.

           * token -- The string identifying the token
           * user -- The user to which the token belongs
        """
        if self.model is not None:
            return self.model
        from pnp_graphql.models import AuthToken
        return AuthToken

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            msg = _('"Authorization" header is required for Token authentication.')
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(token=token)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return token.user, token

    def authenticate_header(self, request):
        return self.keyword
