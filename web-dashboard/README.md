# REL Web Dashboard

React + TypeScript dashboard for REL.

## Run

1. Start the backend API:

```bash
python rest_api.py
```

2. Install and run frontend:

```bash
cd web-dashboard
npm install
npm run dev
```

The dev server proxies `/api` and `/ws` to `http://localhost:8080`.

## OAuth2 Login

- Use your configured admin credentials:
  - `REL_ADMIN_USERNAME` (defaults to `admin`)
  - `REL_ADMIN_PASSWORD` (recommended to set explicitly)

Change credentials with:

- `REL_ADMIN_USERNAME`
- `REL_ADMIN_PASSWORD`

before starting `rest_api.py`.

Optional frontend prefill variables:

- `VITE_REL_DEFAULT_USERNAME`
- `VITE_REL_DEFAULT_PASSWORD`
