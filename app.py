import json
import pandas as pd
df = pd.read_csv("datasets/employees.csv")
df.columns = df.columns.str.lower()
from google import genai
from dotenv import load_dotenv
import os
from google.genai import types
from gemini_service import GeminiService
gemini = GeminiService()
from analysis_engine import AnalysisEngine
engine = AnalysisEngine(df)

load_dotenv()

def create_dataset_profile(df):

    profile = {
        "rows": len(df),
        "columns": {}
    }

    for column in df.columns:

        profile["columns"][column] = {
            "dtype": str(df[column].dtype),
            "missing_values": int(df[column].isna().sum()),
            "unique_values": int(df[column].nunique()),
            "sample_values": (
                df[column]
                .dropna()
                .head(5)
                .tolist()
            )
        }

    return profile


dataset_profile = create_dataset_profile(df)

conversation = []
conversation_summary = ""

while True:
    
    user_prompt = input("Ask Gemini something. To exit, type 'exit': ")
    
    # If the user types "exit", break the loop
    if user_prompt.lower() == "exit":
        break

    # If the conversation is too long, summarize it and keep only the last 10 messages
    # if len(conversation) > 20:

    #     conversation_summary = gemini.summarize_conversation(
    #         conversation
    #     )

    #     conversation = conversation[-10:]
    
    conversation.append(
    {
        "role": "user",
        "content": user_prompt
    }
    )

    #Gemini decides the operation
    request = gemini.create_analysis_request(
        user_prompt,
        dataset_profile,
        # conversation_summary,
        conversation
    )

    print("Gemini requested:")
    print(request)
    print()
    print()

    # If user wants an analysis
    if request.intent == "analysis":
        
        # Python performs calculation
        result = engine.execute(request)
        print(result)
        print()
        print()

        # Gemini explains result
        explanation = gemini.generate(
            f"""
            Explain this result to the user:

            Question:
            {user_prompt}

            Result:
            {result}
            """
        )

        response_text = explanation.text

    # If user wants an explanation
    elif request.intent == "explanation":

        explanation = gemini.generate(
            f"""
            You are a data analyst assistant.

            Use the dataset information below to answer
            the user's question.

            Dataset Information:
            {dataset_profile}

            User Question:
            {user_prompt}
            """
        )

        response_text = explanation.text

    else:

        response_text = (
            "I'm not sure how to answer that question yet."
        )


    print(response_text)
    print()
    print()

    conversation.append(
    {
        "role": "assistant",
        "content": response_text
    }
)