"""
Layout components for the Dash application.
"""

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    dbc.Row([
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
        
        dbc.Col([
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
                    
                    html.Div(id='output-image-upload'),
                    
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
            
            html.Div(id='results-container', className="results-animation", style={'display': 'none'}),
            
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