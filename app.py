from fastapi import FastAPI, File, UploadFile
import os
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
import shutil

app = FastAPI()

UPLOAD_DIR = "uploads"
IMAGES_DIR = "extracted_images"

# Asegurar carpetas de almacenamiento
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "API funcionando. Usa /upload/ para subir un PDF."}

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Guardar el archivo temporalmente
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extraer imágenes
    images = extraer_imagenes_de_pdf(file_path, IMAGES_DIR)

    # Verificar firmas
    firmas = verificar_firmas_basico(file_path)

    return {"message": "Archivo procesado", "firmas": firmas, "imagenes": images}


def verificar_firmas_basico(ruta_pdf):
    try:
        reader = PdfReader(ruta_pdf)
        firmas = []

        if '/AcroForm' in reader.trailer['/Root']:
            acroform = reader.trailer['/Root']['/AcroForm']
            if '/Fields' in acroform:
                for field_ref in acroform['/Fields']:
                    field = field_ref.get_object()
                    if field.get('/FT') == '/Sig' and '/V' in field:
                        sig_dict = field['/V']
                        firma_info = {
                            "firmante": sig_dict.get('/Name', "Desconocido"),
                            "fecha": sig_dict.get('/M', "Desconocida").replace("D:", "").replace("'", ""),
                            "razon": sig_dict.get('/Reason', "No especificada"),
                            "ubicacion": sig_dict.get('/Location', "No especificada"),
                        }
                        firmas.append(firma_info)

        return firmas if firmas else ["No se encontraron firmas digitales"]
    
    except Exception as e:
        return {"error": str(e)}


def extraer_imagenes_de_pdf(ruta_pdf, carpeta_destino):
    try:
        documento = fitz.open(ruta_pdf)
        imagenes_extraidas = []

        for pagina_num in range(len(documento)):
            pagina = documento.load_page(pagina_num)
            lista_imagenes = pagina.get_images(full=True)

            for img_index, img in enumerate(lista_imagenes):
                xref = img[0]
                imagen_base = documento.extract_image(xref)
                imagen_bytes = imagen_base["image"]
                extension = imagen_base["ext"]

                imagen_path = os.path.join(carpeta_destino, f"pagina_{pagina_num + 1}_imagen_{img_index + 1}.{extension}")
                with open(imagen_path, "wb") as img_file:
                    img_file.write(imagen_bytes)
                
                imagenes_extraidas.append(imagen_path)

        return imagenes_extraidas if imagenes_extraidas else ["No se encontraron imágenes"]
    
    except Exception as e:
        return {"error": str(e)}


