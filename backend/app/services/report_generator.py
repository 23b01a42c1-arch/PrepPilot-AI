import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class ReportGenerator:

    def generate(
        self,
        interview_history
    ):

        prompt = f"""
You are a senior technical interviewer.

Analyze the complete interview.

Evaluate:

1. Technical Knowledge (0-100)
2. Communication Skills (0-100)
3. Problem Solving Ability (0-100)
4. Confidence Level (0-100)
5. Overall Score (0-100)

Identify:

- Top Strengths
- Weak Areas
- Missing Concepts

Provide:

- Recommendation
  (Reject / Borderline / Proceed)

Return ONLY valid JSON.

Interview History:

{json.dumps(interview_history, indent=2)}

Generate a final interview report.

Return ONLY JSON.

Schema:

{{
    "overall_score": 0,
    "technical_score": 0,
    "communication_score": 0,
    "strengths": [],
    "weaknesses": [],
    "recommendation": ""
}}
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
        )

        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(content)