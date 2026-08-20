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
        You are an ATS resume parser.

        Read the complete resume and extract only information explicitly present in it.

        Return ONLY one valid JSON object.

        The JSON must have exactly these fields:

        {{
        "name": "",
        "skills": [],
        "projects": [],
        "experience": [],
        "education": []
        }}

        Rules:
        - Output valid JSON only.
        - No markdown.
        - No ```json.
        - No explanations.
        - Do not invent information.
        - Include every project mentioned in the resume.
        - Include all relevant technical skills found in skills, projects, experience, certifications, and technologies.
        - Use empty arrays if a section is missing.

        For each project use:
        {{
        "name": "",
        "description": "",
        "technologies": []
        }}

        For each experience entry use:
        {{
        "role": "",
        "company": "",
        "skills_used": []
        }}

        For each education entry use:
        {{
        "degree": "",
        "institution": ""
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