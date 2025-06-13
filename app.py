import streamlit as st
from PIL import Image
from io import BytesIO
from fpdf import FPDF
import base64

st.set_page_config(page_title="Marketing-Profil Generator", layout="wide")
st.title("Marketing‑Profil Generator (Beta)")

st.header("🖌️ Grafik & CI")
company_name = st.text_input("Unternehmensname")
logo_file = st.file_uploader("Logo hochladen", type=["png","jpg","jpeg"])
signet_file = st.file_uploader("Signet hochladen", type=["png","jpg","jpeg"])
main_color = st.color_picker("Grundfarbe", "#2A9DF4")
second_color = st.color_picker("Zweitfarbe", "#CCCCCC")

st.header("👥 Ansprechpartner (bis 5)")
contacts = []
for i in range(5):
    with st.expander(f"Person {i+1}", expanded=(i==0)):
        head = st.text_input(f"Bereichsleitung {i+1}", key=f"head_{i}")
        marketing = st.text_input(f"Marketingverantwortlicher {i+1}", key=f"marketing_{i}")
        content = st.text_input(f"Contentverantwortlicher {i+1}", key=f"content_{i}")
        if head or marketing or content:
            contacts.append((head, marketing, content))

st.header("📤 PDF-Export")
file_name = st.text_input("Dateiname (ohne .pdf)", value="marketing_profil")
generate = st.button("PDF generieren")
reset = st.button("Formular zurücksetzen")

if reset:
    st.experimental_rerun()

if generate:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_fill_color(*Image.new("RGB", (1,1), main_color).getpixel((0,0)))
    pdf.rect(0, 0, 210, 20, "F")

    if logo_file:
        logo = Image.open(logo_file)
        logo.save("logo_tmp.png")
        pdf.image("logo_tmp.png", x=10, y=5, w=30)

    if signet_file:
        signet = Image.open(signet_file)
        signet.save("signet_tmp.png")
        pdf.image("signet_tmp.png", x=170, y=5, w=30)

    pdf.set_text_color(255,255,255)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 15, company_name, ln=True, align="C")
    pdf.ln(12)

    pdf.set_text_color(0,0,0)
    pdf.set_fill_color(*Image.new("RGB", (1,1), second_color).getpixel((0,0)))
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Ansprechpartner", ln=True, fill=True)
    pdf.set_font("Arial", "", 10)
    for idx,(h,m,c) in enumerate(contacts):
        pdf.cell(0, 8, f"{idx+1}. Leitung: {h} | Marketing: {m} | Content: {c}", ln=True)

    pdf_data = pdf.output(dest='S').encode('latin1')
    st.success("✅ PDF generiert")
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{file_name}.pdf">Download 📄</a>'
    st.markdown(href, unsafe_allow_html=True)
