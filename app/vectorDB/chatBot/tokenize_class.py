from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import SentenceTransformersTokenTextSplitter

class Tokenize:
    def __init__(self):
        self.separators = [" ", "\n", "\t", "\r", "\f", "\v", "\n\n", ". ", ""]

    def tokenize_text(self, text):

        # List to store the cleaned tokens (without stop words and lemmatized)
        all_chunks = []

        # Split the text (Chunks of 1000 characters)
        splitter = RecursiveCharacterTextSplitter(
            separators=self.separators, chunk_size=600, chunk_overlap=0
        )
        character_split_texts = splitter.split_text(text)

        # Split the text into tokens (256 tokens per chunk)
        token_split = SentenceTransformersTokenTextSplitter(
            chunk_overlap=0, tokens_per_chunk=1
        )

        character_split_texts = splitter.split_text(text)
        for chunk in character_split_texts:
            token_chunks = token_split.split_text(chunk)
            all_chunks.append(token_chunks)

        return all_chunks
