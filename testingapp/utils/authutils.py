from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request_optional


def get_identity_if_logged_in():
    try:
        verify_jwt_in_request_optional()
        return get_jwt_identity()
    except Exception:
        return None
