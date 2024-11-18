from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from sentence_transformers import SentenceTransformer
import spacy

# Load a spaCy model
nlp = spacy.load("en_core_web_sm")

class Tokenize:
    def __init__(self):
        self.separators = [" ", "\n", "\t", "\r", "\f", "\v", "\n\n", ". ",""]
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def tokenize_text(self, text):

        # List to store the cleaned tokens (without stop words and lemmatized)
        cleaned_tokens = []

        # Split the text (Chunks of 1000 characters)
        splitter = RecursiveCharacterTextSplitter(
            separators=self.separators,
            chunk_size=1000,
            chunk_overlap=0
        )
        chararter_split_texts = splitter.split_text(text)

        # Split the text into tokens (256 tokens per chunk) 
        token_split = SentenceTransformersTokenTextSplitter(
            chunk_overlap=0,
            tokens_per_chunk=256
        )

        for t in chararter_split_texts:
            tokens = token_split.split_text(t)
    

            # Apply the spacy model to obtain (stop words, base verbs)
            for token in tokens:
                doc = nlp(token)

                # Delete stop Words
                for token in doc:
                    if not token.is_stop:
                        cleaned_tokens.append(token)
                
                # Lemmatize the verbs (Change the verbs to base form)
                cleaned_tokens = [token.lemma_ for token in cleaned_tokens]

        
        return cleaned_tokens