# JREDA Chatbot (split front‑end & back‑end)

This repository now contains two deployable pieces:

* `frontend/` &ndash; static web assets for the chat widget (HTML, CSS, JS,
  images). Suitable for hosting on Netlify or any static site host.
* backend code (remaining files in project root plus `routes/`, `services/`,
  `utils/`). This is a Flask API that can run on Render, Heroku, or any Python
  server.

See `frontend/README.md` and `backend/README.md` for platform-specific
instructions.

## Quick start (local development)

1. Create and activate Python virtual environment (`python -m venv venv`).
2. Install dependencies: `pip install -r requirements.txt`.
3. Set environment variables (copy `.env` and fill in your keys).
4. Run `python app.py` to start the API on `http://127.0.0.1:5000`.
5. Open `frontend/index.html` in your browser (serve it with a simple HTTP
   server such as `python -m http.server` from the `frontend` folder) and the
   widget will communicate with the backend.

## Deployment

* **Frontend** &ndash; push `frontend/` directory to your Git provider and
  configure Netlify to serve it (see `netlify.toml`).
* **Backend** &ndash; point Render at this repository, use the `requirements.txt`
  and `Procfile`, and set the required environment variables.

With this separation you can update the UI independently from backend logic.

---

_Remember to add your own API keys to environment settings on the host platform
and **never commit them** to version control._