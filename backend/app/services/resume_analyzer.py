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

Examples:
- If a project uses LangChain, include LangChain as a skill.
- If a project uses RAG, include RAG as a skill.
- If a project uses FastAPI, include FastAPI as a skill.

CRITICAL OUTPUT RULES:

1. Return ONLY a valid JSON object.
2. Do NOT use markdown.
3. Do NOT include ```json.
4. Do NOT include explanations.
5. Do NOT include text before or after the JSON.
6. Every field in the schema must be present.
7. Use empty arrays when information is unavailable.
8. Do not invent information.

Return exactly this structure:

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
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            max_tokens=3000
            
        )

        print("========== GROQ RESPONSE ==========")
        print("CHOICES:", len(response.choices))

        if response.choices:
            print(
                "CONTENT:",
                repr(response.choices[0].message.content)
            )

            print(
                "REASONING:",
                repr(
                    getattr(
                        response.choices[0].message,
                        "reasoning",
                        None
                    )
                )
            )

        print("===================================")

        if not response.choices:
            return {
                "error": "Groq returned no choices.",
                "raw_response": ""
            }

        message = response.choices[0].message

        content = message.content or ""

        reasoning = getattr(
            message,
            "reasoning",
            None
        ) or ""

        print("========== GROQ RESPONSE ==========")
        print("CONTENT:", repr(content))
        print("REASONING:", repr(reasoning))
        print("===================================")

        # Prefer the normal response content.
        # If content is empty, use reasoning because GPT-OSS
        # may place the generated answer there.
        if not content.strip():
            content = reasoning

        content = content.strip()

        # Remove markdown fences if present
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        # Find the JSON object inside the model response
        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1 or end <= start:
            return {
                "error": "No JSON object found in Groq response.",
                "raw_response": content
            }

        json_content = content[start:end + 1]

        try:
            return json.loads(json_content)

        except json.JSONDecodeError as e:

            print("JSON PARSING ERROR:", str(e))
            print("EXTRACTED JSON:", repr(json_content))

            return {
                "error": str(e),
                "raw_response": json_content
            }