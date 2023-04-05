import pandas as pd
import numpy as np
import joblib
from fastapi import HTTPException
df = pd.read_csv('data/labelencoder_df.csv')
label_encoders = joblib.load('joblib/label_encoders.joblib')

def get_equiv_table(column):
    if column not in label_encoders:
        raise HTTPException(status_code=404, detail=f"Column '{column}' not found")
    if df[column].dtype != 'object':
        return None
    le = label_encoders[column]
    label_values = le.inverse_transform(np.arange(len(le.classes_)))
    encoded_values = np.arange(len(le.classes_))
    equiv_table = dict(zip(label_values, encoded_values))
    return equiv_table
