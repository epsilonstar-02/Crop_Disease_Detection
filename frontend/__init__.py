"""
Frontend package for the Crop Disease Detection application.
"""

from frontend.app import app
from frontend.layouts import layout
from frontend.callbacks import register_callbacks

# Initialize app
app.layout = layout
register_callbacks(app)

def run_server(debug=True, port=8050):
    """Run the Dash server."""
    app.run_server(debug=debug, port=port) 