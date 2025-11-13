import os
import io
import sys

sys.path.append(os.path.abspath("src"))

from agent import Agent



def main():
    # Initialize the feedback agent
    agent = Agent()
    
    print("Welcome to the Feedback Agent!")
    print("You can ask questions about the user responses. Type 'exit' to quit.")
    agent.run()

if __name__ == "__main__":
    main()