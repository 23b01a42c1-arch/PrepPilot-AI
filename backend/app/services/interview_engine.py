from app.services.answer_evaluator import (
    AnswerEvaluator
)

from app.services.followup_generator import (
    FollowupGenerator
)

from app.services.question_selector import (
    QuestionSelector
)

from app.services.communication_evaluator import (
    CommunicationEvaluator
)

INTRODUCTION_QUESTION = """
Hello! Welcome to your AI interview.

Let's begin with a brief introduction.

Please tell me about yourself, including:

• Your educational background
• Your technical skills
• Projects you've worked on
• Internship or work experience
• Your career goals

Take your time. I'm listening.
"""


class InterviewEngine:

    def __init__(self):

        self.roadmap = []

        self.introduction_completed = False

        self.current_index = 0
        self.current_topic = None

        self.history = []

        self.in_followup = False

        self.current_followup = None

        self.followup_count = 0
        self.max_followups = 1

        self.evaluator = (
            AnswerEvaluator()
        )

        self.communication_evaluator = (
            CommunicationEvaluator()
        )

        self.followup_generator = (
            FollowupGenerator()
        )

        self.selector = (
            QuestionSelector()
        )

    # ----------------------------------
    # Start Interview
    # ----------------------------------

    def start_interview(
        self,
        roadmap
    ):

        self.roadmap = roadmap

        self.current_index = 0

        if len(self.roadmap) == 0:

            raise ValueError(
                "Empty roadmap."
            )

        self.current_topic = (
            self.roadmap[0]["topic"]
        )

        print(
            "\nCURRENT TOPIC:",
            self.current_topic
        )

        return INTRODUCTION_QUESTION

    # ----------------------------------
    # Submit Answer
    # ----------------------------------

    def submit_answer(
        self,
        answer
    ):

        # ----------------------------------
        # Introduction Round
        # ----------------------------------

        if not self.introduction_completed:

            communication = (
                self.communication_evaluator.evaluate(
                    answer
                )
            )

            self.history.append(
                {
                    "question": INTRODUCTION_QUESTION,
                    "topic": "Introduction",
                    "answer": answer,
                    "evaluation": {
                        "score": None,
                        "strengths": [],
                        "missing_points": []
                    },
                    "communication": communication,
                    "is_followup": False
                }
            )

            self.introduction_completed = True

            return {
                "type": "question",
                "message": "Great introduction! Let's begin the technical interview.",
                "question": self.roadmap[0]["question"]
            }

        # ----------------------------------
        # Active Question
        # ----------------------------------

        if self.in_followup:

            active_question = (
                self.current_followup
            )

        else:

            active_question = (
                self.roadmap[
                    self.current_index
                ]["question"]
            )

        # ----------------------------------
        # Evaluate Answer
        # ----------------------------------

        evaluation = (
            self.evaluator.evaluate(
                active_question,
                answer
            )
        )

        print("\nEVALUATION:")
        print(evaluation)

        communication = (
            self.communication_evaluator.evaluate(
                answer
            )
        )

        print("\nCOMMUNICATION:")
        print(communication)

        score = (
            evaluation.get(
                "score",
                0
            )
        )

        missing_points = (
            evaluation.get(
                "missing_points",
                []
            )
        )

        # ----------------------------------
        # Store History
        # ----------------------------------

        self.history.append(
            {
                "question": active_question,
                "topic": self.current_topic,
                "answer": answer,
                "evaluation": evaluation,
                "communication": communication,
                "is_followup": self.in_followup
            }
        )

        # ----------------------------------
        # Follow-up Logic
        # ----------------------------------

        needs_followup = False

        if score <= 6:

            needs_followup = True

        elif (
            score <= 8
            and
            len(missing_points) >= 2
        ):

            needs_followup = True

        # ----------------------------------
        # Generate Follow-up
        # ----------------------------------

        if (
            not self.in_followup
            and
            needs_followup
            and
            self.followup_count < self.max_followups
        ):

            followup = (
                self.followup_generator.generate(
                    active_question,
                    answer,
                    evaluation
                )
            )

            self.current_followup = (
                followup[
                    "followup_question"
                ]
            )

            self.in_followup = True

            self.followup_count += 1

            print("\nFOLLOWUP GENERATED:")
            print(self.current_followup)

            return {
                "type": "followup",
                "question": self.current_followup
            }

        # ----------------------------------
        # Finish Follow-up
        # ----------------------------------

        if self.in_followup:

            self.in_followup = False

            self.current_followup = None

            self.followup_count = 0

        # ----------------------------------
        # Select Next Question
        # ----------------------------------

        next_question = (
            self.selector.get_next_question(
                roadmap=self.roadmap,
                current_index=self.current_index,
                score=score
            )
        )

        if next_question["completed"]:

            return {
                "type": "completed"
            }

        self.current_index = (
            next_question["next_index"]
        )

        self.current_topic = (
            next_question["question"]["topic"]
        )

        print(
            "\nCURRENT TOPIC:",
            self.current_topic
        )

        return {
            "type": "question",
            "question": next_question["question"]["question"]
        }

    # ----------------------------------
    # Interview History
    # ----------------------------------

    def get_history(
        self
    ):

        return self.history