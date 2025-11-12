# Feedback Analysis Agent

## Overview
The Feedback Analysis Agent is a Python project designed to analyze user feedback regarding services. It utilizes the Hugging Face API to process and respond to user queries about the feedback data. The project allows users to load feedback data, analyze it, and interactively ask questions about the responses and their corresponding scores.

## Project Structure
```
feedback-analysis-agent
├── src
│   ├── agent.py          # Contains the Agent class for loading and analyzing feedback data
│   ├── load_data.py      # Functions for loading data into a DataFrame
│   ├── hf_client.py      # Manages interactions with the Hugging Face API
│   ├── config.py         # Configuration settings for the project
│   └── __init__.py       # Marks the directory as a Python package
├── tests
│   ├── test_agent.py     # Unit tests for the Agent class
│   └── test_load_data.py # Unit tests for data loading functions
├── .env.example           # Template for environment variables
├── pyproject.toml        # Project configuration file
├── requirements.txt       # List of required Python packages
├── .gitignore            # Files and directories to ignore by Git
└── README.md             # Documentation for the project
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd feedback-analysis-agent
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env` and fill in the necessary values, such as API tokens and file paths.

## Usage
1. Run the agent:
   ```
   python src/agent.py
   ```

2. Follow the prompts to load feedback data and interact with the Hugging Face model.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## הסבר פשוט ובעברית
1. איך להריץ? הרץ את הקובץ 
run_agent.py 
אשר נמצא בתיקית 
scripts.
הקובץ קורא את הדאטה מתיקית דאטה.

2. איך זה עובד?
התוכנה קוראת את הדאטה ומחלקת אותו לצאנקים קטנים כדי שיוכל להיכנס לקונטקסט של 
המודל.
שים לב!!! שלב זה יכול לקחת מספר דקות, סליחה אבל לא 
עשיתי אופטימיזציה לזה.


לאחר מכן נפתח חלון בו ניתן לשאול שאלות