from flask import Blueprint
from models import User
user_bp = Blueprint(
    'users',
    __name__
)

@user_bp.get('/all')
def get_all_users():
    users = User.query.paginate(
        
    )
