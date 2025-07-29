# nori-contacts-server
A server to store the user contacts information of nori.

## How to run

1. Install uv. and prepare postgres server
2. Install Python through uv.
3. Install dependencies
    ```sh
    uv sync
    ```
4. Activate Python virtual environment  
    - for linux(bash)
        ```sh
        source .venv/bin/activate
        ```
    - for windows(PowerShell)
        ```sh
        . .\.venv\Scripts\Activate.ps1
        ```
5. Copy .env.sample to .env and fill in the required values.
6. Run the app in dev mode
    ```sh
    fastapi dev src/main.py
    ```

