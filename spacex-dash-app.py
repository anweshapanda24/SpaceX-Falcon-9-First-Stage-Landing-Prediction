# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Get launch sites
launch_sites = spacex_df['Launch Site'].unique()

# Create app layout
app.layout = html.Div(children=[

    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),

    # TASK 1: Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in launch_sites],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie Chart
    html.Div(
        dcc.Graph(id='success-pie-chart')
    ),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Range Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={
            0: '0',
            2500: '2500',
            5000: '5000',
            7500: '7500',
            10000: '10000'
        },
        value=[0, 10000]
    ),

    html.Br(),

    # TASK 4: Scatter Plot
    html.Div(
        dcc.Graph(id='success-payload-scatter-chart')
    )

])

# TASK 2 CALLBACK
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):

    if selected_site == 'ALL':

        success_counts = spacex_df.groupby(
            'Launch Site'
        )['class'].sum().reset_index()

        fig = px.pie(
            success_counts,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )

        return fig

    else:

        filtered_df = spacex_df[
            spacex_df['Launch Site'] == selected_site
        ]

        outcome_counts = filtered_df['class'].value_counts().reset_index()
        outcome_counts.columns = ['Outcome', 'Count']

        fig = px.pie(
            outcome_counts,
            values='Count',
            names='Outcome',
            title=f'Success vs Failure for {selected_site}'
        )

        return fig


# TASK 4 CALLBACK
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter_plot(selected_site, payload_range):

    low, high = payload_range

    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if selected_site == 'ALL':

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs Launch Success for All Sites'
        )

        return fig

    else:

        filtered_df = filtered_df[
            filtered_df['Launch Site'] == selected_site
        ]

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs Launch Success for {selected_site}'
        )

        return fig


# Run the app
if __name__ == '__main__':
    app.run()