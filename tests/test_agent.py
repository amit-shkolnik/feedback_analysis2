import unittest
import pandas as pd
from src.agent import FeedbackAgent

class TestFeedbackAgent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.agent = FeedbackAgent()
        cls.agent.load_data('data/sample_responses.csv')

    def test_load_data(self):
        self.assertIsInstance(self.agent.data, pd.DataFrame)
        self.assertFalse(self.agent.data.empty)

    def test_answer_question(self):
        response = self.agent.answer_question("What is the average score?")
        self.assertIn("average", response.lower())

    def test_get_response_summary(self):
        summary = self.agent.get_response_summary()
        self.assertIsInstance(summary, dict)
        self.assertIn("total_responses", summary)
        self.assertIn("average_score", summary)

if __name__ == '__main__':
    unittest.main()