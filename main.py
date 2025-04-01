#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 00:51:00 2025

@author: Evgeny Manturov eugen.m4nt@gmail.com
"""
import pandas as pd
import polars as pl
from dash import Dash, dcc, html
import numpy as np
import dash_bio as dashbio
from flask import Flask, jsonify

def fix_formatting(df):
    df[0, 0] = 'ProteinID'
    df.columns = df.row(0)
    df = df[1:, :]
    for column in df.columns:
        try:
            df = df.with_columns(
                [
                    pl.col(column).cast(pl.Float64, strict=True),
                ]
            )
        except:
            pass
    return df

def df_prep(filename: str = 'NIHMS1635539-supplement-1635539_Sup_tab_4.xlsx'):
    df = pl.read_excel(filename, sheet_name='S4B limma results')
    df = fix_formatting(df)
    #Avoid 0 p-value since log does not exist at 0
    df = df.filter(pl.col('adj.P.Val') != 0)
    return df.to_pandas()

def df_vals_prep(filename: str = 'NIHMS1635539-supplement-1635539_Sup_tab_4.xlsx'):
    df = pl.read_excel(filename, sheet_name='S4A values')
    df = fix_formatting(df)
    #Parse YD/OD?
    
    return df.to_pandas()

server = Flask(__name__)
dash_app = Dash(
    __name__,
    server=server,
    url_base_pathname='/dash/',
)

df = df_prep()

dash_app.layout = html.Div([
    html.H1("Gene dashboard will be here"),
    html.Div(
        dcc.Graph(
            id = 'volcano-plot',
            figure=dashbio.VolcanoPlot(
                #Only accepts pandas
                dataframe = df,
                effect_size='logFC',
                p='adj.P.Val',
                snp='ProteinID',
                gene='EntrezGeneSymbol',
                title='Gene volcano plot',
                xlabel='Fold Change (log2)',
                ylabel='Neg log10 adj p-value',
                point_size=5,
                logp=True,
                genomewideline_width=1,
                )
            ),
    ),
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
