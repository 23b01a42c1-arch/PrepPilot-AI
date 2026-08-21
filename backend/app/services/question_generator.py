import json
import os

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

        print(
            "Topics available:",
            "YES" if topics_data else "NO"
        )

        print(
            "Resume data available:",
            bool(resume_data)
        )

        print(
            "JD data available:",
            bool(jd_data)
        )

        print(
            "Match data available:",
            bool(match_data)
        )

        print(
            "Context data available:",
            bool(context_data)
        )

        print("==============================================")

        # --------------------------------------------------
        # SAFETY: Make sure topics_data is usable
        # --------------------------------------------------

        if not topics_data:

            print(
                "WARNING: topics_data is empty."
            )

            # Build topics from resume/JD when topic extraction
            # failed earlier.

            fallback_topics = []

            if isinstance(resume_data, dict):

                skills = resume_data.get(
                    "skills",
                    []
                )

                if isinstance(skills, list):

                    fallback_topics.extend(
                        skills[:10]
                    )

            if isinstance(jd_data, dict):

                required_skills = jd_data.get(
                    "required_skills",
                    []
                )

                if isinstance(required_skills, list):

                    fallback_topics.extend(
                        required_skills[:10]
                    )

            # Remove duplicates

            fallback_topics = list(
                dict.fromkeys(
                    str(topic).strip()
                    for topic in fallback_topics
                    if topic
                )
            )

            topics_data = fallback_topics

        # --------------------------------------------------
        # Normalize topics
        # --------------------------------------------------

        if isinstance(topics_data, dict):

            if "topics" in topics_data:

                topics = topics_data["topics"]

            else:

                topics = list(
                    topics_data.values()
                )

        elif isinstance(topics_data, list):

            topics = topics_data

        else:

            topics = []

        # Convert topic objects into strings if necessary

        normalized_topics = []

        for topic in topics:

            if isinstance(topic, dict):

                topic_name = (
                    topic.get("topic")
                    or topic.get("name")
                    or topic.get("title")
                )

                if topic_name:
                    normalized_topics.append(
                        str(topic_name)
                    )

            elif isinstance(topic, str):

                normalized_topics.append(topic)

        # Remove duplicates

        normalized_topics = list(
            dict.fromkeys(
                topic.strip()
                for topic in normalized_topics
                if topic.strip()
            )
        )

        # --------------------------------------------------
        # Final fallback
        # --------------------------------------------------

        if not normalized_topics:

            normalized_topics = [
                "Programming",
                "Problem Solving",
                "Software Development"
            ]

        print(
            "Normalized topics:",
            normalized_topics
        )

        # --------------------------------------------------
        # JSON SCHEMA
        # --------------------------------------------------

        response_schema = {

            "type": "object",

            "properties": {

                "topics": {

                    "type": "array",

                    "items": {

                        "type": "object",

                        "properties": {

                            "topic": {
                                "type": "string"
                            },

                            "questions": {

                                "type": "array",

                                "items": {

                                    "type": "object",

                                    "properties": {

                                        "difficulty": {

                                            "type": "string",

                                            "enum": [
                                                "easy",
                                                "medium",
                                                "hard"
                                            ]

                                        },

                                        "question": {

                                            "type": "string"

                                        }

                                    },

                                    "required": [
                                        "difficulty",
                                        "question"
                                    ],

                                    "additionalProperties": False

                                }

                            }

                        },

                        "required": [
                            "topic",
                            "questions"
                        ],

                        "additionalProperties": False

                    }

                },

                "project_questions": {

                    "type": "array",

                    "items": {
                        "type": "string"
                    }

                },

                "behavioral_questions": {

                    "type": "array",

                    "items": {
                        "type": "string"
                    }

                },

                "missing_skill_questions": {

                    "type": "array",

                    "items": {
                        "type": "string"
                    }

                }

            },

            "required": [
                "topics",
                "project_questions",
                "behavioral_questions",
                "missing_skill_questions"
            ],

            "additionalProperties": False

        }

        # --------------------------------------------------
        # PROMPT
        # --------------------------------------------------

        prompt = f"""
You are a senior technical interviewer.

Create a personalized technical interview plan.

Return ONLY JSON matching the supplied JSON schema.

IMPORTANT:

Use ONLY these topics:

{json.dumps(normalized_topics, indent=2)}

Candidate Resume:

{json.dumps(resume_data, indent=2)}

Job Description:

{json.dumps(jd_data, indent=2)}

Resume/JD Match:

{json.dumps(match_data, indent=2)}

Context and Evidence:

{json.dumps(context_data, indent=2)}

RULES:

1. For every supplied topic generate exactly:

- 1 easy question
- 1 medium question
- 1 hard question

2. Every technical question must be personalized.

Use evidence from:

- candidate projects
- internship experience
- technologies
- resume skills
- job description
- context data

3. Do NOT generate generic textbook questions when resume evidence exists.

Avoid questions such as:

"What is Python?"

"What is RAG?"

"What is FastAPI?"

"What is CNN?"

"What is machine learning?"

Instead ask implementation-focused questions.

4. EASY questions should focus on:

- implementation
- workflow
- practical usage
- architecture components

5. MEDIUM questions should focus on:

- design decisions
- debugging
- tradeoffs
- architecture
- technology selection

6. HARD questions should focus on:

- scalability
- optimization
- fault tolerance
- production systems
- monitoring
- distributed architecture

7. Generate exactly:

- 3 project questions
- 3 behavioral questions
- 1 question for each missing skill

8. Avoid duplicate questions.

9. Questions should sound like questions asked by a senior software engineer.

10. Use Context and Evidence heavily.

11. Prefer practical engineering questions over definitions.

12. If the candidate has project evidence for a technology, ask about that project.

13. If the candidate has internship evidence, ask production-oriented questions.

14. If both project and internship evidence exist, combine both perspectives.

15. If only skill evidence exists, ask practical engineering questions.

16. Do not invent candidate experience.

17. Do not claim the candidate used a technology unless supported by the resume/context.

Generate the interview plan now.
"""

        # --------------------------------------------------
        # GROQ CALL
        # --------------------------------------------------

        try:

            print(
                "\nCalling Groq GPT-OSS-20B..."
            )

            response = client.chat.completions.create(

                model="openai/gpt-oss-20b",

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.2,

                response_format={

                    "type": "json_schema",

                    "json_schema": {

                        "name": "interview_plan",

                        "strict": True,

                        "schema": response_schema

                    }

                }

            )

            content = (
                response
                .choices[0]
                .message
                .content
            )

            print(
                "\n========== RAW GROQ RESPONSE =========="
            )

            print(content)

            print(
                "========================================"
            )

            # --------------------------------------------------
            # Parse JSON
            # --------------------------------------------------

            result = json.loads(content)

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
                "================================================="
            )

            return result

        except Exception as e:

            print(
                "\n========== GROQ QUESTION GENERATOR ERROR =========="
            )

            print(
                type(e).__name__
            )

            print(
                str(e)
            )

            print(
                "===================================================="
            )

            raise