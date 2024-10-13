from flask import Blueprint
from pydantic import BaseModel, ValidationError
from typing import List, Optional

from api.routes.users import users_bp
from api.routes.posts import posts_bp
from api.routes.follows import follows_bp 

api_base_bp = Blueprint('api_base', __name__, url_prefix='/api/v1')

api_base_bp.register_blueprint(users_bp, url_prefix='/users')
api_base_bp.register_blueprint(posts_bp, url_prefix='/posts')
api_base_bp.register_blueprint(follows_bp, url_prefix='/follows')
