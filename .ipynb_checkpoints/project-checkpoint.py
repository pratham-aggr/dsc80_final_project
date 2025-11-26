import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import matplotlib.pyplot as plt

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
