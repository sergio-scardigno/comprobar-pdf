# Herramienta Procesador de PDF

## Descripción General

Esta herramienta proporciona funcionalidad para procesar archivos PDF de dos maneras principales:

1. **Verificar Firmas Digitales** - Detecta y muestra información sobre firmas digitales en un documento PDF
2. **Extraer Imágenes** - Extrae todas las imágenes de un documento PDF y las guarda en una carpeta especificada

## Instalación

### Requisitos Previos

-   Python 3.6 o superior
-   pip (instalador de paquetes de Python)

### Configuración

1. Clona o descarga este repositorio en tu máquina local
2. Crea y activa un entorno virtual (recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
3. Instala las dependencias requeridas:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

### Uso Básico

```bash
python procesar.py [ruta_pdf] [carpeta_imagenes]
```

Donde:

-   `ruta_pdf` (opcional): Ruta al archivo PDF a procesar (predeterminado: "Documentos.pdf")
-   `carpeta_imagenes` (opcional): Directorio donde se guardarán las imágenes extraídas (predeterminado: "imagenes_extraidas")

### Ejemplos

```bash
# Procesar archivo PDF predeterminado (Documentos.pdf)
python procesar.py

# Procesar un archivo PDF específico
python procesar.py mi_archivo.pdf

# Procesar un archivo PDF específico y guardar imágenes en un directorio personalizado
python procesar.py mi_archivo.pdf imagenes_guardadas
```

## Características

### Verificación de Firma Digital

La herramienta analiza el PDF en busca de campos de firma digital y muestra:

-   Número de firmas encontradas
-   Para cada firma:
    -   Nombre del firmante
    -   Fecha y hora de la firma
    -   Razón de la firma (si está disponible)
    -   Ubicación de la firma (si está disponible)

**Nota**: Esta verificación solo detecta la presencia de campos de firma y sus metadatos. No valida criptográficamente la integridad o autenticidad de las firmas.

### Extracción de Imágenes

La herramienta extrae todas las imágenes incrustadas en el PDF:

-   Crea el directorio de salida si no existe
-   Procesa cada página del documento
-   Extrae imágenes con su formato original (jpg, png, etc.)
-   Nombra los archivos utilizando el patrón: `pagina_X_imagen_Y.ext`

## Solución de Problemas

### ModuleNotFoundError: No module named 'fitz'

Si encuentras este error, significa que la biblioteca PyMuPDF no está instalada. Ejecuta:

```bash
pip install PyMuPDF
```

### Archivo No Encontrado

Si recibes un error sobre que el archivo PDF no existe, verifica que:

-   La ruta del archivo sea correcta
-   Tengas los permisos necesarios para acceder al archivo
-   El nombre del archivo no contenga caracteres especiales que necesiten escape

## Dependencias

-   **PyPDF2**: Utilizado para analizar PDF y detectar firmas
-   **PyMuPDF** (importado como 'fitz'): Utilizado para la extracción de imágenes
