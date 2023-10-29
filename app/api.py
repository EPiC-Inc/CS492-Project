from flask import Blueprint, request, session, render_template
from .sql import query_db, execute_db
from .auth import generate_hash

api = Blueprint('api', __name__)


def search_for_account(to_find: str) -> list:
    if to_find:
        results = query_db("getSearchAccount :to_find", to_find=to_find)
        results = [tuple(row) for row in results]
        return results
    return []


@api.route('/compose/course_manage_form')
def compose_course_manage_form():
    class_code = request.args.get('class_code')
    if class_code:
        return render_template('courses/_compose_course_details.html',
                               class_name="TEST", num_students=20,
                               description="BIG TEST", degree_path=["Electrical"]
                               )
    else:
        return {"error": "No class code provided"}, 422


@api.route("/find_account", methods=["GET"])
def authenticate_and_search() -> "dict | tuple[dict, int]":
    args = request.args

    if not session.get("logged_in"):
        return {"error": "Not logged in"}, 403
    if not (session.get("role") == 1):
        return {"error": "Unauthorized"}, 401

    results = search_for_account(args.get('to_find', ''))
    return {"matches": results}

@api.route("/account_details", methods=["GET"])
def authenticate_and_get_details() -> "dict | tuple[dict, int]":
    args = request.args
    email = args.get("email")
    results = []

    if not session.get("logged_in"):
        return {"error": "Not logged in"}, 403
    if not (session.get("role") == 1):
        return {"error": "Unauthorized"}, 401

    if email:
        results = query_db("getAccountDetail :to_find", to_find=email)
        results = [tuple(row) for row in results][0]
    return {"account": results}

@api.route("/password_reset", methods=["POST"])
def authenticate_and_set_new_password() -> "list | tuple[dict, int]":
    if not session.get("logged_in"):
        return {"error": "Not logged in"}, 403
    if not (session.get("role") == 1):
        return {"error": "Unauthorized"}, 401

    form = request.get_json()
    if id := form.get("id"):
        pass
        #return {"error": "ID found"}
    #elif email := form.get("email"):
    #    email = query_db("getAccountDetail :email", email=email)
    #    if email:
    #        id = email[0][4]
    #    else:
    #        return {"error": "Email not found"}, 400
    else:
        return {"error": "ID not provided"}, 400
    new_password = form.get("new_password")
    if not new_password:
        return {"error":
                "Unable to set password - no new password passed"}, 422

    hash = generate_hash(new_password).decode()
    response = execute_db("updatePassword :id, :new_password",
        id=id, new_password=hash)
    return response
