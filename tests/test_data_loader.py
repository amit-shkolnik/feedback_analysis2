import pandas as pd
from src.data_loader import load_responses

def test_load_responses():
    df = load_responses('data/sample_responses.csv')
    assert isinstance(df, pd.DataFrame), "Loaded data is not a DataFrame"
    assert not df.empty, "DataFrame is empty"
    assert 'response' in df.columns, "Response column is missing"
    assert 'score' in df.columns, "Score column is missing"
    assert df['score'].between(1, 5).all(), "Scores are not in the range of 1-5"