from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from nltk.tokenize import sent_tokenize
import re


class Tokenize:

    def tokenize_text(self, text, file):
        if file == "CIIC-5150-Machine-Learning-Algorithms.txt":
            # Define the pattern to identify section titles (case insensitive)
            pattern = r"(?=(course description:|course objectives:|text books:|course time frame and thematic outline:|instructional strategies:|minimum or\s*required resources available:|evaluation strategies:|grading system|contingency plan in case of an\s*emergency|bibliography))"
        else:
            # Define the pattern to identify section titles (case insensitive)
            pattern = r"(?=(2.\s*course\s*description:|3.\s*pre/co-requisites\s*and\s*other\s*requirements:|4.\s*course\s*objectives:|5.\s*instructional\s*strategies:|minimum\s*or\s*required\s*resources\s*available:|minimum or\s*required resources available:|7.\s*course\s*time\s*frame\s*and\s*thematic\s*outline|8.\s*grading\s*system|9.\s*evaluation\s*strategies|10.\s*bibliography:|11.\s*course\s*outcomes))"

        # Split the text based on the pattern
        chunks = re.split(pattern, text, flags=re.IGNORECASE)

        # Combine the section titles with their corresponding content
        combined_chunks = []
        for i in range(1, len(chunks), 2):
            combined_chunks.append(chunks[i - 1].strip() + "\n" + chunks[i].strip())

        # Handle the last chunk if there is any remaining text
        if len(chunks) % 2 == 1:
            combined_chunks.append(chunks[-1].strip())

        # Debugging: Print the chunks to see how they are divided
        # for idx, chunk in enumerate(combined_chunks):
        #     print(
        #         f"Chunk {idx + 1}: {chunk}...\n"
        #     )  # Print the first 100 characters of each chunk

        return combined_chunks
