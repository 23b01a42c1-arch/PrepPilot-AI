from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


class PDFReportGenerator:

    def generate(
        self,
        report,
        output_path="interview_report.pdf"
    ):

        doc = SimpleDocTemplate(
            output_path
        )

        styles = (
            getSampleStyleSheet()
        )

        content = []

        content.append(
            Paragraph(
                "AI Interview Report",
                styles["Title"]
            )
        )

        content.append(
            Spacer(1, 20)
        )

        content.append(
            Paragraph(
                f"Overall Score: {report['overall_score']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Technical Score: {report['technical_score']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Communication Score: {report['communication_score']}",
                styles["Normal"]
            )
        )

        content.append(
            Spacer(1, 20)
        )

        content.append(
            Paragraph(
                "Topic Scores",
                styles["Heading2"]
            )
        )

        for topic, score in (
            report[
                "topic_scores"
            ].items()
        ):

            content.append(
                Paragraph(
                    f"{topic}: {score}",
                    styles["Normal"]
                )
            )

        content.append(
            Spacer(1, 20)
        )

        content.append(
            Paragraph(
                "Strengths",
                styles["Heading2"]
            )
        )

        for item in report["strengths"]:

            content.append(
                Paragraph(
                    f"• {item}",
                    styles["Normal"]
                )
            )

        content.append(
            Spacer(1, 20)
        )

        content.append(
            Paragraph(
                "Weaknesses",
                styles["Heading2"]
            )
        )

        for item in report["weaknesses"]:

            content.append(
                Paragraph(
                    f"• {item}",
                    styles["Normal"]
                )
            )

        content.append(
            PageBreak()
        )

        content.append(
            Paragraph(
                "Hiring Recommendation",
                styles["Heading1"]
            )
        )

        recommendation = (
            report[
                "recommendation"
            ]
        )

        content.append(
            Paragraph(
                f"Recommendation: {recommendation['recommendation']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Confidence: {recommendation['confidence']}",
                styles["Normal"]
            )
        )

        for reason in (
            recommendation[
                "reasoning"
            ]
        ):

            content.append(
                Paragraph(
                    f"• {reason}",
                    styles["Normal"]
                )
            )

        content.append(
            Spacer(1, 20)
        )

        content.append(
            Paragraph(
                "Learning Roadmap",
                styles["Heading1"]
            )
        )

        for item in (
            report[
                "learning_roadmap"
            ]["roadmap"]
        ):

            content.append(
                Paragraph(
                    item["topic"],
                    styles["Heading3"]
                )
            )

            content.append(
                Paragraph(
                    f"Priority: {item['priority']}",
                    styles["Normal"]
                )
            )

            content.append(
                Paragraph(
                    item["why_improve"],
                    styles["Normal"]
                )
            )

            for step in (
                item[
                    "learning_steps"
                ]
            ):

                content.append(
                    Paragraph(
                        f"• {step}",
                        styles["Normal"]
                    )
                )

        doc.build(content)

        return output_path