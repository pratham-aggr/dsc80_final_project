import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import folium
import requests

def get_variable_lists():
    categorical_vars = [
        'u.s._state',
        'nerc.region',
        'climate.region',
        'climate.category',
        'cause.category',
        'cause.category.detail'
    ]

    numeric_vars = [
        'anomaly.level (numeric)',
        'demand.loss.mw (megawatt)',
        'customers.affected',
        'res.price (cents / kilowatt-hour)',
        'com.price (cents / kilowatt-hour)',
        'ind.price (cents / kilowatt-hour)',
        'total.price (cents / kilowatt-hour)',
        'res.sales (megawatt-hour)',
        'com.sales (megawatt-hour)',
        'ind.sales (megawatt-hour)',
        'total.sales (megawatt-hour)',
        'res.percen (%)',
        'com.percen (%)',
        'ind.percen (%)',
        'res.customers',
        'com.customers',
        'ind.customers',
        'total.customers',
        'res.cust.pct (%)',
        'com.cust.pct (%)',
        'ind.cust.pct (%)',
        'pc.realgsp.state (usd)',
        'pc.realgsp.usa (usd)',
        'pc.realgsp.rel (fraction)',
        'pc.realgsp.change (%)',
        'util.realgsp (usd)',
        'total.realgsp (usd)',
        'util.contri (%)',
        'pi.util.ofusa (%)',
        'population',
        'poppct_urban (%)',
        'poppct_uc (%)',
        'popden_urban (persons per square mile)',
        'popden_uc (persons per square mile)',
        'popden_rural (persons per square mile)',
        'areapct_urban (%)',
        'areapct_uc (%)',
        'pct_land (%)',
        'pct_water_tot (%)',
        'pct_water_inland (%)'
    ]

    datetime_vars = [
        'outage_start',
        'outage_restore'
    ]

    return categorical_vars, numeric_vars, datetime_vars

def plot_single_bar(df,col,color = None):
    vc = df[col].value_counts(normalize=True).reset_index()
    vc.columns = [col, 'proportion']
    fig = make_subplots(rows = 1, cols = 1, subplot_titles = [col])
    fig.add_trace(go.Bar(x=vc[col], y=vc['proportion'], marker_color = color), row=1, col=1)
    
    fig.update_layout(height=500, width=500, title=col)
    return fig
    #courtesy plotly subplots reference: https://plotly.com/python/subplots

def plot_multiple_bars(df, columns ,title = 'Distributions'):
    n = len(columns)
    cols = 3
    rows = (n + cols - 1) // cols
    
    
    fig = make_subplots(rows=rows, cols=cols, subplot_titles=columns)
    
    row, col = 1, 1
    
    for var in columns:
        vc = df[var].value_counts(normalize=True).reset_index()
        vc.columns = [var, 'proportion']
        fig.add_trace(go.Bar(x=vc[var], y=vc['proportion']), row=row, col=col)
        col += 1
        if col > cols:
            col = 1
            row += 1
            
    fig.update_layout(height=500 * rows, width=1200, title=title)
    return fig
def plot_state_choropleth(df, value_col, aggfunc = 'mean'):
    map_df = df.groupby('u.s._state')[value_col].agg(aggfunc).reset_index()
    m = folium.Map([43, -100], zoom_start=4)
    us_states = requests.get(
        "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
    ).json()
    
    folium.Choropleth(
        geo_data=us_states,
        data=map_df,
        columns=["u.s._state", value_col],
        key_on="feature.properties.name",
        line_opacity = 0.9,
        fill_color="YlGn"
    ).add_to(m)
    return m
#courtesy folium choropleth reference: https://python-visualization.github.io/folium/latest/user_guide/geojson/choropleth.html

    