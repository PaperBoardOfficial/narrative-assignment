from __future__ import absolute_import, unicode_literals
import os
from celery import shared_task
import csv

from csv_processor.models import Student

# Define the constant
CHUNK_SIZE = 1 * 1024 * 1024  # 1 MB

@shared_task
def process_csv_file(file_path, is_chunk=False):
    try:
        # Get the directory of the input file
        input_dir = os.path.dirname(file_path)

        # Check the file size
        file_size = os.path.getsize(file_path)
        print("file_size " + str(file_size))
        if file_size > CHUNK_SIZE and not is_chunk:
            # Create the split directory if it doesn't exist
            split_dir = os.path.join(input_dir, 'split')
            os.makedirs(split_dir, exist_ok=True)

            # If the file is larger than CHUNK_SIZE, split it into chunks
            split_file_paths = split_file(file_path, CHUNK_SIZE, split_dir)
            # Create a new task to process each chunk
            for chunk_file_path in split_file_paths:
                print(chunk_file_path)
                # Call the same task for each chunk file
                process_csv_file.delay(chunk_file_path, is_chunk=True)
        else:
            # If the file is smaller than CHUNK_SIZE or it's a chunk file, process it as before
            process_chunk_file(file_path)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_chunk_file(file_path):
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                # Process each row here
                if len(row) == 6:
                    first_name, last_name, class1, class2, school, location = row
                    name = f"{first_name} {last_name}"
                    # Create a new Student object for each class and save it to the database
                    student1 = Student(Name=name, Class=class1, School=school, State=location)
                    student1.save()
                    student2 = Student(Name=name, Class=class2, School=school, State=location)
                    student2.save()
                else:
                    print(f"Skipping row with incorrect number of values: {row}")
    except Exception as e:
        print(f"Error processing chunk file {file_path}: {e}")

def split_file(file_path, chunk_size, split_dir):
    try:
        # Get the base name of the original file without the extension
        base_name = os.path.splitext(os.path.basename(file_path))[0]

        # Read the file and split it into chunks
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Read the header separately
            chunk = [header]  # Start each chunk with the header
            chunk_files = []
            current_size = len(header)
            for i, row in enumerate(reader):
                # Calculate the size of the row in bytes
                row_size = sum(len(cell) for cell in row)
                if current_size + row_size > chunk_size and i > 0:
                    # When the chunk size is reached, write the chunk to a new file
                    chunk_file_path = os.path.join(split_dir, f'{base_name}_{len(chunk_files) + 1}.csv')
                    write_chunk(chunk, chunk_file_path)
                    chunk_files.append(chunk_file_path)
                    chunk = [header]  # Start the new chunk with the header
                    current_size = len(header)
                chunk.append(row)
                current_size += row_size
            # Write the last chunk to a new file
            if chunk:  # Only write the chunk if it's not empty
                chunk_file_path = os.path.join(split_dir, f'{base_name}_{len(chunk_files) + 1}.csv')
                write_chunk(chunk, chunk_file_path)
                chunk_files.append(chunk_file_path)
        return chunk_files
    except Exception as e:
        print(f"Error splitting file {file_path}: {e}")

def write_chunk(chunk, file_path):
    try:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(chunk)
    except Exception as e:
        print(f"Error writing chunk file {file_path}: {e}")