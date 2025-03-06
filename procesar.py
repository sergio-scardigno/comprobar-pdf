import sys
import os
import traceback
from datetime import datetime
import fitz  # PyMuPDF


# Function to verify signatures in PDF
def verificar_firmas_basico(ruta_pdf):
    try:
        # Verify that the file exists
        if not os.path.exists(ruta_pdf):
            print(f"Error: El archivo '{ruta_pdf}' no existe.")
            return
            
        # Open and read the PDF
        from PyPDF2 import PdfReader
        reader = PdfReader(ruta_pdf)
        
        # Check if the PDF has signatures
        if '/AcroForm' in reader.trailer['/Root']:
            acroform = reader.trailer['/Root']['/AcroForm']
            if '/Fields' in acroform:
                fields = acroform['/Fields']
                firmas_encontradas = 0
                
                # Loop through fields to find signature fields
                for i, field_ref in enumerate(fields):
                    field = field_ref.get_object()
                    field_type = field.get('/FT')
                    if field_type == '/Sig':
                        firmas_encontradas += 1
                        print(f"\nFirma {firmas_encontradas}:")
                        
                        # Get signature field information
                        if '/V' in field:
                            sig_dict = field['/V']
                            
                            # Signer name
                            if '/Name' in sig_dict:
                                print(f" - Firmante: {sig_dict['/Name']}")
                                
                            # Signature date
                            if '/M' in sig_dict:
                                fecha_str = sig_dict['/M']
                                if isinstance(fecha_str, str):
                                    # Typical format: 'D:20220315145021+02\'00\''
                                    fecha_str = fecha_str.replace("D:", "").replace("'", "")
                                    try:
                                        # Try to parse the basic format
                                        fecha_basica = fecha_str[:14]  # YYYYMMDDHHmmss
                                        fecha_formateada = f"{fecha_basica[:4]}-{fecha_basica[4:6]}-{fecha_basica[6:8]} {fecha_basica[8:10]}:{fecha_basica[10:12]}:{fecha_basica[12:14]}"
                                        print(f" - Fecha de firma: {fecha_formateada}")
                                    except:
                                        print(f" - Fecha de firma (sin formato): {fecha_str}")
                                        
                            # Signature reason information
                            if '/Reason' in sig_dict:
                                print(f" - Razón: {sig_dict['/Reason']}")
                                
                            # Location
                            if '/Location' in sig_dict:
                                print(f" - Ubicación: {sig_dict['/Location']}")
                
                print(" - NOTA: Esta verificación solo detecta la presencia de firmas,")
                print(" no valida criptográficamente la integridad o autenticidad.")
                
                if firmas_encontradas == 0:
                    print("No se encontraron campos de firma en el documento.")
                else:
                    print(f"\nTotal de firmas encontradas: {firmas_encontradas}")
            else:
                print("No se encontraron campos en el formulario AcroForm.")
        else:
            print("No se encontró estructura AcroForm. El documento probablemente no tiene firmas digitales.")
    
    except Exception as e:
        print(f"Error al procesar el PDF: {str(e)}")
        traceback.print_exc()

# Function to extract images from PDF
def extraer_imagenes_de_pdf(ruta_pdf, carpeta_destino):
    try:
        # Create destination folder if it doesn't exist
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)
            print(f"Se creó la carpeta: {carpeta_destino}")
            
        # Open the PDF document
        # import fitz  # PyMuPDF
        documento = fitz.open(ruta_pdf)
        
        # Loop through each page of the document
        for pagina_num in range(len(documento)):
            pagina = documento.load_page(pagina_num)
            lista_imagenes = pagina.get_images(full=True)
            
            # If there are images on the page
            if lista_imagenes:
                for img_index, img in enumerate(lista_imagenes):
                    xref = img[0]  # Image reference
                    imagen_base = documento.extract_image(xref)
                    imagen_bytes = imagen_base["image"]
                    extension = imagen_base["ext"]
                    
                    # Save the image to the destination folder
                    imagen_path = f"{carpeta_destino}/pagina_{pagina_num + 1}_imagen_{img_index + 1}.{extension}"
                    with open(imagen_path, "wb") as img_file:
                        img_file.write(imagen_bytes)
                    print(f"Imagen guardada: {imagen_path}")
        
        print(f"\nProceso completo. Imágenes extraídas: {carpeta_destino}")
        
    except Exception as e:
        print(f"Error al extraer imágenes: {str(e)}")
        traceback.print_exc()

def main():
    # Default values
    ruta_pdf = "Documentos.pdf"
    carpeta_imagenes = "imagenes_extraidas"
    
    # Process command line arguments
    if len(sys.argv) > 1:
        ruta_pdf = sys.argv[1]
    if len(sys.argv) > 2:
        carpeta_imagenes = sys.argv[2]
    
    # Run both functions
    print("=== VERIFICACIÓN DE FIRMAS DIGITALES ===")
    verificar_firmas_basico(ruta_pdf)
    
    print("\n=== EXTRACCIÓN DE IMÁGENES ===")
    extraer_imagenes_de_pdf(ruta_pdf, carpeta_imagenes)

if __name__ == "__main__":
    main()