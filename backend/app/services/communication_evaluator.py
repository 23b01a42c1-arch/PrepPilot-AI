import json
import os
from tracemalloc import start
from tracemalloc import start
from unittest import result

from groq import Groq
from dotenv import load_dotenv
from sympy import content

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class CommunicationEvaluator:

    def evaluate(
        self,
        answer
    ):

        prompt = f"""
Evaluate the communication quality of this interview answer.

Answer:

{answer}

Return ONLY valid JSON.

Even if the answer is empty, invalid, or too short,
you MUST still return valid JSON.

Example:

    {{
        "communication_score": 0,
        "clarity": 0,
        "structure": 0,
        "confidence": 0,
        "professionalism": 0,
        "feedback": [
            "Answer was empty"
        ]
}}



Scoring:

clarity:
0-10

structure:
0-10

confidence:
0-10

professionalism:
0-10

communication_score:
average of all categories × 10
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
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

        try:

            start = content.find("{")
            end = content.rfind("}")

            if start != -1 and end != -1:
                content = content[start:end + 1]

            result = json.loads(content)

            result["communication_score"] = round(
                (
                    result["clarity"]
                    +
                    result["structure"]
                    +
                    result["confidence"]
                    +
                    result["professionalism"]
                ) / 4 * 10,
                2
            )

            return result

        except Exception as e:

            print("\nCOMMUNICATION EVALUATOR ERROR")
            print(e)

            print("\nRAW RESPONSE")
            print(content)

            return {
                "communication_score": 0,
                "clarity": 0,
                "structure": 0,
                "confidence": 0,
                "professionalism": 0,
                "feedback": [
                    "Failed to evaluate communication"
                ]
            }