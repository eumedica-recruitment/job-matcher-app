import streamlit as st
import pdfplumber
import re
import pandas as pd
from fuzzywuzzy import fuzz

# Funktion zum Extrahieren von Text aus PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

# Funktion zum Extrahieren relevanter Informationen aus dem CV
def parse_cv(cv_text):
    skills_match = re.findall(r"\b(Skills|Expertise|Technologies):?\s*([\w, ]+)\b", cv_text, re.IGNORECASE)
    experience_match = re.findall(r"\b(Experience|Work History):?\s*([\w, ]+)\b", cv_text, re.IGNORECASE)
    skills = [skill[1] for skill in skills_match] if skills_match else []
    experience = [exp[1] for exp in experience_match] if experience_match else []
    return {"skills": skills, "experience": experience}

# Funktion zur Jobsuche (Dummy-Daten)
def fetch_job_listings():
    return [
        {"title": "Software Engineer", "skills": "Python, AI, Machine Learning", "location": "Zürich"},
        {"title": "Data Scientist", "skills": "Python, SQL, Data Analysis", "location": "Remote"},
        {"title": "Project Manager", "skills": "Agile, Scrum, Leadership", "location": "Genf"}
    ]

# Funktion zur Bewertung des Matches
def rate_match(cv_data, job):
    skill_match = max([fuzz.partial_ratio(cv_skill, job["skills"]) for cv_skill in cv_data["skills"]], default=0)
    experience_match = max([fuzz.partial_ratio(cv_exp, job["skills"]) for cv_exp in cv_data["experience"]], default=0)
    return (skill_match + experience_match) / 2

# Streamlit Web-App
st.title("Job Matching basierend auf Lebenslauf")
uploaded_file = st.file_uploader("Lade deinen Lebenslauf (PDF) hoch", type="pdf")

if uploaded_file is not None:
    cv_text = extract_text_from_pdf(uploaded_file)
    cv_data = parse_cv(cv_text)
    job_listings = fetch_job_listings()
    
    matches = []
    for job in job_listings:
        score = rate_match(cv_data, job)
        matches.append({"Job Titel": job["title"], "Ort": job["location"], "Match Score": f"{score:.2f}%"})
    
    df = pd.DataFrame(matches)
    st.write("### Beste Job-Matches:")
    st.dataframe(df)
