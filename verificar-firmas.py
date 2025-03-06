from endesive import pdf

def verificar_firmas_digitales(ruta_pdf):
    # Abrir el documento PDF
    with open(ruta_pdf, "rb") as archivo:
        # Leer el contenido del PDF
        contenido = archivo.read()
        
        # Verificar las firmas digitales
        firmas = pdf.verify(contenido)
        
        # Mostrar resultados
        if firmas:
            print(f"Se encontraron {len(firmas)} firmas digitales en el documento:")
            for i, firma in enumerate(firmas, start=1):
                print(f"\nFirma {i}:")
                print(f"  - Válida: {'Sí' if firma['valid'] else 'No'}")
                print(f"  - Fecha de firma: {firma['timestamp']}")
                print(f"  - Certificado: {firma['signer_certificate']}")
        else:
            print("No se encontraron firmas digitales en el documento.")

# Llamar a la función con la ruta de tu PDF
verificar_firmas_digitales("Documentos.pdf")