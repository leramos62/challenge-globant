# app/crud.py (versión final y corregida)

import io
from fastapi import HTTPException
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPICallError
from .cliente import client, PROJECT_ID, DATASET_ID

def upload_csv_to_bigquery(file_content: bytes, table_name: str):
    """carga de csv a BQ."""
    
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    
    schema = []
    if table_name == "departments":
        schema = [
            bigquery.SchemaField("id", "INT64"),
            bigquery.SchemaField("department", "STRING"),
        ]
    elif table_name == "jobs":
        schema = [
            bigquery.SchemaField("id", "INT64"),
            bigquery.SchemaField("job", "STRING"),
        ]
    elif table_name == "hired_employees":
        schema = [
            bigquery.SchemaField("id", "INT64"),
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("datetime", "TIMESTAMP"),
            bigquery.SchemaField("department_id", "INT64"),
            bigquery.SchemaField("job_id", "INT64"),
        ]
    
    job_config = bigquery.LoadJobConfig(
        # esquema destino
        schema=schema,

        source_format=bigquery.SourceFormat.CSV,
    )

    try:
        file_obj = io.BytesIO(file_content)
        load_job = client.load_table_from_file(file_obj, table_id, job_config=job_config)
        load_job.result()

    except GoogleAPICallError as e:
        raise HTTPException(status_code=400, detail=f"Error al cargar datos a BQ: {e}")

    return {"message": f"Archivo cargado exitosamente a la tabla '{table_name}' en BQ."}