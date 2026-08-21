import json
import os

from groq import Groq, RateLimitError, BadRequestError
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class QuestionGenerator:

    def _compact(self, data, max_chars=6000):
        """
        Convert large objects into a compact JSON string.
        Prevents unnecessarily large prompts.
        """
        try:
            text = json.dumps(
                data,
                ensure_ascii=False,
                separators=(",", ":")
            )
        except Exception:
            text = str(data)

        if len(text) > max_chars:
            text = text[:max_chars] + "...[truncated]"

        return text

    def generate_questions(
        self,
        resume_data,
        jd_data,
        match_data,
        topics_data,
        context_data
    ):

        print("\n========== QUESTION GENERATOR START ==========")

        print(
            "Topics available:",
            bool(topics_data)
        )

        print(
            "Resume data available:",
            bool(resume_data)
        )

        print(
            "JD data available:",
            bool(jd_data)
        )

        print(
            "Match data available:",
            bool(match_data)
        )

        print(
            "Context data available:",
            bool(context_data)
        )

        print("==============================================")

        # -------------------------------------------------
        # Keep prompt size under control
        # -------------------------------------------------

        topics = self._compact(
            topics_data,
            5000
        )

        resume = self._compact(
            resume_data,
            7000
        )

        jd = self._compact(
            jd_data,
            5000
        )

        match = self._compact(
            match_data,
            4000
        )

        context = self._compact(
            context_data,
            6000
        )

        # -------------------------------------------------
        # Compact output schema
        # -------------------------------------------------

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
                "string",
                "string",
                "string"
            ],
            "behavioral_questions": [
                "string",
                "string",
                "string"
            ],
            "missing_skill_questions": [
                "string"
            ]
        }

        prompt = f"""
You are a senior technical interviewer.

Create a personalized interview question plan.

RETURN ONLY JSON.
DO NOT use markdown.
DO NOT use ```json.
DO NOT add explanations before or after JSON.

OUTPUT FORMAT:

{json.dumps(schema, separators=(",", ":"))}

RULES:

1. Use only topics provided in Topics Data.

2. For every topic generate exactly:
- 1 easy question
- 1 medium question
- 1 hard question

3. Technical questions must reference evidence from:
- resume
- projects
- internship
- technologies
- JD requirements

4. Avoid generic textbook questions when resume evidence exists.

BAD:
"What is RAG?"

GOOD:
"In your PDF Question Answering project, how did you use RAG and Qdrant to retrieve relevant document chunks?"

5. Difficulty:

EASY:
Implementation, workflow, practical usage.

MEDIUM:
Architecture, debugging, design decisions, tradeoffs.

HARD:
Scaling, optimization, reliability, production architecture.

6. Generate exactly:
- 3 project questions
- 3 behavioral questions
- 1 question for each missing skill.

7. Avoid duplicates.

8. Questions must sound like a real senior-engineer interview.

9. Behavioral questions should use the candidate's actual experience where possible.

10. Do not invent projects, internships, technologies or experience.

TOPICS:
{topics}

RESUME:
{resume}

JOB DESCRIPTION:
{jd}

MATCH:
{match}

CONTEXT:
{context}
"""

        try:

            print(
                "\nCalling Groq question generation..."
            )

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a senior technical interviewer. "
                            "Return only valid JSON."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_tokens=5000
            )

            content = (
                response
                .choices[0]
                .message
                .content
                .strip()
            )

            print(
                "\n========== RAW GROQ RESPONSE =========="
            )
            print(content)
            print(
                "========================================"
            )

        except RateLimitError as e:

            print(
                "\n========== GROQ RATE LIMIT =========="
            )
            print(str(e))
            print(
                "====================================="
            )

            raise RuntimeError(
                "Groq API rate limit reached. "
                "Please wait for the quota to reset and try again."
            )

        except BadRequestError as e:

            print(
                "\n========== GROQ BAD REQUEST =========="
            )
            print(str(e))
            print(
                "======================================"
            )

            raise RuntimeError(
                f"Groq rejected the question generation request: {str(e)}"
            )

        except Exception as e:

            print(
                "\n========== GROQ QUESTION GENERATOR ERROR =========="
            )
            print(type(e).__name__)
            print(str(e))
            print(
                "===================================================="
            )

            raise RuntimeError(
                f"Question generation failed: {str(e)}"
            )

        # -------------------------------------------------
        # Clean JSON
        # -------------------------------------------------

        content = content.strip()

        if content.startswith("```"):
            content = content.replace(
                "```json",
                ""
            )

            content = content.replace(
                "```",
                ""
            )

            content = content.strip()

        # -------------------------------------------------
        # Parse JSON
        # -------------------------------------------------

        try:

            result = json.loads(content)

        except json.JSONDecodeError as e:

            print(
                "\n========== QUESTION JSON ERROR =========="
            )

            print(
                "Error:",
                str(e)
            )

            print(
                "RAW RESPONSE:"
            )

            print(content)

            print(
                "========================================="
            )

            raise RuntimeError(
                "Groq returned invalid JSON for interview questions."
            )

        # -------------------------------------------------
        # Basic validation
        # -------------------------------------------------

        if not isinstance(result, dict):

            raise RuntimeError(
                "Question generator returned an invalid response."
            )

        if "topics" not in result:

            result["topics"] = []

        if "project_questions" not in result:

            result["project_questions"] = []

        if "behavioral_questions" not in result:

            result["behavioral_questions"] = []

        if "missing_skill_questions" not in result:

            result["missing_skill_questions"] = []

        print(
            "\n========== QUESTION GENERATOR SUCCESS =========="
        )

        print(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False
            )
        )

        print(
            "================================================="
        )

        return result