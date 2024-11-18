import sys
import os
from os.path import join
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))
from os import listdir
from dao.syllabus import SyllabusDao
from dao.fragments import FragmentsDAO
from tokenize_class import Tokenize
import subprocess

# Run the extract_pdf.py script
result1 = subprocess.run(["python", "./app/vectorDB/dao/extract_pdf.py"], capture_output=True, text=True)


files = listdir("./extracted_syllabuses")

#extract chunks
syllabusDao = SyllabusDao()
fragmentsDAO = FragmentsDAO()
tokenize = Tokenize()
for f in files:
    print(f"\033[93mWorking with: {f}\033[0m")
    file_path = join("./extracted_syllabuses", f)
    with open(file_path, "r") as file:
        text = file.read()
        tokenized = tokenize.tokenize_text(text)
        print(tokenized)
        print(f"\033[92m{f} done \n\n\033[0m")
        
    '''chunkid = syllabusDao.insertSyllabus()
        for t in tokenized:
            emb = model.encode(t)
            fragmentsDAO.insertFragment(did, t, emb.tolist())'''
'''
    #split
    character_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=100,
        chunk_overlap=50
    )
    character_split_texts = character_splitter.split_text('\n\n'.join(pdf_texts))

    print(character_split_texts[10])
    print(f"\nTotal chunks: {len(character_split_texts)}")

    [print(t) for t in character_split_texts]
    print()
    #Token
    token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=50, tokens_per_chunk=256)

    token_split_texts = []
    for text in character_split_texts:
        token_split_texts += token_splitter.split_text(text)
    print("token")
    print(token_split_texts[10])
    [print(t) for t in token_split_texts]
    print(f"\nTotal Splitted chunks: {len(token_split_texts)}")
    #exit(1)

    # insert document into table
    did = docDAO.insertDoc(f)


    for t in token_split_texts:
        emb = model.encode(t)
        #print(t)
        #print(emb)
        fraDAO.insertFragment(did, t, emb.tolist())

    print("Done file: " + f)
'''


