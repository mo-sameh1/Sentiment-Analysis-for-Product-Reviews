# Sentiment Analysis for Product Reviews

A Big Data project pipeline for analyzing sentiment in Amazon Fine Food Reviews.

## 1. Project Structure

```text
project_root/
├── docker-compose.yml       # Orchestrates Mongo + Web App
├── .env.example             # Template for environment variables
├── requirements.txt         # Python dependencies
├── Dockerfile               # Definition for the web-app container
├── scripts/
│   └── initialize_db.py     # Script to seed MongoDB with mock data
└── src/
    ├── models.py            # Pydantic data models
    ├── pipeline.py          # Main pipeline logic
    ├── fetchers/            # Data fetching layer
    ├── transformers/        # Data transformation layer
    ├── loaders/             # Model loading/prediction layer
    └── app/
        └── main.py          # Streamlit frontend
```

## 2. Dataset Setup (Required)

This project uses the **Amazon Fine Food Reviews** dataset from Kaggle.

1.  **Get Kaggle API Token**:
    *   Go to your [Kaggle Account Settings](https://www.kaggle.com/me/account).
    *   Scroll to "API" and click "Create New Token".
    *   This downloads a `kaggle.json` file.

2.  **Place the Token**:
    *   Move `kaggle.json` to the root of this project (`project_root/kaggle.json`).
    *   **Note:** This file is ignored by git for security.

## 3. Setup & Installation

### Option A: Running with Docker (Recommended)

1.  **Create Environment File**:
    ```bash
    cp .env.example .env
    ```
    *Note: The `MONGO_URI` in `.env` is for local development. Docker uses its own internal networking.*

2.  **Build and Start Services**:
    ```bash
    docker-compose up --build -d
    ```

3.  **Initialize Database**:
    This will automatically download the dataset (using your `kaggle.json`) and load a sample into MongoDB:
    ```bash
    docker-compose exec web-app python scripts/initialize_db.py
    ```

4.  **Access the App**:
    Open [http://localhost:8501](http://localhost:8501)

### Option B: Running Locally (Development)

1.  **Prerequisites**:
    *   Python 3.10+
    *   MongoDB installed and running locally on port 27017.
    *   `kaggle.json` in the project root (or `~/.kaggle/`).

2.  **Create Virtual Environment**:
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    Ensure your `.env` file has the local connection string:
    ```text
    MONGO_URI=mongodb://localhost:27017/
    ```

5.  **Initialize Database**:
    ```bash
    python scripts/initialize_db.py
    ```

6.  **Run the App**:
    ```bash
    streamlit run src/app/main.py
    ```

## 4. Development Workflow

*   **Data Models**: Defined in `src/models.py`.
*   **Pipeline**: The main logic is in `src/pipeline.py`.
*   **Extending**:
    *   Add new data sources in `src/fetchers/`.
    *   Add new preprocessing steps in `src/transformers/`.
    *   Add new models in `src/loaders/`.
