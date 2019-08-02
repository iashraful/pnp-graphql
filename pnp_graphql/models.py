import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AuthToken(models.Model):
    token = models.CharField(max_length=64, unique=True, verbose_name=_('Token'))
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    def save(self, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        super(AuthToken, self).save(**kwargs)

    class Meta:
        app_label = 'pnp_graphql'

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.token
