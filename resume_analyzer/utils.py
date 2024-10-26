import google.generativeai as genai
from django.conf import settings
from PyPDF2 import PdfReader
from docx import Document

def analyze_resume(file_path, job_role):
    print("Inside analyze_resume function")  # Confirm function call
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    # File ko read karte waqt bhi print karo
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        print("PDF content length:", len(text))  # Debug statement
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        print("DOCX content length:", len(text))  # Debug statement
    else:
        print("Unsupported file format")  # Debug statement for unsupported format
        return "Unsupported file format"

    # Gemini analysis ke liye prompt
    prompt = f"""
    Analyze this resume for a {job_role} position:
    {text}

    Provide:
    1. Current skills mentioned
    2. Missing important skills
    3. Suggestions for improvement
    4. Overall assessment
    """
    
    response = model.generate_content(prompt)
    print("Analysis response:", response)  # Debug statement to see response
    return response.text