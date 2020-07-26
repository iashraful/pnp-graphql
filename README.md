## Plug & Play GraphQL (pnp-graphql)-- [Change Log](https://github.com/iashraful/pnp-graphql/blob/master/CHANGELOG.md)
> A library for making GraphQL API with Python/Django. This is like a flash drive, 
just how you plug into computer and transfer files.

> **Read Full Documentation here: https://docs.ashraful.dev/pnp-graphql** 

### Quick Start
> Documentation is coming soon...

* Install from pip `pip install pnp-graphql`
* Add `graphene_django` on top of installed apps on settings.py
* Add `pnp_graphql` into installed apps on settings.py
* Add PnP GraphQL config on settings.
```python
GRAPHENE = {
    'SCHEMA': 'pnp_graphql.schema.schema'
}

PNP_GRAPHQL = {
    'ENABLED_APPS': ['example_app'],
    # If you want to use Token Authentication. Otherwise it's optional
    'AUTHENTICATION_CLASS': 'pnp_graphql.authentication.TokenAuthentication'
}
```
* Add the following code on `urls.py`
```python
from pnp_graphql.urls import urlpatterns as up

urlpatterns = [
    # ... ... ... 
]
urlpatterns += up
```
* Set `DEBUG = False` for production use.

**That's it :)**  
**Now visit:** `http://your-ip:port/api/graphql-explorer/` for explore GraphQL built-in UI explorer for query.  
**Production ready API :** `http://your-ip:port/api/graphql/`


#### What's working?
* GraphQL query
* Mutation (Create, Update, Delete)
* Pagination
* API filtering for Number, String, Date, DateTime
* Authentication

#### What are the plans?
* Proper error handling
* Field validation
* Caching
* many more ... ... ...

### Waiting for your contribution :smile: