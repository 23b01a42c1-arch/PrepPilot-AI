import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class FollowupGenerator:

    def generate(
        self,
        question,
        answer,
        evaluation
    ):

        prompt = f"""
You are a senior technical interviewer.

Original Question:
{question}

Candidate Answer:
{answer}

Evaluation:
{json.dumps(evaluation, indent=2)}

Generate ONE follow-up question.

Rules:

- Ask deeper about the answer.
- Focus on missing concepts.
- Focus on weak areas.
- Sound like a real interviewer.

Return ONLY JSON.

Schema:

{{
    "followup_question":""
}}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
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

        return json.loads(content)