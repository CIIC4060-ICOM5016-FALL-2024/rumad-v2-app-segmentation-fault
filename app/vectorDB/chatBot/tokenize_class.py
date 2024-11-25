from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from nltk.tokenize import sent_tokenize

class Tokenize:

    def tokenize_text(self, text, chunk_size, overlap_size):
        
        all_chunks = []
        
        # Split the text in sentences
        sentences = sent_tokenize(text)
        '''
        for i in range(0, len(sentences), chunk_size - overlap_size):
            chunk = sentences[i:i + chunk_size]
            all_chunks.append(" ".join(chunk))
        '''
        
        return sentences
    
      