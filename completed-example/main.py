import pandas as pd
import streamlit as st
import plotly.graph_objects as go

import helpers as helpers


# Configure Streamlit styling
st.set_page_config(layout='wide')

# SIDEBAR
st.sidebar.markdown('# Canada COVID-19 Tracker')

# Load provinces & generate sidebar filter
province_df = helpers.load_provinces()
selected_province = st.sidebar.selectbox(
    'Select a Province',
    province_df['name'],
    index=8  # Alberta
)
selected_province_code = province_df[province_df['name'] == selected_province]['code'].iloc[0]
selected_province_population = province_df[province_df['name'] == selected_province]['population'].iloc[0]
st.sidebar.write(province_df[province_df['name'] == selected_province])

# Load province case/vaccination data using selected province
df = helpers.load_data(selected_province_code, selected_province_population)


# Generate hero cards in columns
_, c1, c2, c3, _, = st.beta_columns((1, 3, 3, 3, 1))
c1.markdown(
    helpers.generate_hero_card(
        f'{df["total_cases"].iloc[-1]:,.0f}<small>&nbsp;&nbsp;({df["change_cases"].iloc[-2]:+,.0f})</small>',
        'Total Cases'
    ),
    unsafe_allow_html=True
)

c2.markdown(
    helpers.generate_hero_card(
        f'{df["active_cases"].iloc[-1]:,.0f}<small>&nbsp;&nbsp;({df["delta_active"].iloc[-2]:+,.0f})</small>',
        'Active Cases'
    ),
    unsafe_allow_html=True
)

c3.markdown(
    helpers.generate_hero_card(
        f'{df["total_vaccinations"].iloc[-1]:,.0f}<small>&nbsp;&nbsp;'
        f'({df["change_vaccinations"].iloc[-2]:+,.0f})</small>',
        'Vaccinations'
    ),
    unsafe_allow_html=True
)

# Generate gutter columns
_, c1, _ = st.beta_columns((1, 9, 1))

# Generate plotting df using pandas.melt()
pdf = pd.melt(df, id_vars=['date'])

# Generate active cases figure
active_fig = go.Figure()
active_fig.add_trace(go.Scatter(
    x=pdf[(pdf['variable'] == 'active_cases')]['date'],
    y=pdf[(pdf['variable'] == 'active_cases')]['value'],
    mode='lines',
    stackgroup='one',
    name='Active Cases'
))
active_fig.add_trace(go.Scatter(
    x=pdf[(pdf['variable'] == 'active_7_day')]['date'],
    y=pdf[(pdf['variable'] == 'active_7_day')]['value'],
    mode='lines',
    name='7 Day Average'
))
active_fig.update_layout(
    title='Active Cases',
    margin=dict(l=10, r=10, t=60, b=10),
    colorway=helpers.COLORWAY_LIST,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)
c1.plotly_chart(active_fig, use_container_width=True)

# Vaccinations
vacc_fig = go.Figure()
vacc_fig.add_trace(go.Scatter(
    x=pdf[(pdf['variable'] == 'percent_vaccinated') & (pdf['value'] > 0)]['date'],
    y=pdf[(pdf['variable'] == 'percent_vaccinated') & (pdf['value'] > 0)]['value'],
    mode='lines',
    stackgroup='one',
))
vacc_fig.update_layout(
    title='Percentage of Population Vaccinated',
    margin=dict(l=10, r=10, t=60, b=10),
    yaxis=dict(
        type='linear',
        range=[1, 100],
        ticksuffix='%'
    ),
    colorway=helpers.COLORWAY_LIST[3:]
)
c1.plotly_chart(vacc_fig, use_container_width=True)

# Generate gutter columns
_, c1, _ = st.beta_columns((1, 9, 1))

# Show data in expander
with c1.beta_expander('Show Raw Data'):
    st.write(df)
