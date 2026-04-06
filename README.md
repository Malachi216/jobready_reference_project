
# JobReady Reference Project

A working student reference project for career assessment, skill-gap analysis, and learning recommendations.

## Stack
- FastAPI
- Jinja2 templates
- Vanilla JavaScript
- Session-based state

## Features
- Profile capture
- Dynamic assessment flow
- Career recommendation scoring
- Skill-gap analysis
- Learning recommendations
- Career exploration mode
- Simple admin dashboard for recent results

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000`

## Project structure
```text
jobready_reference_project/
├── app/
│   ├── main.py
│   ├── career_data.py
│   └── logic.py
├── templates/
├── static/
├── data/
└── requirements.txt
```

## Student highlights

### AI & Data students
- `app/logic.py` → `score_assessment()` for recommendation scoring
- `app/logic.py` → `compute_skill_gaps()` for missing and weak skills
- `data/careers.json` → structured career knowledge base
- Strong extension ideas: replace rules with ML ranking, embeddings, recommendation explainability

### Backend engineers
- `app/main.py` → API endpoints and session flow
- Result logging into `data/results_log.json`
- Strong extension ideas: authentication, PostgreSQL, reusable routers, FastAPI schemas

### Frontend engineers
- `templates/assessment.html` + `static/js/assessment.js`
- `templates/career.html` + `static/js/career.js`
- Strong extension ideas: React migration, charting, better state handling, componentization

### Good next upgrades
- add user authentication
- persist assessments in a database
- add CV review and interview module from the advanced backend draft
- attach real learning links or LMS resources
