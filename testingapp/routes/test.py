from flask import Blueprint, request

test_bp = Blueprint('test', __name__)

@test_bp.route('/', methods=['GET', 'POST'])
def get():
    s = request.json()