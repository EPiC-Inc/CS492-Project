from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)

from .auth import generate_hash
from .sql import execute_db, query_db

api = Blueprint('api', __name__)


def search_for_account(to_find: str) -> list:
    if to_find:
        results = query_db("getSearchAccount :to_find", to_find=to_find)
        results = [tuple(row) for row in results]
        return results
    return []


@api.route('/compose/course_manage_form')
def compose_course_manage_form() -> "str | tuple[str, int]":
    if not session.get("logged_in"):
        return "Not logged in", 403

    course_list = query_db("getClasses")
    class_code = request.args.get('class_code')
    degrees = query_db("getDegreePaths")
    print(degrees)
    degrees = [[str(i), j, k] for i, j, k in degrees]
    professors = query_db("getFacultyDetail")

    if class_code:
        class_data = query_db("getClassDetail :class_id", class_id=class_code)[0]
        class_id, class_code, class_title, class_desc, class_start, class_end, professor_id, degree_paths, *_ = class_data
        class_title = class_title.strip()
        return render_template('courses/_compose_course_details.html',
                               chosen_class = int(class_id), course_list = course_list,
                               class_name=class_title, description = class_desc,
                               degrees = degrees, professors = professors,
                               current_professor = professor_id,
                               start_date = class_start, end_date = class_end,
                               num_students=20,
                               degree_paths=degree_paths
                               )
    
    else:
        return render_template('courses/_compose_course_details.html',
                               course_list = course_list, degrees = degrees,
                               professors = professors
                               )

@api.route('/compose/manage_course', methods=["POST"])
def authenticate_and_manage_course():
    if not session.get("logged_in"):
        return {"error": "Not logged in"}, 403
    if not (session.get("role", 99) <= 2):
        return {"error": "Unauthorized"}, 401

    form = request.form
    print(form)
    class_id = form.get('class-id', '')
    existing_courses = query_db("getClasses")
    existing_courses = {str(course[0]): course[1].strip() for course in existing_courses}
    print(existing_courses)
    if class_id == '__new__':
        execute_db("insertClassDetail :code :title :desc :start :end :professor :degrees",
                   code=form.get('new-class-code', '').ljust(10, ' ')[:10], title=form.get('class-name', '').ljust(50, ' ')[:50],
                   desc=form.get('description'), start=form.get('start-date'),
                   end=form.get('end-date'), professor=int(form.get('professor', '')),
                   degrees = ','.join(form.getlist('degree-path'))
                   )
    else:
        execute_db("updateClassDetail :id :code :title :desc :start :end :professor :degrees",
                   id=int(class_id), code=existing_courses.get(str(class_id), '').ljust(10, ' ')[:10],
                   title=form.get('class-name', '').ljust(50, ' ')[:50], desc=form.get('description'),
                   start=form.get('start-date'), end=form.get('end-date'),
                   professor=int(form.get('professor', '')),
                   degrees = ','.join(form.getlist('degree-path'))
                   )

    return redirect(url_for('courses'))


@api.route("/find_account", methods=["GET"])
def authenticate_and_search() -> "dict | tuple[dict, int]":
    if not session.get("logged_in"):
        return {"error": "Not logged in"}, 403
    if not (session.get("role") == 1):
        return {"error": "Unauthorized"}, 401

    args = request.args

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
    elif email := form.get("email"):
        email = query_db("getAccountDetail :email", email=email)
        if email:
            id = email[0][4]
        else:
            return {"error": "Email not found"}, 400
    else:
        return {"error": "ID or email not provided"}, 400
    new_password = form.get("new_password")
    if not new_password:
        return {"error":
                "Unable to set password - no new password passed"}, 422

    hash = generate_hash(new_password).decode()
    response = execute_db("updatePassword :id, :new_password",
        id=id, new_password=hash)
    return response
