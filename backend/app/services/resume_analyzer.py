import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class ResumeAnalyzer:

    def analyze_resume(self, resume_text):

        prompt = f"""
You are an expert ATS resume parser and recruiter.

Analyze the ENTIRE resume.

IMPORTANT:

Extract skills from:
- Skills section
- Projects
- Project technologies
- Work experience
- Certifications
- Frameworks
- Libraries
- Databases
- APIs
- Cloud platforms
- AI/ML technologies

Infer skills from project descriptions.

Example:

If a project uses LangChain,
include LangChain as a skill.

If a project uses RAG,
include RAG as a skill.

If a project uses FastAPI,
include FastAPI as a skill.

Return ONLY valid JSON.

Schema:

{{
    "name": "",

    "skills": [],

    "projects": [
        {{
            "name": "",
            "description": "",
            "technologies": []
        }}
    ],

    "experience": [
        {{
            "role": "",
            "company": "",
            "skills_used": []
        }}
    ],

    "education": [
        {{
            "degree": "",
            "institution": ""
        }}
    ]
}}

Resume:

{resume_text}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
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

        try:

            content = (
                content
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            return json.loads(content)

        except Exception as e:

            return {
                "error": str(e),
                "raw_response": content
            }