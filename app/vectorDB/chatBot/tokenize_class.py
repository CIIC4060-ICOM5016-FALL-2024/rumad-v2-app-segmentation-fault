from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import SentenceTransformersTokenTextSplitter

class Tokenize:
    def __init__(self):
        self.separators = [" ", "\n", "\t", "\r", "\f", "\v", "\n\n", ". ",""]

    def tokenize_text(self, text):
        splitter = RecursiveCharacterTextSplitter(
            separators=self.separators,
            chunk_size=1000,
            chunk_overlap=0
        )
        chararter_split_texts = splitter.split_text(text)

        token_split = SentenceTransformersTokenTextSplitter(
            chunk_overlap=0,
            tokens_per_chunk=256
        )
        token_split_texts = []
        for t in chararter_split_texts:
            token_split_texts += token_split.split_text(t)
        
        print(chararter_split_texts)
        return token_split_texts