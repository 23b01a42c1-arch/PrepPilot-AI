import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class AnswerEvaluator:

    def evaluate(
        self,
        question,
        answer
    ):

        prompt = f"""
You are a senior technical interviewer.

Evaluate the candidate answer.

Return ONLY valid JSON.

Schema:

{{
    "score": 0,
    "strengths": [],
    "missing_points": []
}}

Scoring Guide:

9-10:
Excellent answer.
Comprehensive, technically correct, practical.

7-8:
Good answer.
Minor gaps.

5-6:
Average answer.
Important details missing.

0-4:
Weak answer.
Major gaps or incorrect answer.

Question:
{question}

Answer:
{answer}
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        content = (
            response
            .choices[0]
            .message
            .content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:

            return json.loads(content)

        except Exception:

            return {
                "score": 5,
                "strengths": [],
                "missing_points": [
                    "Failed to parse evaluation"
                ]
            }