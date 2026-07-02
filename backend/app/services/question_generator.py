import json
import os
from app.services.question_difficulty_validator import (
    QuestionDifficultyValidator
)
from groq import Groq
from dotenv import load_dotenv

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

        schema = {
            "topics": [
                {
                    "topic": "",
                    "questions": [
                        {
                            "difficulty": "easy",
                            "question": ""
                        },
                        {
                            "difficulty": "medium",
                            "question": ""
                        },
                        {
                            "difficulty": "hard",
                            "question": ""
                        }
                    ]
                }
            ],
            "project_questions": [],
            "behavioral_questions": [],
            "missing_skill_questions": []
        }

        prompt = f"""
You are a senior technical interviewer.

Generate a personalized interview plan.

Return ONLY valid JSON.

Schema:

{json.dumps(schema, indent=2)}

Rules:

1. Use ONLY topics from Topics Data.

2. For EACH topic generate:

- 1 easy question
- 1 medium question
- 1 hard question

3. Questions MUST be personalized using:

- candidate projects
- internship experience
- technologies used
- resume evidence
- JD requirements

4. NEVER generate generic textbook questions.

Forbidden Examples:

- What is NLP?
- What is FastAPI?
- What is RAG?
- Explain Speech Recognition.
- Define Question Answering.

These questions are NOT allowed when resume evidence exists.

5. Difficulty Guidelines

EASY:

If resume evidence exists:

- ask about implementation
- ask about workflow
- ask about practical usage
- ask about architecture components

Examples:

Good:
In your Retrieval-Augmented PDF Question Answering Application, what role did LangChain and Qdrant play?

Good:
You used Deepgram ASR during your internship. Can you explain the flow from audio input to transcript generation?

MEDIUM:

- design decisions
- tradeoffs
- debugging
- architecture choices
- technology selection

Examples:

Good:
How did you decide on your chunking strategy in the Retrieval-Augmented PDF QA Application, and what tradeoffs did you observe?

Good:
While integrating Deepgram ASR into your pipeline, what latency or accuracy challenges did you face and how did you solve them?

HARD:

- production systems
- scaling
- optimization
- fault tolerance
- monitoring
- distributed architectures

Examples:

Good:
How would you redesign your Retrieval-Augmented PDF QA Application to support one million documents and thousands of concurrent users?

Good:
Design a production-grade speech recognition platform capable of handling real-time audio streams from thousands of users simultaneously.

6. Evidence Usage Rules

For each topic:

If project evidence exists:
- generate implementation-focused questions

If internship evidence exists:
- generate production-focused questions

If both exist:
- combine project and production perspectives

If only skills exist:
- generate practical engineering questions

7. Generate exactly:

- 3 project questions
- 3 behavioral questions
- 1 question per missing skill

8. Avoid duplicate questions.

9. Questions should sound like a real technical interview conducted by a senior engineer.

10. Every technical question MUST reference at least one of:

- a project
- an internship experience
- a technology from the resume

11. Use Context Data heavily.

The Context Data contains the evidence that must be used to personalize questions.

12. Prefer implementation and engineering questions over theory.

13. Avoid asking definitions when project or internship evidence exists.

Topics Data:
{json.dumps(topics_data, indent=2)}

Resume Data:
{json.dumps(resume_data, indent=2)}

JD Data:
{json.dumps(jd_data, indent=2)}

Match Data:
{json.dumps(match_data, indent=2)}

Context Data:
{json.dumps(context_data, indent=2)}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
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

            print("\nQUESTION GENERATOR ERROR\n")
            print(e)

            print("\nRAW RESPONSE\n")
            print(content)

            return {
                "error": str(e),
                "raw_response": content
            }