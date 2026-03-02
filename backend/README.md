# Backend (Render)

The Flask application that powers the chat API lives in the repository root.
When deploying on Render you can point the service to the `backend` directory or
keep the repository root; just ensure the following files are present:

* `requirements.txt` – contains Python dependencies.
* `Procfile` – instructs Render how to start the web process.

## Typical deployment procedure

1. **Commit your code** (including this `backend` folder).
2. **Create a new Web Service** on Render:
   * **Repository**: select the Git repo containing this code.
   * **Root Directory**: set to `backend` if you're deploying only that folder,
     otherwise leave blank to use the project root.
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn app:app` (or `python app.py` for debug).
   * **Environment**: add the required variables:
     * `GEMINI_API_KEY` – your Google Gemini key
     * `SHEETDB_API` – SheetDB REST endpoint
     * any other config used by your services
3. **Deploy**. Render will install dependencies and run gunicorn for you.

### CORS

The Flask application enables Cross-Origin Resource Sharing (CORS) so that the
Netlify-hosted frontend can make API calls without issues. The relevant line is
`CORS(app)` in `app.py`.

### Notes

* When you update Python dependencies, run `pip freeze > backend/requirements.txt`
  (or update the file manually) and commit the changes.
* Logs can be viewed from the Render dashboard; errors will help diagnose
  missing environment variables or import problems.
