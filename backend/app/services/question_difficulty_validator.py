import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class QuestionDifficultyValidator:

    def validate(
        self,
        question
    ):

        prompt = f"""
You are a senior technical interviewer.

Classify the difficulty.

Return ONLY JSON.

{{
    "difficulty": "easy|medium|hard"
}}

Guidelines:

Easy:
- definitions
- fundamentals
- basic workflows
- explaining used technologies

Medium:
- implementation
- debugging
- tradeoffs
- architecture decisions

Hard:
- system design
- scalability
- distributed systems
- optimization
- production scenarios

Question:

{question}
"""

        response = (
            client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )
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