import os
from load_data import load_file
from hf_client import HuggingFaceClient
import config
from config import *

class Agent:
    def __init__(self):
        self.client = HuggingFaceClient(token=config.hf_token)
        self.data_df = None
        self.summary = None
        self.data_json= None
        self.data_length= None                 
        self.data_chunks=None

    def run(self):
        try:
            # Load user feedback data
            print("Running at: {}".format(os.getcwd()))
            data_path = config.data_file
            self.data_df = load_file(data_path)
            self.prepare_context()
            self.data_json = self.data_df.to_json(orient='records', 
                                                  force_ascii=False)
            print("Data loaded successfully. Number of records: {}".format(len(self.data_df)))

            while True:
                user_query = input("Ask a question about the feedback data (or type 'exit' to quit): ")
                if user_query.lower() == 'exit':
                    break
                response = self.handle_query(user_query)
                print("Response: {}".format(response))

        except Exception as e:
            print("Error occurred: {}".format(e))

    def handle_query(self, query):
        """Handle user queries and interact with the Hugging Face model."""
        #feedback_summary = self.summarize_feedback()
        for chunk in self.data_chunks:
                    full_query = f"{query}\n\nFeedback Summary:\n{feedback_summary}"
        return self.client.send_query("openai/gpt-oss-120b", full_query)
        return self.client.get_response(full_query)

    def summarize_feedback(self):
        """Summarize the feedback data for analysis."""
        if self.summary is not None:
            return self.summary
        self.summary = self.data_df.groupby('Level')['Text'].apply(lambda x: ' '.join(x)).to_string()
        return self.summary
    
    def prepare_context(self):
        """
        Prepare the context for the agent by converting the 
        DataFrame to JSON, 
        than split it to chunk - 80000 words each.
        """
        self.data_json = self.data_df.to_json(orient='records', 
                                              force_ascii=False)
        self.data_length = len(self.data_json.split())
        self.data_chunks = [self.data_json[i:i + 80000] for i in range(0, self.data_length, 80000)]
        print("Data len: {} prepared into {} chunks.".format(self.data_length,                  
                                                            len(self.data_chunks)
                                                         ))
        return self.data_json
        

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("Program start. Running at: {}".format(dir_path))

    agent = Agent()
    agent.run()
    print('Program end')