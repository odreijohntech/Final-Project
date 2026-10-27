# GradePilot: local and Vercel setup

## Stack

- Frontend: SvelteKit, Svelte 5, TypeScript, Tailwind CSS, and Lucide icons.
- API: FastAPI on Python 3.12, with the existing scikit-learn model files.
- Hosting: two Vercel Services behind one deployment URL. `/api/*` goes to FastAPI; all other routes go to SvelteKit.

## Run locally

Start the API from the repository root:

```powershell
Set-Location app
.\.venv\Scripts\python.exe -X utf8 -m uvicorn server:app --host 127.0.0.1 --port 8002
```

If this is a fresh checkout, create the Python environment first:

```powershell
Set-Location app
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

In a second terminal, start the frontend:

```powershell
Set-Location frontend
npm ci
npm run dev
```

Open **http://127.0.0.1:8001/**. Vite proxies `/api/*` to the Python API on port 8002. Port 8000 is not used by this app.

## Deploy to Vercel

1. Push the repository to the Git provider connected to Vercel.
2. Import the repository with its repository root as the project root. Keep `vercel.json` at that root.
3. Vercel builds `frontend/` and `app/` as separate services. The root rewrites send `/api/*` to FastAPI and the remaining paths to SvelteKit.
4. Deploy. The model files are in `app/models/`; Python dependencies are in `app/requirements.txt`, and `app/.python-version` pins the runtime to 3.12.

For a local Vercel-style run, install the Vercel CLI and run `vercel dev -L` from the repository root. Vercel Services are currently in beta; check the [Services guide](https://vercel.com/kb/guide/vercel-services) if your Vercel project does not recognize the `services` configuration.
