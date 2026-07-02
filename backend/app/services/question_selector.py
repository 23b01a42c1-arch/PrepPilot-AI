class QuestionSelector:

    def get_next_question(
        self,
        roadmap,
        current_index,
        score
    ):

        if current_index >= len(roadmap) - 1:

            return {
                "completed": True
            }

        current = roadmap[current_index]

        current_topic = current["topic"]

        current_difficulty = current["difficulty"]

        print("\nSELECTOR")
        print("Current Score:", score)
        print("Current Topic:", current_topic)
        print("Current Difficulty:", current_difficulty)

        # -------------------------
        # Excellent Answer
        # -------------------------

        if (
            score >= 9
            and
            current_difficulty == "easy"
        ):

            for i in range(
                current_index + 1,
                len(roadmap)
            ):

                q = roadmap[i]

                if (
                    q["topic"] == current_topic
                    and
                    q["difficulty"] == "hard"
                ):

                    print(
                        "Selector Decision: EASY -> HARD"
                    )

                    return {
                        "completed": False,
                        "next_index": i,
                        "question": q
                    }

        # -------------------------
        # Weak Answer
        # -------------------------

        if score <= 4:

            for i in range(
                current_index + 1,
                len(roadmap)
            ):

                q = roadmap[i]

                if q["topic"] != current_topic:

                    print(
                        "Selector Decision: NEXT TOPIC"
                    )

                    return {
                        "completed": False,
                        "next_index": i,
                        "question": q
                    }

        # -------------------------
        # Normal Flow
        # -------------------------

        print(
            "Selector Decision: NEXT QUESTION"
        )

        return {
            "completed": False,
            "next_index":
                current_index + 1,
            "question":
                roadmap[
                    current_index + 1
                ]
        }