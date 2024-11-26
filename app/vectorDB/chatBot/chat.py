import sys
import os
import json
import numpy as np

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dao.syllabus import SyllabusDAO
from dao.course import ClassDAO
from vectorDB.chatBot.embedding import embeddingClass
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# question = "Tell me at least 3 topics that are taught in the introduction to database (CIIC4060) course?"
# question = "What are the textbooks used in the Machine Learning course?"
#question = "What are the prerequisites for the course (CIIC4020)?"
# question = "What are the prerequisites for the course CIIC 4020?"

def chatbot(question):
    # List of sentences to encode
    class_dao = ClassDAO()
    cid_in_Q = False

    # Analyze the question
    q_fragments = question.split(" ")
    for i in range(len(q_fragments) - 1):
        if q_fragments[i] == "CIIC" or q_fragments[i] == "INSO":
            cname = q_fragments[i]
            ccode = q_fragments[i + 1]
            expected_course_id = class_dao.getClassByCname_Ccode(cname, ccode)
            cid_in_Q = True
        else:
            pass

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
    if cid_in_Q:
        fragments = dao.getAllFragments(
            str(normalizer(emtText).tolist()), expected_course_id[0]
        )
    else:
        fragments = dao.getAllFragments2(str(normalizer(emtText).tolist()))

    context = []

    for f in fragments:
        context.append(str(f[2]))

    documents = "\n".join(c for c in context)

    # Define the prompt template for the LLM
    promt = PromptTemplate(
        template="""You are an assistant for question-answering tasks.
        Use the following documents to answer the question.
        If you don't know the answer, just say that you don't know.
        Use five sentences maximum and keep the answer concise:
        Documents: {documents}
        Question: {question}
        Answer:
        """,
        input_variables=["question", "documents"],
    )

    print(promt.format(question=question, documents=documents))

    # Initialize the LLM with llama 3.1 model
    llm = ChatOllama(
        model="llama3.1",
        temperature=0,
    )

    # Create a chain combining the prompt template and LLM
    chain = promt | llm | StrOutputParser()

    try:
        response = chain.invoke({"question": question, "documents": documents})
        if response is None:
            raise ValueError("The response from the model was None.")
        print(response)
    except TypeError as e:
        return json.dumps({"error": "TypeError occurred", "details": str(e)})
    except ValueError as e:
        return json.dumps({"error": "ValueError occurred", "details": str(e)})
    except ConnectionError as e:
        return json.dumps({"error": "Connection error", "details": str(e)})
    except Exception as e:
        return json.dumps({"error": "An unexpected error occurred", "details": str(e)})

    print("done")

    return json.dumps(response)