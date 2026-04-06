
from __future__ import annotations
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CAREERS = json.loads((DATA_DIR / "careers.json").read_text())

CAREER_LIST = list(CAREERS.keys())

QUESTION_BANK = [
    {
        "category": "Interest",
        "text": "Which type of work sounds most exciting to you?",
        "options": [
            "Building user interfaces and experiences",
            "Designing APIs, databases, and server logic",
            "Working with data, machine learning, or AI",
            "Securing systems or managing cloud infrastructure",
        ],
        "weights": {
            "Building user interfaces and experiences": {"Frontend": 5, "UI/UX Designer": 4, "Mobile App Developer": 3},
            "Designing APIs, databases, and server logic": {"Backend": 5, "Backend Developer": 4, "Full Stack Developer": 3, "DevOps Engineer": 2},
            "Working with data, machine learning, or AI": {"AI/Data Science": 5, "AI Engineer": 4, "Data Scientist": 4, "Machine Learning Engineer": 4, "Data Analyst": 3},
            "Securing systems or managing cloud infrastructure": {"Cybersecurity": 4, "Cloud Engineer": 4, "Cybersecurity Analyst": 4, "DevOps Engineer": 3},
        },
    },
    {
        "category": "Frontend",
        "text": "How comfortable are you building layouts with HTML and CSS?",
        "options": ["Not comfortable yet", "Basic comfort", "Comfortable", "Very comfortable"],
        "weights": {
            "Not comfortable yet": {"Frontend": 1},
            "Basic comfort": {"Frontend": 2},
            "Comfortable": {"Frontend": 4, "Full Stack Developer": 2},
            "Very comfortable": {"Frontend": 5, "Frontend Developer": 4, "UI/UX Designer": 2},
        },
    },
    {
        "category": "Frontend",
        "text": "How confident are you with JavaScript and modern frontend frameworks?",
        "options": ["Just starting", "I know the basics", "I can build small apps", "I can build real projects"],
        "weights": {
            "Just starting": {"Frontend": 1},
            "I know the basics": {"Frontend": 2},
            "I can build small apps": {"Frontend": 4, "Frontend Developer": 3, "Full Stack Developer": 2},
            "I can build real projects": {"Frontend": 5, "Frontend Developer": 4, "Mobile App Developer": 2},
        },
    },
    {
        "category": "Backend",
        "text": "How confident are you designing APIs and backend routes?",
        "options": ["No experience yet", "Beginner level", "I can build CRUD APIs", "I can design solid backend services"],
        "weights": {
            "No experience yet": {"Backend": 1},
            "Beginner level": {"Backend": 2},
            "I can build CRUD APIs": {"Backend": 4, "Backend Developer": 4, "Full Stack Developer": 2},
            "I can design solid backend services": {"Backend": 5, "Backend Developer": 5, "DevOps Engineer": 2},
        },
    },
    {
        "category": "Backend",
        "text": "How comfortable are you with SQL or database design?",
        "options": ["Not yet", "Basic queries only", "I can build and query databases", "I can model data well"],
        "weights": {
            "Not yet": {"Backend": 1, "DSA": 1},
            "Basic queries only": {"Backend": 2, "AI/Data Science": 2},
            "I can build and query databases": {"Backend": 4, "Backend Developer": 3, "Data Analyst": 3, "Full Stack Developer": 2},
            "I can model data well": {"Backend": 5, "Data Engineer": 3, "AI Engineer": 2},
        },
    },
    {
        "category": "AI/Data Science",
        "text": "How comfortable are you using Python for analysis or automation?",
        "options": ["Not yet", "Beginner", "Comfortable", "Advanced"],
        "weights": {
            "Not yet": {"AI/Data Science": 1, "Backend": 1},
            "Beginner": {"AI/Data Science": 2, "Backend": 2},
            "Comfortable": {"AI/Data Science": 4, "Data Analyst": 3, "Backend Developer": 2},
            "Advanced": {"AI/Data Science": 5, "AI Engineer": 4, "Machine Learning Engineer": 4, "Data Engineer": 3},
        },
    },
    {
        "category": "AI/Data Science",
        "text": "How familiar are you with machine learning concepts?",
        "options": ["No exposure", "I know the ideas", "I have trained models", "I can build end-to-end ML projects"],
        "weights": {
            "No exposure": {"AI/Data Science": 1},
            "I know the ideas": {"AI/Data Science": 3, "Data Scientist": 2},
            "I have trained models": {"AI/Data Science": 4, "Data Scientist": 4, "AI Engineer": 3},
            "I can build end-to-end ML projects": {"AI/Data Science": 5, "AI Engineer": 5, "Machine Learning Engineer": 5},
        },
    },
    {
        "category": "DSA",
        "text": "How strong are your algorithms and problem-solving skills?",
        "options": ["Still weak", "Average", "Good", "Strong"],
        "weights": {
            "Still weak": {"DSA": 1},
            "Average": {"DSA": 2},
            "Good": {"DSA": 4, "Backend Developer": 2, "Machine Learning Engineer": 2},
            "Strong": {"DSA": 5, "Backend Developer": 3, "AI Engineer": 2},
        },
    },
    {
        "category": "Cloud / Ops",
        "text": "How interested are you in cloud, deployment, or infrastructure work?",
        "options": ["Not interested", "A little interested", "Interested", "Very interested"],
        "weights": {
            "Not interested": {"Backend": 1},
            "A little interested": {"Backend": 2},
            "Interested": {"Cloud Engineer": 4, "DevOps Engineer": 4, "Backend": 3},
            "Very interested": {"Cloud Engineer": 5, "DevOps Engineer": 5, "Backend": 4},
        },
    },
    {
        "category": "Security",
        "text": "How interested are you in protecting systems, data, and networks?",
        "options": ["Not interested", "Some interest", "Interested", "Very interested"],
        "weights": {
            "Not interested": {"Cybersecurity": 1},
            "Some interest": {"Cybersecurity": 2},
            "Interested": {"Cybersecurity": 4, "Cybersecurity Analyst": 4},
            "Very interested": {"Cybersecurity": 5, "Cybersecurity Analyst": 5},
        },
    },
    {
        "category": "Soft Skills",
        "text": "How would you rate your communication and collaboration skills?",
        "options": ["Need improvement", "Fair", "Good", "Excellent"],
        "weights": {
            "Need improvement": {"Soft Skills": 1},
            "Fair": {"Soft Skills": 2},
            "Good": {"Soft Skills": 4},
            "Excellent": {"Soft Skills": 5, "Product Manager": 3, "UI/UX Designer": 2},
        },
    },
    {
        "category": "Soft Skills",
        "text": "How would you rate your attention to detail and quality focus?",
        "options": ["Need improvement", "Fair", "Good", "Excellent"],
        "weights": {
            "Need improvement": {"Soft Skills": 1},
            "Fair": {"Soft Skills": 2},
            "Good": {"Soft Skills": 4, "QA Engineer": 2},
            "Excellent": {"Soft Skills": 5, "QA Engineer": 4, "Cybersecurity Analyst": 2},
        },
    },
]

SCALE_MAP = {
    "Not comfortable yet": 20,
    "No experience yet": 20,
    "No exposure": 20,
    "Not interested": 20,
    "Still weak": 20,
    "Need improvement": 25,
    "Just starting": 25,
    "Basic comfort": 40,
    "Basic queries only": 40,
    "I know the basics": 40,
    "Beginner level": 40,
    "Beginner": 40,
    "Some interest": 45,
    "A little interested": 45,
    "Average": 50,
    "Fair": 50,
    "Comfortable": 70,
    "I know the ideas": 65,
    "I can build CRUD APIs": 75,
    "I can build and query databases": 75,
    "Interested": 75,
    "Good": 75,
    "I can build small apps": 75,
    "I have trained models": 80,
    "I can model data well": 85,
    "Advanced": 90,
    "Very comfortable": 90,
    "I can build real projects": 90,
    "I can design solid backend services": 90,
    "I can build end-to-end ML projects": 95,
    "Very interested": 90,
    "Strong": 90,
    "Excellent": 90,
}
