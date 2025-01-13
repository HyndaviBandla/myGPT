from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# CDP Documentation Links
CDP_DOCS = {
    "Segment": "https://segment.com/docs/?ref=nav",
    "mParticle": "https://docs.mparticle.com/",
    "Lytics": "https://docs.lytics.com/",
    "Zeotap": "https://docs.zeotap.com/home/en-us/"
}

def get_gemini_response(question, prompt):
    """
    Query the Gemini API with a structured prompt and user question.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([question, prompt])
    return response.text

def find_relevant_docs(question):
    """
    Match the question to a relevant CDP documentation link.
    """
    for platform, link in CDP_DOCS.items():
        if platform.lower() in question.lower():
            return link
    return None

# Streamlit App
st.set_page_config(page_title="CDP How-To Assistant")
st.header("CDP How-To Assistant")
st.markdown("Ask your 'how-to' questions about Segment, mParticle, Lytics, or Zeotap, and get answers with relevant documentation links.")

# Input for the question
user_question = st.text_area("Ask your question here (e.g., How do I set up a new source in Segment?):")

# Button to submit the question
submit_question = st.button("Submit Question")

if submit_question:
    if user_question.strip():
        # Define a prompt for the Gemini API
        gemini_prompt = """
        You are a knowledgeable assistant specializing in four Customer Data Platforms (CDPs): 
        Segment, mParticle, Lytics, and Zeotap. Based on the question, provide clear and concise 
        steps or guidelines for accomplishing the task in the relevant platform. 
        Reference the official documentation where possible. is irrelevant questions or
        out of the domain questions asked say "irrelevant question".
        """
        
        # Fetch response from Gemini API
        response = get_gemini_response(user_question, gemini_prompt)
        
        # Identify relevant documentation link
        relevant_doc = find_relevant_docs(user_question)
        
        # Display the response
        st.subheader("Response:")
        st.write(response)
        
        # Display the relevant documentation link
        if relevant_doc:
            st.markdown(f"**Relevant Documentation:** [Click here]({relevant_doc})")
        else:
            st.write("No specific documentation link found for your query.")
    else:
        st.error("Please enter a valid question.")
