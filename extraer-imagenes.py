import fitz  # PyMuPDF

def extraer_imagenes_de_pdf(ruta_pdf, carpeta_destino):
    # Abrir el documento PDF
    documento = fitz.open(ruta_pdf)
    
    # Recorrer cada página del documento
    for pagina_num in range(len(documento)):
        pagina = documento.load_page(pagina_num)
        lista_imagenes = pagina.get_images(full=True)
        
        # Si hay imágenes en la página
        if lista_imagenes:
            for img_index, img in enumerate(lista_imagenes):
                xref = img[0]  # Referencia de la imagen
                imagen_base = documento.extract_image(xref)
                imagen_bytes = imagen_base["image"]
                extension = imagen_base["ext"]
                
                # Guardar la imagen en la carpeta de destino
                with open(f"{carpeta_destino}/pagina_{pagina_num + 1}_imagen_{img_index + 1}.{extension}", "wb") as img_file:
                    img_file.write(imagen_bytes)
                    print(f"Imagen guardada: pagina_{pagina_num + 1}_imagen_{img_index + 1}.{extension}")

# Llamar a la función con la ruta de tu PDF y la carpeta de destino
extraer_imagenes_de_pdf("Documentos.pdf", "imagenes_extraidas")