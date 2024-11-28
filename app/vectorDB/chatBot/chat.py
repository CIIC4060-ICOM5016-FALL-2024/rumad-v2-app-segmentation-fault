import sys
import os
import json
import numpy as np
import re

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dao.syllabus import SyllabusDAO
from dao.course import ClassDAO
from vectorDB.chatBot.embedding import embeddingClass
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# List of sentences to encode
class_dao = ClassDAO()
# question = "What are the requisites of the course CIIC 4151 (Design Project)?"
# question = "How are grades divided in the INSO 5111 course?"
# question = "What are the textbooks used in the Machine Learning course?"
# question = "Tell me at least 3 topics that are taught in the introduction to database (CIIC4060) course?"
# question = "What are the prerequisites for the course (CIIC4020)?"
# question = "What are the most important diferences between CIIC 4060 and CIIC 4020?"
question = "What are the Instructional strategies for the course CIIC 3015?"

# Analize the question
expected_cnames = ["CIIC", "INSO"]

pattern = rf"({'|'.join(expected_cnames)})[\s]*(\d+)"
matches = re.findall(pattern, question, flags=re.IGNORECASE)
expected_course_ids = None
expected_course_id = None
result = []
for match in matches:
    result.append({"cname": match[0].upper(), "ccode": match[1]})

# Manage multiple coursesids
if result and len(result) > 1:
    expected_course_ids = []
    for r in result:
        expected_course_ids.append(
            class_dao.getClassByCname_Ccode(r["cname"].upper(), r["ccode"])[0]
        )
    # print(expected_course_ids)

elif result:  # TODO check if multiple coursesid
    expected_course_id = class_dao.getClassByCname_Ccode(
        result[0]["cname"].upper(), result[0]["ccode"]
    )[0]
    # print(expected_course_id)

# Embedding of the first question
emb = embeddingClass()
emtText = emb.embed(question)


# Ensure the dimensions match
def normalizer(vector):
    vector = np.array(vector)
    padded_vector = np.pad(vector, pad_width=(0, 500 - len(vector)), mode="constant")
    return padded_vector


# Get all fragments
dao = SyllabusDAO()
if expected_course_id:
    fragments = dao.getAllFragments(
        str(normalizer(emtText).tolist()), expected_course_id
    )
# Manage multiple coursesids
elif expected_course_ids:
    fragments = dao.getAllFragments3(
        str(normalizer(emtText).tolist()), expected_course_ids
    )
else:
    fragments = dao.getAllFragments2(str(normalizer(emtText).tolist()))

context = []

for f in fragments:
    context.append(str(f[2]))

documents = "\n".join(c for c in context)

# Define the promt template for the LLM
promt = PromptTemplate(
    template="""You are an assistant for question-answering tasks.
    Use the following documents to answer the question. Follow these rules:
    - Answer using the provided documents only.
    - Use a concise and formal style.
    - Structure the response with proper bullet points and line breaks.
    - Reference the course syllabus
    - Start the response with: "Based on the syllabus for this class:"
    - If you don't know the answer, just say that you don't know.
    - Provide up to five sentences in the response.
    - Ensure bullets are well-organized, with one topic per line.

    Documents: {documents}
    Question: {question}
    Answer:
    """,
    input_variables=["question", "documents"],
)

# print(promt.format(question=question, documents=documents))

# Initialize the LLM with llama 3.1 model
llm = ChatOllama(
    model="llama3.1",
    temperature=3,
)

# Create a chain combining the promt template and LLM
chain = promt | llm | StrOutputParser()

try:
    response = chain.invoke({"question": question, "documents": documents})
    if response is None:
        raise ValueError("The response from the model was None.")
    print(response)
except TypeError as e:
    print(f"Error: {e}")
    print("The response from the model was None.")
except ValueError as e:
    print(f"Error: {e}")

print("done")
