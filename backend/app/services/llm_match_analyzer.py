import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class LLMMatchAnalyzer:

    def analyze(
        self,
        resume_data,
        jd_data
    ):

        prompt = f"""
You are an expert technical recruiter and ATS evaluator.

Analyze the candidate's resume against the job description.

IMPORTANT:

Do not rely only on exact skill matches.

Infer skills from:
- Projects
- Technologies used
- Work experience
- Internship experience
- AI/ML frameworks
- APIs
- Tools

Examples:

TensorFlow -> Machine Learning
PyTorch -> Deep Learning
LangChain -> LLMs
RAG -> Generative AI
FastAPI -> API Development
Node.js -> Backend Development
OpenAI -> Generative AI

A skill cannot appear in both matched_skills and missing_skills.

Before generating the final response:
1. Remove duplicates.
2. Ensure matched_skills and missing_skills are mutually exclusive.

Return ONLY valid JSON.

Do NOT explain.
Do NOT add markdown.
Do NOT write anything before or after the JSON.

Schema:

{{
    "match_percentage": 0,
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "reasoning": ""
}}

Resume:

{json.dumps(resume_data, indent=2)}

Job Description:

{json.dumps(jd_data, indent=2)}
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

            # Extract only the JSON object
            start = content.find("{")
            end = content.rfind("}")

            if start == -1 or end == -1:
                raise ValueError("No JSON object found.")

            content = content[start:end + 1]

            result = json.loads(content)

            # Ensure all required keys exist
            result.setdefault("match_percentage", 0)
            result.setdefault("matched_skills", [])
            result.setdefault("missing_skills", [])
            result.setdefault("strengths", [])
            result.setdefault("reasoning", "")

            return result

        except Exception as e:

            print("\nLLM MATCH ANALYZER ERROR")
            print(e)

            print("\nRAW RESPONSE")
            print(content)

            return {
                "match_percentage": 0,
                "matched_skills": [],
                "missing_skills": [],
                "strengths": [],
                "reasoning": "Unable to analyze resume and job description."
            }