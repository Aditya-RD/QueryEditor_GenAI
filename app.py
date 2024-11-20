import os
import openai
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS  # Import flask_cors

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/')
def home():
    return "Welcome to the Flask API! Use /get_data with parameters."

@app.route('/get_data', methods=['POST'])
def get_data():
    # Retrieve the JSON payload from the POST request
    data = request.get_json()
    prompttext = data.get('prompt')

    # Get the current timestamp
    timestamp = datetime.now().isoformat()

    openai.api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=openai.api_key
    )

    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                template="""You are a highly knowledgeable SQL expert. Please provide clear and executable SQL queries based on the inputs given,  
                and ensure the queries are optimized, accurate, and adhere to best practices.
                Note : Your response should always have only the executable sql query, don't add any other information."""
            ),
            HumanMessagePromptTemplate.from_template(
                template=("User question : {user_ques}")
            ),
        ],
    )

    output_llm = LLMChain(prompt=prompt, llm=llm)
    output = output_llm.run(**{'user_ques': prompttext}, verbose=True)

    # Create a JSON response
    response = {
        "prompttext": prompttext,
        "timestamp": timestamp,
        "output": output
    }

    return jsonify(response)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"})


if __name__ == '__main__':
    app.run(debug=True)