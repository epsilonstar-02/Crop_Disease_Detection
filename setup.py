from setuptools import setup, find_packages

setup(
    name="crop_disease_detection",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-cors",
        "torch",
        "torchvision",
        "timm",
        "pillow",
        "google-generativeai",
        "reportlab",
        "python-dotenv",
        "python-dateutil",
        "dash",
        "dash-bootstrap-components",
        "requests"
    ],
) 