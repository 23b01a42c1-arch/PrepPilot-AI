from collections import Counter

from app.services.topic_mastery_tracker import (
    TopicMasteryTracker
)

from app.services.learning_roadmap_generator_v2 import (
    LearningRoadmapGeneratorV2
)

from app.services.hiring_recommendation_engine import (
    HiringRecommendationEngine
)


class ReportGeneratorV2:

    def generate(
        self,
        history,
        resume_data,
        jd_data
    ):

        if not history:

            return {
                "overall_score": 0,
                "technical_score": 0,
                "communication_score": 0,
                "topic_scores": {},
                "strengths": [],
                "weaknesses": [],
                "recommendation": {},
                "learning_roadmap": {}
            }

        # ----------------------------------
        # Overall Score
        # ----------------------------------

        scores = [

            item["evaluation"].get(
                "score",
                0
            )

            for item in history

        ]

        overall_score = round(

            (
                sum(scores)
                /
                len(scores)
            )
            * 10,

            2

        )

        # ----------------------------------
        # Topic Scores
        # ----------------------------------

        topic_scores = (

            TopicMasteryTracker()
            .calculate(history)

        )

        # ----------------------------------
        # Technical Score
        # ----------------------------------

        technical_topics = {}

        for topic, score in (

            topic_scores.items()

        ):

            if topic not in [

                "Behavioral",
                "Projects"

            ]:

                technical_topics[
                    topic
                ] = score

        if technical_topics:

            technical_score = round(

                sum(
                    technical_topics.values()
                )

                /

                len(
                    technical_topics
                ),

                2

            )

        else:

            technical_score = overall_score

        # ----------------------------------
        # Communication Score
        # ----------------------------------

        communication_scores = [

            item.get(
                "communication",
                {}
            ).get(
                "communication_score",
                0
            )

            for item in history
        ]

        if communication_scores:

            communication_score = round(
                sum(communication_scores)
                /
                len(communication_scores),
                2
        )

        else:

            communication_score = 0

        

        # ----------------------------------
        # Strengths
        # ----------------------------------

        strength_counter = Counter()

        for item in history:

            strengths = (

                item["evaluation"]
                .get(
                    "strengths",
                    []
                )

            )

            strength_counter.update(
                strengths
            )

        strengths = [

            strength

            for strength, count

            in strength_counter.most_common(
                5
            )

        ]

        # ----------------------------------
        # Weaknesses
        # ----------------------------------

        weakness_counter = Counter()

        for item in history:

            weaknesses = (

                item["evaluation"]
                .get(
                    "missing_points",
                    []
                )

            )

            weakness_counter.update(
                weaknesses
            )

        weaknesses = [

            weakness

            for weakness, count

            in weakness_counter.most_common(
                5
            )

        ]

        # ----------------------------------
        # Hiring Recommendation
        # ----------------------------------

        recommendation = (

            HiringRecommendationEngine()
            .generate(
                overall_score,
                technical_score,
                communication_score,
                topic_scores
            )

        )

        # ----------------------------------
        # Learning Roadmap
        # ----------------------------------

        learning_roadmap = (

            LearningRoadmapGeneratorV2()
            .generate(
                resume_data=resume_data,
                jd_data=jd_data,
                topic_scores=topic_scores,
                interview_history=history
            )

        )

        # ----------------------------------
        # Final Report
        # ----------------------------------

        return {

            "overall_score":
                overall_score,

            "technical_score":
                technical_score,

            "communication_score":
                communication_score,

            "topic_scores":
                topic_scores,

            "strengths":
                strengths,

            "weaknesses":
                weaknesses,

            "recommendation":
                recommendation,

            "learning_roadmap":
                learning_roadmap

        }