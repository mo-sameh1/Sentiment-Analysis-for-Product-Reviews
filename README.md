# Sentiment Analysis for Product Reviews

A Big Data project implementing a complete ETL pipeline for sentiment analysis on Amazon Fine Food Reviews.

## 🎯 Features

- **Data Pipeline**: Fetch → Transform → Load architecture
- **MongoDB Storage**: Persistent data storage with Docker volume support
- **ML Classification**: TF-IDF vectorization + Logistic Regression
- **Interactive Dashboard**: Streamlit-based UI with multiple pages
- **Batch Processing**: Analyze multiple reviews via CSV upload

## 📁 Project Structure

```text
project_root/
├── streamlit_app.py          # Main Streamlit entry point
├── docker-compose.yml        # Orchestrates Mongo + Web App
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container definition
│
├── data/                     # Data directory (gitignored)
│   ├── Reviews.csv           # Raw dataset from Kaggle
│   ├── model.pkl             # Trained model (persistent)
│   └── vectorizer.pkl        # Fitted vectorizer (persistent)
│
├── scripts/
│   ├── download_data.py      # Kaggle dataset download
│   ├── initialize_db.py      # Load CSV into MongoDB
│   └── train_model.py        # Train and save ML model
│
└── src/
    ├── config.py             # Centralized configuration
    ├── models.py             # Pydantic data models
    ├── pipeline.py           # Pipeline orchestration
    ├── inference.py          # Prediction utilities
    │
    ├── fetchers/             # Data fetching layer
    │   ├── base.py
    │   ├── csv_fetcher.py
    │   └── mongo_fetcher.py
    │
    ├── transformers/         # Data transformation layer
    │   ├── base.py
    │   └── text_sentiment_transformer.py
    │
    ├── loaders/              # Model loading/prediction
    │   ├── base.py
    │   └── sentiment_loader.py
    │
    └── ui/                   # Streamlit UI
        ├── pages/            # Page modules
        ├── components/       # Reusable components
        └── services/         # Business logic
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- MongoDB (local or Docker)
- Kaggle API credentials (`kaggle.json`)

### Option A: Local Development

1. **Clone and Setup**
   ```bash
   git clone <repo-url>
   cd Sentiment-Analysis-for-Product-Reviews
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env if needed (defaults work for local MongoDB)
   ```

3. **Start MongoDB** (if not running)
   ```bash
   docker run -d -p 27017:27017 --name mongo mongo:latest
   ```

4. **Initialize Data**
   ```bash
   python scripts/download_data.py   # Download from Kaggle
   python scripts/initialize_db.py   # Load into MongoDB
   ```

5. **Train Model**
   ```bash
   python scripts/train_model.py
   ```

6. **Run Application**
   ```bash
   streamlit run streamlit_app.py
   ```

### Option B: Docker (Recommended)

Run the entire application in containers - works on any machine with Docker.

1. **Prerequisites**
   - Docker and Docker Compose installed
   - Kaggle API credentials (`kaggle.json`) in project root

2. **First Time Setup (Initialize Data & Train Model)**
   ```bash
   # Build and run with initialization profile
   docker-compose --profile init up --build
   ```
   This will:
   - Start MongoDB
   - Download the dataset from Kaggle
   - Load data into MongoDB
   - Train the ML model

3. **Regular Usage (After Initialization)**
   ```bash
   # Start the application
   docker-compose up -d
   
   # View logs
   docker-compose logs -f app
   
   # Stop
   docker-compose down
   ```

4. **Access Application**
   Open [http://localhost:8501](http://localhost:8501)

5. **Re-initialize (if needed)**
   ```bash
   # Run initialization again
   docker-compose --profile init up init
   ```

### Docker Commands Reference

```bash
# Build without cache
docker-compose build --no-cache

# Start in foreground (see logs)
docker-compose up

# Start in background
docker-compose up -d

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes (fresh start)
docker-compose down -v

# View running containers
docker-compose ps

# Execute command in running container
docker-compose exec app python scripts/train_model.py
```

## 💾 Persistence

### Database Persistence
- MongoDB data is stored in a Docker volume (`mongo_data`)
- Data survives container restarts
- No need to re-initialize after server restart

### Model Persistence
- Trained model and vectorizer are stored in Docker volume (`app_data`)
- **Once trained, predictions work immediately** on container restart
- No need to retrain unless you want to update the model

### Volume Management
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect sentiment-analysis-for-product-reviews_app_data

# Remove all project volumes (fresh start)
docker-compose down -v
```

## 📊 Dashboard Pages

| Page | Description |
|------|-------------|
| **Home** | Project overview and system status |
| **Data Explorer** | Visualize data with charts and word clouds |
| **Single Prediction** | Real-time sentiment analysis for text input |
| **Batch Analysis** | Upload CSV for bulk sentiment analysis |
| **Pipeline Status** | Monitor connections and run pipeline scripts |

## 🛠️ Configuration

All configuration is centralized in `src/config.py`:

- MongoDB connection settings
- Model/vectorizer paths
- Training parameters
- UI constants

Environment variables (`.env`):
```
MONGO_URI=mongodb://localhost:27017/
DB_NAME=sentiment_db
COLLECTION_NAME=reviews
```

## 📝 License

MIT License
