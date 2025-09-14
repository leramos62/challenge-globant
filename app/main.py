from fastapi import FastAPI, UploadFile, File, HTTPException
from . import crud

# Inicializamos la aplicación FastAPI
app = FastAPI(title="mi api hijs del pico")

@app.post("/upload-csv/{table_name}", tags=["Carga de Archivos CSV"])
async def upload_csv_endpoint(table_name: str, file: UploadFile = File(...)):
    """
    carga tu wea
    """
    # Vvalidacion ed tablas permitidas
    allowed_tables = ["departments", "jobs", "hired_employees"]
    if table_name not in allowed_tables:
        raise HTTPException(status_code=400, detail=f"Nombre de tabla no válido. Usa uno de: {allowed_tables}")

    content = await file.read()

    # llamado a funcion d carga
    return crud.upload_csv_to_bigquery(content, table_name)