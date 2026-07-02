class ResumeEvidenceExtractor:

    def extract(
        self,
        resume_data
    ):

        evidence = {}

        skills = resume_data.get(
            "skills",
            []
        )

        projects = resume_data.get(
            "projects",
            []
        )

        # -----------------------
        # Skills
        # -----------------------

        for skill in skills:

            evidence.setdefault(
                skill,
                []
            )

            evidence[skill].append(
                skill
            )

        # -----------------------
        # Projects
        # -----------------------

        for project in projects:

            project_name = (
                project.get(
                    "name",
                    ""
                )
            )

            technologies = (
                project.get(
                    "technologies",
                    []
                )
            )

            for tech in technologies:

                evidence.setdefault(
                    tech,
                    []
                )

                evidence[
                    tech
                ].append(
                    project_name
                )

        return evidence