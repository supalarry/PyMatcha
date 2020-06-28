from flask import Blueprint
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from PyMatcha.models.like import Like
from PyMatcha.models.match import Match
from PyMatcha.models.user import get_user
from PyMatcha.utils.errors import BadRequestError
from PyMatcha.utils.errors import NotFoundError
from PyMatcha.utils.success import Success
from PyMatcha.utils.success import SuccessOutput

like_bp = Blueprint("like", __name__)


@like_bp.route("/like/<uid>", methods=["POST"])
@jwt_required
def like_profile(uid):
    try:
        u = get_user(uid)
    except NotFoundError:
        raise NotFoundError(f"User {uid} not found")
    if current_user.id == u.id:
        raise BadRequestError("Cannot like yourself")
    if current_user.already_likes(u.id):
        raise BadRequestError("You already liked this person")
    Like.create(liker_id=current_user.id, liked_id=u.id)

    if u.already_likes(current_user.id):
        Match.create(user_1=current_user.id, user_2=u.id)
        return Success("It's a match !")

    return Success("Liked user.")


@like_bp.route("/unlike/<uid>", methods=["POST"])
@jwt_required
def unlike_profile(uid):
    try:
        u = get_user(uid)
    except NotFoundError:
        raise NotFoundError(f"User {uid} not found")
    if current_user.id == u.id:
        raise BadRequestError("Cannot unlike yourself")
    if not current_user.already_likes(u.id):
        raise BadRequestError("You never liked this person in the first place")
    Like.get_multi(liked_id=u.id, liker_id=current_user.id).delete()
    return Success(f"Unliked user {u.id}.")


@like_bp.route("/likes", methods=["GET"])
@jwt_required
def see_my_likes():
    received = current_user.get_likes_received()
    sent = current_user.get_likes_sent()
    returned_dict = {"received": [r.to_dict() for r in received], "sent": [s.to_dict() for s in sent]}
    return SuccessOutput("likes", returned_dict)
