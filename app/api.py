from flask import Blueprint, request, session
from .sql import query_db

api = Blueprint('api', __name__)

@api.route("/find_account", methods=["GET"])
def search_for_account() -> dict | tuple[dict, int]:
    if not session.get("logged_in"):
        return {"error": "Not authorized."}, 400
    args = request.args

    results = []    
    if email := args.get('email'):
        results = query_db("select * from Accounts where Accounts_Email=:email",
                 email=email)
    elif name := args.get('name'):
        results = query_db("select * from Accounts where Accounts_First_Name=:name OR Accounts_Last_Name=:name",
                 name=name)
    results = [tuple(row) for row in results]

    return {"matches": results}