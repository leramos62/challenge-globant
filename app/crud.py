import io
import csv
from typing import List

from fastapi import HTTPException
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPICallError

from .cliente import client, PROJECT_ID, DATASET_ID
from . import schemas

# funcion par ainsertar en batch.
def process_and_insert_csv_in_batches(file_content: bytes, table_name: str):
    """
    lee un archivo csv, lo agrupa en lotes de 1000, y los inserta en bigquery.
    cumple con todos los requisitos de la sección 1 en una sola operación.
    """
    # --- Parametrizacion---
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}" # parametrizacion de tabla con valores GCP
    batch = [] # crea una lista vacía para  filas de  lote
    total_rows_inserted = 0
    BATCH_SIZE = 1000 # tamaño máximo de cada lote

    # --- 2. definir las columnas ed tablas
    headers_map = {
        "departments": ["id", "department"],
        "jobs": ["id", "job"],
        "hired_employees": ["id", "name", "datetime", "department_id", "job_id"],
    }
    
    headers = headers_map.get(table_name)
    if not headers:
        raise HTTPException(status_code=400, detail=f"Tabla '{table_name}' no reconocida.")

    # --- 3. lee y procesa  archivo csv ---
    try:
        decoded_content = file_content.decode('utf-8') # decodifica los archivos a texto
        csv_reader = csv.reader(io.StringIO(decoded_content)) # lee el texto como un archivo csv

        # bucle en cada fila
        for row in csv_reader:
            if not row: continue # salta filas vacías

            # convierte la fila clave: valor
            row_dict = dict(zip(headers, row))

            # --- 4. validación y conversión de tipos ---
            try:
                for key in ['id', 'department_id', 'job_id']:
                    if key in row_dict:
                        row_dict[key] = int(row_dict[key])
            except (ValueError, TypeError):
                print(f"adv: saltando fila con datos mal formados: {row}")
                continue
            
            batch.append(row_dict) # añade la fila procesada al lote actual

            # --- 5. inserta el lote al llegar a batch=1000 ---
            if len(batch) == BATCH_SIZE:
                errors = client.insert_rows_json(table_id, batch) 
                if errors:
                    raise HTTPException(status_code=400, detail=f"error insertando lote: {errors}")
                
                total_rows_inserted += len(batch) 
                print(f"info: se insertó un lote de {len(batch)} filas en '{table_name}'.")
                batch = [] 

        # --- 6. Ultimo lote (puede ser menor a 1000) ---
        if batch:
            errors = client.insert_rows_json(table_id, batch) 
            if errors:
                raise HTTPException(status_code=400, detail=f"error insertando el lote final: {errors}")

            total_rows_inserted += len(batch)
            print(f"info: se insertó el lote final de {len(batch)} filas en '{table_name}'.")

    except GoogleAPICallError as e:
        raise HTTPException(status_code=500, detail=f"error de api al insertar datos en bigquery: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"error procesando el archivo csv: {e}")

    return {"message": f"proceso completado. se insertaron un total de {total_rows_inserted} filas en la tabla '{table_name}'."}