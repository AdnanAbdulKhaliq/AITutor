from dotenv import load_dotenv
import os

# Load environment variables from app.env
load_dotenv("app.env")

# Access all environment variables as needed
google_api_key = os.getenv("GOOGLE_API_KEY")
llm_model_name = os.getenv("LLM_MODEL_NAME")
database_url = os.getenv("DATABASE_URL")
# embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")
llm_temperature = os.getenv("LLM_TEMPERATURE")
