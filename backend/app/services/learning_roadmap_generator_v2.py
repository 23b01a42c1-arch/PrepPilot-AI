import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


class LearningRoadmapGeneratorV2:

    def generate(
        self,
        resume_data,
        jd_data,
        topic_scores,
        interview_history
    ):

        prompt = f"""
You are a senior AI career coach.

Generate a personalized learning roadmap.

Return ONLY JSON.

Schema:

{{
    "roadmap": [
        {{
            "topic": "",
            "priority": "high",
            "current_score": 0,
            "why_improve": "",
            "learning_steps": [],
            "project_recommendations": []
        }}
    ]
}}

Rules:

1. Focus only on weak topics.

2. Weak topic:
score < 70

3. Recommend:

- concepts
- technologies
- projects

4. Learning steps must be actionable.

Bad:

"Learn NLP"

Good:

"Implement tokenization using HuggingFace"

5. Project recommendations should be practical.

Resume:
{json.dumps(resume_data, indent=2)}

JD:
{json.dumps(jd_data, indent=2)}

Topic Scores:
{json.dumps(topic_scores, indent=2)}

Interview History:
{json.dumps(interview_history, indent=2)}
"""

        response = (
            client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )
        )

        content = (
            response
            .choices[0]
            .message
            .content
            .replace(
                "```json",
                ""
            )
            .replace(
                "```",
                ""
            )
            .strip()
        )

        return json.loads(content)