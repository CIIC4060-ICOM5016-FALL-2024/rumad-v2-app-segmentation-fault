from flask import jsonify
from sentence_transformers import SentenceTransformer
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from dao.syllabus import SyllabusDAO
import numpy as np

# Ensure the dimensions match
def normalizer(vector):
    vector = np.array(vector)
    padded_vector = np.pad(vector, pad_width=(0, 500 - len(vector)), mode="constant")
    return padded_vector

class ChatbotHandler:
    def mapToDict(self, tuple):
        result = {
            "context": tuple[1],
            "answer": tuple[2]
        }
        return result
    
    def getResponse(self, context_json):
        if not context_json or "context" not in context_json:
            return jsonify(UpdateStatus="Missing required fields"), 400
        
        if not isinstance(context_json["context"], str):
            return jsonify(UpdateStatus="Invalid context type"), 400
        
        context = context_json["context"]
        emb_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        context_embedding = emb_transformer.encode(context)
        context_embedding_str = str(normalizer(context_embedding).tolist())

        dao = SyllabusDAO()

        # try:
        fragments = dao.getAllFragments2(context_embedding_str)
        documents = "\n".join(fragment[2] for fragment in fragments)

        # Define the prompt template for the LLM
        promt = PromptTemplate(
            template="""You are an assistant for question-answering tasks.
            Use the following documents to answer the question.
            If you don't know the answer, just say that you don't know.
            Use five sentences maximum and keep the answer concise:
            Documents: {documents}
            Question: {context}
            Answer:
            """,
            input_variables=["context", "documents"],
        )

        llm = ChatOllama(
            model="llama3.1",
            temperature=0,
        )

            # try:
        chain = promt | llm | StrOutputParser()
        response = chain.invoke({"context": context, "documents": documents})
        if response is None:
            raise ValueError("The response was None.")
        tupl = (context, response)
        return jsonify(self.mapToDict(tupl))

        #     except Exception as e:
        #         return jsonify(UpdateStatus=f"Internal error: {str(e)}"), 500

        # except Exception as e:
        #     return jsonify(UpdateStatus=f"Internal error: {str(e)}"), 500

    