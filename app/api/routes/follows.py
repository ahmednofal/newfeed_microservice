from flask import Blueprint, request, jsonify

follows_bp = Blueprint('follows', __name__, url_prefix='/follows')

@follows_bp.route('/', methods=['GET'])
def get_follows():
    return jsonify({"message": "List of follows"})

@follows_bp.route('/', methods=['POST'])
def post_follow():
    data = request.json
    follower_id = data.get('follower_id')
    followed_id = data.get('followed_id')

    return jsonify({"message": "List of follows"})

@follows_bp.route('/<int:followed_id>', methods=['GET'])
def get_followers(followed_id):
    return jsonify({"message": f"Follow {followed_id}"})

@follows_bp.route('/<int:follower_id>', methods=['GET'])
def get_followed(follower_id):
    return jsonify({"message": f"Follow {follower_id}"})