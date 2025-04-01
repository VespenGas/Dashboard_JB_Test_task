#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 00:51:00 2025

@author: Evgeny Manturov eugen.m4nt@gmail.com
"""
import dash_bio as dashbio
import polars as pl
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import os

from dash import Dash, dcc, html, Input, Output
from flask import Flask, redirect, url_for

def fix_formatting(df: pd.DataFrame):
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
    return df.unique()

def df_prep(filename: str = 'NIHMS1635539-supplement-1635539_Sup_tab_4.xlsx') -> pd.DataFrame:
    df = pl.read_excel(filename, sheet_name='S4B limma results')
    df = fix_formatting(df)
    #Avoid 0 p-value since log does not exist at 0
    df = df.filter(pl.col('adj.P.Val') != 0)
    return df.to_pandas()

def df_vals_prep(filename: str = 'NIHMS1635539-supplement-1635539_Sup_tab_4.xlsx') -> pl.DataFrame:
    df = pl.read_excel(filename, sheet_name='S4A values')
    df = fix_formatting(df)
    return df

#Server definitions
server = Flask(__name__)
dash_app = Dash(
    __name__,
    server=server,
    url_base_pathname='/dash/',
)

df = df_prep()
df_vals = df_vals_prep()

def get_YO_cols(first_datacol:str = 'Set002.H4.OD12.dup'):
    out = {'YD':[], 'OD':[]}
    datacols = df_vals.columns[df_vals.columns.index(first_datacol):]
    for col in datacols:
        if 'YD' in col and 'OD' in col:
            print(f'Undetermined subset: {col}')
            continue
        elif 'YD' in col:
            out['YD'].append(col)
        elif 'OD' in col:
            out['OD'].append(col)
        #Optional else
        else:
            print(f'Neither subset: {col}')
    return out

first_datacol = 'Set002.H4.OD12.dup'
datacols = get_YO_cols(first_datacol)

@dash_app.callback(
    Output('boxplots', 'figure'),
    Input('volcano-plot', 'clickData')
    )
def draw_boxplot_from_data(click_data) -> go.Figure:
    if not click_data:
        return {}
    clicked_protein = click_data['points'][0]['text']
    #Gene not needed for now
    clicked_protein_snp, _ = [i.partition(': ')[-1] for i in clicked_protein.split('<br>')]
    if clicked_protein_snp not in df_vals['ProteinID']:
        print('Gene not found!')
        return {}
    
    datacols_out = dict()
    row = df_vals.filter(pl.col('ProteinID') == clicked_protein_snp)
    datacols_out['YD'] = row[datacols['YD']].transpose().to_series().to_list()
    datacols_out['OD'] = row[datacols['OD']].transpose().to_series().to_list()
    df = pd.DataFrame(datacols_out)
    fig = px.box(
        df,
        title="Box plot of protein concentration distribution",
        labels={
            'variable': 'Donor age',
            'value': 'Protein concentration',
            },
        
        )
    #Optional range tweaks
    fig.update_yaxes(range=[0, 15], autorange=False)
    fig.update_yaxes(griddash='dash', gridcolor='grey', gridwidth=1)
    return fig

dash_app.layout = html.Div([
    html.H1("Gene dashboard"),
    html.Div([
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
                genomewideline_value=1.3,
                highlight=False,
                )
            ),
        dcc.Graph(
            id='boxplots'
        )
    ]),
])

@server.route('/')
def index():
    return redirect(url_for('/dash/'), code=302)

if __name__ == '__main__':
    server.run(host='0.0.0.0',
               port=int(os.environ.get('PORT', 8855)),
               debug=False,)
