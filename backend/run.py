# run.py
from backend.app import create_app
from backend.utils.config import API_HOST, API_PORT

if __name__ == '__main__':
    app = create_app()
    print(f"Starting Flask server on {API_HOST}:{API_PORT}...")
    app.run(debug=True, port=API_PORT, host=API_HOST) 