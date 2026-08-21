#interview_router.py
from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel
from app.schemas.interview import (
    GenerateInterviewRequest
)
from app.services.text_to_speech import TextToSpeech
from app.core.session_store import session_manager
from app.services.parser import extract_text
from app.services.resume_analyzer import ResumeAnalyzer
from app.services.jd_analyzer import JDAnalyzer
from app.services.llm_match_analyzer import LLMMatchAnalyzer
from app.services.topic_extractor import TopicExtractor
from app.services.resume_context_builder import ResumeContextBuilder
from app.services.question_generator import QuestionGenerator
from app.services.interview_roadmap_builder import (
    InterviewRoadmapBuilder
)

router = APIRouter()

class AnswerRequest(BaseModel):
    session_id: str
    answer: str
@router.post("/generate")
def generate_interview(
    request: GenerateInterviewRequest
):

    resume_path = (
        f"uploads/{request.resume_filename}"
    )

    # Resume

    resume_text = extract_text(
        resume_path
    )

    resume_data = (
        ResumeAnalyzer()
        .analyze_resume(
            resume_text
        )
    )

    # JD


    jd_data = (
        JDAnalyzer()
        .analyze_jd(
            request.jd_text
        )
    )
    if len(jd_data.get("required_skills", [])) < 3:
        return {
        "error": "Please provide a detailed Job Description with required skills."
        }

    # Match

    match_data = (
        LLMMatchAnalyzer()
        .analyze(
            resume_data,
            jd_data
        )
    )
    print(match_data)

    # Topics

    topics_data = (
        TopicExtractor()
        .extract_topics(
            resume_data
        )
    )
    print("\n========== TOPICS DATA ==========")
    print(topics_data)
    print("=================================\n")

    # Resume Context

    context_data = (
        ResumeContextBuilder()
        .build(
            resume_data,
            topics_data
        )
    )

    # Questions

    try:

        questions_data = (
            QuestionGenerator()
            .generate_questions(
                resume_data,
                jd_data,
                match_data,
                topics_data,
                context_data
            )
        )

    except Exception as e:

        print("\n========== QUESTION GENERATION FAILED ==========")
        print(type(e).__name__)
        print(str(e))
        print("=================================================")

        raise HTTPException(
            status_code=500,
            detail=f"Question generation failed: {str(e)}"
        )
    # Roadmap

    roadmap = (
        InterviewRoadmapBuilder()
        .build(
            questions_data
        )
    )
    print("\n========== ROADMAP ==========")

    for i, q in enumerate(roadmap):
        print(
            i,
            q["topic"],
            q["difficulty"],
            q["question"]
        )

    print("=============================\n")
    print("\n========== ROADMAP ==========")
    print("Total Questions:", len(roadmap))

    for i, q in enumerate(roadmap):
        print(
            f"{i+1}. [{q['type']}] "
            f"{q['topic']} | "
            f"{q['difficulty']}"
        )
        print(q["question"])
        print("-" * 80)

    print("=============================")
    session_id, first_question = (
    session_manager.create_session(
        roadmap,
        resume_data,
        jd_data,
        match_data
    )
)


    tts = TextToSpeech()

    tts.speak(
    first_question,
    "audio/question.mp3"
)
    return {

    "session_id": session_id,

    "match_percentage":
        match_data["match_percentage"],

    "total_questions":
        len(roadmap),

    "first_question": {

        "question": first_question,
        "audio": "/audio/question.mp3"
    }
}
@router.post("/answer")
def submit_answer(request: AnswerRequest):

    session = session_manager.get_session(request.session_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    engine = session["engine"]

    result = engine.submit_answer(request.answer)

    return result