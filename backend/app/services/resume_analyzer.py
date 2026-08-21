import json
import os

from groq import Groq, RateLimitError, BadRequestError
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class ResumeAnalyzer:

    def analyze_resume(self, resume_text):

        # Prevent unnecessarily huge prompts.
        # Resume text itself is the important input.
        if not resume_text or not resume_text.strip():
            return {
                "error": "Resume text is empty.",
                "name": "",
                "skills": [],
                "projects": [],
                "experience": [],
                "education": []
            }

        # Keep extremely large resumes from consuming excessive tokens.
        # Normal resumes will not be affected.
        resume_text = resume_text.strip()

        if len(resume_text) > 30000:
            resume_text = resume_text[:30000]

        prompt = f"""
You are an ATS resume parser.

Extract ONLY information explicitly present in the resume.

Return ONLY one valid JSON object.

Required JSON structure:

{{
  "name": "",
  "skills": [],
  "projects": [],
  "experience": [],
  "education": []
}}

Rules:

- Valid JSON only.
- No markdown.
- No ```json.
- No explanations.
- Do not invent information.
- Include every project mentioned.
- Include relevant technical skills from the resume.
- Use [] when a section is missing.

Project format:

{{
  "name": "",
  "description": "",
  "technologies": []
}}

Experience format:

{{
  "role": "",
  "company": "",
  "skills_used": []
}}

Education format:

{{
  "degree": "",
  "institution": ""
}}

Resume:

{resume_text}
"""

        try:

            print("\n========== RESUME ANALYZER ==========")
            print(
                "Resume characters:",
                len(resume_text)
            )
            print("Calling Groq...")
            print("=====================================")

            response = client.chat.completions.create(

                model="llama-3.1-8b-instant",

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an ATS resume parser. "
                            "Return only valid JSON."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0,

                # Smaller maximum output.
                # Resume extraction does not need thousands
                # of generated tokens.
                max_tokens=1800
            )

        except RateLimitError as e:

            print("\n========== GROQ RATE LIMIT ==========")
            print(str(e))
            print("=====================================")

            raise RuntimeError(
                "Groq API rate limit reached. "
                "Please wait for the Groq quota to reset."
            )

        except BadRequestError as e:

            print("\n========== GROQ BAD REQUEST ==========")
            print(str(e))
            print("======================================")

            raise RuntimeError(
                f"Groq rejected the resume analysis request: {str(e)}"
            )

        except Exception as e:

            print("\n========== RESUME ANALYZER ERROR ==========")
            print(type(e).__name__)
            print(str(e))
            print("===========================================")

            raise RuntimeError(
                f"Resume analysis failed: {str(e)}"
            )

        # --------------------------------------------------
        # Get model response
        # --------------------------------------------------

        if not response.choices:

            raise RuntimeError(
                "Groq returned no choices."
            )

        message = response.choices[0].message

        content = message.content or ""

        reasoning = getattr(
            message,
            "reasoning",
            None
        ) or ""

        print("\n========== GROQ RESPONSE ==========")

        print(
            "CONTENT:",
            repr(content)
        )

        print(
            "REASONING:",
            repr(reasoning)
        )

        print("===================================")

        # GPT-OSS can sometimes place useful output
        # in reasoning if content is empty.
        if not content.strip():
            content = reasoning

        content = content.strip()

        # --------------------------------------------------
        # Remove markdown fences
        # --------------------------------------------------

        if "```json" in content:
            content = content.replace(
                "```json",
                ""
            )

        if "```" in content:
            content = content.replace(
                "```",
                ""
            )

        content = content.strip()

        # --------------------------------------------------
        # Extract JSON object
        # --------------------------------------------------

        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1 or end <= start:

            print(
                "\n========== INVALID GROQ RESPONSE =========="
            )

            print(content)

            print(
                "==========================================="
            )

            raise RuntimeError(
                "Groq did not return a valid JSON object."
            )

        json_content = content[
            start:end + 1
        ]

        # --------------------------------------------------
        # Parse JSON
        # --------------------------------------------------

        try:

            result = json.loads(
                json_content
            )

        except json.JSONDecodeError as e:

            print(
                "\n========== JSON PARSING ERROR =========="
            )

            print(
                "ERROR:",
                str(e)
            )

            print(
                "RAW:",
                repr(json_content)
            )

            print(
                "========================================"
            )

            raise RuntimeError(
                "Groq returned malformed JSON."
            )

        # --------------------------------------------------
        # Ensure expected fields always exist
        # --------------------------------------------------

        result.setdefault(
            "name",
            ""
        )

        result.setdefault(
            "skills",
            []
        )

        result.setdefault(
            "projects",
            []
        )

        result.setdefault(
            "experience",
            []
        )

        result.setdefault(
            "education",
            []
        )

        print(
            "\n========== RESUME ANALYSIS SUCCESS =========="
        )

        print(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False
            )
        )

        print(
            "============================================="
        )

        return result