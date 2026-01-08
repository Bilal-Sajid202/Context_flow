import uvicorn
import sys
import os

# Add the project root directory to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    uvicorn.run("app.src.main:app", host="127.0.0.1", port=8000, reload=True)
