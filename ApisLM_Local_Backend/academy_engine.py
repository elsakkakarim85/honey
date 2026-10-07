import json
import base64
from typing import List, Optional
from pydantic import BaseModel, Field
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

# --- Adaptive Curriculum Pydantic Schemas ---

class QuizOption(BaseModel):
    id: str
    text: str
    is_correct: bool
    explanation: str

class QuizQuestion(BaseModel):
    question: str
    options: List[QuizOption]

class CourseChapter(BaseModel):
    title: str
    markdown_content: str
    svg_diagram_b64: Optional[str] = None
    audio_script: str
    quiz: List[QuizQuestion]

class AdaptiveSyllabus(BaseModel):
    course_title: str
    target_role: str
    difficulty_level: str
    chapters: List[CourseChapter]

# --- Zero-Cost Certification System ---

def generate_certificate(user_name: str, course_name: str, private_key_path: str = "../.apiary_private_key.pem"):
    """
    Generates a PDF certificate and cryptographically signs it 
    using the Zero-Gas Ed25519 DPP keys.
    """
    pdf_path = f"certificate_{user_name.replace(' ', '_')}.pdf"
    
    # 1. Generate PDF via ReportLab
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 600, "ApisLM Omnimodal Academy")
    c.setFont("Helvetica", 18)
    c.drawString(100, 550, f"Certificate of Completion: {course_name}")
    c.drawString(100, 500, f"Awarded to: {user_name}")
    c.drawString(100, 450, "Status: Master Beekeeper / Factory Manager")
    c.save()
    
    # 2. Cryptographically Sign the Certificate (Zero-Gas DPP)
    try:
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
            
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
            
        signature = private_key.sign(pdf_data)
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        print(f"Certificate cryptographically signed. Ed25519 Signature: {signature_b64}")
        return pdf_path, signature_b64
    except Exception as e:
        print(f"Error signing certificate: {e}")
        return pdf_path, None

# --- Curriculum Generation Engine (Mock logic for local GGUF) ---

def generate_course(role: str, topic: str) -> AdaptiveSyllabus:
    """
    Instructs the local ApisLM GGUF model to output structured JSON 
    matching the AdaptiveSyllabus Pydantic schema.
    """
    print(f"Loading local LLaMA-3 GGUF... Generating {topic} course for {role}")
    # Simulated model response adhering strictly to the schema
    mock_syllabus = {
        "course_title": f"Advanced {topic}",
        "target_role": role,
        "difficulty_level": "Expert",
        "chapters": [
            {
                "title": "Module 1: Fundamentals",
                "markdown_content": "# Overview\nBees are essential...",
                "audio_script": "Welcome to module one. Today we discuss the fundamentals.",
                "quiz": [
                    {
                        "question": "What is the optimal brood temperature?",
                        "options": [
                            {"id": "a", "text": "30 C", "is_correct": False, "explanation": "Too cold."},
                            {"id": "b", "text": "35 C", "is_correct": True, "explanation": "Correct. 34.5 to 35.5 is optimal."}
                        ]
                    }
                ]
            }
        ]
    }
    return AdaptiveSyllabus(**mock_syllabus)

if __name__ == "__main__":
    syllabus = generate_course("Commercial Beekeeper", "Varroa Mite Management")
    print(syllabus.json(indent=2))
