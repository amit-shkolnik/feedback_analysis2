import os
import io
import pandas as pd
from huggingface_hub import InferenceClient

# Configuration settings
data_file = "data/feedback.csv"
hf_token = "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"