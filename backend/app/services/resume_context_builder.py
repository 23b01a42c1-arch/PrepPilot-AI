import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


class ResumeContextBuilder:

    def build(
        self,
        resume_data,
        topics_data
    ):

        prompt = f"""
You are a senior technical interviewer.

Your job is to connect the candidate's
resume evidence with the extracted topics.

For each topic:

1. Find relevant skills
2. Find relevant projects
3. Find relevant experience

Return ONLY JSON.

Schema:

{{
    "domains": [
        {{
            "topic": "",
            "evidence": []
        }}
    ]
}}

Resume:

{resume_data}

Topics:

{topics_data}
"""

        response = (
            client.chat.completions.create(
                model=
                "openai/gpt-oss-20b",

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
        )

        try:

            content = (
                content
                .replace(
                    "```json",
                    ""
                )
                .replace(
                    "```",
                    ""
                )
                .strip()
            )

            return json.loads(
                content
            )

        except Exception:

            return {
                "error":
                    "Failed to parse response",

                "raw_response":
                    content
            }