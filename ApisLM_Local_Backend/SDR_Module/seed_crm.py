from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from local_crm_sender import Lead, Base
import random

def seed_database():
    engine = create_engine('sqlite:///local_erp.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    mock_leads = [
        {"company": "Dubai Golden Sweets", "focus": "Premium Organic Honey", "country": "UAE", "email": "purchasing@dubaigoldensweets.com"},
        {"company": "Berlin Organic Co.", "focus": "Raw Forest Honey", "country": "Germany", "email": "sourcing@berlinorganic.de"},
        {"company": "London Artisan Bakes", "focus": "Bulk Baking Honey", "country": "UK", "email": "ingredients@londonartisan.co.uk"},
        {"company": "Tokyo Matcha House", "focus": "Acacia Honey Blends", "country": "Japan", "email": "procurement@tokyomatcha.jp"},
        {"company": "New York Wellness Apothecary", "focus": "Medicinal Grade Honey", "country": "USA", "email": "vendor@nywellness.com"},
    ]

    print("Seeding CRM Database with mock leads...")
    
    for l in mock_leads:
        existing = session.query(Lead).filter_by(company_name=l["company"]).first()
        if not existing:
            new_lead = Lead(
                apiary_id="tenant_alpha_01",
                company_name=l["company"],
                email=l["email"],
                focus_area=l["focus"],
                country=l["country"],
                status="New"
            )
            session.add(new_lead)
            
    session.commit()
    print("CRM Seeding Complete! AI SDR has new targets.")

if __name__ == "__main__":
    seed_database()
