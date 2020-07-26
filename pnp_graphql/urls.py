from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=False))),
]

if settings.DEBUG:
    urlpatterns += [path('graphql-explorer/', csrf_exempt(GraphQLView.as_view(graphiql=True)))]
