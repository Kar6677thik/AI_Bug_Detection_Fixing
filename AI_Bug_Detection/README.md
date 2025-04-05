# AI Bug Detection System

An offline AI-powered system for detecting and fixing bugs in source code, optimized for low-end machines.

## Features

- Detects functional bugs in Python and JavaScript code
- Suggests fixes with confidence scores
- Works offline without requiring cloud services
- Optimized for low-end machines through model quantization
- Web interface and API endpoints

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the API Server
```bash
uvicorn backend.api.app:app --reload
```

### Using the Web Interface
1. Start the API server
2. Open `frontend/index.html` in a web browser
3. Paste your code and click "Analyze Code"

### API Endpoints
- `POST /analyze` - Full analysis (detection + fixes)
- `POST /detect` - Bug detection only
- `POST /fix` - Fix suggestions only
- `GET /health` - Health check

## Configuration

Edit `backend/model/bug_detection.py` to:
- Change the default model
- Adjust quantization settings
- Modify detection thresholds

## Testing

Run unit tests:
```bash
python -m unittest discover tests
```

## License
MIT