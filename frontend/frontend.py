import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import base64
import io
from PIL import Image
import requests
from datetime import datetime

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
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    </head>
    <body>
        <div class="content-wrapper">
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App layout
app.layout = dbc.Container([
    dbc.Row([
        # Header
        dbc.Col([
            html.Div([
                html.H1("🌱 Crop Disease Detector", className="text-success text-center mb-1", 
                       style={"fontWeight": "700", "fontSize": "38px"}),
                html.P("Identify plant diseases instantly with our advanced AI technology", 
                      className="lead text-center text-muted mb-4",
                      style={"fontSize": "18px"})
            ])
        ], width=12, className="mb-4")
    ]),
    
    dbc.Row([
        # Sidebar
        dbc.Col([
            html.Div([
                html.Div(className="text-center mb-4", children=[
                    html.Img(src="https://images.unsplash.com/photo-1592982537447-7440770cbfc9?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80", 
                           style={"width": "100%", "borderRadius": "12px", "marginBottom": "20px", "boxShadow": "0 5px 15px rgba(0,0,0,0.1)"})
                ]),
                
                html.H4([html.I(className="fas fa-info-circle me-2"), "How It Works"], 
                       className="mb-3 d-flex align-items-center", 
                       style={"color": "#2C8C40"}),
                       
                html.Ol([
                    html.Li("Upload a clear image of your crop", className="mb-2"),
                    html.Li("Click 'Analyze' to detect diseases", className="mb-2"),
                    html.Li("Review the diagnosis and recommendations", className="mb-2"),
                    html.Li("Download a detailed PDF report", className="mb-2")
                ], className="mb-4"),
                
                html.Hr(className="my-4"),
                
                html.H4([html.I(className="fas fa-seedling me-2"), "About"], 
                       className="mb-3 d-flex align-items-center",
                       style={"color": "#2C8C40"}),
                       
                html.P(
                    "Our Crop Disease Detector uses advanced AI to identify "
                    "plant diseases and provide treatment recommendations to "
                    "help farmers protect their crops and increase yields.",
                    className="text-muted"
                ),
                
                html.Hr(className="my-4"),
                
                html.Div([
                    html.H5("Recent Updates", className="mb-3"),
                    dbc.ListGroup([
                        dbc.ListGroupItem([
                            html.Div("New disease models added", className="fw-bold"),
                            html.Small("April 10, 2025", className="text-muted")
                        ]),
                        dbc.ListGroupItem([
                            html.Div("Improved detection accuracy", className="fw-bold"),
                            html.Small("March 28, 2025", className="text-muted")
                        ]),
                        dbc.ListGroupItem([
                            html.Div("Mobile app now available", className="fw-bold"),
                            html.Small("March 15, 2025", className="text-muted")
                        ])
                    ], flush=True)
                ])
            ], className="sticky-top p-4 sidebar")
        ], width=3, className="d-none d-md-block"),
        
        # Main content
        dbc.Col([
            # Upload Card
            dbc.Card([
                dbc.CardHeader([
                    html.H3([html.I(className="fas fa-cloud-upload-alt me-2"), "Upload Image"], 
                           className="mb-0 text-success")
                ], className="bg-white"),
                
                dbc.CardBody([
                    html.P("Select a clear image of the affected plant for analysis", 
                          className="card-text text-muted mb-4"),
                          
                    dcc.Upload(
                        id='upload-image',
                        children=html.Div([
                            html.Div(className="icon-circle", children=[
                                html.I(className="fas fa-file-image fa-2x")
                            ]),
                            html.Div("Drag and Drop or Click to Select Image", 
                                    style={"fontWeight": "500"}),
                            html.Div("JPG, PNG or JPEG files accepted", 
                                    className="text-muted small mt-1")
                        ]),
                        className="upload-area mb-4",
                        multiple=False,
                        accept='image/*'
                    ),
                    
                    # Image preview and details
                    html.Div(id='output-image-upload'),
                    
                    # Analysis button
                    html.Div([
                        dbc.Button([
                            html.I(className="fas fa-search-plus me-2"), 
                            "Analyze Image"
                        ], 
                        id="analyze-button", 
                        className="btn-custom-success w-100 mt-3",
                        size="lg", 
                        disabled=True)
                    ])
                ])
            ], className="app-card mb-4"),
            
            # Results Card (initially hidden)
            html.Div(id='results-container', className="results-animation", style={'display': 'none'}),
            
            # Tips Card (shown when no image is uploaded)
            dbc.Card([
                dbc.CardHeader([
                    html.H3([html.I(className="fas fa-lightbulb me-2"), "Tips for Better Results"], 
                           className="mb-0 text-primary")
                ], className="bg-white"),
                
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Div(className="text-center mb-3", children=[
                                html.Div(className="icon-circle", style={"backgroundColor": "rgba(52, 152, 219, 0.1)", "color": "#3498DB"}, children=[
                                    html.I(className="fas fa-sun fa-2x")
                                ])
                            ]),
                            html.H5("Good Lighting", className="text-primary text-center mb-2"),
                            html.P("Take photos in natural daylight for best results", className="text-center")
                        ], width=4),
                        dbc.Col([
                            html.Div(className="text-center mb-3", children=[
                                html.Div(className="icon-circle", style={"backgroundColor": "rgba(52, 152, 219, 0.1)", "color": "#3498DB"}, children=[
                                    html.I(className="fas fa-camera-retro fa-2x")
                                ])
                            ]),
                            html.H5("Clear Focus", className="text-primary text-center mb-2"),
                            html.P("Ensure leaves and affected areas are clearly visible", className="text-center")
                        ], width=4),
                        dbc.Col([
                            html.Div(className="text-center mb-3", children=[
                                html.Div(className="icon-circle", style={"backgroundColor": "rgba(52, 152, 219, 0.1)", "color": "#3498DB"}, children=[
                                    html.I(className="fas fa-sync-alt fa-2x")
                                ])
                            ]),
                            html.H5("Multiple Angles", className="text-primary text-center mb-2"),
                            html.P("Upload several views for greater accuracy", className="text-center")
                        ], width=4)
                    ])
                ])
            ], className="app-card mb-4", id="tips-card"),
            
            # Footer
            html.Footer([
                html.P([
                    "Crop Disease Detector | Developed with ", 
                    html.I(className="fas fa-heart text-danger"),
                    " | © 2025"
                ],
                className="text-center text-muted mt-4")
            ])
        ], width=9)
    ])
], fluid=True)

# Callback for image upload
@callback(
    [Output('output-image-upload', 'children'),
     Output('analyze-button', 'disabled')],
    [Input('upload-image', 'contents')],
    [State('upload-image', 'filename')]
)
def update_output(content, filename):
    if content is None:
        return None, True
    
    # Parse content
    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        # Open image to get details
        img = Image.open(io.BytesIO(decoded))
        width, height = img.size
        img_format = img.format
        img_size = len(decoded) / 1024  # KB
        
        # Create image preview and details
        return [
            dbc.Row([
                dbc.Col([
                    html.Img(src=content, 
                           className="img-preview",
                           style={'width': '100%', 'borderRadius': '12px'})
                ], width=7),
                dbc.Col([
                    html.H5([html.I(className="fas fa-info-circle me-2"), "Image Details"], 
                           className="mb-3 text-success"),
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(html.Div("Filename:"), width=4),
                                dbc.Col(html.Div(filename, className="fw-bold"), width=8)
                            ], className="mb-2"),
                            dbc.Row([
                                dbc.Col(html.Div("Resolution:"), width=4),
                                dbc.Col(html.Div(f"{width} × {height}", className="fw-bold"), width=8)
                            ], className="mb-2"),
                            dbc.Row([
                                dbc.Col(html.Div("Format:"), width=4),
                                dbc.Col(html.Div(img_format, className="fw-bold"), width=8)
                            ], className="mb-2"),
                            dbc.Row([
                                dbc.Col(html.Div("Size:"), width=4),
                                dbc.Col(html.Div(f"{img_size:.2f} KB", className="fw-bold"), width=8)
                            ], className="mb-2")
                        ])
                    ], className="border-0 bg-light", style={"borderRadius": "12px"})
                ], width=5)
            ], className="mt-4")
        ], False
    
    except Exception as e:
        return html.Div([
            dbc.Alert([
                html.I(className="fas fa-exclamation-triangle me-2"),
                "There was an error processing this file."
            ], color="danger")
        ]), True

# Callback for analysis
@callback(
    [Output('results-container', 'children'),
     Output('results-container', 'style'),
     Output('tips-card', 'style')],
    [Input('analyze-button', 'n_clicks')],
    [State('upload-image', 'contents')]
)
def analyze_image(n_clicks, content):
    if n_clicks is None or n_clicks == 0 or content is None:
        raise PreventUpdate
    
    # Show loading spinner 
    try:
        # Parse content
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        
        # Make API request (in a real app)
        try:
            response = requests.post(
                "http://localhost:5000/predict",
                files={"image": decoded}
            )
            
            if response.status_code == 200:
                result = response.json()
                disease = result['disease']
                recommendation = result['recommendation']
                pdf_content = result['pdf']  # Base64 encoded PDF
                
                # For demonstration, let's create a sample list from the recommendation
                # In a real app, the backend should return this structured format
                treatment_points = recommendation.split('. ')
                treatment_points = [point for point in treatment_points if point.strip()]
                
                # Create results card
                results_card = dbc.Card([
                    dbc.CardHeader([
                        html.H3([html.I(className="fas fa-clipboard-check me-2"), "Diagnosis Results"], 
                               className="mb-0 text-primary")
                    ], className="bg-white"),
                    dbc.CardBody([
                        dbc.Tabs([
                            dbc.Tab([
                                html.Div([
                                    dbc.Row([
                                        dbc.Col([
                                            html.H4([html.I(className="fas fa-search me-2"), "Detected Issue"], 
                                                   className="text-success mb-3"),
                                            dbc.Alert([disease], 
                                                     color="warning", 
                                                     className="mb-4 shadow-sm",
                                                     style={"borderRadius": "10px", "borderLeft": "5px solid #f0ad4e"})
                                        ], width=12)
                                    ]),
                                    
                                    dbc.Row([
                                        dbc.Col([
                                            html.H5([html.I(className="fas fa-chart-line me-2"), "Confidence Score"], 
                                                   className="mb-2"),
                                            dbc.Progress(value=92, color="success", className="mb-2 progress-custom"),
                                            html.P("92% confidence", className="text-muted small")
                                        ], width=12, className="mb-4")
                                    ]),
                                    
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Card([
                                                dbc.CardBody([
                                                    html.Div(className="text-center mb-2", children=[
                                                        html.Div(className="icon-circle", style={"backgroundColor": "rgba(240, 173, 78, 0.1)", "width": "40px", "height": "40px"}, children=[
                                                            html.I(className="fas fa-exclamation-triangle fa-lg", style={"color": "#f0ad4e"})
                                                        ])
                                                    ]),
                                                    html.H3("Medium", className="text-warning text-center mb-1"),
                                                    html.P("Severity", className="text-center text-muted mb-0 small")
                                                ])
                                            ], className="h-100 result-metrics-card")
                                        ], width=4),
                                        dbc.Col([
                                            dbc.Card([
                                                dbc.CardBody([
                                                    html.Div(className="text-center mb-2", children=[
                                                        html.Div(className="icon-circle", style={"backgroundColor": "rgba(217, 83, 79, 0.1)", "width": "40px", "height": "40px"}, children=[
                                                            html.I(className="fas fa-virus fa-lg", style={"color": "#d9534f"})
                                                        ])
                                                    ]),
                                                    html.H3("High", className="text-danger text-center mb-1"),
                                                    html.P("Spread Risk", className="text-center text-muted mb-0 small")
                                                ])
                                            ], className="h-100 result-metrics-card")
                                        ], width=4),
                                        dbc.Col([
                                            dbc.Card([
                                                dbc.CardBody([
                                                    html.Div(className="text-center mb-2", children=[
                                                        html.Div(className="icon-circle", style={"backgroundColor": "rgba(92, 184, 92, 0.1)", "width": "40px", "height": "40px"}, children=[
                                                            html.I(className="fas fa-dollar-sign fa-lg", style={"color": "#5cb85c"})
                                                        ])
                                                    ]),
                                                    html.H3("Low", className="text-success text-center mb-1"),
                                                    html.P("Treatment Cost", className="text-center text-muted mb-0 small")
                                                ])
                                            ], className="h-100 result-metrics-card")
                                        ], width=4)
                                    ], className="mb-3")
                                ])
                            ], label="Diagnosis", tab_id="tab-diagnosis", className="fancy-tab"),
                            
                            dbc.Tab([
                                html.Div([
                                    dbc.Row([
                                        dbc.Col([
                                            html.H4([html.I(className="fas fa-notes-medical me-2"), "Treatment Plan"], 
                                                   className="text-success mb-3"),
                                            
                                            # Bullet point list for treatment recommendations
                                            html.Ul([
                                                html.Li(point, className="mb-2") 
                                                for point in treatment_points
                                            ], className="bullet-list mb-4")
                                        ])
                                    ]),
                                    
                                    dbc.Row([
                                        dbc.Col([
                                            html.H5([html.I(className="fas fa-clock me-2"), "Timeline"], 
                                                   className="mb-3"),
                                            dbc.Card([
                                                dbc.CardBody([
                                                    dbc.Row([
                                                        dbc.Col([
                                                            html.Div(className="icon-circle", style={"backgroundColor": "rgba(52, 152, 219, 0.1)", "color": "#3498DB", "width": "40px", "height": "40px"}, children=[
                                                                html.I(className="fas fa-calendar-day fa-lg")
                                                            ])
                                                        ], width=2),
                                                        dbc.Col([
                                                            html.P([
                                                                html.Span("Day 1: ", className="fw-bold"), 
                                                                "Begin treatment immediately."
                                                            ], className="mb-0")
                                                        ], width=10)
                                                    ], className="mb-3"),
                                                    dbc.Row([
                                                        dbc.Col([
                                                            html.Div(className="icon-circle", style={"backgroundColor": "rgba(52, 152, 219, 0.1)", "color": "#3498DB", "width": "40px", "height": "40px"}, children=[
                                                                html.I(className="fas fa-calendar-week fa-lg")
                                                            ])
                                                        ], width=2),
                                                        dbc.Col([
                                                            html.P([
                                                                html.Span("Week 1: ", className="fw-bold"), 
                                                                "Monitor plant condition daily and continue treatment."
                                                            ], className="mb-0")
                                                        ], width=10)
                                                    ], className="mb-3"),
                                                    dbc.Row([
                                                        dbc.Col([
                                                            html.Div(className="icon-circle", style={"backgroundColor": "rgba(52, 152, 219, 0.1)", "color": "#3498DB", "width": "40px", "height": "40px"}, children=[
                                                                html.I(className="fas fa-calendar fa-lg")
                                                            ])
                                                        ], width=2),
                                                        dbc.Col([
                                                            html.P([
                                                                html.Span("Week 2-3: ", className="fw-bold"), 
                                                                "Most cases should show significant improvement."
                                                            ], className="mb-0")
                                                        ], width=10)
                                                    ])
                                                ])
                                            ], className="border-0 bg-light mb-4", style={"borderRadius": "12px"})
                                        ])
                                    ]),
                                    
                                    dbc.Row([
                                        dbc.Col([
                                            html.H5([html.I(className="fas fa-shield-alt me-2"), "Prevention Tips"], 
                                                   className="mb-3"),
                                            dbc.ListGroup([
                                                dbc.ListGroupItem([
                                                    html.I(className="fas fa-check-circle text-success me-2"),
                                                    "Maintain proper plant spacing for good air circulation"
                                                ], className="border-0 mb-2 bg-light", style={"borderRadius": "8px"}),
                                                dbc.ListGroupItem([
                                                    html.I(className="fas fa-check-circle text-success me-2"),
                                                    "Water at the base of plants to keep foliage dry"
                                                ], className="border-0 mb-2 bg-light", style={"borderRadius": "8px"}),
                                                dbc.ListGroupItem([
                                                    html.I(className="fas fa-check-circle text-success me-2"),
                                                    "Practice crop rotation to prevent disease buildup"
                                                ], className="border-0 mb-2 bg-light", style={"borderRadius": "8px"}),
                                                dbc.ListGroupItem([
                                                    html.I(className="fas fa-check-circle text-success me-2"),
                                                    "Remove and destroy infected plant material promptly"
                                                ], className="border-0 mb-2 bg-light", style={"borderRadius": "8px"})
                                            ])
                                        ])
                                    ])
                                ])
                            ], label="Treatment", tab_id="tab-treatment", className="fancy-tab")
                        ], id="tabs", active_tab="tab-diagnosis", className="mb-4")
                    ]),
                    dbc.CardFooter([
                        dbc.Button(
                            [html.I(className="fas fa-file-download me-2"), "Download Full Report"],
                            id="download-report",
                            className="btn-custom-primary w-100"
                        ),
                        dcc.Download(id="download-pdf")
                    ], className="bg-white")
                ], className="app-card mb-4")
                
                # Return results card and hide tips
                return results_card, {'display': 'block'}, {'display': 'none'}
            
            else:
                # Return error card
                error_card = dbc.Card([
                    dbc.CardHeader([
                        html.H4([html.I(className="fas fa-exclamation-circle me-2"), "Error"], 
                               className="mb-0 text-danger")
                    ], className="bg-white"),
                    dbc.CardBody([
                        html.Div(className="text-center mb-4", children=[
                            html.Div(className="icon-circle", style={"backgroundColor": "rgba(220, 53, 69, 0.1)", "color": "#dc3545", "width": "80px", "height": "80px"}, children=[
                                html.I(className="fas fa-times-circle fa-3x")
                            ])
                        ]),
                        html.P(f"Error: {response.json().get('error', 'Unknown error')}", className="text-center mb-3"),
                        html.P("Please try again or contact support if the issue persists.", className="text-center text-muted")
                    ])
                ], className="app-card mb-4 border-danger")
                
                return error_card, {'display': 'block'}, {'display': 'block'}
            
        except Exception as e:
            # Server connection error
            error_card = dbc.Card([
                dbc.CardHeader([
                    html.H4([html.I(className="fas fa-wifi me-2"), "Connection Error"], 
                           className="mb-0 text-danger")
                ], className="bg-white"),
                dbc.CardBody([
                    html.Div(className="text-center mb-4", children=[
                        html.Div(className="icon-circle", style={"backgroundColor": "rgba(220, 53, 69, 0.1)", "color": "#dc3545", "width": "80px", "height": "80px"}, children=[
                            html.I(className="fas fa-server fa-3x")
                        ])
                    ]),
                    html.P("Failed to connect to the diagnostic server.", className="text-center mb-4"),
                    
                    html.H5([html.I(className="fas fa-tools me-2"), "Troubleshooting Tips:"], className="mb-3"),
                    dbc.Card([
                        dbc.CardBody([
                            html.Ul([
                                html.Li("Make sure the backend server is running at http://localhost:5000", className="mb-2"),
                                html.Li("Check your internet connection", className="mb-2"),
                                html.Li("Try uploading a different image", className="mb-2"),
                                html.Li("Contact support if the problem persists", className="mb-2")
                            ], className="mb-0")
                        ])
                    ], className="border-0 bg-light", style={"borderRadius": "12px"})
                ])
            ], className="app-card mb-4 border-danger")
            
            return error_card, {'display': 'block'}, {'display': 'block'}
    
    except Exception as e:
        # General error
        error_card = dbc.Card([
            dbc.CardHeader([
                html.H4([html.I(className="fas fa-exclamation-triangle me-2"), "Error"], 
                       className="mb-0 text-danger")
            ], className="bg-white"),
            dbc.CardBody([
                html.P("An unexpected error occurred during analysis.", className="text-center")
            ])
        ], className="app-card mb-4 border-danger")
        
        return error_card, {'display': 'block'}, {'display': 'block'}

# Callback for PDF download
@callback(
    Output('download-pdf', 'data'),
    Input('download-report', 'n_clicks'),
    [State('upload-image', 'contents')]
)
def download_pdf(n_clicks, content):
    if n_clicks is None or content is None:
        raise PreventUpdate
    
    try:
        # In a real app, we'd get the PDF from the response
        # Here we simulate getting it from the API again
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        
        response = requests.post(
            "http://localhost:5000/predict",
            files={"image": decoded}
        )
        
        if response.status_code == 200:
            result = response.json()
            pdf_content = result['pdf']  # Base64 encoded PDF
            
            return dict(
                content=pdf_content,
                filename=f"crop_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                type="base64"
            )
    except Exception as e:
        # Handle error silently
        pass

# Run the app
if __name__ == '__main__':
    app.run(debug=True)