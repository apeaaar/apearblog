"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from app import fapp



fapp.run(debug=True,port=5024,host="0.0.0.0")