import json
import os

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

        print("\n========== QUESTION GENERATOR START ==========")
        print("Topics available:", topics_data is not None)
        print("Resume data available:", resume_data is not None)
        print("JD data available:", jd_data is not None)
        print("Match data available:", match_data is not None)
        print("Context data available:", context_data is not None)
        print("==============================================")

        # --------------------------------------------------
        # SAFE DEFAULT
        # --------------------------------------------------

        schema = {
            "type": "object",
            "properties": {
                "topics": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string"
                            },
                            "questions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "difficulty": {
                                            "type": "string",
                                            "enum": [
                                                "easy",
                                                "medium",
                                                "hard"
                                            ]
                                        },
                                        "question": {
                                            "type": "string"
                                        }
                                    },
                                    "required": [
                                        "difficulty",
                                        "question"
                                    ],
                                    "additionalProperties": False
                                }
                            }
                        },
                        "required": [
                            "topic",
                            "questions"
                        ],
                        "additionalProperties": False
                    }
                },

                "project_questions": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },

                "behavioral_questions": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },

                "missing_skill_questions": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },

            "required": [
                "topics",
                "project_questions",
                "behavioral_questions",
                "missing_skill_questions"
            ],

            "additionalProperties": False
        }

        # --------------------------------------------------
        # PROMPT
        # --------------------------------------------------

        prompt = f"""
You are a senior technical interviewer.

Generate a personalized interview question plan.

IMPORTANT:
Return ONLY valid JSON.
Do not use markdown.
Do not use ```json.
Do not add explanations outside JSON.

The output MUST follow the provided JSON schema.

RULES:

1. Use ONLY topics present in Topics Data.

2. For every topic generate:
   - exactly 1 easy question
   - exactly 1 medium question
   - exactly 1 hard question

3. Questions must be personalized using:
   - candidate projects
   - internship experience
   - technologies
   - resume evidence
   - job description

4. NEVER ask generic definition questions when resume evidence exists.

Bad:
"What is RAG?"

Bad:
"What is FastAPI?"

Bad:
"What is NLP?"

Good:
"In your Retrieval-Augmented PDF Question Answering Application, how did LangChain and Qdrant work together during retrieval?"

5. EASY questions should focus on:
   - implementation
   - workflow
   - practical usage
   - architecture components

6. MEDIUM questions should focus on:
   - design decisions
   - tradeoffs
   - debugging
   - architecture choices
   - technology selection

7. HARD questions should focus on:
   - production systems
   - scaling
   - optimization
   - fault tolerance
   - monitoring
   - distributed architecture

8. Evidence rules:

If project evidence exists:
ask implementation-focused questions.

If internship evidence exists:
ask production-focused questions.

If both exist:
combine project and production perspectives.

If only skills exist:
ask practical engineering questions.

9. Generate exactly:
   - 3 project questions
   - 3 behavioral questions
   - 1 question for every missing skill

10. Avoid duplicate questions.

11. Questions must sound like a real senior engineering interview.

12. Every technical question must reference at least one:
   - project
   - internship
   - technology from resume

13. Use Context Data heavily.

14. Prefer engineering and implementation questions over textbook theory.

TOPICS DATA:
{json.dumps(topics_data, ensure_ascii=False)}

RESUME DATA:
{json.dumps(resume_data, ensure_ascii=False)}

JD DATA:
{json.dumps(jd_data, ensure_ascii=False)}

MATCH DATA:
{json.dumps(match_data, ensure_ascii=False)}

CONTEXT DATA:
{json.dumps(context_data, ensure_ascii=False)}
"""

        # --------------------------------------------------
        # GROQ REQUEST
        # --------------------------------------------------

        try:

            response = client.chat.completions.create(

                model="openai/gpt-oss-20b",

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.2,

                max_completion_tokens=8000,

                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "interview_questions",
                        "strict": True,
                        "schema": schema
                    }
                },

                reasoning_format="hidden"

            )

        except Exception as e:

            print("\n========== GROQ API ERROR ==========")
            print(type(e).__name__)
            print(str(e))
            print("====================================\n")

            raise RuntimeError(
                f"Question generation failed: {str(e)}"
            )

        # --------------------------------------------------
        # READ RESPONSE
        # --------------------------------------------------

        try:

            content = response.choices[0].message.content

            if not content:
                raise ValueError(
                    "Groq returned an empty response."
                )

            print("\n========== RAW GROQ RESPONSE ==========")
            print(content)
            print("========================================")

        except Exception as e:

            print("\n========== GROQ RESPONSE ERROR ==========")
            print(str(e))
            print("==========================================")

            raise RuntimeError(
                "Groq returned an invalid response."
            )

        # --------------------------------------------------
        # PARSE JSON
        # --------------------------------------------------

        try:

            result = json.loads(content)

        except json.JSONDecodeError as e:

            print("\n========== JSON PARSE ERROR ==========")
            print(str(e))
            print("\nRAW RESPONSE:")
            print(content)
            print("======================================")

            raise RuntimeError(
                "Groq returned invalid JSON."
            )

        # --------------------------------------------------
        # VALIDATE BASIC STRUCTURE
        # --------------------------------------------------

        required_keys = [
            "topics",
            "project_questions",
            "behavioral_questions",
            "missing_skill_questions"
        ]

        for key in required_keys:

            if key not in result:

                raise RuntimeError(
                    f"Question generator response missing key: {key}"
                )

        print("\n========== QUESTION GENERATOR SUCCESS ==========")
        print(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False
            )
        )
        print("================================================\n")

        return result