from flask import Blueprint
from pydantic import BaseModel, ValidationError
from typing import List, Optional

from api.routes.users import users_bp
from api.routes.posts import posts_bp # , comments_bp, likes_bp, shares_bp
from api.routes.follows import follows_bp 

api_base_bp = Blueprint('api_base', __name__, url_prefix='/api/v1')

api_base_bp.register_blueprint(users_bp, url_prefix='/users')
api_base_bp.register_blueprint(posts_bp, url_prefix='/posts')
# api_base_bp.register_blueprint(comments_bp, url_prefix='/comments')
# api_base_bp.register_blueprint(likes_bp, url_prefix='/likes')
# api_base_bp.register_blueprint(shares_bp, url_prefix='/shares')
api_base_bp.register_blueprint(follows_bp, url_prefix='/follows')
