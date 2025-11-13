import os
import io
import pandas as pd
from huggingface_hub import InferenceClient

from env_data import HF_API_TOKEN
# Configuration settings
data_file = "data/feedback.csv"
hf_token = HF_API_TOKEN

NUM_OF_FEEDBACK_TO_READ=250  # Set to 0 to read all feedback

model= "openai/gpt-oss-120b"
#model="zai-org/GLM-4.6:cerebras"

token_chunk_size=15000

prompt_prolog="""You are an expert data analyst. Given the user feedback data, 
provide insights and summaries as requested.
The data is in Hebrew. Please respond in Hebrew.
When summarizing, focus on key themes, common issues, and notable suggestions from users. 
If the data is insufficient to answer the query, respond with "אין מספיק מידע במידע שסופק כדי לענות על השאלה."
ANSWER IN JSON FORMAT with keys: {"question":[enter here original question], "answer":[enter here the answer],}.
"""

final_answer_prompt_prolog="""my dataset was splitted into chunks due to its large size.
From the previous answers to my question, please provide a final summarized answer for the whole dataset.
Please respond in Hebrew.
"""

