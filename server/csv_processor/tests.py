from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from rest_framework import status

class FileUploadViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_upload_csv_file(self):
        # Create a simple test file
        content = b'column1,column2\nvalue1,value2\n'
        test_file = SimpleUploadedFile('test.csv', content)
        # Send the file in a POST request
        response = self.client.post('/upload/', {'file': test_file})
        # Check that the response status code is 204 (No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_upload_non_csv_file(self):
        # Create a simple test file
        content = b'This is not a CSV file.'
        test_file = SimpleUploadedFile('test.txt', content)
        # Send the file in a POST request
        response = self.client.post('/upload/', {'file': test_file})
        # Check that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)