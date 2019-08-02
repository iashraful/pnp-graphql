from django.contrib import admin

from pnp_graphql.models import AuthToken


class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'user', 'created')
    fields = ('user',)
    ordering = ('-created',)


admin.site.register(AuthToken, AuthTokenAdmin)
