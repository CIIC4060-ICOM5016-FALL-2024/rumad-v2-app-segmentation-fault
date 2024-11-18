from sentence_transformers import SentenceTransformer

class embeddingClass:
   def __init__(self):
     self.model = SentenceTransformer('all-MiniLM-L6-v2')
     
   def embed(self, sentence):
        return self.model.encode(sentence)
        
        
