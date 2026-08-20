import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class JDAnalyzer:

    def analyze_jd(self, jd_text):

        prompt = f"""
You are an expert job description analyzer.

Extract information from the job description.

Return ONLY valid JSON.

Schema:

{{
    "job_title": "",
    "required_skills": [],
    "responsibilities": [],
    "experience_required": ""
}}

Job Description:

{jd_text}
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