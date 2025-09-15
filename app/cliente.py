# Documentacion en comentarios
# importacion de librerias
import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

# Obtencion y asignacion de variables
client = bigquery.Client()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BIGQUERY_DATASET_ID")

if not PROJECT_ID or not DATASET_ID:
    raise ValueError("variable no correctas en  .env")
