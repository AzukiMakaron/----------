# user_session.py

class UserSession:
    current_user_id = None

    @classmethod
    def set_user_id(cls, user_id):
        cls.current_user_id = user_id

    @classmethod
    def get_user_id(cls):
        return str(cls.current_user_id) if cls.current_user_id is not None else None