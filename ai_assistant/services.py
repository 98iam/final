import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from django.conf import settings

# Load environment variables from .env file
load_dotenv()

class AIService:
    """Service for interacting with Google Gemini AI API"""

    def __init__(self):
        # Get API key from environment variables
        self.api_key = os.environ.get('GOOGLE_GEMINI_API_KEY', 'your-gemini-api-key-here')
        self.model = "gemini-1.5-pro"  # You can change this to a different model

        # Configure the Gemini API
        genai.configure(api_key=self.api_key)

    def create_prompt(self, query, user=None):
        """Create a prompt for the AI with inventory context"""
        system_message = (
            "You are an AI assistant for an inventory management system. "
            "You can answer questions about inventory, products, sales, and related topics. "
            "Keep your answers concise and focused on inventory management."
        )

        # In Phase 1, we're not adding specific inventory data to the context
        # In later phases, we would fetch relevant data here

        # Combine system message and user query
        prompt = f"{system_message}\n\nUser query: {query}"
        return prompt

    def query_ai(self, query, user=None):
        """Send a query to the Google Gemini API and get a response"""
        try:
            # Check if we should use the real API or simulated responses
            use_real_api = self.api_key != 'your-gemini-api-key-here'

            # Print debugging information
            print(f"API Key: {self.api_key[:5]}...{self.api_key[-5:] if len(self.api_key) > 10 else ''}")
            print(f"Using real API: {use_real_api}")
            print(f"Model: {self.model}")

            if use_real_api:
                # Create the prompt
                prompt = self.create_prompt(query, user)
                print(f"Prompt: {prompt[:100]}...")

                # Initialize the model
                model = genai.GenerativeModel(self.model)

                # Generate response
                print("Sending request to Gemini API...")
                response = model.generate_content(prompt)
                print(f"Response received: {response}")

                if response and hasattr(response, 'text'):
                    return {
                        "success": True,
                        "response": response.text
                    }
                else:
                    return {
                        "success": False,
                        "error": "Failed to get a valid response from Gemini API"
                    }
            else:
                # Simulated response for Phase 1 (when no API key is provided)
                if "product" in query.lower() and "stock" in query.lower():
                    return {
                        "success": True,
                        "response": "Based on the current inventory data, you have 157 products in stock across all categories. The category with the highest stock is 'Electronics' with 42 items."
                    }
                elif "sales" in query.lower():
                    return {
                        "success": True,
                        "response": "Your total sales for the current month are $24,580. This is a 12% increase compared to the same period last month."
                    }
                elif "low stock" in query.lower():
                    return {
                        "success": True,
                        "response": "There are currently 8 products that are below their minimum stock levels. The most critical is 'Wireless Headphones' with only 2 units remaining (minimum: 10)."
                    }
                else:
                    return {
                        "success": True,
                        "response": "I'm your inventory assistant. You can ask me questions about your products, stock levels, sales, and more. For Phase 1, I have limited capabilities, but I'll be able to provide more detailed information in future updates."
                    }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error: {str(e)}"
            }

# Create a singleton instance
ai_service = AIService()
