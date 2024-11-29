from flask import jsonify
from sentence_transformers import SentenceTransformer
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import numpy as np

# Ensure the dimensions match
def normalizer(vector):
    vector = np.array(vector)
    padded_vector = np.pad(vector, pad_width=(0, 500 - len(vector)), mode="constant")
    return padded_vector

class OllamaChatHandler:
    def mapToDict(self, tuple):
        result = {
            "context": tuple[0],
            "answer": tuple[1]
        }
        return result
    
    def getEmbedding(self, text_json):
        if not text_json or "text" not in text_json:
            return jsonify(UpdateStatus="Missing required fields"), 400
        
        if not isinstance(text_json["text"], str):
            return jsonify(UpdateStatus="Invalid text type"), 400
        
        text = text_json["text"]
        emb_transformer = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        text_embedding = emb_transformer.encode(text)
        text_embedding_str = str(normalizer(text_embedding).tolist())

        return jsonify({"embedding": text_embedding_str})
    
    def getResponse(self, context_json):
        if not context_json or "context" not in context_json or "question" not in context_json:
            return jsonify(UpdateStatus="Missing required fields"), 400
        
        if not isinstance(context_json["context"], str) or not isinstance(context_json["question"], str):
            return jsonify(UpdateStatus="Invalid context type"), 400
        
        context = context_json["context"]
        question = context_json["question"]

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
            - If the question is from something in the past, try to use the Context.
            - Don't use the Context as a question, only as additional information.
            - Don't reference the use of the Context only use it.
            - Don't change the format of the answer for something present in the Context.
            - When asking for course descriptions, look for the documents in the Context and use the '2. Course Description' section.
            - When asking for the text books of a course differentiate between the bibliography and the Text Books, add one section for only text books and other section for the bibliography.

            Context: {context}
            Question: {question}
            Answer:
            """,
            input_variables=["context", "question"],
        )

        llm = ChatOllama(
            model="llama3.1",
            temperature=0,
        )

        chain = promt | llm | StrOutputParser()
        response = chain.invoke({"context": context, "question": question})
        if not response:
            response = "Response was None"
        context += question
        tupl = (context, response)
        return jsonify(self.mapToDict(tupl))
        
        