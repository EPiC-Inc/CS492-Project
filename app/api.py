from flask import Blueprint, request, session
from .sql import query_db

api = Blueprint('api', __name__)

@api.route("/find_account", methods=["GET"])
def search_for_account() -> dict | tuple[dict, int]:
    args = request.args

    if not session.get("logged_in"):
        return {"error": "Not logged in"}, 403
    if not (session.get("role") == "Faculty Administrator"):
        return {"error": "Unauthorized"}, 401

    results = []    
    if email := args.get('email'):
        results = query_db("select * from Accounts where Accounts_Email=:email",
                 email=email)
    elif name := args.get('name'):
        results = query_db("select * from Accounts where Accounts_First_Name=:name OR Accounts_Last_Name=:name",
                 name=name)
    results = [tuple(row) for row in results]

    return {"matches": results}