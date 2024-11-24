from langchain.text_splitter import SentenceTransformersTokenTextSplitter, RecursiveCharacterTextSplitter
from nltk.tokenize import sent_tokenize
class Tokenize:
    def __init__(self):
        self.separators = [" "]

    def tokenize_text(self, text):
        
        all_chunks = []
        
        # Split the text in sentences
        sentences = sent_tokenize(text)

        # Split the sentences as desired TODO
        for sentence in sentences:
            
            splitter = RecursiveCharacterTextSplitter(
                separators=self.separators,
                chunk_size=500,  
                chunk_overlap=250
            )
            sentence_chunks = splitter.split_text(sentence)

            tokensSplitter = SentenceTransformersTokenTextSplitter(
                chunk_overlap=50, 
                tokens_per_chunk=256
                )
            
            for chunk in sentence_chunks:
                tokensChunks = tokensSplitter.split_text(chunk)
                all_chunks.extend(tokensChunks)
        
        return all_chunks # TODO Now is returning the raw sentences, modify.