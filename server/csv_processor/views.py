import os
import time
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .tasks import process_csv_file

class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        if 'file' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        file = request.data['file']
        if not file.name.endswith('.csv'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Create a directory in the tmp folder with the current timestamp
        timestamp = str(int(time.time()))
        directory_path = os.path.join('/tmp', timestamp)
        os.makedirs(directory_path, exist_ok=True)

        # Save the uploaded file to the new directory
        file_path = os.path.join(directory_path, file.name)
        with open(file_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Trigger a Celery task to process the file
        process_csv_file.delay(file_path)

        return Response(status=status.HTTP_204_NO_CONTENT)