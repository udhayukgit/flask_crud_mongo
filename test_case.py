from werkzeug.datastructures import FileStorage
from flask_mongoengine import MongoEngine
import unittest
import os
import sys
import datetime
from flask_mongo import app

filename = '1620724715_20210118092356.jpeg'
file = os.path.join(app.config['UPLOAD_FOLDER'], filename) 

image = FileStorage(
    stream=open(file, "rb"),
    filename="1620724715_20210118092356.jpeg",
    content_type="jpeg/png/jpg",
),

edit_image = FileStorage(
    stream=open(file, "rb"),
    filename="1620724715_20210118092356-edit.jpeg",
    content_type="jpeg/png/jpg",
),

class TestUsers(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_read(self):
        self.app = app.test_client()
        rv = self.app.get('/')

        assert rv.status_code == 200

    def test_01_add(self):
        rv = self.app.post('/user', data=dict(
                username='Test',
                email='test@gmail.com',
                password = 'test@1234',
                mobile_no=1234567890,
                file =  image,
                ),content_type="multipart/form-data", follow_redirects=True)
        print(rv.data)
        assert "success" in rv.data.decode('utf-8')

    def test_02_Update(self):

        with app.app_context():
            
            rv = self.app.put(
                '/user', data=dict(
                    username = 'Test',
                    email='test_update@gmail.com',
                    password = 'test_update@1234',
                    mobile_no='1234567890',
                    file =  edit_image,
                    ),content_type="multipart/form-data", follow_redirects=True)
            print(rv.data)
            assert "success" in rv.data.decode('utf-8')

    def test_03_delete(self):
        with app.app_context():
            
            rv = self.app.delete(
                '/user', data=dict(
                    username='Test',
                ),follow_redirects=True)
            print(rv.data)
            assert "success" in rv.data.decode('utf-8')

if __name__ == '__main__':
    unittest.main()
