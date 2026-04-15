import pandas as pd
import numpy as np


def clean_data(data):
    if isinstance(data, dict):
        return {k: clean_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_data(v) for v in data]
    elif isinstance(data, float) and (np.isnan(data) or np.isinf(data)):
        return None
    return data


def analyze_dataframe(df):
    analysis = {}

    analysis["columns"] = list(df.columns)

    analysis["dtypes"] = {col: str(df[col].dtype) for col in df.columns}

    analysis["missing_values"] = df.isnull().sum().to_dict()

    analysis["duplicate_rows"] = int(df.duplicated().sum())

    analysis["unnamed_columns"] = [
        col for col in df.columns if "unnamed" in col.lower()
    ]

    analysis["sample_data"] = df.head(5).to_dict(orient="records")

    # 🔥 تنظيف NaN
    analysis = clean_data(analysis)

    return analysis
