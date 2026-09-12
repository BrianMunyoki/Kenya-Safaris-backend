# Kenya Safaris Backend

Django + Django REST Framework + MySQL backend for kenyasavannah.com
(Kenya Safaris frontend). Three apps:

- **catalog** — `Destination` and `SafariPackage` models, read-only API,
  editable in Django admin.
- **leads** — `ContactEnquiry` and `TripEnquiry` models, capture the Contact
  page form and the Plan My Trip wizard. Write-only API (POST), viewable in
  admin.
- **pages** — `Page` (per-page title/subtitle/hero image/body/sections) and
  `FAQ`, so you can edit About Us, Sustainability, Press & Media, DMC
  Corporate, etc. from the admin instead of hardcoding them in React.
- **blog** — `BlogPost` model powering the "Guides & Blog" hub and each
  individual article (Kenya Safari Cost, Masai Mara Safari Cost, etc.) —
  title, tag, excerpt, full body, read time, all editable in admin.

## 1. Set up the environment

```bash
cd backend
python -m venv venv
# Windows (Git Bash):
source venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` — put your real MySQL credentials and your DB name in. Create
that database first in MySQL if it doesn't exist yet:

```sql
CREATE DATABASE kenya_safaris CHARACTER SET utf8mb4;
```

## 2. Create tables and an admin login

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 3. Run it

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/admin/` and log in — this is where you add
safari packages, destinations, page content, and view captured leads.

## API endpoints (what the frontend will call)

| Method | URL | Purpose |
|---|---|---|
| GET | `/api/catalog/destinations/` | List published destinations |
| GET | `/api/catalog/destinations/<slug>/` | One destination |
| GET | `/api/catalog/packages/` | List published safari packages (optional `?destination=<slug>`) |
| GET | `/api/catalog/packages/<slug>/` | One safari package |
| POST | `/api/leads/contact/` | Submit the Contact form |
| POST | `/api/leads/plan-my-trip/` | Submit the Plan My Trip wizard |
| GET | `/api/pages/<slug>/` | One editable page's content |
| GET | `/api/pages/faqs/` | List FAQs for the Contact page |
| GET | `/api/blog/` | List published guides/blog posts |
| GET | `/api/blog/<slug>/` | One full article |

## Connecting the React frontend

Nothing in the frontend calls these yet — `Contact.tsx` and
`PlanMyTrip.tsx` just set local state on submit, and `SafariPackages.tsx`
uses a hardcoded array. The next step per page is a small `fetch`/`axios`
call:

```ts
// Contact.tsx handleSubmit, replacing the local setSubmitted(true):
const res = await fetch('http://127.0.0.1:8000/api/leads/contact/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(form),
})
if (res.ok) setSubmitted(true)
```

Do this one page at a time — Contact and Plan My Trip first (highest
value, capture leads immediately), then swap the hardcoded `ALL` array in
`SafariPackages.tsx` for a `fetch('/api/catalog/packages/')` call once
you've entered your real packages into the admin.

`django-cors-headers` is already configured to allow your Vite dev server
(`http://localhost:5173`) and `https://kenyasavannah.com` — add any other
origin (e.g. a staging URL) to `CORS_ALLOWED_ORIGINS` in `.env`.

## Notes

- Images (`ImageField`) are stored to `media/` locally in dev. For
  production you'll want them on a real file store (S3-compatible or
  similar) — not required to get started.
- `highlights`, `destinations`, `duration`, `budget`, `safari_type` are all
  stored as JSON lists, matching the arrays already used in the React
  components — no reshaping needed on the frontend side.
