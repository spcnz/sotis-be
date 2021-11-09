from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request_optional
from testingapp.models.usermodels import User


def get_user_if_logged_in():
    try:
        verify_jwt_in_request_optional()
        user_data = get_jwt_identity()
        return User.query.filter_by(id=user_data.get('id', -1)).first()
    except Exception:
        return None
