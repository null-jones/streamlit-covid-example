import pandas as pd
import streamlit as st

# Plotting colors
COLORWAY_LIST = [
    '#00a5bb',
    '#f79141',
    '#499585',
    '#d81e52',
    '#6cb2c5',
    '#6c77c5',
    '#c5ba6c',
    '#56ce93',
    '#d88fBf',
    '#ffd505',
]


@st.cache
def load_provinces():
    '''Loads list of provinces from API'''
    return pd.read_json('https://api.covid19tracker.ca/provinces')


@st.cache
def load_data(province_code, population):
    '''Loads provincial case data w/ provided province code'''
    df = pd.json_normalize(
        pd.read_json(f'https://api.covid19tracker.ca/reports/province/{province_code.lower()}')['data']
    )

    df['active_cases'] = df['change_cases'].rolling(14).sum()
    df['active_7_day'] = df['active_cases'].rolling(7).mean()
    df['delta_active'] = df['active_cases'].rolling(2).apply(lambda x: x[-1] - x[0], raw=True)
    df['percent_vaccinated'] = (df['total_vaccinations'] / population) * 100
    df['test_positivity'] = df['']

    return df


@st.cache
def generate_hero_card(title, subtitle):
    '''Generates HTML string for card'''
    return f'''
        <div style='text-align: center'>
            <h1 style='margin-top: 0; padding-top: 0.2rem;'>{title}</h1>
            <h2 style='margin-top: 0; padding-top: 0'>{subtitle}</h2>
        </div>
    '''
