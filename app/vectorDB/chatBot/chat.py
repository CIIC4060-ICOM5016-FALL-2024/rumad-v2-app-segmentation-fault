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
# print(f"Dimensions of embedded vector: {len(emtText)}")

# Ensure the dimensions match the expected dimensions in the database
expected_dimensions = 500  # Update this to match your database schema
current_dimensions = len(emtText)

if current_dimensions < expected_dimensions:
    # Append zeros to the vector to match the required dimensions
    emtText = np.pad(emtText, (0, expected_dimensions - current_dimensions), "constant")
elif current_dimensions > expected_dimensions:
    raise ValueError(
        f"Expected embedding dimensions {expected_dimensions}, but got {current_dimensions}"
    )


# Get all fragments
dao = SyllabusDAO()
fragments = dao.getAllFragments(str(emtText.tolist()))
context = []

for f in fragments:
    print(f)
    context.append(str(f[3]))

# Ensure context is populated before accessing its elements
if context:
    print(context[0])
else:
    print("Context is empty")

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

print(promt)
print(promt.format(question=question, documents=documents))

# Initialize the LLM with llama 3.1 model
llm = ChatOllama(
    model="llama3.1",
    temperature=0,
)


# Create a chain combining the promt template and LLM
chain = promt | llm | StrOutputParser()

answer = chain.invoke({"question": question, "documents": documents})
print(answer)
print("done")
