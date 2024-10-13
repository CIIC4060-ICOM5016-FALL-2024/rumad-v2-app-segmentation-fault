import pandas as pd

def get_meeting_data():
    df = pd.read_csv('data/meeting.csv')
    return df
  
  
if __name__ == '__main__':
    get_meeting_data()
    