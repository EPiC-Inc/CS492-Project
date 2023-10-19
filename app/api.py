from flask import Blueprint, request, session
from .sql import query_db

api = Blueprint('api', __name__)

def search_for_account(to_find: str) -> list:
    if to_find:
        results = query_db("getSearchAccount :to_find", to_find=to_find)
        results = [tuple(row) for row in results]
        return results
    return [] 

@api.route("/find_account", methods=["GET"])
def authenticate_and_search() -> dict | tuple[dict, int]:
    args = request.args

    if not session.get("logged_in"):
        return {"error": "Not logged in"}, 403
    if not (session.get("role") == "Faculty Administrator"):
        return {"error": "Unauthorized"}, 401

    results = search_for_account(args.get('to_find', ''))
    return {"matches": results}

@api.route("/account_details", methods=["GET"])
def authenticate_and_get_details() -> dict | tuple[dict, int]:
    args = request.args
    email = args.get("email")
    results = []

    if not session.get("logged_in"):
        return {"error": "Not logged in"}, 403
    if not (session.get("role") == "Faculty Administrator"):
        return {"error": "Unauthorized"}, 401

    if email:
        results = query_db("getAccountDetail :to_find", to_find=email)
        results = [tuple(row) for row in results][0]
    return {"account": results}