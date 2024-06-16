PDF RAG Assistant
This repository contains a Streamlit-based application designed to assist users in retrieving and generating answers from PDF documents using advanced AI models. The application leverages OpenAI's GPT-4 for generating textual answers and provides options for generating visual representations using various image models like DALL-E and Together AI's models.

Features
Textual Answer Generation: Utilizes OpenAI's GPT-4 to generate concise answers based on user queries and retrieved passages from PDF documents.
Image Generation: Offers options to generate visual representations of the answers using:
OpenAI DALL-E
Prompt Hero Openjourney
Runway ML Stable Diffusion 1.5
SG161222 Realistic Vision 3.0
Stability AI Stable Diffusion 2.1
Stability AI Stable Diffusion XL 1.0
Wavymulder Analog Diffusion
Document Embedding and Retrieval: Uses Qdrant for efficient document embedding and retrieval.
User-Friendly Interface: Streamlit application with easy-to-use input fields and dropdowns for model selection.
Technologies Used
Streamlit: For creating an interactive and user-friendly web application.
OpenAI: For GPT-4 based textual answer generation and DALL-E image generation.
Together AI: For generating images using various AI models.
Qdrant: For document embedding and retrieval.
SentenceTransformers: For embedding PDF documents.
PyMuPDF (fitz): For extracting text from PDF documents.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/pdf-rag-assistant.git
cd pdf-rag-assistant
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required packages:

bash
Copy code
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the project root directory.
Add the following variables to the .env file:
env
Copy code
OPENAI_API_KEY=your_openai_api_key
TOGETHER_AI_API_KEY=your_together_ai_api_key
TOGETHER_AI_API_ENDPOINT=https://api.together.xyz/v1
TOGETHER_AI_API_IMAGE_ENDPOINT=https://api.together.xyz/v1/images/generations
Usage
Run the Streamlit application:

bash
Copy code
streamlit run app.py
Interact with the application:

Enter your query in the text input field.
Select the desired image model from the dropdown.
Click the "Get Answer" button to retrieve passages, generate answers, and create visual representations.
Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
Special thanks to the developers of Streamlit, OpenAI, Together AI, Qdrant, SentenceTransformers, and PyMuPDF for providing the tools and libraries used in this project.
