import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------
# OpenAI
# ------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ------------------------------------------------------------
# TOGETHER AI
# ------------------------------------------------------------
TOGETHERAI_API_CHAT_ENDPOINT = os.getenv("TOGETHERAI_API_CHAT_ENDPOINT")
TOGETHERAI_API_IMAGE_ENDPOINT = os.getenv("TOGETHERAI_API_IMAGE_ENDPOINT")
TOGETHER_AI_API_KEY = os.getenv("TOGETHER_AI_API_KEY")
TOGETHER_AI_MODEL_NAME = os.getenv("TOGETHER_AI_MODEL_NAME")

# ------------------------------------------------------------
# Qdrant
# ------------------------------------------------------------
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
QDRANT_ENDDPOINT = os.getenv('QDRANT_ENDDPOINT')
