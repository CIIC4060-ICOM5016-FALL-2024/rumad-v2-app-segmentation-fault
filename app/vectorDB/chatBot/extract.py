import fitz  # PyMuPDF
import textwrap
import re
import os


class Extract:
    def __init__(self):
        pass

    def extract_directory(self, folder_path, output_folder):
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f"No such directory: '{folder_path}'")

        for f in os.listdir(folder_path):
            if f.endswith(".pdf"):
                input_path = os.path.join(folder_path, f)
                pdf_text_extractor(input_path, output_folder)


def text_formatter(raw_text, base_name):
    # Remove excessive line breaks and combine multiple spaces into one
    normalized_text = re.sub(r"\n\s*\n", "\n", raw_text)  # Remove multiple newlines
    # Replace multiple spaces with one
    normalized_text = re.sub(r"\s{2,}", " ", normalized_text)
    # Remove unnecessary leading/trailing whitespace
    normalized_text = normalized_text.strip()
    # Clean invisible and indivisible spaces (Malfunction in tokenize if leave)
    normalized_text = re.sub(r"[\u200B-\u200D\uFEFF]", "", normalized_text)
    normalized_text = re.sub(r"\u00A0", "", normalized_text)
    # Divides the sentences for headers.
    normalized_text = re.sub(r"(?<!\.) (\d{2}\.)\s", r". \1", normalized_text)
    normalized_text = re.sub(r"(?<!\.) (\d{1}\.)\n", r". \1", normalized_text)
    # "Delete" space after header number (only if change the format)
    normalized_text = re.sub(r"(\d\.)\n", r"\1", normalized_text)
    # Convert text to lowercase
    normalized_text = normalized_text.lower()

    # Wrap text to the specified line length
    wrapped_text = textwrap.fill(normalized_text, width=80)
    # Remove "Page X of Y" lines
    wrapped_text = re.sub(r"page \d+ of \d+", "", wrapped_text)

    if base_name == "CIIC-5150-Machine-Learning-Algorithms":
        # Remove header
        wrapped_text = re.sub(
            r"university of puerto rico.*?course syllabus",
            "course syllabus",
            wrapped_text,
            flags=re.DOTALL,
        )
        # Remove innecesary and duplicate information
        wrapped_text = re.sub(
            r"reasonable accommodation.*?grading system",
            "grading system",
            wrapped_text,
            flags=re.DOTALL,
        )
    else:
        # Remove Header
        wrapped_text = re.sub(
            r"university of puerto rico - mayagüez campus.*?\b\d{4}\b",
            "",
            wrapped_text,
            flags=re.DOTALL,
        )
        # Remove innecesary and duplicate information
        wrapped_text = re.sub(r"12\.  a.*", "", wrapped_text, flags=re.DOTALL)

    # Remove unnecessary spaces
    wrapped_text = wrapped_text.replace("  ", " ")
    wrapped_text = wrapped_text.replace("   ", " ")
    wrapped_text = wrapped_text.replace("    ", " ")
    wrapped_text = wrapped_text.replace(" .", ". ")
    wrapped_text = wrapped_text.replace(" ,", ", ")
    wrapped_text = wrapped_text.replace(" :", ": ")
    wrapped_text = wrapped_text.replace(" ;", "; ")
    wrapped_text = wrapped_text.replace("  .", ". ")
    wrapped_text = wrapped_text.replace("  ,", ", ")
    wrapped_text = wrapped_text.replace("  :", ": ")
    wrapped_text = wrapped_text.replace(". ", ". ")
    wrapped_text = wrapped_text.replace(", ", ", ")
    wrapped_text = wrapped_text.replace(": ", ": ")
    wrapped_text = wrapped_text.replace("; ", "; ")
    wrapped_text = wrapped_text.replace(".  ", ". ")
    wrapped_text = wrapped_text.replace(",  ", ", ")
    wrapped_text = wrapped_text.replace(":  ", ": ")
    wrapped_text = wrapped_text.replace(";  ", "; ")
    wrapped_text = wrapped_text.replace(".    ", ". ")
    wrapped_text = wrapped_text.replace(",    ", ", ")
    wrapped_text = wrapped_text.replace(":    ", ": ")
    wrapped_text = wrapped_text.replace(";    ", "; ")
    wrapped_text = wrapped_text.replace(" . ", ". ")

    return wrapped_text


def pdf_text_extractor(pdf_path, output_folder):
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"No such file: '{pdf_path}'")

    # Extract the base name of the PDF file without extension
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Open the PDF file
    with fitz.open(pdf_path) as doc:
        extracted_text = ""
        for page_number in range(len(doc)):
            page = doc[page_number]
            text = page.get_text()
            extracted_text += f"{text}\n"

    # Clean the extracted text
    cleaned_text = text_formatter(extracted_text, base_name)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Save the cleaned text to a .txt file with the same base name in the output folder
    output_path = os.path.join(output_folder, f"{base_name}.txt")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(cleaned_text)

    print(f"Syllabus \033[92m{base_name}\033[0m has been extracted.")
    return output_path
