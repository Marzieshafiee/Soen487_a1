import unittest
import json
from main import app as tested_app
from main import db as tested_db
from config import TestConfig
from models import Paper

tested_app.config.from_object(TestConfig)


class TestPaper(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Paper(id=1, title="Software", content="Computer project", student_id=1))
        self.db.session.add(Paper(id=2, title="Art", content="Art project", student_id=2))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Paper.query.delete()
        self.db.session.commit()

    def test_get_all_paper(self):
        # send the request and check the response status code
        response = self.app.get("/paper")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        paper_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(paper_list), list)
        self.assertDictEqual(paper_list[0], {"id": "1", "title": "Software", "content": "Computer project", "student_id": "1"})
        self.assertDictEqual(paper_list[1], {"id": "2", "title": "Art", "content": "Art project", "student_id": "2"})

    def test_get_paper_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/paper/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        paper = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(paper, {"id": "1", "title": "Software", "content": "Computer project", "student_id": "1"})

    def test_get_paper_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/paper/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this paper id."})

    def test_put_paper_without_id(self):
        # do we really need to check counts?
        initial_count = Paper.query.filter_by(title="Math", content="Math project").count()

        # send the request and check the response status code
        response = self.app.put("/paper", data={"title": "Math", "content": "Math project"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = Paper.query.filter_by(title="Math", content="Math project").count()
        self.assertEqual(updated_count, initial_count+1)

    def test_put_paper_with_new_id(self):
        # send the request and check the response status code
        response = self.app.put("/paper", data={"id": 3, "title": "Math", "content": "Math project", "student_id": 3})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        paper = Paper.query.filter_by(id=3).first()
        self.assertEqual(paper.title, "Math")
        self.assertEqual(paper.content, "Math project")

