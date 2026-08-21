import json
import os

from dotenv import load_dotenv
from groq import Groq

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

        # ---------------------------------------------------------
        # OUTPUT SCHEMA
        # ---------------------------------------------------------

        schema = {
            "topics": [
                {
                    "topic": "string",
                    "questions": [
                        {
                            "difficulty": "easy",
                            "question": "string"
                        },
                        {
                            "difficulty": "medium",
                            "question": "string"
                        },
                        {
                            "difficulty": "hard",
                            "question": "string"
                        }
                    ]
                }
            ],
            "project_questions": [
                "string"
            ],
            "behavioral_questions": [
                "string"
            ],
            "missing_skill_questions": [
                "string"
            ]
        }

        # ---------------------------------------------------------
        # CLEAN DATA
        # ---------------------------------------------------------

        def safe_json(data):
            try:
                return json.dumps(
                    data,
                    ensure_ascii=False,
                    separators=(",", ":")
                )
            except Exception:
                return "{}"

        topics_json = safe_json(topics_data)
        resume_json = safe_json(resume_data)
        jd_json = safe_json(jd_data)
        match_json = safe_json(match_data)
        context_json = safe_json(context_data)

        # ---------------------------------------------------------
        # PROMPT
        # ---------------------------------------------------------

        prompt = f"""
You are a senior technical interviewer creating a personalized interview.

Return ONLY one valid JSON object.
Do NOT return markdown.
Do NOT return ```json.
Do NOT return explanations outside the JSON.

The JSON MUST follow this exact structure:

{json.dumps(schema, indent=2)}

IMPORTANT RULES:

1. Use ONLY topics present in Topics Data.

2. For every selected topic generate exactly:
   - 1 easy question
   - 1 medium question
   - 1 hard question

3. Personalize technical questions using evidence from:
   - Resume Data
   - Projects
   - Internship/experience
   - Technologies
   - JD requirements
   - Context Data

4. Do NOT invent projects, technologies, companies, experience,
   achievements, or responsibilities.

5. If resume evidence exists for a technology, prefer practical
   implementation questions instead of definitions.

6. Avoid generic questions such as:
   - What is Python?
   - What is RAG?
   - What is FastAPI?
   - What is NLP?
   - Define machine learning.

7. Difficulty:

EASY:
Ask about implementation, workflow, usage, or architecture
components that the candidate actually used.

MEDIUM:
Ask about design decisions, tradeoffs, debugging,
architecture choices, or technology selection.

HARD:
Ask about scaling, optimization, reliability,
fault tolerance, monitoring, security, or production design.

8. If project evidence exists, create implementation-focused questions.

9. If internship/experience evidence exists, create
   production-oriented questions.

10. If both project and experience evidence exist, combine
    both perspectives.

11. If only a skill is available, ask a practical engineering
    question about that skill.

12. Generate exactly:
    - 3 project questions
    - 3 behavioral questions
    - 1 question for every missing skill

13. Do not duplicate questions.

14. Every technical question MUST reference at least one
    project, internship/experience, or technology from the resume.

15. Behavioral questions should be based on the candidate's
    actual experience where possible.

16. Missing-skill questions should target skills listed in
    Match Data as missing.

17. Use Context Data heavily for personalization.

18. Keep questions concise and interview-ready.

19. The response MUST be valid JSON.

TOPICS DATA:
{topics_json}

RESUME DATA:
{resume_json}

JD DATA:
{jd_json}

MATCH DATA:
{match_json}

CONTEXT DATA:
{context_json}
"""

        # ---------------------------------------------------------
        # DEBUG LOG
        # ---------------------------------------------------------

        print("\n========== QUESTION GENERATOR START ==========")
        print("Topics available:", len(topics_data) if isinstance(topics_data, list) else "N/A")
        print("Resume data available:", bool(resume_data))
        print("JD data available:", bool(jd_data))
        print("Match data available:", bool(match_data))
        print("Context data available:", bool(context_data))
        print("==============================================\n")

        # ---------------------------------------------------------
        # GROQ REQUEST
        # ---------------------------------------------------------

        try:

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a senior technical interviewer. "
                            "Always return valid JSON matching the requested schema."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.2,

                response_format={
                    "type": "json_object"
                }
            )

        except Exception as e:

            print("\n========== GROQ QUESTION GENERATOR ERROR ==========")
            print(type(e).__name__)
            print(str(e))
            print("===================================================\n")

            raise

        # ---------------------------------------------------------
        # EXTRACT RESPONSE
        # ---------------------------------------------------------

        try:

            content = response.choices[0].message.content

            if not content:
                raise ValueError("Groq returned an empty response.")

            content = content.strip()

            print("\n========== RAW QUESTION GENERATOR RESPONSE ==========")
            print(content)
            print("======================================================\n")

        except Exception as e:

            print("\n========== RESPONSE EXTRACTION ERROR ==========")
            print(str(e))
            print("===============================================\n")

            raise

        # ---------------------------------------------------------
        # REMOVE MARKDOWN IF MODEL ADDS IT
        # ---------------------------------------------------------

        if content.startswith("```json"):
            content = content[7:]

        elif content.startswith("```"):
            content = content[3:]

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        # ---------------------------------------------------------
        # PARSE JSON
        # ---------------------------------------------------------

        try:

            result = json.loads(content)

        except json.JSONDecodeError as e:

            print("\n========== QUESTION JSON PARSE ERROR ==========")
            print("Error:", str(e))
            print("Raw response:")
            print(content)
            print("===============================================\n")

            raise ValueError(
                f"Question generator returned invalid JSON: {e}"
            )

        # ---------------------------------------------------------
        # VALIDATE TOP-LEVEL STRUCTURE
        # ---------------------------------------------------------

        required_fields = [
            "topics",
            "project_questions",
            "behavioral_questions",
            "missing_skill_questions"
        ]

        for field in required_fields:

            if field not in result:
                raise ValueError(
                    f"Question generator response missing field: {field}"
                )

        # ---------------------------------------------------------
        # NORMALIZE ARRAYS
        # ---------------------------------------------------------

        if not isinstance(result["topics"], list):
            result["topics"] = []

        if not isinstance(result["project_questions"], list):
            result["project_questions"] = []

        if not isinstance(result["behavioral_questions"], list):
            result["behavioral_questions"] = []

        if not isinstance(result["missing_skill_questions"], list):
            result["missing_skill_questions"] = []

        # ---------------------------------------------------------
        # VALIDATE TOPIC QUESTIONS
        # ---------------------------------------------------------

        valid_topics = []

        for topic in result["topics"]:

            if not isinstance(topic, dict):
                continue

            topic_name = topic.get("topic")

            questions = topic.get("questions")

            if not topic_name or not isinstance(questions, list):
                continue

            valid_questions = []

            for question in questions:

                if not isinstance(question, dict):
                    continue

                difficulty = question.get("difficulty")
                question_text = question.get("question")

                if difficulty not in [
                    "easy",
                    "medium",
                    "hard"
                ]:
                    continue

                if not question_text:
                    continue

                valid_questions.append(
                    {
                        "difficulty": difficulty,
                        "question": str(question_text).strip()
                    }
                )

            if valid_questions:

                valid_topics.append(
                    {
                        "topic": str(topic_name).strip(),
                        "questions": valid_questions
                    }
                )

        result["topics"] = valid_topics

        # ---------------------------------------------------------
        # CLEAN QUESTION ARRAYS
        # ---------------------------------------------------------

        def clean_question_list(items):

            cleaned = []

            for item in items:

                if isinstance(item, str):

                    question = item.strip()

                    if question:
                        cleaned.append(question)

                elif isinstance(item, dict):

                    question = item.get("question")

                    if question:
                        cleaned.append(
                            str(question).strip()
                        )

            # Remove duplicates while preserving order

            return list(dict.fromkeys(cleaned))

        result["project_questions"] = clean_question_list(
            result["project_questions"]
        )

        result["behavioral_questions"] = clean_question_list(
            result["behavioral_questions"]
        )

        result["missing_skill_questions"] = clean_question_list(
            result["missing_skill_questions"]
        )

        # ---------------------------------------------------------
        # FINAL LOG
        # ---------------------------------------------------------

        print("\n========== QUESTION GENERATOR SUCCESS ==========")

        print(
            "Topics:",
            len(result["topics"])
        )

        print(
            "Project questions:",
            len(result["project_questions"])
        )

        print(
            "Behavioral questions:",
            len(result["behavioral_questions"])
        )

        print(
            "Missing skill questions:",
            len(result["missing_skill_questions"])
        )

        print("================================================\n")

        return result