import os
import warnings
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import fitz
import uuid
import concurrent.futures
from llama_index.core import Document, GPTVectorStoreIndex
from utilities.constants import QDRANT_API_KEY,QDRANT_ENDDPOINT
from threadpoolctl import threadpool_limits

# Suppress the FutureWarning for resume_download
warnings.filterwarnings(
    "ignore", category=FutureWarning, module="huggingface_hub.file_download"
)

# Set the number of threads to control OpenMP loading
with threadpool_limits(limits=1, user_api="blas"):
    # Load environment variables
    load_dotenv()

    # Load the embedding model
    embedding_model = SentenceTransformer("BAAI/bge-m3")

    # Set up Qdrant client
    qdrant_client = QdrantClient(
        url=QDRANT_ENDDPOINT,
        api_key=QDRANT_API_KEY,
    )

    print(qdrant_client.get_collections())

    # Create or recreate a collection in Qdrant
    collection_name = "documents"
    if qdrant_client.collection_exists(collection_name):
        qdrant_client.delete_collection(collection_name)
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=embedding_model.get_sentence_embedding_dimension(),
            distance=Distance.COSINE,
        ),
    )

    def extract_text_from_page(doc, page_num):
        try:
            page = doc.load_page(page_num)
            return (doc.name, page_num, page.get_text())
        except Exception as e:
            print(f"Error extracting text from page {page_num} of {doc.name}: {e}")
            return None

    def extract_text_from_pdf(pdf_path):
        try:
            doc = fitz.open(pdf_path)
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=8
            ) as executor:  # Increased number of threads
                texts = list(
                    executor.map(
                        lambda page_num: extract_text_from_page(doc, page_num),
                        range(len(doc)),
                    )
                )
            # Filter out None values in case of errors
            texts = [text for text in texts if text is not None]
            return texts
        except Exception as e:
            print(f"Error extracting text from PDF {pdf_path}: {e}")
            return []

    def extract_texts_from_folder(folder_path):
        texts = []
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=4
        ) as executor:  # Increased number of threads
            futures = [
                executor.submit(
                    extract_text_from_pdf, os.path.join(folder_path, file_name)
                )
                for file_name in os.listdir(folder_path)
                if file_name.lower().endswith(".pdf")
            ]
            for future in concurrent.futures.as_completed(futures):
                try:
                    texts.extend(future.result())
                except Exception as e:
                    print(f"Error processing a future result: {e}")
        return texts

    def store_embeddings_in_qdrant(texts):
        for pdf, page, text in texts:
            paragraphs = text.split("\n\n")
            for paragraph in paragraphs:
                if paragraph.strip():  # Only process non-empty paragraphs
                    try:
                        vector = embedding_model.encode(paragraph).tolist()
                        qdrant_client.upsert(
                            collection_name=collection_name,
                            points=[
                                PointStruct(
                                    id=str(uuid.uuid4()),  # Generate a unique ID
                                    vector=vector,
                                    payload={
                                        "pdf": pdf,
                                        "page": page,
                                        "text": paragraph,
                                    },
                                )
                            ],
                        )
                    except Exception as e:
                        print(
                            f"Error storing embedding for paragraph in {pdf} page {page}: {e}"
                        )

    def retrieve_relevant_passages(query, num_passages=5):
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

    def index_documents_with_llama(texts):
        documents = [
            Document(text=text) for pdf, page, text in texts if text.strip()
        ]  # Ensure only non-empty texts
        if documents:  # Ensure there are documents to index
            try:
                index = GPTVectorStoreIndex(documents)  # Ensure correct usage
                index.save_to_disk("index.json")
            except Exception as e:
                print(f"Error indexing documents with Llama: {e}")

    def query_llama_index(query):
        try:
            index = GPTVectorStoreIndex.load_from_disk(
                "index.json"
            )  # Ensure correct usage
            response = index.query(query)
            return response
        except Exception as e:
            print(f"Error querying Llama index: {e}")
            return ""

    # Process PDFs in the "example_rag" directory
    folder_path = "example_rag"
    if os.path.isdir(folder_path):
        print(f"Extracting text from PDF files in {folder_path}...")
        texts = extract_texts_from_folder(folder_path)
        store_embeddings_in_qdrant(texts)
        index_documents_with_llama(texts)
        print("Text extraction and indexing completed.")
    else:
        print(
            f"Folder '{folder_path}' does not exist. Please ensure the folder path is correct."
        )
