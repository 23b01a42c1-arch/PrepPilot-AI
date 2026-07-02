class InterviewRoadmapBuilder:

    def build(
        self,
        questions_data
    ):

        roadmap = []

        # ----------------------
        # Topic Questions
        # ----------------------

        for topic_block in questions_data.get(
            "topics",
            []
        ):

            topic_name = topic_block.get(
                "topic",
                "Unknown"
            )

            for q in topic_block.get(
                "questions",
                []
            ):

                roadmap.append(
                    {
                        "type": "technical",
                        "topic": topic_name,
                        "difficulty": q.get(
                            "difficulty",
                            "medium"
                        ),
                        "question": q.get(
                            "question"
                        )
                    }
                )

        # ----------------------
        # Project Questions
        # ----------------------

        for q in questions_data.get(
            "project_questions",
            []
        ):

            roadmap.append(
                {
                    "type": "project",
                    "topic": "Projects",
                    "difficulty": "medium",
                    "question":
                        q["question"]
                        if isinstance(q, dict)
                        else q
                }
            )

        # ----------------------
        # Behavioral Questions
        # ----------------------

        for q in questions_data.get(
            "behavioral_questions",
            []
        ):

            roadmap.append(
                {
                    "type": "behavioral",
                    "topic": "Behavioral",
                    "difficulty": "medium",
                    "question":
                        q["question"]
                        if isinstance(q, dict)
                        else q
                }
            )

        # ----------------------
        # Missing Skill Questions
        # ----------------------

        for q in questions_data.get(
            "missing_skill_questions",
            []
        ):

            roadmap.append(
                {
                    "type": "missing_skill",
                    "topic": "Skill Gap",
                    "difficulty": "medium",
                    "question":
                        q["question"]
                        if isinstance(q, dict)
                        else q
                }
            )

        return roadmap