# Developing a Screening API using FastAPI

## Fuzzy Matching

Fuzzy matching, also known as approximate string matching, is a technique used to find strings that approximately match a given pattern. The basis of text similarity in this API will consider the following operations:

* **Insertion:** Adding a character to a string.
* **Deletion:** Removing a character from a string.
* **Transposition:** Swapping the positions of adjacent characters in a string.

Several algorithms can quantify these similarities, including:

* **Levenshtein distance:** Measures the minimum number of single-character edits (insertions, deletions, or substitutions) required to change one word into the other.
* **Hamming distance:** Measures the number of positions at which the corresponding symbols are different. This is applicable only to strings of equal length.
* **Indel distance:** A generalization of the Levenshtein distance that only considers insertions and deletions.
* **Damerau-Levenshtein distance:** Similar to Levenshtein distance but also includes transpositions among the allowed operations.

## Setting Up the Python Environment

Follow these steps to set up your Python development environment:

1.  **Initialize Git:**
    ```bash
    git init .
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv env
    ```

3.  **Ignore the Virtual Environment:**
    ```bash
    new-item .gitignore
    ```
    Open the `.gitignore` file and add `env/` to it to prevent the virtual environment from being committed to version control.

4.  **Activate the Virtual Environment:**
    * **On Windows:**
        ```bash
        .\env\Scripts\activate
        ```
    * **On macOS and Linux:**
        ```bash
        source env/bin/activate
        ```

5.  **Create `requirements.txt`:**
    Create a file named `requirements.txt` in your project directory and add the following dependencies:
    ```
    ipykernel
    pandas
    sqlalchemy
    psycopg2
    pyarrow
    rapidfuzz
    fastapi
    uvicorn[standard]
    orjson
    python-environ
    ```

6.  **Install Dependencies:**
    ```bash
    pip install -r .\requirements.txt
    ```

## Creating a Simple API with FastAPI

1.  **Create `app.py`:**
    Create a Python file named `app.py` where you will define your API.

2.  **Run the API:**
    To start the FastAPI application, use the following command in your terminal (make sure your virtual environment is activated and you are in the project directory):
    ```bash
    uvicorn app.main:screening_app --reload
    ```
    * `app`: Refers to the `app.py` file.
    * `screening_app`: Refers to the FastAPI application instance you will create within `app.py`.
    * `--reload`: Enables automatic reloading of the server upon code changes, which is helpful during development.

## Creating the Screening Endpoint

1.  **Configure Environment Variables:**
    You will need to configure environment variables to securely store your database credentials. You can typically do this in your shell's activation script or through other environment variable management tools. In your activate script(s) (e.g., `env/Scripts/activate` on Windows or `env/bin/activate` on macOS/Linux), set the following environment variables:
    ```bash
    $Env:DB_HOST="your_db_host"
    $Env:DB_PORT="your_db_port"
    $Env:DB_NAME="your_db_name"
    $Env:DB_USER="your_db_user"
    $Env:DB_PASS="your_db_password"
    ```
    *(Remember to replace the placeholder values with your actual database credentials.)*

2.  **Import Necessary Libraries in `app.py`:**
    Add the following import statements at the beginning of your `app.py` file:
    ```python
    import re
    import pandas as pd
    import environ
    from sqlalchemy import create_engine, URL, Engine
    from rapidfuzz import fuzz
    from fastapi import FastAPI, Request
    from fastapi.responses import ORJSONResponse
    ```

3.  **Create Helper Functions:**
    You will likely need to create helper functions to perform tasks such as:
    * Fetching data from the database.
    * Implementing the fuzzy matching logic using the `rapidfuzz` library.
    * Processing and comparing the input text with the fetched data.

4.  **Connect to the PostgreSQL Database:**
    Use the imported libraries to establish a connection to your PostgreSQL database. This typically involves:
    * Reading the environment variables for database credentials using the `environ` library.
    * Constructing a database URL using `sqlalchemy.URL`.
    * Creating a database engine using `sqlalchemy.create_engine`.