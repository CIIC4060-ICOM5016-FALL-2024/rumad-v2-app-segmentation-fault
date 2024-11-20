import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language

class StopWords:
    def __init__(self):
        # Register the LanguageDetector with spaCy
        @Language.factory("language_detector")
        def create_language_detector(nlp, name):
            return LanguageDetector()

        # spaCy models for English and Spanish
        self.nlp_en = spacy.load("en_core_web_sm")
        self.nlp_es = spacy.load("es_core_news_sm")

        # Add the LanguageDetector to the pipeline
        self.nlp_lang = spacy.load("en_core_web_sm")  # Use a base model to detect language
        self.nlp_lang.add_pipe("language_detector", last=True)

    def detect_language(self, text):
        # Detect the language of the text
        doc = self.nlp_lang(text)
        return doc._.language["language"]

    def text_formatter(self, raw_text, base_name):
        # List of prepositions in English
        english_prepositions = [
            "about", "above", "across", "after", "against", "along", "among", "around", "at", 
            "before", "behind", "below", "beneath", "beside", "between", "beyond", "but", 
            "by", "concerning", "despite", "down", "during", "except", "for", "from", 
            "in", "inside", "into", "like", "near", "of", "off", "on", "onto", "out", 
            "outside", "over", "past", "regarding", "since", "through", "throughout", 
            "till", "to", "toward", "under", "underneath", "until", "up", "upon", "with", 
            "within", "without"
        ]

        # List of prepositions in Spanish
        spanish_prepositions = [
            "a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "durante", 
            "en", "entre", "hacia", "hasta", "mediante", "para", "por", "según", "sin", 
            "so", "sobre", "tras", "versus", "vía"
        ]
        
        # Combine both lists of prepositions
        all_prepositions = english_prepositions + spanish_prepositions
        
        normalized_text = raw_text
        
        # Detect the language of the text
        detected_language = self.detect_language(normalized_text)
        
        # Use the appropriate spaCy model
        if detected_language == "en":
            doc = self.nlp_en(normalized_text)
        elif detected_language == "es":
            doc = self.nlp_es(normalized_text)
        else:
            raise ValueError(f"Unsupported language detected: {detected_language}")

        # Lemmatize verbs
        lemmatized_words = [
            token.lemma_ if token.pos_ == "VERB" else token.text for token in doc
        ]
        
        # Remove prepositions
        words = [word for word in lemmatized_words if word not in all_prepositions]
        normalized_text = ' '.join(words)

        return normalized_text