from http.client import responses
import os
from load_data import load_file
from hf_client import HuggingFaceClient
from token_counter import split_json_to_token_chunks
import config
from config import *

class Agent:
    """Agent to analyze user feedback data using a Hugging Face model."""
    def __init__(self):
        self.client = HuggingFaceClient(token=config.hf_token)
        self.data_df = None
        self.summary = None
        #self.data_json= None
        self.data_chunks=None

    def run(self):
        try:
            # Load user feedback data
            print("Running at: {}".format(os.getcwd()))
            data_path = config.data_file
            self.data_df = load_file(data_path)
            self.prepare_context()
            # self.data_json = self.data_df.to_json(orient='records', 
            #                                       force_ascii=False)
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
        responses=[]
        for chunk in self.data_chunks:
                full_query = self.construct_query(chunk, query)
                responses.append( self.client.send_query(
                    config.model, 
                    full_query))
                print(f"Processed chunk, got response: {responses[-1]}")
        # Finaly send another query to summarize all responses
        final_query=self.construct_final_query(responses, query)
        final_response = self.client.send_query(config.model,
                                                final_query)
        return final_response
    
    def construct_query(self, data_chunk, user_query):
        """Construct the full query to send to the model."""
        prompt = f"{config.prompt_prolog}\n\nנתוני המשוב הם:\n{data_chunk}\n\nהשאלה שלי היא: {user_query}\n"
        return prompt
    
    def construct_final_query(self, responses, query):
        """Construct the final query to summarize previous answers."""
        prompt = f""" {config.final_answer_prompt_prolog}\n\n
        [{", ".join([i for i in responses])}]\n\n
        """
        return prompt
    
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
        self.data_chunks= split_json_to_token_chunks(config.data_file)
        return
                         

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("Program start. Running at: {}".format(dir_path))

    agent = Agent()
    agent.run()
    print('Program end')