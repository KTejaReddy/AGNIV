import json
from sqlalchemy.orm import Session
from app.database.models import Setting

class SettingsManager:
    @staticmethod
    def get_setting(db: Session, key: str, default=None):
        setting = db.query(Setting).filter(Setting.key == key).first()
        if setting and setting.value:
            try:
                return json.loads(setting.value)
            except json.JSONDecodeError:
                return setting.value
        return default

    @staticmethod
    def set_setting(db: Session, key: str, value):
        setting = db.query(Setting).filter(Setting.key == key).first()
        str_value = json.dumps(value)
        if setting:
            setting.value = str_value
        else:
            setting = Setting(key=key, value=str_value)
            db.add(setting)
        db.commit()
        db.refresh(setting)
        return setting
