from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def generate_pdf(data: dict) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    def add_section(title, content):
        elements.append(Paragraph(f"<b>{title}</b>", styles["Heading3"]))
        if not content:
            elements.append(Paragraph("No data available.", styles["Normal"]))
        elif isinstance(content, list):
            for idx, item in enumerate(content, 1):
                if isinstance(item, dict):
                    elements.append(Paragraph(f"<b>Entry {idx}:</b>", styles["Normal"]))
                    for k, v in item.items():
                        elements.append(Paragraph(f"{k}: {v}", styles["Normal"]))
                    elements.append(Spacer(1, 8))
                else:
                    elements.append(Paragraph(str(item), styles["Normal"]))
        elif isinstance(content, dict):
            for k, v in content.items():
                elements.append(Paragraph(f"{k}: {v}", styles["Normal"]))
        else:
            elements.append(Paragraph(str(content), styles["Normal"]))
        elements.append(Spacer(1, 12))

    # Header
    elements.append(Paragraph("Med-Mitra Clinical Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Patient Name: {data.get('patient_name', 'N/A')}", styles["Normal"]))
    elements.append(Paragraph(f"Patient ID: {data.get('patient_id', 'N/A')}", styles["Normal"]))
    elements.append(Paragraph(f"Case ID: {data.get('case_id', 'N/A')}", styles["Normal"]))
    elements.append(Paragraph(f"Confidence: {data.get('confidence', 'N/A')}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Sections
    add_section("Summary", data.get("summary"))
    add_section("SOAP Note", data.get("soap"))
    add_section("Diagnoses", data.get("diagnoses"))
    add_section("Investigations", data.get("investigations"))
    add_section("Treatment", data.get("treatment"))

    interp = data.get("interpretations", {})
    add_section("Interpretation: Lab Results", interp.get("lab_results"))
    add_section("Interpretation: Radiology", interp.get("radiology"))

    # Build PDF
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
