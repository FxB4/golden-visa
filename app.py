# app.py
import os
import PyPDF2
import docx
import streamlit as st

# Set criteria for Golden Visa eligibility
criteria = {
    "academic_achievements": "Demonstrating exceptional academic achievements and innovative contributions to education.",
    "raising_quality": "Proven success in raising the quality of education at their institutions.",
    "community_impact": "Creating a positive impact and recognition from the wider educational community.",
    "student_outcomes": "Proven contributions to improving student outcomes, including academic progress and qualifications."
}

# Function to process PDF documents and extract text
def extract_text_from_pdf(file_path):
    reader = PyPDF2.PdfReader(file_path)
    text = ''.join([page.extract_text() for page in reader.pages])
    return text

# Function to process DOCX documents and extract text
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

# Function to check eligibility based on extracted text
def check_eligibility(text):
    results = {}
    reasons = []

    # Check for each criteria
    if "exceptional academic achievements" in text.lower():
        results['academic_achievements'] = True
    else:
        results['academic_achievements'] = False
        reasons.append(criteria["academic_achievements"])

    if "raising quality of education" in text.lower():
        results['raising_quality'] = True
    else:
        results['raising_quality'] = False
        reasons.append(criteria["raising_quality"])

    if "positive impact" in text.lower():
        results['community_impact'] = True
    else:
        results['community_impact'] = False
        reasons.append(criteria["community_impact"])

    if "improving student outcomes" in text.lower():
        results['student_outcomes'] = True
    else:
        results['student_outcomes'] = False
        reasons.append(criteria["student_outcomes"])

    # Determine overall eligibility
    eligible = all(results.values())
    
    return eligible, reasons

# Streamlit UI for the app
def main():
    st.title('Golden Visa Eligibility Checker for Educators')

    st.write("""
    Upload a single document (PDF or DOCX) to check eligibility for the Golden Visa based on academic achievements, contributions to education, and student outcomes.
    """)
    
    # Upload a single document
    uploaded_file = st.file_uploader("Upload your document", type=['pdf', 'docx'])
    
    if uploaded_file is not None:
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        if file_extension == '.pdf':
            text = extract_text_from_pdf(uploaded_file)
        elif file_extension == '.docx':
            text = extract_text_from_docx(uploaded_file)
        else:
            st.error("Unsupported file format")
            return

        # Check eligibility
        eligible, reasons = check_eligibility(text)

        # Display the results
        if eligible:
            st.success("The teacher is eligible for the Golden Visa!")
        else:
            st.error("The teacher is not eligible for the Golden Visa.")
            st.write("Reasons for ineligibility:")
            for reason in reasons:
                st.write(f"- {reason}")

if __name__ == "__main__":
    main()
