import sys
import os
#add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from dao.fragments import FragmentsDAO
from embedding import embeddingClass
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# List of sentences to encode
questions = ["what is the prerequisite for CIIC-4010?"]

# Embedding of the first question
emb = embeddingClass()
emtText = emb.embed(questions[0])

# Get all fragments
dao = FragmentsDAO()
fragments = dao.getAllFragments(str(emtText.tolist()))
context = []

for f in fragments:
    print(f)
    context.append(f[3])

print(context[0])

documents = "\\n".join(c for c in context)

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
    input_variables=["questions[0]", "documents"], 
)

print(promt)
print(promt.format(question=questions[0], documents=documents))

# Initialize the LLM with llama 3.1 model
llm = ChatOllama(
    model="llama3.1",
    temperature=0,
)


# Create a chain combining the promt template and LLM
chain = promt | llm | StrOutputParser()

answer = chain.invoke({"question": questions[0], "documents": documents})
print(answer)
print("done")



