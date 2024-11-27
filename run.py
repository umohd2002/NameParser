# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 22:50:56 2024

@author: onais
"""

from waitress import serve
from FlaskApp import app  as application

# import your Flask app

serve(application, host='0.0.0.0', port=8080)