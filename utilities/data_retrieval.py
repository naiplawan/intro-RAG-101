import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from utilities.constants import QDRANT_API_KEY

# Load environment variables
load_dotenv()

# Load the embedding model
embedding_model = SentenceTransformer("BAAI/bge-m3")

# Set up Qdrant client
qdrant_client = QdrantClient(
    url="https://31e21270-9280-487a-a780-6db757d62030.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key=QDRANT_API_KEY,
)

collection_name = "documents"


def retrieve_relevant_passages(query, num_passages=5):
    """
    Retrieve relevant passages from Qdrant based on the given query.

    Args:
    - query (str): The query to search for.
    - num_passages (int): The number of relevant passages to retrieve.

    Returns:
    - List of tuples containing (pdf, page, text) for each relevant passage.
    """
    try:
        query_vector = embedding_model.encode(query).tolist()
        search_result = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=num_passages,
        )
        return [
            (hit.payload["pdf"], hit.payload["page"], hit.payload["text"])
            for hit in search_result
        ]
    except Exception as e:
        print(f"Error retrieving relevant passages: {e}")
        return []
