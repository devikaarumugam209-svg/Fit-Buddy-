# FitBuddy
FitBuddy is a FastAPI fitness assistant that creates structured seven-day workout plans, concise nutrition tips, and feedback-based plan updates with Gemini.

## Run locally

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

Copy `.env.example` to `.env` and add your Gemini API key. Never commit `.env`.

## Deployment

The included `render.yaml` contains the Render web-service configuration. Add `GEMINI_API_KEY` and `ADMIN_TOKEN` as secret environment variables in Render.

## Prerequisites and Documentation

Before contributing to FitBuddy, review these technologies and references:

1. **FastAPI framework:** [FastAPI Documentation](https://devdocs.io/fastapi/)
2. **Gemini API:** [Google Generative AI Documentation](https://ai.google.dev/)
3. **HTML, CSS, and templates:** [W3Schools HTML/CSS/Jinja2 Tutorials](https://www.w3schools.com/)
4. **Python:** [Python Documentation](https://docs.python.org/3/)
5. **Version control:** [Git Documentation](https://git-scm.com/doc)
6. **SQLite and database basics:** [SQLite Documentation](https://www.sqlite.org/docs.html)
7. **Environment setup:** [Virtualenv Guide](https://virtualenv.pypa.io/en/latest/)
8. **Uvicorn ASGI server:** [Uvicorn Documentation](https://www.uvicorn.org/)

FitBuddy currently uses Python's built-in `sqlite3` module for local storage. SQLAlchemy knowledge is useful for future database migrations, but SQLAlchemy is not required to run the current application.