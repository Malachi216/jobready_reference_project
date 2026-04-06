
from __future__ import annotations
from collections import defaultdict
from statistics import mean
from typing import Any
from .career_data import CAREERS, QUESTION_BANK, SCALE_MAP

LEARNING_RESOURCES = {
    "Frontend": ["MDN HTML/CSS/JS", "freeCodeCamp Front End Development", "Frontend Mentor"],
    "Backend": ["FastAPI tutorial", "Node/Express crash course", "SQLBolt"],
    "AI/Data Science": ["Kaggle Learn", "Andrew Ng ML Specialization", "scikit-learn tutorials"],
    "DSA": ["NeetCode roadmap", "Grokking Algorithms", "LeetCode study plan"],
    "Soft Skills": ["Team communication practice", "Presentation practice", "Write technical summaries weekly"],
}

AREA_BOOSTS = {
    "technology": ["AI Engineer", "Backend Developer", "Frontend Developer", "Data Scientist"],
    "engineering": ["Backend Developer", "Cloud Engineer", "DevOps Engineer", "Data Engineer"],
    "business": ["Product Manager", "Data Analyst"],
    "science": ["Data Scientist", "AI Engineer", "Machine Learning Engineer"],
}

TRACK_GROUPS = {
    "Frontend": {"Frontend Developer", "UI/UX Designer", "Mobile App Developer", "Full Stack Developer"},
    "Backend": {"Backend Developer", "Cloud Engineer", "DevOps Engineer", "QA Engineer", "Full Stack Developer"},
    "AI/Data Science": {"AI Engineer", "Data Analyst", "Data Engineer", "Data Scientist", "Machine Learning Engineer"},
    "DSA": {"Backend Developer", "AI Engineer", "Machine Learning Engineer", "Full Stack Developer"},
}

QUESTION_TEMPLATE = {q["text"]: q for q in QUESTION_BANK}


def build_assessment(careers: list[str] | None = None) -> list[dict[str, Any]]:
    questions = []
    for q in QUESTION_BANK:
        if careers:
            # keep question if its weights touch one of selected careers or a general skill bucket
            flattened = set()
            for answer_weights in q["weights"].values():
                flattened.update(answer_weights.keys())
            if not any(c in flattened for c in careers):
                if q["category"] not in {"Interest", "Soft Skills", "DSA", "Frontend", "Backend", "AI/Data Science"}:
                    continue
        questions.append({
            "category": q["category"],
            "text": q["text"],
            "options": q["options"],
        })
    return questions


def score_assessment(answers: list[str], profile: dict[str, Any] | None = None) -> dict[str, Any]:
    profile = profile or {}
    track_scores = defaultdict(float)
    career_scores = defaultdict(float)
    selected_values = []

    for index, answer in enumerate(answers):
        if index >= len(QUESTION_BANK):
            break
        question = QUESTION_BANK[index]
        selected_values.append(SCALE_MAP.get(answer, 50))
        for key, value in question["weights"].get(answer, {}).items():
            if key in TRACK_GROUPS:
                track_scores[key] += value
            else:
                career_scores[key] += value
                for track, career_set in TRACK_GROUPS.items():
                    if key in career_set:
                        track_scores[track] += value * 0.35

    # profile boosts
    area = profile.get("areaOfInterest")
    for career in AREA_BOOSTS.get(area, []):
        career_scores[career] += 1.5
    study_level = str(profile.get("studyLevel", ""))
    if study_level in {"300", "400"}:
        track_scores["DSA"] += 1.0
        track_scores["Backend"] += 0.5
    elif study_level in {"100", "200"}:
        track_scores["Soft Skills"] += 0.5

    # default missing track scores
    for track in ["Frontend", "Backend", "AI/Data Science", "DSA", "Soft Skills"]:
        track_scores.setdefault(track, 0.0)

    if not career_scores:
        career_scores["Full Stack Developer"] = 1.0

    ordered = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
    top_career, top_score = ordered[0]

    top_track = max((t for t in ["Frontend", "Backend", "AI/Data Science", "DSA"]), key=lambda t: track_scores[t])
    track_percentages = normalize_track_scores(track_scores)
    readiness = round(mean(selected_values), 1) if selected_values else 0
    domain_fit = min(100, round(55 + (top_score * 6), 1))
    tag_similarity = min(100, round(50 + (ordered[0][1] - ordered[1][1]) * 4, 1)) if len(ordered) > 1 else 82.0
    score = int(round((readiness * 0.55) + (domain_fit * 0.30) + (tag_similarity * 0.15)))

    gaps = compute_skill_gaps(top_career, track_percentages, readiness)

    return {
        "career": top_career,
        "score": max(35, min(98, score)),
        "skills": {
            "Frontend": track_percentages["Frontend"],
            "Backend": track_percentages["Backend"],
            "AI/Data Science": track_percentages["AI/Data Science"],
            "DSA": track_percentages["DSA"],
            "Soft Skills": track_percentages["Soft Skills"],
            "Domain Fit": int(domain_fit),
            "Tag Similarity": int(tag_similarity),
            "Readiness": int(readiness),
        },
        "gaps": gaps,
        "top_matches": [{"career": c, "score": round(s, 2)} for c, s in ordered[:5]],
        "recommended_track": top_track,
    }


def normalize_track_scores(scores: dict[str, float]) -> dict[str, int]:
    max_possible = {
        "Frontend": 16,
        "Backend": 18,
        "AI/Data Science": 20,
        "DSA": 10,
        "Soft Skills": 10,
    }
    normalized = {}
    for key, max_value in max_possible.items():
        pct = int(round(min(100, (scores.get(key, 0) / max_value) * 100)))
        normalized[key] = max(15, pct) if scores.get(key, 0) > 0 else 10
    return normalized


def compute_skill_gaps(career: str, track_scores: dict[str, int], readiness: float) -> dict[str, Any]:
    career_info = CAREERS[career]
    required_skills = list(career_info["required_skills"].keys())

    track_map = {
        "Frontend": ["HTML/CSS", "JavaScript", "React/Vue", "UI Frameworks", "Figma", "Wireframing", "Prototyping", "Mobile UI Design"],
        "Backend": ["APIs", "Databases", "Server Architecture", "Backend Frameworks", "Cloud Platforms", "CI/CD", "Docker", "Kubernetes"],
        "AI/Data Science": ["Python", "Machine Learning", "Deep Learning", "SQL", "Data Visualization", "Statistics", "Data Pipelines", "ETL", "Model Deployment", "Statistical Modeling"],
        "DSA": ["Logical Thinking", "Algorithms", "Problem Solving"],
        "Soft Skills": ["Communication", "Collaboration", "Creativity", "Attention to Detail", "Leadership", "Decision Making", "Empathy", "Adaptability"],
    }

    def infer_track(skill: str) -> str:
        for track, keywords in track_map.items():
            if skill in keywords:
                return track
        return "Soft Skills"

    missing, weak = [], []
    resources = {}
    for skill in required_skills:
        track = infer_track(skill)
        score = track_scores.get(track, 0)
        if score < 45:
            missing.append(skill)
            if skill in career_info.get("resources", {}):
                resources[skill] = career_info["resources"][skill]
        elif score < 70:
            weak.append(skill)
            if skill in career_info.get("resources", {}):
                resources[skill] = career_info["resources"][skill]

    # fallback to track recommendations if too few specific resources
    if not resources:
        weakest = sorted(track_scores.items(), key=lambda x: x[1])[:2]
        for track, _ in weakest:
            resources[track] = LEARNING_RESOURCES.get(track, [])

    return {"missing": missing[:6], "weak": weak[:6], "resources": resources}
