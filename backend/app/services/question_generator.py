import json
import os
from app.services.question_difficulty_validator import (
    QuestionDifficultyValidator
)
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class QuestionGenerator:

    def generate_questions(
        self,
        resume_data,
        jd_data,
        match_data,
        topics_data,
        context_data
    ):

        schema = {
            "topics": [
                {
                    "topic": "",
                    "questions": [
                        {
                            "difficulty": "easy",
                            "question": ""
                        },
                        {
                            "difficulty": "medium",
                            "question": ""
                        },
                        {
                            "difficulty": "hard",
                            "question": ""
                        }
                    ]
                }
            ],
            "project_questions": [],
            "behavioral_questions": [],
            "missing_skill_questions": []
        }

        prompt = f"""
    You are a senior technical interviewer.

    Generate a personalized interview plan from the supplied candidate evidence.

    Return ONLY valid JSON matching this structure:

    {json.dumps(schema)}

    IMPORTANT:
    - Output JSON only.
    - No markdown.
    - No explanations.
    - Do not add fields.
    - Do not remove fields.
    - Do not invent resume evidence.
    - Keep every question concise.
    - Avoid duplicate questions.

    TOPIC QUESTIONS:
    For every topic in Topics Data generate exactly:
    - 1 easy
    - 1 medium
    - 1 hard

    QUESTION PERSONALIZATION:
    Every technical question must use evidence from:
    - candidate projects
    - internship
    - resume technologies
    - JD requirements

    If project evidence exists, ask implementation questions.
    If internship evidence exists, ask production/engineering questions.
    If both exist, combine them.

    Do NOT ask generic definition questions when resume evidence exists.

    Difficulty:
    Easy = implementation, workflow, practical usage.
    Medium = design decisions, tradeoffs, debugging, architecture.
    Hard = scaling, optimization, reliability, monitoring, production architecture.

    ALSO GENERATE:
    - exactly 3 project questions
    - exactly 3 behavioral questions
    - exactly 1 question for each missing skill

    Behavioral questions may use the candidate's actual projects/internship.
    Missing-skill questions must target skills genuinely missing from Match Data.

    Topics Data:
    {json.dumps(topics_data)}

    Resume Data:
    {json.dumps(resume_data)}

    JD Data:
    {json.dumps(jd_data)}

    Match Data:
    {json.dumps(match_data)}

    Context Data:
    {json.dumps(context_data)}
    """

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
            max_tokens=5000
        )

        content = response.choices[0].message.content

        try:

            result = json.loads(content)

            print("\n========== QUESTION GENERATOR ==========")
            print(json.dumps(result, indent=2))
            print("========================================\n")

            return result

        except json.JSONDecodeError as e:

            print("\nQUESTION GENERATOR JSON ERROR\n")
            print(e)

            print("\nRAW RESPONSE\n")
            print(content)

            return {
                "error": "Invalid JSON returned by question generator",
                "raw_response": content
            }