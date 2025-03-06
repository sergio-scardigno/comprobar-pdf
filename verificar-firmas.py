import sys
import os
from PyPDF2 import PdfReader
from datetime import datetime

def verificar_firmas_basico(ruta_pdf):
    try:
        # Verificar que el archivo existe
        if not os.path.exists(ruta_pdf):
            print(f"Error: El archivo '{ruta_pdf}' no existe.")
            return
            
        # Abrir y leer el PDF
        reader = PdfReader(ruta_pdf)
        
        # Comprobar si el PDF tiene firmas
        if '/AcroForm' in reader.trailer['/Root']:
            acroform = reader.trailer['/Root']['/AcroForm']
            if '/Fields' in acroform:
                fields = acroform['/Fields']
                firmas_encontradas = 0
                
                # Recorrer los campos para encontrar campos de firma
                for i, field_ref in enumerate(fields):
                    field = field_ref.get_object()
                    field_type = field.get('/FT')
                    
                    if field_type == '/Sig':
                        firmas_encontradas += 1
                        print(f"\nFirma {firmas_encontradas}:")
                        
                        # Obtener información del campo de firma
                        if '/V' in field:
                            sig_dict = field['/V']
                            
                            # Nombre del firmante
                            if '/Name' in sig_dict:
                                print(f" - Firmante: {sig_dict['/Name']}")
                            
                            # Fecha de firma
                            if '/M' in sig_dict:
                                fecha_str = sig_dict['/M']
                                if isinstance(fecha_str, str):
                                    # Formato típico: 'D:20220315145021+02\'00\''
                                    fecha_str = fecha_str.replace("D:", "").replace("'", "")
                                    try:
                                        # Intentar parsear el formato básico
                                        fecha_basica = fecha_str[:14]  # YYYYMMDDHHmmss
                                        fecha_formateada = f"{fecha_basica[:4]}-{fecha_basica[4:6]}-{fecha_basica[6:8]} {fecha_basica[8:10]}:{fecha_basica[10:12]}:{fecha_basica[12:14]}"
                                        print(f" - Fecha de firma: {fecha_formateada}")
                                    except:
                                        print(f" - Fecha de firma (sin formato): {fecha_str}")
                            
                            # Información sobre la razón de la firma
                            if '/Reason' in sig_dict:
                                print(f" - Razón: {sig_dict['/Reason']}")
                            
                            # Ubicación
                            if '/Location' in sig_dict:
                                print(f" - Ubicación: {sig_dict['/Location']}")
                            
                            print(" - NOTA: Esta verificación solo detecta la presencia de firmas,")
                            print("   no valida criptográficamente la integridad o autenticidad.")
                
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
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ruta_pdf = "Documentos.pdf"
    if len(sys.argv) > 1:
        ruta_pdf = sys.argv[1]
    verificar_firmas_basico(ruta_pdf)