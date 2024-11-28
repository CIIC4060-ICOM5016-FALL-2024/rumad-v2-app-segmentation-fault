import sys
import os
import numpy as np
import gc
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dao.course import ClassDAO
from dao.syllabus import SyllabusDAO
from tokenize_class import Tokenize
from embedding import embeddingClass
from extract import Extract

# Use a relative path for the syllabus directory
input_directory = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../syllabuses")
)
output_directory = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../extracted_syllabuses")
)

# Extract the Syllabus pdf into .txt files
extract_pdf = Extract()
extract_pdf.extract_directory(input_directory, output_directory)

# Initialize the DAOs and folder path
syllabusDao = SyllabusDAO()
tokenize = Tokenize()
emb = embeddingClass()
class_Dao = ClassDAO()
folder_path = output_directory


def normalizer(vector):
    vector = np.array(vector)
    padded_vector = np.pad(vector, pad_width=(0, 500 - len(vector)), mode="constant")
    return padded_vector


def process_file(f):
    file_path = os.path.join(folder_path, f)
    with open(file_path, "r") as file:
        text = file.read()
        text = tokenize.tokenize_text(text, 1, 0)

        for actual_chunk in text:
            embText = normalizer(emb.embed(actual_chunk)).tolist()
            # Insert syllabus into the database
            course_tags = f.split("-")
            cid = class_Dao.getClassByCname_Ccode(course_tags[0], course_tags[1])[0]
            chunk_with_tag = (
                f"From {course_tags[0]} {course_tags[1]} Syllabus:\n{actual_chunk}"
            )
            syllabusDao.insertSyllabus(cid, embText, chunk_with_tag)
            del embText
            del actual_chunk
            del chunk_with_tag
            del cid
            gc.collect()

    return f


# Iterate over the extracted syllabus files (.txt) using multithreading
folder = os.listdir(folder_path)
count = 0

with ThreadPoolExecutor() as executor:
    futures = {executor.submit(process_file, f): f for f in folder}
    for future in as_completed(futures):
        count += 1
        f = futures[future]
        try:
            result = future.result()
            print("File: " "%s/%s" % (count, len(folder)))
            print(f"\033[34m{result} chunks insertion:\033[92m done \n\033[0m")
        except Exception as e:
            print(f"File {f} generated an exception: {e}")

folder.clear()
