# Fork & Flame — Restaurant Frontend

A responsive vanilla HTML/CSS/JavaScript frontend for the Restaurant FastAPI project.

## Run it

1. Keep your FastAPI app running in Docker at `http://localhost:8000`.
2. Open this folder in VS Code.
3. Use the **Live Server** extension and choose **Open with Live Server** on `index.html`.
4. The frontend will normally open at `http://127.0.0.1:5500`.

## What works now

- Responsive restaurant landing page and sample menu
- Category filters and search
- Cart quantities and subtotal saved in `localStorage`
- Login/register forms that send JSON to `/users/login` and `/users/register`
- API health indicator that checks `/health`

## Important API integration notes

- If the browser reports a CORS error, configure CORS in FastAPI `main.py` for the Live Server origin (`http://127.0.0.1:5500` and/or `http://localhost:5500`). Do not use wildcard origins together with credentials.
- Login expects `{ "email": "...", "password": "..." }` and register expects `{ "name": "...", "phone_number": "...", "email": "...", "password": "..." }`, based on the project's current schemas.
- The cart is currently local to the browser. Real server-side cart sync and checkout need to be aligned with the backend request/response contract before enabling production checkout.
- Menu entries are demo data in `app.js` until a menu endpoint is available.
- Do not deploy with development passwords or secrets. Rotate any credentials that were shared and keep `.env` out of version control.
