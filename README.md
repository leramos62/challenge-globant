# Desafío de Ingeniería de Datos - Globant V. 1.00

Este repositorio contiene la solución el desafío de codificación de Ingeniería de Datos. El proyecto es una API construida con FastAPI que implementa un pipeline de ingesta de datos robusto: recibe archivos CSV, los procesa, y los inserta en Google BigQuery en lotes controlados.

## Lógica de Ingesta

La funcionalidad principal de la API es manejar la carga de grandes volúmenes de datos de manera eficiente. En lugar de una simple subida de archivos, el proceso es el siguiente:

1.  La API recibe un archivo CSV a través de un endpoint.
2.  El código lee el archivo en memoria, línea por línea.
3.  Las filas se agrupan en lotes (chunks) de hasta 1000 registros.
4.  Cada lote se convierte a formato JSON y se inserta en BigQuery mediante el método de "streaming inserts".
5.  Este proceso se repite hasta que se han insertado todas las filas del archivo.

Este enfoque cumple con todos los requisitos de la Sección 1 en una sola operación.

---

## Arquitectura

*   **Framework de API:** FastAPI (Python)
*   **Almacén de Datos:** Google BigQuery
*   **Autenticación con GCP:** Cuenta de Servicio (Service Account)

---

## Cómo Ejecutar el Proyecto Localmente

### Prerrequisitos

*   Python 3.8+
*   Un proyecto en Google Cloud con la API de BigQuery habilitada.

### 1. Configuración del Entorno

1.  **Clonar el repositorio:**
    ```bash
    git clone [URL-DEL-REPOSITORIO]
    cd [NOMBRE-DEL-REPOSITORIO]
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    # En Windows
    python -m venv venv
    .\venv\Scripts\activate

    # En macOS/Linux
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

### 2. Configuración de Credenciales de GCP

1.  **Cuenta de Servicio:** Asegúrate de tener un archivo de credenciales JSON de una cuenta de servicio de GCP con el rol `Editor de datos de BigQuery`.
2.  **Renombrar y Mover:** Coloca el archivo de credenciales en la raíz del proyecto y renómbralo a `gcp-credentials.json`.
3.  **Archivo `.env`:** Crea un archivo llamado `.env` en la raíz del proyecto y añade la siguiente configuración, reemplazando los valores correspondientes:
    ```ini
    GOOGLE_APPLICATION_CREDENTIALS="gcp-credentials.json"
    GCP_PROJECT_ID="tu-id-de-proyecto-gcp"
    BIGQUERY_DATASET_ID="globant_challenge_dataset"
    ```

### 3. Iniciar la API

Con el entorno virtual activado, ejecuta el siguiente comando:
```bash
uvicorn app.main:app --reload