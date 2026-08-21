import json
import os
import re

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class QuestionGenerator:

    def generate_questions(
        self,
        resume_data,
        jd_data,
        match_data,
        topics_data,
        context_data
    ):

        print("\n========== QUESTION GENERATOR START ==========")
        print("Topics available:", topics_data if topics_data else "N/A")
        print("Resume data available:", bool(resume_data))
        print("JD data available:", bool(jd_data))
        print("Match data available:", bool(match_data))
        print("Context data available:", bool(context_data))
        print("==============================================")

        # --------------------------------------------------
        # Normalize topics
        # --------------------------------------------------

        if isinstance(topics_data, dict):

            topics = (
                topics_data.get("topics")
                or topics_data.get("technical_topics")
                or topics_data.get("technology_topics")
                or []
            )

        elif isinstance(topics_data, list):

            topics = topics_data

        else:

            topics = []

        # Convert topic objects into readable strings
        normalized_topics = []

        for topic in topics:

            if isinstance(topic, str):

                normalized_topics.append(topic)

            elif isinstance(topic, dict):

                name = (
                    topic.get("topic")
                    or topic.get("name")
                    or topic.get("technology")
                )

                if name:
                    normalized_topics.append(str(name))

        # Remove duplicates
        normalized_topics = list(
            dict.fromkeys(normalized_topics)
        )

        # --------------------------------------------------
        # Fallback topics
        # --------------------------------------------------

        if not normalized_topics:

            normalized_topics = [
                "Python",
                "Machine Learning",
                "TensorFlow",
                "GitHub",
                "MySQL",
                "DBMS"
            ]

        print(
            "Normalized topics:",
            normalized_topics
        )

        # --------------------------------------------------
        # Output schema
        # --------------------------------------------------

        schema = {
            "topics": [
                {
                    "topic": "Python",
                    "questions": [
                        {
                            "difficulty": "easy",
                            "question": "Example question"
                        },
                        {
                            "difficulty": "medium",
                            "question": "Example question"
                        },
                        {
                            "difficulty": "hard",
                            "question": "Example question"
                        }
                    ]
                }
            ],
            "project_questions": [
                "Example project question"
            ],
            "behavioral_questions": [
                "Example behavioral question"
            ],
            "missing_skill_questions": [
                "Example missing skill question"
            ]
        }

        # --------------------------------------------------
        # Build prompt
        # --------------------------------------------------

        prompt = f"""
You are a senior technical interviewer.

Create a personalized technical interview plan.

IMPORTANT:
Return ONLY valid JSON.
Do NOT use markdown.
Do NOT use ```json.
Do NOT add explanations before or after the JSON.

The JSON MUST follow this exact structure:

{json.dumps(schema, indent=2)}

INTERVIEW RULES:

1. Use the candidate's resume heavily.

2. Use the Job Description heavily.

3. Use Match Data and Context Data.

4. Questions must be personalized.

5. Avoid generic textbook questions whenever resume evidence exists.

6. For every topic generate exactly:

- 1 easy question
- 1 medium question
- 1 hard question

7. EASY questions should focus on:

- implementation
- workflow
- practical usage
- architecture components

8. MEDIUM questions should focus on:

- design decisions
- tradeoffs
- debugging
- architecture choices
- technology selection

9. HARD questions should focus on:

- scalability
- optimization
- production systems
- fault tolerance
- monitoring
- distributed systems

10. Generate exactly:

- 3 project questions
- 3 behavioral questions
- 1 question for every missing skill

11. Avoid duplicate questions.

12. Technical questions should reference:

- a project
- internship experience
- or a technology appearing in the resume

13. Do not ask simple definitions when implementation evidence exists.

BAD:
"What is Python?"

BAD:
"What is TensorFlow?"

BAD:
"What is RAG?"

GOOD:
"How did you use TensorFlow when developing your CNN model, and what preprocessing steps were required before training?"

GOOD:
"How did you structure your Python code for your machine learning workflow?"

GOOD:
"How would you improve the scalability of your ML pipeline if the dataset increased significantly?"

TOPICS:

{json.dumps(normalized_topics, indent=2)}

RESUME DATA:

{json.dumps(resume_data, indent=2, default=str)}

JOB DESCRIPTION DATA:

{json.dumps(jd_data, indent=2, default=str)}

MATCH DATA:

{json.dumps(match_data, indent=2, default=str)}

CONTEXT DATA:

{json.dumps(context_data, indent=2, default=str)}
"""

        # --------------------------------------------------
        # Call Groq
        # --------------------------------------------------

        try:

            response = client.chat.completions.create(

                model="openai/gpt-oss-20b",

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You generate interview questions. "
                            "Return only valid JSON."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.2,

                max_tokens=8000
            )

            content = (
                response
                .choices[0]
                .message
                .content
                .strip()
            )

            print("\n========== RAW GROQ RESPONSE ==========")
            print(content)
            print("========================================")

        except Exception as e:

            print(
                "\n========== GROQ API ERROR =========="
            )

            print(type(e).__name__)
            print(str(e))

            print(
                "===================================="
            )

            return self._fallback_result(
                normalized_topics,
                match_data
            )

        # --------------------------------------------------
        # Clean response
        # --------------------------------------------------

        content = self._clean_json(content)

        # --------------------------------------------------
        # Parse JSON
        # --------------------------------------------------

        try:

            result = json.loads(content)

        except json.JSONDecodeError as e:

            print(
                "\n========== JSON PARSE ERROR =========="
            )

            print(str(e))

            print("\nCleaned response:")
            print(content)

            print(
                "====================================="
            )

            # Try extracting JSON object
            extracted = self._extract_json(content)

            if extracted:

                try:

                    result = json.loads(extracted)

                except Exception:

                    return self._fallback_result(
                        normalized_topics,
                        match_data
                    )

            else:

                return self._fallback_result(
                    normalized_topics,
                    match_data
                )

        # --------------------------------------------------
        # Validate structure
        # --------------------------------------------------

        result = self._validate_result(
            result,
            normalized_topics
        )

        print(
            "\n========== QUESTION GENERATOR SUCCESS =========="
        )

        print(
            json.dumps(
                result,
                indent=2
            )
        )

        print(
            "=================================================="
        )

        return result

    # ======================================================
    # CLEAN JSON
    # ======================================================

    def _clean_json(self, content):

        if not content:
            return ""

        content = content.strip()

        # Remove markdown fences
        content = re.sub(
            r"^```json\s*",
            "",
            content,
            flags=re.IGNORECASE
        )

        content = re.sub(
            r"^```\s*",
            "",
            content
        )

        content = re.sub(
            r"\s*```$",
            "",
            content
        )

        return content.strip()

    # ======================================================
    # EXTRACT JSON
    # ======================================================

    def _extract_json(self, content):

        if not content:
            return None

        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1:
            return None

        return content[start:end + 1]

    # ======================================================
    # VALIDATE
    # ======================================================

    def _validate_result(
        self,
        result,
        topics
    ):

        if not isinstance(result, dict):

            return self._fallback_result(
                topics,
                {}
            )

        result.setdefault(
            "topics",
            []
        )

        result.setdefault(
            "project_questions",
            []
        )

        result.setdefault(
            "behavioral_questions",
            []
        )

        result.setdefault(
            "missing_skill_questions",
            []
        )

        # Make sure topics is a list
        if not isinstance(
            result["topics"],
            list
        ):

            result["topics"] = []

        # Make sure every topic has questions
        cleaned_topics = []

        for topic in result["topics"]:

            if not isinstance(
                topic,
                dict
            ):
                continue

            topic_name = (
                topic.get("topic")
                or "Unknown"
            )

            questions = topic.get(
                "questions",
                []
            )

            if not isinstance(
                questions,
                list
            ):
                questions = []

            cleaned_questions = []

            for q in questions:

                if not isinstance(
                    q,
                    dict
                ):
                    continue

                question = q.get(
                    "question"
                )

                difficulty = q.get(
                    "difficulty",
                    "medium"
                )

                if question:

                    cleaned_questions.append(
                        {
                            "difficulty": difficulty,
                            "question": str(question)
                        }
                    )

            if cleaned_questions:

                cleaned_topics.append(
                    {
                        "topic": str(topic_name),
                        "questions": cleaned_questions
                    }
                )

        result["topics"] = cleaned_topics

        return result

    # ======================================================
    # FALLBACK
    # ======================================================

    def _fallback_result(
        self,
        topics,
        match_data
    ):

        print(
            "\n========== USING FALLBACK QUESTIONS =========="
        )

        fallback_topics = []

        for topic in topics:

            topic_name = str(topic)

            fallback_topics.append(
                {
                    "topic": topic_name,
                    "questions": [
                        {
                            "difficulty": "easy",
                            "question": (
                                f"How have you used "
                                f"{topic_name} in your projects?"
                            )
                        },
                        {
                            "difficulty": "medium",
                            "question": (
                                f"What implementation challenges "
                                f"did you face while working with "
                                f"{topic_name}, and how did you solve them?"
                            )
                        },
                        {
                            "difficulty": "hard",
                            "question": (
                                f"How would you design a production-scale "
                                f"system using {topic_name} while considering "
                                f"performance, reliability, and scalability?"
                            )
                        }
                    ]
                }
            )

        missing_skills = []

        if isinstance(
            match_data,
            dict
        ):

            missing_skills = (
                match_data.get(
                    "missing_skills",
                    []
                )
            )

        missing_questions = []

        for skill in missing_skills:

            missing_questions.append(
                (
                    f"You have limited experience with "
                    f"{skill}. How would you learn and apply "
                    f"it to an AI engineering project?"
                )
            )

        result = {

            "topics": fallback_topics,

            "project_questions": [
                "Explain one of your projects and the most difficult engineering problem you solved.",
                "What design decision in one of your projects would you change today?",
                "How would you improve one of your projects for production use?"
            ],

            "behavioral_questions": [
                "Tell me about a technical problem that required significant debugging.",
                "Describe a time when you had to learn a new technology quickly.",
                "Tell me about a project where you had to make an important technical decision."
            ],

            "missing_skill_questions": missing_questions
        }

        print(
            "Fallback generated successfully."
        )

        return result