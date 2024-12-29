import os
import yaml
import streamlit as st
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from streamlit_quill import st_quill


# ===============================
# Load Configuration
# ===============================

config_path = 'config.yaml'

def load_config(config_path: str = 'config.yaml') -> dict:
    if not os.path.exists(config_path):
        st.sidebar.error(f"Configuration file `{config_path}` not found.")
        st.stop()
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        st.sidebar.error(f"Error parsing the configuration file: {e}")
        st.stop()

        
# Load configuration from 'config.yaml'
config = load_config()


# Extract OpenAI configuration
openai_config = config.get('openai', {})
TEMPERATURE = openai_config.get('temperature', 0.7)
MAX_TOKENS = openai_config.get('max_tokens', 500)
TOP_P = openai_config.get('top_p', 1.0)
FREQUENCY_PENALTY = openai_config.get('frequency_penalty', 0.0)
PRESENCE_PENALTY = openai_config.get('presence_penalty', 0.0)
MODEL_NAME = openai_config.get('model_name', 'gpt-4o-mini')
OPENAI_API_KEY = openai_config.get('api_key')




# Streamlit App Layout
st.set_page_config(
    page_title="Email Mentor",
    page_icon="📧",
    layout="wide",
)

st.title("📧 Cuesta Email Mentor")
st.markdown("""
Welcome to the **Cuesta Email Mentor** app! Paste your email below, and receive recommendations to improve it.
""")



# ===============================
# Initialize Chat-Based Model
# ===============================

# Initialize ChatOpenAI with the selected model and configuration
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model_name=MODEL_NAME,
    temperature=TEMPERATURE,
    max_tokens=MAX_TOKENS,
    top_p=TOP_P,
    frequency_penalty=FREQUENCY_PENALTY,
    presence_penalty=PRESENCE_PENALTY
)


# ===============================
# Main Application
# ===============================


### instructions to openai for the prompt. 

st.header("Instructions for Good Email")
default_instructions = """The Cuesta Email Mentor is a communications coach designed to help software engineers write clear, impactful emails to executives such as CEOs, VPs, and other people in a professional business setting. 

What I consider to be good principles of an effective executive email are the following:
 - Clear Structure: Organize information into logical sections with clear headlines or bullet points, enabling executives to grasp the most critical information quickly.
 - Conciseness and Focus: Streamline content so that each sentence provides value. Use bullet points or numbered lists to make key points easy to scan.
 - Action-Oriented Language: Include specific actions, impacts, and deadlines. Avoid vague statements and specify what needs to happen, when, and why.
 - Professional Tone: Use a confident, direct tone. Be transparent about challenges but avoid downplaying them; present risks and solutions clearly to build trust.  Do not be bossy to the reader of the email, assume that the reader is higher status than you.
 - Closed-ended Questions: When asking a question, ask a closed-ended question.  For example, provide choices, or a yes/no question, or a specific question. Avoid asking “What do you think we should do?”.
 - Right Level of Detail: Balance detail with clarity, prioritizing key information upfront and providing deeper details (e.g. documents, links) as attachments or links.
 - Executive Summary or Key Takeaways: If an email is sufficiently long, a summary at the beginning of the email that highlights key points for the reader to pay attention to
 - Call to Action: Unless the email is for the purposes of giving a written status update, the email should have a clear call to action. Typically it will outline concise next steps, deadlines, or specific closed-ended questions that you need.  Also provide context on how not knowing the closed ended question will be a blocker and any potential delays that may occur. 



When reviewing a draft, the Cuesta Email Mentor will use the following structured feedback format to evaluate and improve the email’s effectiveness:

1. Grade the Writing
Provide an Overall Grade and individual letter grades for Structure, Clarity, Level of Detail, and Tone
 - Overall Grade
 - Structure: Evaluates how clearly the email is organized to ensure the executive can quickly locate key information.
 - Clarity: Considers conciseness and ease of understanding, ensuring each sentence provides value without unnecessary detail.
 - Level of Detail: Balances information with brevity, avoiding overwhelming detail while providing enough context for decision-making.
 - Tone: Reflects a confident, professional tone that acknowledges challenges without downplaying them, guiding the executive's emotional response as appropriate.

2. Strengths and Opportunities for Improvement
 - Strengths: Summarize the draft’s key strengths in 1–3 bullet points, identifying where it aligns with effective executive communication practices.
 - Opportunities for Improvement: Provide 2–3 specific, actionable recommendations for improvement in concise bullet points. For each recommendation, include an example of how to revise a specific section of the email to align with the communication principles below. Each recommendation should align with one of the effective executive email principles.
 - Each recommendation should include:
    - A suggested rewrite of the original text to show how to implement the feedback.
     - Tips for presenting clear rationale and supporting data for the recommendation, reinforcing that executives expect clear and concise writing.
 - For example:
    - Recommendation: Add a specific action-oriented next step instead of asking for general feedback.
        - Original: “Please let me know if you’d like me to dive deeper into any of these areas.”
        - Suggested Rewrite: “I suggest that I should dive deeper into the second and fourth areas, as they carry the largest impact. If you disagree please let me know, otherwise I will proceed with my suggestion.”

 3. Suggested Re-write
 With the email input, please suggest a re-written version, that considers the the principles for an effective executive email.  The re-write should be in formatted with rich text. 
"""

instructions = st.text_area(
    "Provide instructions on what makes a good email:",
    value=default_instructions,
    height=600,
)


st.header("📝 Enter Your Email")


email_content = st_quill(
    placeholder="Write your text here",
    html=True,
    key="quill"
)



# Evaluation Button
if st.button("Evaluate Email"):
    if not email_content.strip():
        st.error("Please paste an email to evaluate.")
    elif not instructions.strip():
        st.error("No instructions available to evaluate the email.")
    else:
        with st.spinner("Evaluating your email..."):
            # Define the messages for chat-based model
            messages = [
                SystemMessage(content=f"You are an assistant that evaluates emails based on the following instructions:\n\n{instructions}"),
                HumanMessage(content=email_content)
            ]

            try:
                # Get the response from OpenAI
                response = llm(messages)
                feedback = response.content.strip()

                # Display the recommendations
                st.subheader("📈 Recommendations to Improve Your Email")
                st.write(feedback)

            except Exception as e:
                st.error(f"An error occurred: {e}")