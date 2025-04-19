"""
Dash app initialization module.
"""

import dash
import dash_bootstrap_components as dbc

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.FLATLY, 
                                      dbc.icons.FONT_AWESOME],
                suppress_callback_exceptions=True)

# Custom CSS for enhanced visual appeal
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Crop Disease Detector</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-image: url('https://images.unsplash.com/photo-1473773508845-188df298d2d1?ixlib=rb-1.2.1&auto=format&fit=crop&w=2850&q=80');
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
                font-family: 'Poppins', sans-serif;
            }
            
            .content-wrapper {
                backdrop-filter: blur(10px);
                background-color: rgba(255, 255, 255, 0.9);
                min-height: 100vh;
                padding: 30px;
            }
            
            .app-card {
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                border: none;
                overflow: hidden;
                transition: transform 0.3s, box-shadow 0.3s;
            }
            
            .app-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
            }
            
            .card-header {
                background-color: #ffffff;
                border-bottom: 1px solid rgba(0, 0, 0, 0.05);
                padding: 20px;
            }
            
            .card-body {
                padding: 25px;
            }
            
            .result-metrics-card {
                border-radius: 12px;
                overflow: hidden;
                border: none;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
                transition: transform 0.2s;
            }
            
            .result-metrics-card:hover {
                transform: translateY(-3px);
            }
            
            .fancy-tab .nav-link {
                border-radius: 30px;
                padding: 10px 20px;
                margin-right: 10px;
                font-weight: 500;
            }
            
            .fancy-tab .nav-link.active {
                background-color: #2C8C40;
                color: white;
                box-shadow: 0 5px 15px rgba(44, 140, 64, 0.3);
            }
            
            .btn-custom-success {
                background: linear-gradient(135deg, #2C8C40, #3DAF58);
                border: none;
                border-radius: 30px;
                padding: 12px 30px;
                font-weight: 500;
                box-shadow: 0 5px 15px rgba(44, 140, 64, 0.3);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            
            .btn-custom-success:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(44, 140, 64, 0.4);
                background: linear-gradient(135deg, #3DAF58, #2C8C40);
            }
            
            .btn-custom-primary {
                background: linear-gradient(135deg, #2C3E50, #3498DB);
                border: none;
                border-radius: 30px;
                padding: 12px 30px;
                font-weight: 500;
                box-shadow: 0 5px 15px rgba(44, 62, 80, 0.3);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            
            .btn-custom-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(44, 62, 80, 0.4);
                background: linear-gradient(135deg, #3498DB, #2C3E50);
            }
            
            .upload-area {
                border: 2px dashed #ddd;
                border-radius: 15px;
                padding: 30px;
                text-align: center;
                cursor: pointer;
                background-color: #f9f9f9;
                transition: all 0.3s;
            }
            
            .upload-area:hover {
                border-color: #2C8C40;
                background-color: #f0f7f0;
            }
            
            .icon-circle {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background-color: rgba(44, 140, 64, 0.1);
                color: #2C8C40;
                margin-bottom: 15px;
            }
            
            .sidebar {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            }
            
            .img-preview {
                border-radius: 12px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }
            
            .progress-custom {
                height: 10px;
                border-radius: 5px;
            }
            
            .treatment-list li {
                padding: 10px 0;
                border-bottom: 1px solid rgba(0,0,0,0.05);
            }
            
            /* Animation for results */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .results-animation {
                animation: fadeIn 0.6s ease-out forwards;
            }
            
            /* Custom styling for list items */
            .bullet-list {
                padding-left: 20px;
            }
            
            .bullet-list li {
                position: relative;
                padding: 8px 0 8px 30px;
                list-style-type: none;
            }
            
            .bullet-list li:before {
                content: '';
                position: absolute;
                left: 0;
                top: 14px;
                width: 12px;
                height: 12px;
                background-color: #2C8C40;
                border-radius: 50%;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
''' 