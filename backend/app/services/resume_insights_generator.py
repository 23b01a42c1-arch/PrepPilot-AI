import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class ResumeInsightsGenerator:

    def generate(
        self,
        resume_data,
        jd_data,
        match_data
    ):

        prompt = f"""
You are a senior ATS recruiter and resume reviewer.

Analyze the resume against the job description.

Return ONLY valid JSON.

Schema:

{{
    "ats_score": 0,
    "readiness_score": 0,
    "strengths": [],
    "weaknesses": [],
    "suggestions": [],
    "match_breakdown": {{
        "skills": 0,
        "projects": 0,
        "experience": 0,
        "education": 0
    }}
}}

Rules:

ATS Score:
0-100

Readiness Score:
0-100

Generate 5 strengths.

Generate 5 weaknesses.

Generate 5 suggestions.

Match Breakdown should contain percentages
for:

Skills
Projects
Experience
Education

Resume:

{json.dumps(resume_data, indent=2)}

Job Description:

{json.dumps(jd_data, indent=2)}

Match Data:

{json.dumps(match_data, indent=2)}
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

        try:

            content = (
                content
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            return json.loads(content)

        except Exception:

            return {

                "ats_score": 0,

                "readiness_score": 0,

                "strengths": [],

                "weaknesses": [],

                "suggestions": [],

                "match_breakdown": {

                    "skills": 0,

                    "projects": 0,

                    "experience": 0,

                    "education": 0
                }
            }