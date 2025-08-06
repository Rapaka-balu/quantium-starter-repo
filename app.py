import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load the processed data
df = pd.read_csv("filtered_sales.csv")

# Convert 'date' to datetime
df['date'] = pd.to_datetime(df['date'])

# Sort by date
df = df.sort_values(by='date')

# Group by date and sum sales across all regions
daily_sales = df.groupby('date', as_index=False)['sales'].sum()

# Create the line chart
fig = px.line(
    daily_sales,
    x='date',
    y='sales',
    title='Pink Morsel Sales Over Time',
    labels={'date': 'Date', 'sales': 'Total Sales ($)'}
)

# Add vertical line for Jan 15, 2021 price increase
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
            font=dict(color="red")
        )
    ]
)





# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods Pink Morsel Sales Visualiser"),
    dcc.Graph(
        id='sales-line-chart',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)

