import unittest
import json
from main import app as tested_app
from main import db as tested_db
from config import TestConfig
from models import Student

tested_app.config.from_object(TestConfig)


class TestStudent(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Student(id=1, username="Alice"))
        self.db.session.add(Student(id=2, username="Bob"))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Student.query.delete()
        self.db.session.commit()

    def test_get_all_student(self):
        # send the request and check the response status code
        response = self.app.get("/student")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        student_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(student_list), list)
        self.assertDictEqual(student_list[0], {"id": "1", "username": "Alice"})
        self.assertDictEqual(student_list[1], {"id": "2", "username": "Bob"})

    def test_get_student_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/student/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        student = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(student, {"id": "1", "username": "Alice"})

    def test_get_student_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/student/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this student id."})

    def test_put_student_without_id(self):
        # do we really need to check counts?
        initial_count = Student.query.filter_by(username="Amy").count()

        # send the request and check the response status code
        response = self.app.put("/student", data={"username": "Amy"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Student.query.filter_by(username="Amy").count()
        self.assertEqual(updated_count, initial_count+1)

    def test_put_student_with_new_id(self):
        # send the request and check the response status code
        response = self.app.put("/student", data={"id": 3, "username": "Amy"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        student = Student.query.filter_by(id=3).first()
        self.assertEqual(student.username, "Amy")
