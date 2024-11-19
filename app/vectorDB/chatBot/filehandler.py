import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import numpy as np
from dao.course import ClassDAO
from dao.syllabus import SyllabusDAO
from tokenize_class import Tokenize
from embedding import embeddingClass
import subprocess

# Run the extract_pdf.py script
#result1 = subprocess.run(["python", "./app/vectorDB/dao/extract_pdf.py"], capture_output=True, text=True)

# Initialize the DAOs and folder path
syllabusDao = SyllabusDAO()
tokenize = Tokenize()
emb = embeddingClass()
class_Dao = ClassDAO()
folder_path = "./extracted_syllabuses"

def normalizer(vector):
    vector = np.array(vector)
    padded_vector = np.pad(vector,pad_width=(0,500 - len(vector)), mode='constant')
    return padded_vector


# Iterate over the extracted syllabus files (.txt)
for f in os.listdir(folder_path):
    print(f"\033[93mWorking with: {f}\033[0m")

    file_path = os.path.join(folder_path, f)
    count = 0
    with open(file_path, "r") as file:
        text = file.read()
        text = tokenize.tokenize_text(text)

        for actual_chunk in text:
            count += 1
            print(f"\033[94mChunk {count}\033[0m")
            embText = normalizer(emb.embed(actual_chunk[0])).tolist()
            print(actual_chunk)
            # Insert syllabus into the database
            cid = class_Dao.getClassByCname_Ccode(f.split("-")[0], f.split("-")[1])[0]
            chunkid = syllabusDao.insertSyllabus(cid, embText, actual_chunk)

        print(f"\033[92m{f} done \n\n\033[0m")



