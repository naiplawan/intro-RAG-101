import os
import streamlit as st
from utilities.llm import openai_api_call, generate_image_dalle, generate_answer, generate_image_together
from utilities.data_retrieval import retrieve_relevant_passages


st.title("PDF RAG Assistant")

query = st.text_input("Enter your query:")

# Image model selection dropdown
image_model_choice = st.selectbox(
    "Choose an image model:",
    [
        "OpenAI DALL-E",
        "Prompt Hero Openjourney",
        "Runway ML Stable Diffusion 1.5",
        "SG161222 Realistic Vision 3.0",
        "Stability AI Stable Diffusion 2.1",
        "Stability AI Stable Diffusion XL 1.0",
        "Wavymulder Analog Diffusion",
    ],
)

# Mapping image model names to Together AI model strings
image_model_map = {
    "OpenAI DALL-E": None,
    "Prompt Hero Openjourney": "prompthero/openjourney",
    "Runway ML Stable Diffusion 1.5": "runwayml/stable-diffusion-v1-5",
    "SG161222 Realistic Vision 3.0": "SG161222/Realistic_Vision_V3.0_VAE",
    "Stability AI Stable Diffusion 2.1": "stabilityai/stable-diffusion-2-1",
    "Stability AI Stable Diffusion XL 1.0": "stabilityai/stable-diffusion-xl-base-1.0",
    "Wavymulder Analog Diffusion": "wavymulder/Analog-Diffusion",
}

if st.button("Get Answer"):
    if query:
        with st.spinner("Retrieving relevant passages..."):
            passages = retrieve_relevant_passages(query)
            context = "\n\n".join(
                [
                    f"Source: {pdf}, Page: {page}\n\n{paragraph}"
                    for pdf, page, paragraph in passages
                ]
            )

        with st.spinner("Querying OpenAI GPT-4..."):
            answer = generate_answer(context, query)
            st.write("### Answer")
            st.markdown(answer)

        with st.spinner("Generating image..."):
            image_prompt = f"A visual representation of the following answer: {answer}"
            if image_model_choice == "OpenAI DALL-E":
                image_url = generate_image_dalle(image_prompt)
            else:
                model_string = image_model_map[image_model_choice]
                image_url = generate_image_together(image_prompt, model_string)
            if image_url:
                st.image(image_url, caption="Generated Image from Model")
            else:
                st.error("Failed to generate image")

        st.write("### Sources")
        for pdf, page, paragraph in passages:
            with st.expander(f"Source: {pdf}, Page: {page}"):
                st.write(f"{paragraph}")
    else:
        st.error("Please enter a query.")
