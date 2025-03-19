#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 00:51:00 2025

@author: Evgeny Manturov eugen.m4nt@gmail.com
"""

import dash
import dash_core_components as dcc
import dash_html_components as html

from flask import Flask, jsonify, make_response

server = Flask(__name__)

dash_app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname='/dash/',
)

dash_app.layout = html.Div([
    html.H1("Gene dashboard will be here"),
])

@server.route('/')
def index():
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp

if __name__ == '__main__':
    server.run(host='0.0.0.0',
               port=8855,
               debug=True,)
