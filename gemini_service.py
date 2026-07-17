import os
from urllib import response
from google import genai
from google.genai import types
from dotenv import load_dotenv
from schemas import AnalysisRequest

load_dotenv()

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-2.5-flash"


    def generate(self, prompt, response_schema=None, conversation=None):

        config = None

        if response_schema:
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_schema
            )

        response = self.client.models.generate_content(
            model=self.model,
            contents=conversation if conversation else prompt,
            config=config
        )

        return response

    def summarize_conversation(self, conversation):

        prompt = f"""

        Summarize this conversation.

        Keep important:
        - user goals
        - questions asked
        - conclusions
        - important dataset findings

        Conversation:

        {conversation}

        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text

    def create_analysis_request(
            self,
            question,
            dataset_profile,
            conversation_summary,
            conversation
        ):

        conversation_text = "\n".join(
            [
                f"{message['role']}: {message['content']}"
                for message in conversation
            ]
        )

        prompt = f"""

        You are an AI data analyst.

        Dataset information:
        {dataset_profile}

        Conversation Summary:
        {conversation_summary}

        Previous conversation:
        {conversation_text}


        Classify the user's question.

        Possible intents:

        1. analysis
        - requires calculating something from the dataframe
        - use this when the answer requires a calculation, aggregation, filtering, or statistical operation

        2. explanation
        - can be answered using the dataset information alone
        - use this for questions about columns, dataset meaning, or general explanations


        User question:

        {question}


        If analysis is required, provide the operation.

        """


        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AnalysisRequest
            )
        )


        return response.parsed