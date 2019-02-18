from flask import Flask, jsonify, make_response, request
from config import DevConfig

import sqlalchemy

# need an app before we import models because models need it
app = Flask(__name__)
from models import db, row2dict, Paper, Professor, Student

app.config.from_object(DevConfig)


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@app.route('/')
def soen487_a1():
    return jsonify({"title": "SOEN487 Assignment 1",
                    "student": {"id": "40016801", "name": "Marzie Shafiee"}})


@app.route("/student")
def get_all_student():
    student_list = Student.query.all()
    return jsonify([row2dict(student) for student in student_list])


@app.route("/student/<student_id>")
def get_student(student_id):
    # id is a primary key, so we'll have max 1 result row
    student = Student.query.filter_by(id=student_id).first()
    if student:
        return jsonify(row2dict(student))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this student id."}), 404)


@app.route("/student", methods={"PUT"})
def put_student():
    # get the name first, if no name then fail
    username = request.form.get("username")
    if not username:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot put student. Missing mandatory fields."}), 403)
    student_id = request.form.get("id")
    if not student_id:
        p = Student(username=username)
    else:
        p = Student(id=student_id, username=username)

    db.session.add(p)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put student. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "success"})


# paper
@app.route("/paper")
def get_all_paper():
    paper_list = Paper.query.all()
    return jsonify([row2dict(paper) for paper in paper_list])


@app.route("/paper/<paper_id>")
def get_paper(paper_id):
    # id is a primary key, so we'll have max 1 result row
    paper = Paper.query.filter_by(id=paper_id).first()
    if paper:
        return jsonify(row2dict(paper))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this paper id."}), 404)


@app.route("/paper", methods={"PUT"})
def put_paper():
    # get the title first, if no title then fail
    title = request.form.get("title")
    content = request.form.get("content")
    if not title:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot put student. Missing mandatory fields."}), 403)
    paper_id = request.form.get("id")
    if not paper_id:
        p = Paper(title=title, content=content)
    else:
        p = Paper(id=paper_id, title=title, content=content, student_id=paper_id)

    db.session.add(p)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put student. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "success"})


# professor
@app.route("/professor")
def get_all_professor():
    professor_list = Professor.query.all()
    return jsonify([row2dict(professor) for professor in professor_list])


@app.route("/professor/<professor_id>")
def get_professor(professor_id):
    # id is a primary key, so we'll have max 1 result row
    professor = Professor.query.filter_by(id=professor_id).first()
    if professor:
        return jsonify(row2dict(professor))
    else:
        return make_response(jsonify({"code": 404, "msg": "Cannot find this professor id."}), 404)


@app.route("/professor", methods={"PUT"})
def put_professor():
    # get the name first, if no name then fail
    title = request.form.get("title")
    if not title:
        return make_response(jsonify({"code": 403,
                                      "msg": "Cannot put student. Missing mandatory fields."}), 403)
    professor_id = request.form.get("id")
    if not professor_id:
        p = Professor(title=title)
    else:
        p = Professor(id=professor_id, title=title, student_id=professor_id)

    db.session.add(p)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put student. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return jsonify({"code": 200, "msg": "success"})


if __name__ == '__main__':
    app.run(debug=True)
