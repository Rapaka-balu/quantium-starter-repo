from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv("filtered_sales.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

regions = ['north', 'east', 'south', 'west', 'all']
region_labels = ['North', 'East', 'South', 'West']

app = Dash(__name__)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background: linear-gradient(135deg, #181b27 0%, #2f2f38 100%);
                min-height: 100vh;
            }
            .radio-custom label {
                background: #242934;
                padding: 9px 18px;
                border-radius: 22px;
                margin: 0 7px;
                font-weight: bold;
                font-size: 16px;
                transition: box-shadow 0.2s, background 0.2s, color 0.2s;
                cursor: pointer;
                border: 1.8px solid #FF69B4;
                color: #FF69B4;
                box-shadow: 0 1.5px 10px 0 rgba(255,105,180,0.08);
            }
            .radio-custom input[type="radio"] {
                display: none;
            }
            .radio-custom label:hover, .radio-custom input[type="radio"]:checked + label {
                background: linear-gradient(90deg, #17141f 0%, #FF69B4 110%);
                color: white;
                border: 1.8px solid #FF69B4;
                box-shadow: 0 2px 16px 0 rgba(255,105,180,0.25);
            }
            .modern-btn {
                background: linear-gradient(90deg, #FF69B4 25%, #5e2750 100%);
                border: none;
                color: #fff;
                border-radius: 25px;
                font-size: 16px;
                padding: 10px 28px;
                font-weight: bold;
                box-shadow: 0 2px 18px 0 rgba(255,105,180,0.17);
                margin-left: 20px;
                cursor: pointer;
                transition: background 0.18s, transform 0.18s, box-shadow 0.18s;
            }
            .modern-btn:hover {
                background: linear-gradient(90deg, #5e2750 10%, #FF69B4 100%);
                color: #fff;
                transform: translateY(-2px) scale(1.04);
                box-shadow: 0 4px 32px 0 rgba(255,105,180,0.38);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div(
    style={
        'fontFamily': 'Arial',
        'padding': '20px 0',
        'maxWidth': '1000px',
        'margin': 'auto'
    },
    children=[
        html.H1(
            "Soul Foods Pink Morsel 3D Sales Visualiser",
            style={'textAlign': 'center', 'color': '#FF69B4', 'marginBottom': '38px', 'letterSpacing': '1px'}
        ),
        html.Div([
            html.Label("Select a Region:", style={'fontWeight': 'bold', 'fontSize': '17.5px', 'marginRight': '13px', 'color': '#fae4ee'}),
            html.Span([
                dcc.RadioItems(
                    id='region-selector',
                    options=[{'label': region.capitalize(), 'value': region} for region in regions],
                    value='all',
                    inline=True,
                    className="radio-custom",
                    inputStyle={'marginRight': '7px'}
                )
            ]),
            html.Button(
                "Apply Filter",
                id="apply-btn",
                className="modern-btn",
                n_clicks=0
            ),
        ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'marginBottom': '32px', 'gap': '17px'}),
        html.Div([
            dcc.Graph(id='sales-3d-chart', config={'displayModeBar': True}),
        ], style={
            'padding': '20px',
            'background': 'rgba(24,27,39,0.97)',
            'borderRadius': '12px',
            'boxShadow': '0 2px 18px 0 rgba(255,105,180,0.045)'
        })
    ]
)

@app.callback(
    Output('sales-3d-chart', 'figure'),
    [Input('region-selector', 'value'), Input('apply-btn', 'n_clicks')]
)
def update_3d_chart(selected_region, n_clicks):
    traces = []
    show_regions = regions[:-1] if selected_region == 'all' else [selected_region]

    color_map = {
        'north': '#8e54e9',
        'east': '#FF69B4',
        'south': '#52e5e7',
        'west': '#f7971e'
    }

    for idx, reg in enumerate(show_regions):
        region_df = df if selected_region == 'all' else df[df['region'] == reg]
        if selected_region == 'all':
            region_df = df[df['region'] == reg]

        daily = region_df.groupby('date', as_index=False)['sales'].sum()
        # Y is region index for visual track separation
        traces.append(go.Scatter3d(
            x=daily['date'],
            y=[idx]*len(daily),
            z=daily['sales'],
            mode='lines+markers',
            name=reg.capitalize(),
            line=dict(color=color_map.get(reg, '#FF69B4'), width=7),
            marker=dict(size=4, color=color_map.get(reg, '#FF69B4')),
            hovertemplate=f"Region: {reg.capitalize()}<br>Date: %{{x|%Y-%m-%d}}<br>Sales: $%{{z}}<extra></extra>",
        ))

    # Price increase indicator as 3D mark
    date_loc = pd.to_datetime("2021-01-15")
    for idx, reg in enumerate(show_regions):
        traces.append(go.Scatter3d(
            x=[date_loc], y=[idx], z=[df[df['date']==date_loc]['sales'].max() or 0],
            mode='markers+text',
            text=["<b>💲 Price Jump!</b>"],
            textposition="top center",
            marker=dict(size=14, color="#FF69B4", symbol="diamond"),
            hoverinfo='skip',
            showlegend=False
        ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='Date', backgroundcolor='#101013', color='#e4e2ee', showbackground=True, gridcolor="#40404a"),
            yaxis=dict(
                title='Region',
                tickvals=list(range(len(show_regions))),
                ticktext=[r.capitalize() for r in show_regions],
                backgroundcolor='#101013',
                color='#e4e2ee',
                showbackground=True,
                gridcolor="#40404a",
            ),
            zaxis=dict(title='Sales ($)', backgroundcolor='#101013', color='#e4e2ee', showbackground=True, gridcolor="#40404a"),
        ),
        margin=dict(t=65, r=20, l=20, b=30),
        plot_bgcolor='#181b27',
        paper_bgcolor='rgba(24,27,39,0.85)',
        title={
            'text': "3D Sales Visualisation" if selected_region == 'all' else f"3D Sales: {selected_region.capitalize()} Region",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(color="#f6a8d6", size=24, family="Arial Black")
        },
        legend=dict(bgcolor="#21213a", font=dict(color="#FF69B4", size=15)),
        height=680
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
