import sys
import os
import numpy as np

# add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dao.syllabus import SyllabusDAO
from embedding import embeddingClass
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# List of sentences to encode
question = "what is the prerequisite for CIIC-4010?"

# Embedding of the first question
emb = embeddingClass()
emtText = emb.embed(question)

# Ensure the dimensions match
if len(emtText) < 500:
    # Append zeros to the required dimensions
    emtText = np.pad(emtText, (0, 500 - len(emtText)), "constant")
elif len(emtText) > 500:
    raise ValueError(f"Expected embedding dimensions {500}, but got {len(emtText)}")


# Get all fragments
dao = SyllabusDAO()
fragments = dao.getAllFragments(str(emtText.tolist()))
context = []

for f in fragments:
    context.append(str(f[3]))

documents = "\n".join(c for c in context)

# Define the promt template for the LLM
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
