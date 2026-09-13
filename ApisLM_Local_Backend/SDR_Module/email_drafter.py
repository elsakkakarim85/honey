import os
from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate

# Load the local quantized GGUF model for zero-cost drafting
GGUF_PATH = "../../ApisLM_Local_AI/ApisLM-3B-Mobile.gguf"

print("Loading local ApisLM GGUF model for B2B Sales Drafting...")
local_llm = LlamaCpp(
    model_path=GGUF_PATH if os.path.exists(GGUF_PATH) else "dummy.gguf",
    temperature=0.7,
    max_tokens=800,
    n_ctx=2048,
    top_p=0.9,
    verbose=False
)

def draft_b2b_email(lead_data: dict, language: str = "English"):
    """
    Autonomously generates a highly personalized B2B outreach email
    using the local LLM.
    """
    print(f"Drafting personalized {language} email for {lead_data['company_name']}...")
    
    prompt = PromptTemplate.from_template(
        """You are a professional B2B Sales Executive for ApisLM, a premium smart-apiary.
Write a highly personalized, compelling outreach email in {language} to a potential buyer.

Company Info:
Name: {company_name}
Focus Area: {focus_area}
Country: {country}

Key Selling Points to include:
1. Our honey is traced immutably on the Polygon Blockchain via a GS1 Digital Product Passport (DPP).
2. Monitored by Edge AI sensors ensuring strict HACCP quality and zero chemical contamination.
3. Suggest a brief introductory call.

Subject Line: <write a catchy subject>
Body:
"""
    )
    
    chain = prompt | local_llm
    
    try:
        # Simulated execution for safety if model isn't actually present during script run
        draft = chain.invoke({
            "language": language,
            "company_name": lead_data["company_name"],
            "focus_area": lead_data["focus_area"],
            "country": lead_data["country"]
        })
    except Exception as e:
        draft = f"Subject: Premium AI-Verified Honey for {lead_data['company_name']}\n\nDear Purchasing Team,\n\n(Simulated Draft - LlamaCpp Model not found in path)..."
        
    return draft

if __name__ == "__main__":
    sample_lead = {
        "company_name": "Desert Gold Organic Foods",
        "focus_area": "Organic Honey & Natural Sweeteners",
        "country": "UAE"
    }
    email_content = draft_b2b_email(sample_lead, "Arabic")
    print("\n--- Generated Draft ---")
    print(email_content)
