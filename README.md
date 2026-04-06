# JobReady – AI Career Assessment Platform

## Overview
JobReady is an AI-inspired career assessment platform that guides users from profile creation to career recommendation, skill gap analysis, and learning suggestions.

## Features
- Profile creation
- Assessment flow
- AI-style analysis screen
- Career recommendation
- Skill gap detection
- Learning suggestions
- Admin dashboard

## Setup (Windows)
```powershell
git clone https://github.com/Malachi216/jobready_reference_project.git
cd jobready_reference_project
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8010
start http://127.0.0.1:8010
```

## Common Issues
- Port error → use 8010
- Template error → use correct TemplateResponse signature
- Admin empty → run assessment first

## Screenshots
Add images under /screenshots folder:
home.png, profile.png, assessment.png, analyzing.png, career-result.png, learning.png, admin.png
