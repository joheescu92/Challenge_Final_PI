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

# Crear instancias
cct_76_75 = Metadata_Document(
    file="ConvenioColectivoTrabajo76-75.pdf",
    title="Convenio Colectivo de Trabajo 76/75",
    chunks=507, #Aproximadamente el tamaño de cada articulo
    overlap=79,
    description="La Convención Colectiva de Trabajo Nº 76/75 establece las condiciones laborales, categorías, y derechos para trabajadores de la construcción en Argentina, con vigencia de 24 meses (12 para cláusulas económicas). Incluye disposiciones sobre jornadas, escalafón, licencias, contratación a través de la UOCRA y tareas específicas según especialidad. Regula relaciones entre empleadores y obreros de diversas ramas de la construcción."
)

cct_petrolifero_gasifero = Metadata_Document(
    file="CCT_YacimientosPetroliferos_Gasiferos.pdf",
    title="Convenio de Trabajadores Constructores en areas petrolíferas y gasíficas cct 545/08",
    chunks=476, #Aproximadamente el tamaño de cada articulo
    overlap=70,
    description="El convenio regula las condiciones laborales de trabajadores de la construcción en yacimientos petrolíferos y gasíferos, abordando tareas específicas como obra civil, montaje, ductos, electricidad y movimiento de suelos. Establece su ámbito de aplicación territorial y actividades comprendidas, garantizando condiciones dignas conforme a la legislación vigente."
)

# Convertir las instancias a una lista de diccionarios
documents = [cct_76_75.model_dump(), cct_petrolifero_gasifero.model_dump()]

# Ruta relativa a la carpeta metadatas desde models/asd.py
file_path = ".backend/metadatas/metadata_documents.json"

# Crear el archivo JSON o sobrescribirlo
os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Asegurarse de que el directorio exista

# Guardar la lista de documentos en el archivo JSON
with open(file_path, "w") as json_file:
    json.dump(documents, json_file, indent=2)  # Escribe los datos de los documentos en el archivo
    print(f"Datos guardados en: {file_path}")