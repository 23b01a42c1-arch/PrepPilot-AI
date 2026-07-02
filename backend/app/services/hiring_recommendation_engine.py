class HiringRecommendationEngine:

    def generate(
        self,
        overall_score,
        technical_score,
        communication_score,
        topic_scores
    ):

        # --------------------------
        # Recommendation
        # --------------------------

        if (
            technical_score >= 85
            and
            communication_score >= 70
        ):

            recommendation = (
                "Strong Hire"
            )

        elif technical_score >= 75:

            recommendation = (
                "Hire"
            )

        elif technical_score >= 60:

            recommendation = (
                "Borderline"
            )

        else:

            recommendation = (
                "Reject"
            )

        # --------------------------
        # Confidence
        # --------------------------

        confidence = round(
            (
                technical_score
                +
                communication_score
            ) / 2,
            2
        )

        # --------------------------
        # Strength Areas
        # --------------------------

        strengths = []

        for topic, score in (
            topic_scores.items()
        ):

            if score >= 80:

                strengths.append(
                    topic
                )

        # --------------------------
        # Weak Areas
        # --------------------------

        weaknesses = []

        for topic, score in (
            topic_scores.items()
        ):

            if score < 60:

                weaknesses.append(
                    topic
                )

        # --------------------------
        # Reasoning
        # --------------------------

        reasoning = []

        reasoning.append(
            f"Technical Score: {technical_score}"
        )

        reasoning.append(
            f"Communication Score: {communication_score}"
        )

        if len(strengths):

            reasoning.append(
                "Strong topics: "
                +
                ", ".join(strengths)
            )

        if len(weaknesses):

            reasoning.append(
                "Weak topics: "
                +
                ", ".join(weaknesses)
            )

        return {

            "recommendation":
                recommendation,

            "confidence":
                confidence,

            "reasoning":
                reasoning
        }