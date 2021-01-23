import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie

Assistant = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktLbHBHYm43MmpWN1RGa3RrMHhRdyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdWRhY2l0eS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwYzdiZGM5YzJmMDgwMDY5ZWFkYjE3IiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTYxMTQzMTA1MiwiZXhwIjoxNjExNTE3NDUyLCJhenAiOiJXTXZVcW5EMUdBSmcyT0gwNmk0TXVzcTB2bGxoeXNNaCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.JpQGgPZxOesg491hjpwTMkJEqx3nd3LjD8S2lXbzvPxuNGJo0i9ORf6Eh5UW4gtQYoxKRlpWmW1tdhsFgzyXQoFohMCN5P48dzsOENdPO_7zFk96RiYAUhcPoPsZ0KEQJ3F2w4kIa3_4MmUvTLXxPNFl6nqRf6Ly5BkBS2kAJwa0oHeW5L9dgnAr2Tr6Pg7eEu2ZBi3KCwM1O49U1e4GzZziCtRPr4QO3YtvWXXIwTbdAHy7lrjus3XqlRCqzo7EZ75W_0e7KsZ7Crk_TAeQyTgB1LP47HtuiSHz_AYfPzFluQ2jAJDUDf7Vp0JT2hiP33QtGLbxbJos1XjwWrG85g'
}


Director = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktLbHBHYm43MmpWN1RGa3RrMHhRdyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdWRhY2l0eS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwYzdiZjQ4ZTVmNTMwMDZhODIyMzgzIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTYxMTQzMTEwOSwiZXhwIjoxNjExNTE3NTA5LCJhenAiOiJXTXZVcW5EMUdBSmcyT0gwNmk0TXVzcTB2bGxoeXNNaCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.IvLpzXCVHOg1M5vF-T-xAaz4g4r7BeFDlxL9hIJOFgn5LejYRbLbtB05Pn4I1FZ-eUtCzkCEnAmupTC5-MwQI6VNa0CekjWwEp5S0icczxAsOh4xernNVnadOC7uIAtb5QoYHrzAl1AY0ccj-vK6xmi1KBEZbnrFaD59s0yeYMIqCzu4OZXKfIGEwS2UsiFqt8PJsIuGVQfR5XiQ_xOXa5-MEW7ElsqtdNq7zEFd4fnEg5-IJrEshu74bzUeMUFXGhxUP0D9wmxW-ZFyR27oPtvcH6wXXX28Lp3eGaTfL9jM7KKBLFseztuAL6BylfF4OnPrgy4vWLE0rrPgs4pzkg'
}
Executive = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktLbHBHYm43MmpWN1RGa3RrMHhRdyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtdWRhY2l0eS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwYzdjMTE4ZTVmNTMwMDZhODIyMzhiIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTYxMTQzMTE3MywiZXhwIjoxNjExNTE3NTczLCJhenAiOiJXTXZVcW5EMUdBSmcyT0gwNmk0TXVzcTB2bGxoeXNNaCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.eLg_2bbrV7laI4ehJ5xcEV4G6Su5LkpoCGJw3-MhpxfzNCHLM0WhduAOW8v50ihE75u8eI2zMHIU2N7Jf0PIkL_LXUELHDBdb9EBWc_bV3UYsB5I3CWD-GkZiB7K2OBgh2iklTk6uPZ0hNs-aGKVOokHT4nuAsDAljp1wj_meD6Ljxv-v6ooINR28VJD4vprZkkxVy5MZfspB-AB2ptB92KZQX4AADIIa2PHoD9xRV0h91-nQ5_QWgMihVTvyh7agd_hwsvrj5LJmopf6ju00TAZwJtfLOpIVwESOIqsfIfGu19-2F8kGhVaP0-n0v_8xDWGb2NPIImaw4cHrVHnog'
}


class CapstoneTest(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

################## Successful Tests ##################

    def test_get_actors(self):
        res = self.client().get('/actors', headers=Assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['actors'], list)

    def test_get_movies(self):
        res = self.client().get('/movies', headers=Assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['movies'], list)

    def test_post_actors(self):
        res = self.client().post('/actors', headers=Director, json={
            "name": "Mohammad",
            "age": "20",
            "gender": "male"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['created_id'], 1)

    def test_post_movies(self):
        res = self.client().post('/movies', headers=Executive, json={
            "title": "The Mud",
            "release_date": "10/20/2010"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['created_id'], 1)

    def test_patch_actors(self):
        res = self.client().patch('/actors/1', headers=Director,
                                  json={
                                      "name": "Malak",
                                  })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_patch_movies(self):
        res = self.client().patch('/movies/1', headers=Executive, json={
            "title": "Terminator",
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_delete_actors(self):
        res = self.client().delete('/actors/1', headers=Director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted_id'], 1)

    def test_delete_movies(self):
        res = self.client().delete('/movies/1', headers=Executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted_id'], 1)

################## Unsuccessful Tests ##################

    def test_u_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_u_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_u_post_actors(self):
        res = self.client().post('/actors', json={
            "name": "Mohammad",
            "age": "20",
            "gender": "male"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_u_post_movies(self):
        res = self.client().post('/movies', json={
            "title": "The Mud",
            "release_date": "10/20/2015"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_u_patch_actors(self):
        res = self.client().patch('/actors/1', json={
            "name": "Mohammad",
            "age": "25",
            "gender": "male"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_u_patch_movies(self):
        res = self.client().patch('/movies/1', json={
            "title": "The Mud",
            "release_date": "10/20/2010"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_u_delete_actors(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_u_delete_movies(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main()
