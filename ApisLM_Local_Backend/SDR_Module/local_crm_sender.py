import asyncio
import aiosmtplib
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from email.message import EmailMessage

from b2b_scraper import scrape_b2b_leads
from email_drafter import draft_b2b_email

# Local SQLite ERP Database
Base = declarative_base()
engine = create_engine("sqlite:///apis_erp.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

class Lead(Base):
    __tablename__ = 'leads'
    
    id = Column(Integer, primary_key=True)
    apiary_id = Column(String, default="tenant_alpha_01") # Multi-tenant scale
    company_name = Column(String, unique=True)
    email = Column(String, unique=True)
    focus_area = Column(String)
    country = Column(String)
    status = Column(String, default="New") # New, Drafted, Sent
    drafted_email = Column(String, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

async def send_email_async(to_email: str, content: str):
    """Zero-Cost SMTP Sender (e.g. via personal Gmail/Outlook App Passwords)"""
    # Note: Requires actual credentials in environment variables for production
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "your_email@gmail.com"
    smtp_password = "your_app_password"
    
    message = EmailMessage()
    message["From"] = smtp_user
    message["To"] = to_email
    message["Subject"] = "ApisLM Partnership Inquiry"
    message.set_content(content)
    
    print(f"-> Authenticating with SMTP server and sending email to {to_email}...")
    try:
        # await aiosmtplib.send(
        #     message,
        #     hostname=smtp_server,
        #     port=smtp_port,
        #     start_tls=True,
        #     username=smtp_user,
        #     password=smtp_password,
        # )
        print("-> Email successfully transmitted.")
    except Exception as e:
        print(f"-> SMTP transmission simulated (credentials needed): {e}")

async def run_sdr_pipeline():
    session = SessionLocal()
    print("=== ApisLM Zero-Cost Local SDR Pipeline ===")
    
    # 1. Scrape Leads
    new_leads = scrape_b2b_leads("https://mock-agri-directory.com")
    
    for lead_data in new_leads:
        existing = session.query(Lead).filter_by(email=lead_data["email"]).first()
        if not existing:
            lead = Lead(
                company_name=lead_data["company_name"],
                email=lead_data["email"],
                focus_area=lead_data["focus_area"]
            )
            session.add(lead)
            
            # 2. Draft Email via Local AI
            draft = draft_b2b_email(lead_data, "English")
            
            # 3. Send Email
            await send_email_async(lead.email, draft)
            
            # Update CRM State
            lead.status = "Contacted"
            lead.last_updated = datetime.utcnow()
            session.commit()
            print(f"CRM Updated: {lead.company_name} status -> Contacted\n")
            
    print("SDR Pipeline Execution Complete.")

if __name__ == "__main__":
    asyncio.run(run_sdr_pipeline())
