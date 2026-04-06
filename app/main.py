
from __future__ import annotations
import io
import json
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from .career_data import CAREERS
from .logic import build_assessment, score_assessment

BASE_DIR = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = BASE_DIR / "data"
RESULT_LOG = DATA_DIR / "results_log.json"

app = FastAPI(title="JobReady Reference Project")
app.add_middleware(SessionMiddleware, secret_key="jobready-reference-secret")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"career_count": len(CAREERS)})


@app.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request):
    return templates.TemplateResponse(request,"profile.html", {})


@app.get("/assessment", response_class=HTMLResponse)
def assessment_page(request: Request):
    return templates.TemplateResponse(request, "assessment.html", {})


@app.get("/analyzing", response_class=HTMLResponse)
def analyzing_page(request: Request):
    return templates.TemplateResponse(request, "analyzing.html", {})


@app.get("/career", response_class=HTMLResponse)
def career_page(request: Request):
    return templates.TemplateResponse(request, "career.html", {})


@app.get("/learning", response_class=HTMLResponse)
def learning_page(request: Request):
    return templates.TemplateResponse(request, "learning.html", {})


@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    results = []
    if RESULT_LOG.exists():
        results = json.loads(RESULT_LOG.read_text())[-20:][::-1]

    return templates.TemplateResponse(
        request,
        "admin.html",
        {"results": results}
    )


@app.post("/api/save-profile")
async def save_profile(request: Request):
    payload = await request.json()
    request.session["profile"] = payload
    return {"success": True}


@app.post("/api/clear-cache")
def clear_cache(request: Request):
    profile = request.session.get("profile")
    request.session.clear()
    if profile:
        request.session["profile"] = profile
    return {"success": True}


@app.post("/api/generate-assessment")
async def generate_assessment(request: Request):
    payload = await request.json()
    selected_careers = request.session.get("exploration_careers")
    questions = build_assessment(selected_careers)
    request.session["assessment_questions"] = questions
    request.session["assessment_answers"] = []
    request.session["question_index"] = 0
    request.session["assessment_type"] = payload.get("assessment_type", "initial")
    request.session.pop("result", None)
    return {"success": True, "total_questions": len(questions)}


@app.post("/api/start-exploration")
async def start_exploration(request: Request):
    payload = await request.json()
    selected = payload.get("careers", [])[:5]
    request.session["exploration_careers"] = selected
    questions = build_assessment(selected)
    request.session["assessment_questions"] = questions
    request.session["assessment_answers"] = []
    request.session["question_index"] = 0
    request.session.pop("result", None)
    return {"success": True, "total_questions": len(questions)}


@app.get("/api/current-question")
def current_question(request: Request):
    questions = request.session.get("assessment_questions") or []
    index = int(request.session.get("question_index", 0))
    if not questions:
        return {"error": "Assessment not generated yet."}
    if index >= len(questions):
        return {"finished": True}
    return {
        "current": index + 1,
        "total": len(questions),
        "question": questions[index],
        "finished": False,
    }


@app.get("/api/get-current-answers")
def get_current_answers(request: Request):
    answers = request.session.get("assessment_answers", [])
    return {"answers": {i: answer for i, answer in enumerate(answers)}}


@app.post("/api/next-question")
async def next_question(request: Request):
    payload = await request.json()
    answer = payload.get("answer")
    answers = request.session.get("assessment_answers", [])
    questions = request.session.get("assessment_questions", [])
    index = int(request.session.get("question_index", 0))

    if not questions:
        return JSONResponse({"error": "Assessment not initialized."}, status_code=400)
    if index >= len(questions):
        return {"finished": True}

    if index < len(answers):
        answers[index] = answer
    else:
        answers.append(answer)

    request.session["assessment_answers"] = answers
    request.session["question_index"] = index + 1

    finished = index + 1 >= len(questions)
    if finished:
        profile = request.session.get("profile", {})
        result = score_assessment(answers, profile)

        # keep only small session data
        request.session.pop("assessment_questions", None)
        request.session.pop("exploration_careers", None)
        request.session["assessment_answers"] = answers[-5:]  # optional, small
        request.session["result"] = result

        _log_result(profile, result)
        return {"finished": True}

    return {"finished": False, "current_index": index + 1}


@app.post("/api/go-to-previous")
def go_previous(request: Request):
    index = max(0, int(request.session.get("question_index", 0)) - 1)
    request.session["question_index"] = index
    return {"success": True, "current_index": index}


@app.get("/api/result")
def get_result(request: Request):
    result = request.session.get("result")
    if not result:
        return {"error": "No completed assessment found."}
    return result


@app.get("/api/career-exploration")
def career_exploration():
    cards = []
    for name, details in CAREERS.items():
        cards.append({
            "name": name,
            "category": details["category"],
            "average_salary": details["average_salary"],
            "growth_rate": details["growth_rate"],
            "description": details["description"],
            "required_skills": details["required_skills"],
            "icon": details["icon"],
        })
    return {"success": True, "careers": cards}


@app.get("/api/download-report")
def download_report(request: Request):
    profile = request.session.get("profile", {})
    result = request.session.get("result")
    if not result:
        return JSONResponse({"error": "No result available."}, status_code=404)

    lines = [
        "JOBREADY CAREER REPORT",
        "=" * 30,
        f"Name: {profile.get('fullName', 'N/A')}",
        f"Email: {profile.get('email', 'N/A')}",
        f"Recommended Career: {result['career']}",
        f"Readiness Score: {result['score']}%",
        "",
        "Skill Summary:",
    ]
    for k, v in result["skills"].items():
        lines.append(f"- {k}: {v}%")
    lines += ["", "Skill Gaps:"]
    for skill in result["gaps"].get("missing", []):
        lines.append(f"- Missing: {skill}")
    for skill in result["gaps"].get("weak", []):
        lines.append(f"- Improve: {skill}")
    lines += ["", "Learning Resources:"]
    for skill, resources in result["gaps"].get("resources", {}).items():
        lines.append(f"- {skill}: {', '.join(resources)}")
    content = "\n".join(lines)
    return StreamingResponse(io.BytesIO(content.encode("utf-8")), media_type="text/plain", headers={"Content-Disposition": "attachment; filename=jobready-report.txt"})


def _log_result(profile: dict, result: dict) -> None:
    rows = []
    if RESULT_LOG.exists():
        rows = json.loads(RESULT_LOG.read_text())
    rows.append({
        "name": profile.get("fullName", "Student"),
        "career": result["career"],
        "score": result["score"],
    })
    RESULT_LOG.write_text(json.dumps(rows[-100:], indent=2))
