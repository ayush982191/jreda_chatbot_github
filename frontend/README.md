# Frontend (Netlify)

This directory contains the static chat widget assets that can be deployed on
Netlify (or any static-hosting service). The files here are just HTML, CSS, and
JavaScript.

## Deployment steps

1. **Push to Git**: Make sure the `frontend/` folder is committed to your
   repository.
2. **Configure Netlify site**:
   * Connect Netlify to your GitHub/GitLab/Bitbucket repository.
   * Set the **build command** to _none_ (since there is no build step) or leave
     it blank.
   * Set the **publish directory** to `frontend` (this is also specified in
     `netlify.toml`).
3. **Environment variables**: The frontend doesn’t use any server-side
   variables, but you may want to define a variable for the backend base URL,
   e.g. `REACT_APP_API_URL` if you modify the JS accordingly.
4. **API redirects** (optional): Add redirect rules in `netlify.toml` or via
   the Netlify UI to forward `/api/*` requests to your backend running on
   Render.

### Notes

* The HTML references `script.js` and `style.css` directly, so the entire
  `frontend` folder can be served without modification.
* When calling the backend (e.g. `/chat`), make sure your JS fetches from the
  correct domain or use relative paths and rely on Netlify redirects.
