import streamlit as st
import requests

API_URL = "http://localhost:8000/upload/"

st.title("Subir PDF y Extraer Información")

uploaded_file = st.file_uploader("Sube un archivo PDF", type=["pdf"])

if uploaded_file is not None:
    st.write("Archivo cargado:", uploaded_file.name)

    if st.button("Procesar PDF"):
        with st.spinner("Procesando..."):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(API_URL, files=files)

            if response.status_code == 200:
                data = response.json()
                st.success("✅ Archivo procesado correctamente")

                st.subheader("Firmas Encontradas:")
                for firma in data.get("firmas", []):
                    st.write(f"👤 **Firmante:** {firma.get('firmante', 'Desconocido')}")
                    st.write(f"📅 **Fecha:** {firma.get('fecha', 'Desconocida')}")
                    st.write(f"📝 **Razón:** {firma.get('razon', 'No especificada')}")
                    st.write(f"📍 **Ubicación:** {firma.get('ubicacion', 'No especificada')}")
                    st.write("---")

                st.subheader("Imágenes Extraídas:")
                for img_path in data.get("imagenes", []):
                    st.image(img_path, caption=img_path, use_column_width=True)

            else:
                st.error("⚠ Error al procesar el archivo")
