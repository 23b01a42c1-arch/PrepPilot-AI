import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class TopicExtractor:

    def extract_topics(
        self,
        resume_data
    ):

        prompt = f"""
You are an expert AI technical interviewer.

Analyze the candidate profile.

Identify technical KNOWLEDGE DOMAINS.

Prioritize:

- project experience
- internship experience
- technologies repeatedly used

Avoid generic domains like:
- Data Storage
- Human Computer Interaction
- Programming

Do NOT return:

- programming languages
- frameworks
- libraries
- tools

Return higher-level domains only.

Return ONLY valid JSON.

Schema:

{{
    "topics": [
        {{
            "name": "",
            "confidence": 0
        }}
    ]
}}

Rules:

- confidence must be between 0 and 100
- return top 5 topics only
- sort by confidence descending

Candidate:

{resume_data}
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
                "topics": []
            }