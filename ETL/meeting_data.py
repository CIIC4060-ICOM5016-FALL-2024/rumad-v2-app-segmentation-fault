import pandas as pd

def get_meeting_data():
    df = pd.read_csv('data/raw/meeting.csv')
    df = df.dropna()
    df.to_csv('data/processed/meeting.csv')

    return df
  
  
if __name__ == '__main__':
    get_meeting_data()
    