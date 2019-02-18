import unittest
import json
from main import app as tested_app
from main import db as tested_db
from config import TestConfig
from models import Professor

tested_app.config.from_object(TestConfig)


class TestProfessor(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Professor(id=1, title="Teacher Assistant", student_id=1))
        self.db.session.add(Professor(id=2, title="Professor", student_id=2))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Professor.query.delete()
        self.db.session.commit()

    def test_get_all_professor(self):
        # send the request and check the response status code
        response = self.app.get("/professor")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        professor_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(professor_list), list)
        self.assertDictEqual(professor_list[0], {"id": "1", "title": "Teacher Assistant", "student_id": "1"})
        self.assertDictEqual(professor_list[1], {"id": "2", "title": "Professor", "student_id": "2"})

    def test_get_professor_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/professor/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        professor = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(professor, {"id": "1", "title": "Teacher Assistant", "student_id": "1"})

    def test_get_professor_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/professor/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this professor id."})

    def test_put_professor_without_id(self):
        # do we really need to check counts?
        initial_count = Professor.query.filter_by(title="Teacher 2").count()

        # send the request and check the response status code
        response = self.app.put("/professor", data={"title": "Teacher 2"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Professor.query.filter_by(title="Teacher 2").count()
        self.assertEqual(updated_count, initial_count+1)

    def test_put_professor_with_new_id(self):
        # send the request and check the response status code
        response = self.app.put("/professor", data={"id": 3, "title": "Teacher 2", "student_id": 3})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        professor = Professor.query.filter_by(id=3).first()
        self.assertEqual(professor.title, "Teacher 2")
