"""
Dash callbacks for the frontend application.
"""

from dash import Input, Output, State, callback, html, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import base64
from io import BytesIO
from PIL import Image

from frontend.utils import (
    parse_image_content,
    get_image_details,
    api_predict,
    format_treatment_points,
    get_severity,
    get_spread_risk,
    get_treatment_cost
)


def register_callbacks(app):
    """
    Register all callbacks for the Dash application.
    
    Args:
        app: The Dash application instance
    """
    
    @callback(
        [Output('output-image-upload', 'children'),
         Output('analyze-button', 'disabled')],
        [Input('upload-image', 'contents')],
        [State('upload-image', 'filename')]
    )
    def update_output(content, filename):
        """
        Update the output based on the uploaded image.
        """
        if content is None:
            return None, True
        
        try:
            decoded = parse_image_content(content)
            
            width, height, img_format, img_size = get_image_details(decoded)
            
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
                    f"There was an error processing this file: {str(e)}"
                ], color="danger")
            ]), True

    @callback(
        [Output('results-container', 'children'),
         Output('results-container', 'style'),
         Output('tips-card', 'style')],
        [Input('analyze-button', 'n_clicks')],
        [State('upload-image', 'contents')]
    )
    def analyze_image(n_clicks, content):
        """
        Analyze the uploaded image when the analyze button is clicked.
        """
        if n_clicks is None or n_clicks == 0 or content is None:
            raise PreventUpdate
        
        try:
            decoded = parse_image_content(content)
            
            try:
                result = api_predict(decoded)
                
                disease = result['disease']
                recommendation = result['recommendation']
                confidence = result.get('confidence', 92)
                
                treatment_points = format_treatment_points(recommendation)
                
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
                                            dbc.Progress(value=confidence, color="success", className="mb-2 progress-custom"),
                                            html.P(f"{confidence}% confidence", className="text-muted small")
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
                                                    html.H3(get_severity(disease), className="text-warning text-center mb-1"),
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
                                                    html.H3(get_spread_risk(disease), className="text-danger text-center mb-1"),
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
                                                    html.H3(get_treatment_cost(disease), className="text-success text-center mb-1"),
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
                                                                "Monitor progress and reapply treatments as needed."
                                                            ], className="mb-0")
                                                        ], width=10)
                                                    ], className="mb-3"),
                                                    dbc.Row([
                                                        dbc.Col([
                                                            html.Div(className="icon-circle", style={"backgroundColor": "rgba(52, 152, 219, 0.1)", "color": "#3498DB", "width": "40px", "height": "40px"}, children=[
                                                                html.I(className="fas fa-calendar-alt fa-lg")
                                                            ])
                                                        ], width=2),
                                                        dbc.Col([
                                                            html.P([
                                                                html.Span("Long-term: ", className="fw-bold"), 
                                                                "Implement preventative measures for future crops."
                                                            ], className="mb-0")
                                                        ], width=10)
                                                    ])
                                                ])
                                            ], className="bg-light", style={"borderRadius": "12px", "border": "none"})
                                        ], width=12)
                                    ]),
                                    
                                    dbc.Row([
                                        dbc.Col([
                                            html.Div([
                                                dbc.Button([
                                                    html.I(className="fas fa-file-download me-2"), 
                                                    "Download PDF Report"
                                                ], 
                                                id="download-report", 
                                                className="btn-custom-primary w-100 mt-4",
                                                size="lg")
                                            ]),
                                            dcc.Download(id="download-pdf")
                                        ], width=12)
                                    ])
                                ])
                            ], label="Treatment", tab_id="tab-treatment", className="fancy-tab")
                        ], active_tab="tab-diagnosis", className="mb-3")
                    ])
                ], className="app-card mb-4")
                
                return results_card, {'display': 'block'}, {'display': 'none'}
                
            except Exception as e:
                error_card = dbc.Card([
                    dbc.CardBody([
                        dbc.Alert([
                            html.I(className="fas fa-exclamation-circle me-2"),
                            f"Error connecting to the API: {str(e)}"
                        ], color="danger")
                    ])
                ], className="app-card mb-4")
                
                return error_card, {'display': 'block'}, {'display': 'block'}
            
        except Exception as e:
            error_card = dbc.Card([
                dbc.CardBody([
                    dbc.Alert([
                        html.I(className="fas fa-exclamation-circle me-2"),
                        f"Error processing image: {str(e)}"
                    ], color="danger")
                ])
            ], className="app-card mb-4")
            
            return error_card, {'display': 'block'}, {'display': 'block'}

    @callback(
        Output('download-pdf', 'data'),
        Input('download-report', 'n_clicks'),
        [State('upload-image', 'contents')]
    )
    def download_pdf(n_clicks, content):
        """
        Download the PDF report when the download button is clicked.
        """
        if n_clicks is None or n_clicks == 0 or content is None:
            raise PreventUpdate
        
        try:
            decoded = parse_image_content(content)
            result = api_predict(decoded)
            
            disease = result['disease']
            recommendation = result['recommendation']
            confidence = result.get('confidence', 92)
            
            if result.get('pdf') and result['pdf'] is not None:
                import base64
                pdf_data = base64.b64decode(result['pdf'])
                return dcc.send_bytes(pdf_data, f"crop_disease_report.pdf")
            
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle(
                'Title',
                parent=styles['Heading1'],
                fontSize=20,
                textColor=colors.darkgreen,
                spaceAfter=24
            )
            
            heading_style = ParagraphStyle(
                'Heading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.darkblue,
                spaceBefore=12,
                spaceAfter=6
            )
            
            elements = []
            
            elements.append(Paragraph("Crop Disease Analysis Report", title_style))
            elements.append(Spacer(1, 0.25*inch))
            
            if content:
                try:
                    img_data = parse_image_content(content)
                    img = Image.open(BytesIO(img_data))
                    
                    img_buffer = BytesIO()
                    img.save(img_buffer, format='PNG')
                    img_buffer.seek(0)
                    
                    img_width, img_height = img.size
                    aspect = img_height / float(img_width)
                    max_width = 4 * inch
                    
                    image = RLImage(img_buffer, width=max_width, height=(max_width * aspect))
                    elements.append(image)
                    elements.append(Spacer(1, 0.25*inch))
                except Exception as e:
                    elements.append(Paragraph(f"Error including image: {str(e)}", styles["BodyText"]))
                    elements.append(Spacer(1, 0.25*inch))
            
            elements.append(Paragraph("Detected Disease", heading_style))
            elements.append(Paragraph(disease, styles["BodyText"]))
            elements.append(Spacer(1, 0.2*inch))
            
            elements.append(Paragraph("Confidence Score", heading_style))
            elements.append(Paragraph(f"{confidence:.1f}%", styles["BodyText"]))
            elements.append(Spacer(1, 0.2*inch))
            
            elements.append(Paragraph("Treatment Recommendations", heading_style))
            treatment_points = format_treatment_points(recommendation)
            
            for point in treatment_points:
                elements.append(Paragraph(f"• {point}", styles["BodyText"]))
            
            elements.append(Spacer(1, 0.2*inch))
            
            doc.build(elements)
            buffer.seek(0)
            
            return dcc.send_bytes(buffer.getvalue(), f"crop_disease_report.pdf")
        except Exception as e:
            return dict(
                content=f"Error generating PDF: {str(e)}",
                filename="error_report.txt"
            ) 