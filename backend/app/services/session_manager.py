import uuid

from app.services.interview_engine import InterviewEngine


class SessionManager:

    def __init__(self):

        self.sessions = {}

    def create_session(
    self,
    roadmap,
    resume_data,
    jd_data,
    match_data
):

        session_id = str(uuid.uuid4())

        engine = InterviewEngine()

        first_question = engine.start_interview(
        roadmap
        )

        self.sessions[session_id] = {

            "engine": engine,

            "resume_data": resume_data,

            "jd_data": jd_data,

            "match_data": match_data
        }

        return session_id, first_question

    def get_session(
        self,
        session_id
    ):

        return self.sessions.get(session_id)

    def delete_session(
        self,
        session_id
    ):

        self.sessions.pop(
            session_id,
            None
        )