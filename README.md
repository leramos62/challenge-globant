# Desafío de Ingeniería de Datos - Globant  -- V 0.1

Este repositorio contiene la solución el desafío de codificación de Ingeniería de Datos. El proyecto es una API construida con FastAPI que implementa un pipeline de ingesta de datos robusto: recibe archivos CSV, los procesa, y los inserta en Google BigQuery en lotes controlados.

## Estado Actual

Actualmente, se han completado las siguientes secciones:

*   **Sección 1: API de Ingesta de Datos**
*   **Sección 2: API de Métricas y Consultas**

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
