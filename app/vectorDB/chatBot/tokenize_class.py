from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from sentence_transformers import SentenceTransformer
import spacy


nlp = spacy.load("en_core_web_sm")

class Tokenize:
    def __init__(self):
        self.separators = [" ", "\n", "\t", "\r", "\f", "\v", "\n\n", ". ",""]
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.model.to('cpu')
    def tokenize_text(self, text):
        # Split the text into chunks of 1000 characters
        splitter = RecursiveCharacterTextSplitter(
            separators=self.separators,
            chunk_size=1000,
            chunk_overlap=0
        )
        chararter_split_texts = splitter.split_text(text)

        # First tokenize the text 
        token_split = SentenceTransformersTokenTextSplitter(
            chunk_overlap=0,
            tokens_per_chunk=256
        )
        token_split_texts = []
        for t in chararter_split_texts:
            tokens = token_split.split_text(t)
            cleaned_tokens = []

        # Delete stop Words and Lem
            for token in tokens:
                doc = nlp(token)
                words = [token.lemma_ for token in doc if not token.is_stop]
                cleaned_tokens.append(" ".join(words))
            token_split_texts.extend(cleaned_tokens)
        
        return token_split_texts