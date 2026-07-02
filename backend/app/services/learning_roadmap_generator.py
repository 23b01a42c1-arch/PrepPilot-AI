class LearningRoadmapGenerator:

    def generate(
        self,
        topic_scores
    ):

        roadmap = {}

        for topic, score in (
            topic_scores.items()
        ):

            if score >= 70:
                continue

            if topic == (
                "Speech Recognition"
            ):

                roadmap[topic] = [
                    "Speech-to-Text fundamentals",
                    "ASR architectures",
                    "Deepgram API",
                    "Streaming audio processing"
                ]

            elif topic == (
                "Question Answering"
            ):

                roadmap[topic] = [
                    "Vector Databases",
                    "RAG pipelines",
                    "Retrieval strategies",
                    "Evaluation metrics"
                ]

            elif topic == (
                "Natural Language Processing"
            ):

                roadmap[topic] = [
                    "Tokenization",
                    "Embeddings",
                    "Transformers",
                    "Prompt Engineering"
                ]

            elif topic == (
                "Behavioral"
            ):

                roadmap[topic] = [
                    "STAR Method",
                    "Leadership stories",
                    "Conflict resolution",
                    "Communication skills"
                ]

            else:

                roadmap[topic] = [
                    "Practice interview questions",
                    "Build mini projects",
                    "Study fundamentals"
                ]

        return roadmap