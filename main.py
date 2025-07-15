from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os


def get_response(bullets):
    load_dotenv("keys.env")

    if "GROQ_API_KEY" not in os.environ:
        print("No groq api keyyyy")
        return
    if "GOOGLE_API_KEY" not in os.environ:
        print("No gemini api keyyyy")
        return

    # Initialize LLMs
    llm_llama = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.0,
        max_retries=2,
    )
    llm_gemini = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-001",
        temperature=0.0,
        max_retries=2,
    )

    # Prompting strategies
    strategies = {
        "Standard": """
        You are a professional resume builder.
        Rewrite each bullet point using the following rules:
        - Start with a strong action verb (e.g., Led, Designed, Analyzed, Developed, etc.)
        - Include relevant industry keywords based on the given role (e.g., CRM, Agile, SQL, cold outreach, React)
        - Mention measurable achievements when reasonably inferred (e.g., %/ increase, time saved)
        - Keep it concise but informative (around 12-20 words)
        - Use professional, clear language
        - Avoid generic phrases like "responsible for", "helped with", or vague fluff

        Do not add preambles, summaries, or explanations.
        Just return the rewritten bullet points in plain text, line by line.

        Now rewrite the following original bullet points following the above rules:
        {bullets} 
        """,
        "Few-Shot": """
        You are a resume optimization expert.

        Below are examples of weak and improved bullet points:

        Weak: Managed social media  
        Strong: Managed 4 brand social media accounts, increasing engagement by 35% through targeted content campaigns

        Weak: Helped organize files  
        Strong: Organized and digitized 2,000+ records, reducing file retrieval time by 40%

        Now, rewrite the bullet points provided by the user using the same principles:
        - Start with a strong action verb
        - Use job-relevant terms and quantifiable outcomes
        - Be concise and impactful (12-20 words)
        - Avoid fluff or generic phrasing

        Do not add preambles, summaries, or explanations.
        Just return the improved bullet points in plain text, line by line.
        Now rewrite the following original bullet points following the above rules:
        {bullets} 
        """,
        "Recruiter": """
        You are a corporate recruiter reviewing a candidate's resume. You want each bullet point to clearly showcase the candidate's value.

        Your goal is to:
        - Emphasize what the candidate accomplished, not just what they were assigned
        - Use strong action verbs and keywords that recruiters look for
        - Quantify impact where appropriate (e.g., saved time, improved efficiency, increased revenue)
        - Write in a clean, professional tone with no extra words (12-20 words per bullet)
        - Avoid vague phrases like "assisted with" or "responsible for"

        Rephrase each resume bullet provided so it stands out to hiring managers.
        Do not add preambles, summaries, or explanations.
        Just return the rewritten bullet points in plain text, line by line.
        Now rewrite the following original bullet points following the above rules:
        {bullets} 
        """
    }

    # LLMs
    llms = {
        "LLaMA (Groq)": llm_llama,
        "Gemini": llm_gemini
    }

    # Run all combinations
    for strategy_name, system_template in strategies.items():
        for llm_name, llm in llms.items():
            print(f"\n==============================")
            print(f">>> Strategy: {strategy_name} | LLM: {llm_name}")
            print("==============================")

            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_template),
                ("user", "{bullets}")
            ])

            prompt = prompt_template.invoke({"bullets": bullets})
            
            try:
                response = llm.invoke(prompt)
                print(response.content.strip())
            except Exception as e:
                print(f"Error with {strategy_name} | {llm_name}: {e}")

# Input your bullet points here
raw_bullets = """
Scheduled appointments, managed emails and calls for senior leadership.
Provided end-to-end event logistics and meeting support.
Familiarity with audit techniques, processes, and tools.
Proficiency in using GST portals for registration, payment, and return filing.
Extracted, cleaned & integrated multi-source datasets (Insurance Records, Customer Feedback); performed data profiling & executed sentiment analysis via Power Query to deliver customer-centric insights.
Designed & deployed dynamic dashboards using Bar, Line, Ribbon, Donut & Matrix visualizations; implemented Role-Based Security (RLS) & scheduled automated data refresh for real-time, secure reporting.
"""

get_response(raw_bullets)