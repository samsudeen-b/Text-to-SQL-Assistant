# Deploy QueryAI to Vercel

1. Import this repository at https://vercel.com/new after merging this branch.
2. Use the repository root (not frontend or backend) as Root Directory.
3. Select FastAPI if it is not detected. Keep build and output overrides disabled; pyproject.toml supplies the build command.
4. Add GROQ_API_KEY in Environment Variables for Production and Preview. Never commit its value.
5. Deploy. Open /api/health, then ask "Show all customers from Chennai" on the homepage.

The build stages frontend/index.html in public/. The API creates its fictional sample database in memory for each query, so it does not store user edits. Use a hosted database if persistent writes are needed.

Local run:

```sh
pip install -r requirements.txt
python build.py
uvicorn backend.main:app --reload
```

Open http://127.0.0.1:8000 (not the HTML file directly). Set GROQ_API_KEY in your environment or a local .env file. The original Streamlit app.py remains separate from the Vercel entrypoint.

