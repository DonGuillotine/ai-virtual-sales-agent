import unittest
from unittest.mock import patch, MagicMock

from langchain_core.messages import HumanMessage
from virtual_sales_agent.graph import graph


class TestGraph(unittest.TestCase):
    """Test cases for the LangGraph."""
    
    @patch('langchain_openai.ChatOpenAI')
    def test_graph_basic_invocation(self, mock_chat_openai):
        """Test basic graph invocation."""
        # Mock the LLM to return a fixed response
        mock_ai_message = MagicMock()
        mock_ai_message.content = "Hello! How can I help you with your shopping today?"
        mock_llm_instance = mock_chat_openai.return_value
        mock_llm_instance.invoke.return_value = mock_ai_message
        
        # Create test input
        test_input = {
            "messages": [
                HumanMessage(content="Hello, I'm looking for a gaming mouse")
            ]
        }
        
        config = {
            "configurable": {
                "customer_id": "test123",
                "thread_id": "test-thread-001"
            }
        }
        
        # Run the graph
        with patch('virtual_sales_agent.graph.llm', mock_llm_instance):
            result = graph.invoke(test_input, config)
        
        # Assert result contains messages
        self.assertIn("messages", result)


if __name__ == '__main__':
    unittest.main()