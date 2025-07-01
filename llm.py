from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from config import google_api_key, llm_model_name, llm_temperature

llm = ChatGoogleGenerativeAI(
    model=llm_model_name, google_api_key=google_api_key, temperature=llm_temperature
)

if __name__ == "__main__":
    try:
        print("Testing connection to Gemini...")
        response = llm.invoke(
            "Hello, Gemini! Please respond with a short confirmation message."
        )
        print("Connection to Gemini successful!")
        print("Response:", response.content)
    except Exception as e:
        print(f"An error occurred while connecting to Gemini: {e}")
