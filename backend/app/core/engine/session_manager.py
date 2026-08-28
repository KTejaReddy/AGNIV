import uuid
import json
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.database.models import Session as SessionModel
from app.core.logging import logger

class SessionManager:
    def __init__(self):
        self.current_session_id = None

    async def initialize(self):
        # Auto-create or load active session using runtime_controller
        from app.services.runtime.controller import runtime_controller
        with SessionLocal() as db:
            active = db.query(SessionModel).filter(SessionModel.id == runtime_controller.session_id).first()
            if not active:
                new_session = SessionModel(id=runtime_controller.session_id)
                db.add(new_session)
                db.commit()
                logger.info(f"Created new DB session: {runtime_controller.session_id}")

    def get_current_session(self):
        from app.services.runtime.controller import runtime_controller
        return runtime_controller.session_id

session_manager = SessionManager()
