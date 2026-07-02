class TopicMasteryTracker:

    def calculate(
        self,
        history
    ):

        topic_scores = {}

        topic_counts = {}

        for item in history:

            topic = item.get(
                "topic",
                "General"
            )

            score = (
                item["evaluation"]
                .get(
                    "score",
                    0
                )
            )

            if topic not in topic_scores:

                topic_scores[topic] = 0
                topic_counts[topic] = 0

            topic_scores[topic] += score
            topic_counts[topic] += 1

        result = {}

        for topic in topic_scores:

            avg = (
                topic_scores[topic]
                /
                topic_counts[topic]
            )

            result[topic] = round(
                avg * 10,
                2
            )

        return result