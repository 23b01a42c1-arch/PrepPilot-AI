from fastapi import APIRouter

from app.schemas.interview import (
    GenerateInterviewRequest
)

from app.services.parser import extract_text
from app.services.resume_analyzer import ResumeAnalyzer
from app.services.jd_analyzer import JDAnalyzer
from app.services.llm_match_analyzer import LLMMatchAnalyzer
from app.services.resume_insights_generator import (
    ResumeInsightsGenerator
)

router = APIRouter()


@router.post("/analyze")
def analyze_resume(
    request: GenerateInterviewRequest
):

    resume_path = (
        f"uploads/{request.resume_filename}"
    )

    # -----------------------------
    # Resume Analysis
    # -----------------------------

    resume_text = extract_text(
        resume_path
    )

    resume_data = (
        ResumeAnalyzer()
        .analyze_resume(
            resume_text
        )
    )

    # -----------------------------
    # JD Analysis
    # -----------------------------

    jd_data = (
        JDAnalyzer()
        .analyze_jd(
            request.jd_text
        )
    )

    # -----------------------------
    # Resume Match
    # -----------------------------

    match_data = (
        LLMMatchAnalyzer()
        .analyze(
            resume_data,
            jd_data
        )
    )

    # -----------------------------
    # Resume Insights
    # -----------------------------

    insights = (
        ResumeInsightsGenerator()
        .generate(
            resume_data,
            jd_data,
            match_data
        )
    )

    return {

        "match_percentage":
            match_data.get(
                "match_percentage",
                0
            ),

        "ats_score":
            insights.get(
                "ats_score",
                0
            ),

        "readiness_score":
            insights.get(
                "readiness_score",
                0
            ),

        "matched_skills":
            match_data.get(
                "matched_skills",
                []
            ),

        "missing_skills":
            match_data.get(
                "missing_skills",
                []
            ),

        "strengths":
            insights.get(
                "strengths",
                []
            ),

        "weaknesses":
            insights.get(
                "weaknesses",
                []
            ),

        "suggestions":
            insights.get(
                "suggestions",
                []
            ),

        "match_breakdown":
            insights.get(
                "match_breakdown",
                {
                    "skills": 0,
                    "projects": 0,
                    "experience": 0,
                    "education": 0
                }
            ),

        "resume_data":
            resume_data,

        "jd_data":
            jd_data,

        "match_data":
            match_data
    }
