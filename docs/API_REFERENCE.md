# API Reference (summary)

Base URL: `/` (router exposes registered viewsets)

Authentication
- Token auth: include header `Authorization: Token <token>` for authenticated endpoints.

Author / Account
- `GET /account/account/` — list user accounts
- `GET /account/account/?user_id=<id>` — filter by user
- `POST /account/register/` — register (sends confirmation email)
- `POST /account/login/` — login (returns token and user_id)
- `POST /account/logout/` — logout (delete token)

Blog
- `GET /blog/list/` — list blogs (searchable by user and category)
- `GET /blog/list/?user_id=<id>` — blogs by user
- `GET /blog/review/` — list reviews
- `GET /blog/review/?blog_id=<id>` — reviews for a blog

Category
- `GET /category/list/` — list categories

Contact Us
- `GET /contact_us/list/` — list contact messages
- `POST /contact_us/list/` — create contact message

Notes
- Use DRF browsable API for interactive exploration in development.
- Pagination: `BlogPagination` with default `page_size=50`.
