import os
import pandas as pd

# Paths for raw data (input) and processed data (output)
EXTRACTED_DATA_FOLDER = "data/extracted"

# data frame for the data
df_meetings = pd.read_csv(os.path.join(EXTRACTED_DATA_FOLDER, "extracted_meetings.csv"))
df_sections = pd.read_csv(os.path.join(EXTRACTED_DATA_FOLDER, "extracted_sections.csv"))
df_requisites = pd.read_csv(os.path.join(EXTRACTED_DATA_FOLDER, "extracted_requisites.csv"))
