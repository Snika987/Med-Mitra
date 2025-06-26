import streamlit as st

# Set page configuration
st.set_page_config(page_title="Med-Mitra Clinical Assistant", layout="centered")

# Hide sidebar navigation (optional)
st.markdown("""
    <style>
        section[data-testid="stSidebarNav"] ul {
            display: none;
        }
        [data-testid="stSidebarNav"] > div:first-child {
            display: none;
        }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Main title
st.title("Med-Mitra Clinical Insight Assistant")

# Welcome message
st.markdown("""
<div style='padding: 1rem 0; font-size: 1.1rem; line-height: 1.6;'>
Welcome to <strong>Med-Mitra</strong>, your AI-powered assistant designed for modern clinical workflows.

This platform helps doctors and healthcare providers streamline patient evaluations with smart, structured insights.

<hr style='margin: 1.5rem 0;'>

<h4 style='margin-bottom: 0.8rem;'>What You Can Do:</h4>

<ul style='margin-left: 1rem;'>
<li><strong>Create Patient Records</strong> with summaries, lab reports (CSV/PDF) and radiology images</li>
<li><strong>Receive Structured Insights</strong> including SOAP notes, diagnoses, treatment plans and interpretation summaries</li>
<li><strong>Access and Export Cases</strong> using Case ID or Patient ID</li>
</ul>

<hr style='margin: 1.5rem 0;'>

Built to enhance decision-making, reduce cognitive load and save time at the point of care.
</div>
""", unsafe_allow_html=True)
