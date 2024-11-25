import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import numpy as np
from dao.course import ClassDAO
from dao.syllabus import SyllabusDAO
from tokenize_class import Tokenize
from embedding import embeddingClass
from extract import Extract
import gc

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
folder_path = "./extracted_syllabuses"


def normalizer(vector):
    vector = np.array(vector)
    padded_vector = np.pad(vector, pad_width=(0, 500 - len(vector)), mode="constant")
    return padded_vector


# Iterate over the extracted syllabus files (.txt)
folder = os.listdir(folder_path)
count = 0

for f in folder:
        
    count += 1
    print("File: " "%s/%s" % (count, len(folder)))
    print(f"\033[93mWorking with: {f}\033[0m")

    file_path = os.path.join(folder_path, f)
    with open(file_path, "r") as file:
        text = file.read()
        text = tokenize.tokenize_text(text, 1, 0)
    
        for actual_chunk in text:
            embText = normalizer(emb.embed(actual_chunk)).tolist()
            # Insert syllabus into the database
            course_tags = f.split("-")
            cid = class_Dao.getClassByCname_Ccode(course_tags[0], course_tags[1])[0]
            #chunk_with_tag = f"{course_tags[0]} {course_tags[1]}:\n{actual_chunk}"
            syllabusDao.insertSyllabus(cid, embText, actual_chunk)
            del embText
            del actual_chunk
            #del chunk_with_tag
            del cid
            gc.collect()
         
    print(f"\033[34m{f} chunks insertion:\033[92m done \n\033[0m")


folder.clear()
