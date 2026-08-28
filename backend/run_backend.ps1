$ErrorActionPreference = "Stop"

# Activate the virtual environment
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    . .\venv\Scripts\Activate.ps1
} else {
    Write-Host "Virtual environment not found. Please ensure venv exists." -ForegroundColor Red
    exit 1
}

# Run the backend with python protobuf implementation to fix UPB crashes in MediaPipe
$env:PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="python"
python -u -m uvicorn app.main:app --host 0.0.0.0 --port 8000
