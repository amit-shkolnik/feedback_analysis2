import os
import io
import pandas as pd
from huggingface_hub import InferenceClient

# Configuration settings
data_file = "data/feedback.csv"
hf_token = "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"
model= "openai/gpt-oss-120b"
token_chunk_size=15000