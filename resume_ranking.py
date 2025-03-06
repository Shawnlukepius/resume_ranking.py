from os import renames
import pdb
from xml.dom.minidom import Document
import streamlit as st
from PyPDF2 import PdfReader 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file) 
    text = ""
    for page in pdf_reader.pages: 
        text += page.extract_text() + "\n"
    return text


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_resumes(job_description, resumes):
    vectorizer = TfidfVectorizer()
    all_texts = [job_description] + resumes
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    job_vec = tfidf_matrix[0]  
    resume_vecs = tfidf_matrix[1:] 
    
    scores = cosine_similarity(job_vec, resume_vecs).flatten()
    return scores

if __name__ == "__main__":
    
    st.title("AI Resume Screening & Candidate Ranking System")
    st.header("Job Description")
    job_description = st.text_area("Enter the job description")

    st.header("Upload Resumes")
    uploaded_files = st.file_uploader("Upload PDF files", type=['pdf'], accept_multiple_files=True)

    if uploaded_files and job_description:
        st.header("Ranking Resumes")
        resumes = []
        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            resumes.append(text)

            scores = rank_resumes(job_description, resumes)
    
            results = pd.DataFrame({"Resume": [file.name for file in uploaded_files], "Score": scores})
            results = results.sort_values(by="Score", ascending=False)
    
            st.write(results)