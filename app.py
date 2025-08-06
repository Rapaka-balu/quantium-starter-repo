from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load and prepare data
df = pd.read_csv("filtered_sales.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

# Create list of regions
regions = ['north', 'east', 'south', 'west', 'all']

# Start Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div(
    style={'fontFamily': 'Arial', 'padding': '20px', 'backgroundColor': '#f8f8f8'},
    children=[
        html.H1(
            "Soul Foods Pink Morsel Sales Visualiser",
            style={'textAlign': 'center', 'color': '#FF69B4'}
        ),

        html.Div([
            html.Label("Select a Region:", style={'fontWeight': 'bold'}),
            dcc.RadioItems(
                id='region-selector',
                options=[{'label': region.capitalize(), 'value': region} for region in regions],
                value='all',
                inline=True,
                style={'marginBottom': '30px'}
            )
        ]),

        dcc.Graph(id='sales-line-chart')
    ]
)

# Callback to update graph based on region
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-selector', 'value')
)
def update_chart(selected_region):
    # Filter the data
    if selected_region == 'all':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['region'] == selected_region]

    # Group by date
    daily_sales = filtered_df.groupby('date', as_index=False)['sales'].sum()

    # Create line chart
    fig = px.line(
        daily_sales,
        x='date',
        y='sales',
        title=f"Sales Over Time - {selected_region.capitalize()} Region" if selected_region != 'all' else "Sales Over Time - All Regions",
        labels={'date': 'Date', 'sales': 'Total Sales ($)'}
    )

    # Add vertical line for price increase
    fig.update_layout(
        shapes=[
            dict(
                type="line",
                x0="2021-01-15",
                x1="2021-01-15",
                y0=0,
                y1=1,
                xref='x',
                yref='paper',
                line=dict(color="red", width=2, dash="dash")
            )
        ],
        annotations=[
            dict(
                x="2021-01-15",
                y=1,
                xref='x',
                yref='paper',
                text="Price Increase",
                showarrow=False,
                font=dict(color="red", size=12)
            )
        ],
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
