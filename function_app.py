import azure.functions as func
import logging
import os
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# --- Configuration from Environment Variables ---
# Load credentials from the Function App's Application Settings
AZURE_AI_SEARCH_ENDPOINT = os.environ.get("AZURE_AI_SEARCH_ENDPOINT")
AZURE_AI_SEARCH_KEY = os.environ.get("AZURE_AI_SEARCH_KEY")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_SEARCH_INDEX_NAME = "phishing-urls-index" # The name of the index we created

# Initialize the Azure Function App
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="analyze")
def analyze(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # --- 1. Get User Input ---
    # Try to get the user's text from the request body
    try:
        req_body = req.get_json()
        user_input = req_body.get('text')
    except ValueError:
        return func.HttpResponse("Invalid request: Please provide a JSON body with a 'text' field.", status_code=400)

    if not user_input:
        return func.HttpResponse("Invalid request: 'text' field cannot be empty.", status_code=400)

    try:
        # --- 2. Retrieve Relevant Data (The "R" in RAG) ---
        # Initialize the AI Search client
        search_client = SearchClient(
            endpoint=AZURE_AI_SEARCH_ENDPOINT,
            index_name=AZURE_SEARCH_INDEX_NAME,
            credential=AzureKeyCredential(AZURE_AI_SEARCH_KEY)
        )
        
        # Perform a search to find similar, known phishing URLs from our knowledge base
        search_results = search_client.search(search_text=user_input, top=3, select="url")
        
        context_from_search = "\n".join([f"- {result['url']}" for result in search_results])
        
        if not context_from_search:
            context_from_search = "No similar known phishing URLs were found in the database."

        # --- 3. Generate the AI Response (The "G" in RAG) ---
        # Initialize the Azure OpenAI client
        openai_client = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_KEY,
            api_version="2024-02-01" # A recent, stable API version
        )

        # Construct the detailed prompt for the AI model
        system_prompt = """
        You are an AI phishing detector. Your task is to analyze the user's text and determine if it is likely a phishing attempt.
        You must classify it as 'Safe', 'Suspicious', or 'Malicious'.
        You must provide a short, clear, one-paragraph explanation for your conclusion, written for a non-technical user.
        Base your analysis on the user's input and the provided context of known phishing URLs.
        """
        
        user_prompt = f"""
        Please analyze the following text:
        ---
        User Input: "{user_input}"
        ---
        For context, here are some similar known phishing URLs from our database:
        ---
        Context:
        {context_from_search}
        ---
        Based on all this information, what is your analysis?
        """

        # Call the OpenAI model
        response = openai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )

        ai_response = response.choices[0].message.content

        # Return the AI's analysis to the user
        return func.HttpResponse(ai_response, status_code=200, mimetype="text/plain")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return func.HttpResponse("Sorry, an internal error occurred. Please try again later.", status_code=500)