import pandas as pd
from src.data_loader import load_responses
from src.agent import FeedbackAgent

def main():
    # Load the user responses data
    df = load_responses('data/sample_responses.csv')
    
    # Initialize the feedback agent
    agent = FeedbackAgent(df)
    
    print("Welcome to the Feedback Agent!")
    print("You can ask questions about the user responses. Type 'exit' to quit.")
    
    while True:
        user_input = input("Your question: ")
        if user_input.lower() == 'exit':
            break
        
        # Get the answer from the agent
        answer = agent.answer_question(user_input)
        print(f"Agent: {answer}")

if __name__ == "__main__":
    main()