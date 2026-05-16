# Architecture Overview

This document describes the high-level architecture of the Creatifinity REST API.

Apps
- `author`: User account models and auth endpoints (registration, login, logout, profile)
- `blog`: Blog posts, categories relation, and review model
- `category`: Category model used by `blog` (name, slug)
- `contact_us`: Simple contact messages model

Core components
- Django as the web framework
- Django REST Framework for API layer and viewsets
- Token authentication via `rest_framework.authtoken`
- `django-environ` for environment configuration
- SQLite by default for local development (configurable to Postgres)

Data flow
1. HTTP request arrives at `creatifinity_blog/urls.py` and is routed to app routers.
2. Router dispatches to a ViewSet in the appropriate app.
3. ViewSet uses a Serializer to validate/serialize data and interacts with Models.
4. ORM performs DB transactions; responses are serialized and returned.

Auth flow (registration)
1. Client POSTs to `/account/register/` with user details.
2. `UserRegistrationSerializers` validates and creates the `User` (inactive by default comment), then sends confirmation email with uid/token.
3. User clicks confirmation link; `Active` view activates the account.

Files of interest
- Project settings: `creatifinity_blog/settings.py`
- Top-level router: `creatifinity_blog/urls.py`
- User API: `creatifinity_blog/views.py` and `creatifinity_blog/serializers.py`
- App endpoints: `author/urls.py`, `blog/urls.py`, `category/urls.py`, `contact_us/urls.py`
