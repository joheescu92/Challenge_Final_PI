from pydantic import BaseModel
import json
import os

class Metadata_Document(BaseModel):
    file: str
    title: str
    chunks: int
    overlap: int
    description: str


##Creacion de instancias

# # Crear instancias
# cct_76_75 = Metadata_Document(
#     file="ConvenioColectivoTrabajo76-75.pdf",
#     title="Convenio Colectivo de Trabajo 76/75",
#     chunks=1320, #Aproximadamente el tamaño de cada articulo
#     overlap=205,
#     description="La Convencion Colectiva de Trabajo Nº 76/75 establece las condiciones laborales, categorias, y derechos para trabajadores de la construccion en Argentina, con vigencia de 24 meses (12 para cláusulas economicas). Incluye disposiciones sobre jornadas, escalafon, licencias, contratacion a través de la UOCRA y tareas especificas segun especialidad. Regula relaciones entre empleadores y obreros de diversas ramas de la construccion."
# )

# cct_petrolifero_gasifero = Metadata_Document(
#     file="CCT_YacimientosPetroliferos_Gasiferos.pdf",
#     title="Convenio de Trabajadores Constructores en areas petrolíferas y gasíficas cct 545/08",
#     chunks=1020, #Aproximadamente el tamaño de cada articulo
#     overlap=174,
#     description="El convenio regula las condiciones laborales de trabajadores de la construccion en yacimientos petroliferos y gasiferos, abordando tareas especificas como obra civil, montaje, ductos, electricidad y movimiento de suelos. Establece su ambito de aplicacion territorial y actividades comprendidas, garantizando condiciones dignas conforme a la legislacion vigente."
# )

# # Convertir las instancias a una lista de diccionarios
# documents = [cct_76_75.model_dump(), cct_petrolifero_gasifero.model_dump()]

# # Ruta absoluta hacia backend/metadatas/metadata_documents.json
# current_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(current_dir, "..", "metadatas", "metadata_documents.json")
# file_path = os.path.normpath(file_path)

# # Crear el directorio si no existe
# os.makedirs(os.path.dirname(file_path), exist_ok=True)

# # Guardar en el archivo JSON
# with open(file_path, "w") as json_file:
#     json.dump(documents, json_file, indent=2)
#     print(f"Datos guardados en: {file_path}")