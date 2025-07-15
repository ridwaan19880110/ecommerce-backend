#!/bin/bash

# Optional: load env variables if needed
# source .env

# Start FastAPI app using uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000