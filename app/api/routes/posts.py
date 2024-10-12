from flask import Blueprint, jsonify

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/', methods=['GET'])
def get_posts():
    return jsonify({"message": "List of post"})

@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    return jsonify({"message": f"Post {post_id}"})

@posts_bp.route('/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    return jsonify({"message": f"Post {post_id} Comments"})

@posts_bp.route('/<int:post_id>/comments/<int:comment_id>', methods=['GET'])
def get_comment(post_id, comment_id):
    return jsonify({"message": f"Post {post_id}, Comment {comment_id}"})

@posts_bp.route('/<int:post_id>/likes', methods=['GET'])
def get_likes(post_id):
    return jsonify({"message": f"Post {post_id} Likes"})

@posts_bp.route('/<int:post_id>/likes/<int:like_id>', methods=['GET'])
def get_like(post_id, like_id):
    return jsonify({"message": f"Post {post_id}, Like {like_id}"})

@posts_bp.route('/<int:post_id>/shares', methods=['GET'])
def get_shares(post_id):
    return jsonify({"message": f"Post {post_id} Shares"})

@posts_bp.route('/<int:post_id>/shares/<int:share_id>', methods=['GET'])
def get_share(post_id, share_id):
    return jsonify({"message": f"Post {post_id}, Share {share_id}"})
