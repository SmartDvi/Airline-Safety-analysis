import pandas as pd
import dash_mantine_components as dmc
import dash_ag_grid as dag
from dash import Input, Output, callback, Dash, html, dcc
from dash_iconify import DashIconify
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils import (df_long, df_wide, colors, key_metrics,
                   available_airlines, available_improvement_status,
                   available_metrics, available_periods,
                   available_risk_categories)

# Initialize the app
app = Dash(__name__, external_stylesheets=dmc.styles.ALL)

# Custom CSS for better styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Airline Safety Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
            }
            .mantine-Paper-root {
                transition: box-shadow 0.2s ease-in-out;
            }
            .mantine-Paper-root:hover {
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            .metric-card {
                transition: transform 0.2s ease-in-out;
            }
            .metric-card:hover {
                transform: translateY(-2px);
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

# Header Component
header = dmc.Paper(
    p='md',
    mb='xl',
    style={
        'background': colors['accent_gradient'],
        'color': 'white',
        'borderRadius': '12px',
        'boxShadow': '0 4px 12px rgba(44, 90, 160, 0.2)'
    },
    children=[
        dmc.Stack(
            children=[
                dmc.Group(
                    justify="apart",
                    children=[
                        dmc.Stack(
                            gap=0,
                            children=[
                                dmc.Title("✈️ Airline Safety Analytics", order=1, c='white', size='h2'),
                                dmc.Text(
                                    "Comprehensive analysis of airline safety data from 1985-2014", 
                                    c='white',
                                    size='lg',
                                    opacity=0.9
                                )
                            ]
                        ),
                        dmc.Group(
                            children=[
                                dmc.ActionIcon(
                                    DashIconify(icon="mdi:github", width=20),
                                    variant="subtle",
                                    color="white",
                                    size="lg"
                                ),
                                dmc.ActionIcon(
                                    DashIconify(icon="mdi:information", width=20),
                                    variant="subtle",
                                    color="white",
                                    size="lg"
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# Key Metrics Cards
def create_metrics_cards():
    return dmc.Grid(
        children=[
            dmc.GridCol(span=2, children=[
                dmc.Paper(
                    className="metric-card",
                    p="md",
                    withBorder=True,
                    radius="md",
                    shadow="sm",
                    style={'backgroundColor': colors['card_bg'], 'borderLeft': f'4px solid {colors["primary"]}'},
                    children=[
                        dmc.Stack(
                            gap=0,
                            align="center",
                            children=[
                                dmc.ThemeIcon(
                                    size=40,
                                    radius="md",
                                    variant="light",
                                    color="blue",
                                    children=[DashIconify(icon="mdi:airplane", width=24)]
                                ),
                                dmc.Text("Total Airlines", size="sm", c=colors['text_secondary'], mt=5),
                                dmc.Title(f"{key_metrics['total_airlines']:,}", order=3, c=colors['text_primary'])
                            ]
                        )
                    ]
                )
            ]),
            dmc.GridCol(span=2, children=[
                dmc.Paper(
                    className="metric-card",
                    p="md",
                    withBorder=True,
                    radius="md",
                    shadow="sm",
                    style={'backgroundColor': colors['card_bg'], 'borderLeft': f'4px solid {colors["warning"]}'},
                    children=[
                        dmc.Stack(
                            gap=0,
                            align="center",
                            children=[
                                dmc.ThemeIcon(
                                    size=40,
                                    radius="md",
                                    variant="light",
                                    color="orange",
                                    children=[DashIconify(icon="mdi:alert", width=24)]
                                ),
                                dmc.Text("Total Incidents", size="sm", c=colors['text_secondary'], mt=5),
                                dmc.Title(f"{key_metrics['total_incidents']:,}", order=3, c=colors['text_primary'])
                            ]
                        )
                    ]
                )
            ]),
            dmc.GridCol(span=2, children=[
                dmc.Paper(
                    className="metric-card",
                    p="md",
                    withBorder=True,
                    radius="md",
                    shadow="sm",
                    style={'backgroundColor': colors['card_bg'], 'borderLeft': f'4px solid {colors["danger"]}'},
                    children=[
                        dmc.Stack(
                            gap=0,
                            align="center",
                            children=[
                                dmc.ThemeIcon(
                                    size=40,
                                    radius="md",
                                    variant="light",
                                    color="red",
                                    children=[DashIconify(icon="mdi:heart-broken", width=24)]
                                ),
                                dmc.Text("Total Fatalities", size="sm", c=colors['text_secondary'], mt=5),
                                dmc.Title(f"{key_metrics['total_fatalities']:,}", order=3, c=colors['text_primary'])
                            ]
                        )
                    ]
                )
            ]),
            dmc.GridCol(span=2, children=[
                dmc.Paper(
                    className="metric-card",
                    p="md",
                    withBorder=True,
                    radius="md",
                    shadow="sm",
                    style={'backgroundColor': colors['card_bg'], 'borderLeft': f'4px solid {colors["success"]}'},
                    children=[
                        dmc.Stack(
                            gap=0,
                            align="center",
                            children=[
                                dmc.ThemeIcon(
                                    size=40,
                                    radius="md",
                                    variant="light",
                                    color="green",
                                    children=[DashIconify(icon="mdi:trending-up", width=24)]
                                ),
                                dmc.Text("Improved Airlines", size="sm", c=colors['text_secondary'], mt=5),
                                dmc.Title(f"{key_metrics['improved_airlines']}", order=3, c=colors['text_primary'])
                            ]
                        )
                    ]
                )
            ]),
            dmc.GridCol(span=2, children=[
                dmc.Paper(
                    className="metric-card",
                    p="md",
                    withBorder=True,
                    radius="md",
                    shadow="sm",
                    style={'backgroundColor': colors['card_bg'], 'borderLeft': f'4px solid {colors["danger"]}'},
                    children=[
                        dmc.Stack(
                            gap=0,
                            align="center",
                            children=[
                                dmc.ThemeIcon(
                                    size=40,
                                    radius="md",
                                    variant="light",
                                    color="red",
                                    children=[DashIconify(icon="mdi:trending-down", width=24)]
                                ),
                                dmc.Text("Worsened Airlines", size="sm", c=colors['text_secondary'], mt=5),
                                dmc.Title(f"{key_metrics['worsened_airlines']}", order=3, c=colors['text_primary'])
                            ]
                        )
                    ]
                )
            ]),
            dmc.GridCol(span=2, children=[
                dmc.Paper(
                    className="metric-card",
                    p="md",
                    withBorder=True,
                    radius="md",
                    shadow="sm",
                    style={'backgroundColor': colors['card_bg'], 'borderLeft': f'4px solid {colors["accent"]}'},
                    children=[
                        dmc.Stack(
                            gap=0,
                            align="center",
                            children=[
                                dmc.ThemeIcon(
                                    size=40,
                                    radius="md",
                                    variant="light",
                                    color="cyan",
                                    children=[DashIconify(icon="mdi:shield", width=24)]
                                ),
                                dmc.Text("Avg Safety Score", size="sm", c=colors['text_secondary'], mt=5),
                                dmc.Title(f"{key_metrics['avg_safety_score']:.2f}", order=3, c=colors['text_primary'])
                            ]
                        )
                    ]
                )
            ]),
        ],
        gutter="md"
    )

# Filter Components
filters_card = dmc.Paper(
    p="md",
    withBorder=True,
    radius="md",
    shadow="sm",
    style={'backgroundColor': colors['card_bg']},
    children=[
        dmc.Stack(
            children=[
                dmc.Title("🔍 Filters & Controls", order=4, c=colors['text_primary']),
                
                dmc.MultiSelect(
                    id='time-period',
                    label='📅 Time Period',
                    data=[{'label': period, 'value': period} for period in available_periods],
                    value=available_periods,
                    clearable=True,
                    searchable=True,
                    placeholder="Select time periods...",
                    style={'marginBottom': "15px"}
                ),
                
                dmc.MultiSelect(
                    id='airlines-filter',
                    label='🏢 Airlines',
                    data=[{'label': airline, 'value': airline} for airline in available_airlines],
                    value=available_airlines[:5],
                    clearable=True,
                    searchable=True,
                    placeholder="Select airlines...",
                    style={'marginBottom': "15px"}
                ),
                
                dmc.MultiSelect(
                    id='improvement-status',
                    label='📈 Improvement Status',
                    data=[{'label': status, 'value': status} for status in available_improvement_status],
                    value=available_improvement_status,
                    clearable=True,
                    searchable=True,
                    placeholder="Select improvement status...",
                    style={'marginBottom': "15px"}
                ),
                
                dmc.MultiSelect(
                    id='risk-category',
                    label='⚠️ Risk Category',
                    data=[{'label': risk, 'value': risk} for risk in available_risk_categories],
                    value=available_risk_categories,
                    clearable=True,
                    searchable=True,
                    placeholder="Select risk categories...",
                    style={'marginBottom': "15px"}
                ),
                
                dmc.MultiSelect(
                    id='metric-type',
                    label='📊 Metric Types',
                    data=[{'label': metric.replace('_', ' ').title(), 'value': metric} for metric in available_metrics],
                    value=available_metrics,
                    clearable=True,
                    searchable=True,
                    placeholder="Select metric types...",
                    style={'marginBottom': "15px"}
                ),
                
                dmc.Button(
                    "Apply Filters",
                    id="apply-filters",
                    leftSection=DashIconify(icon="mdi:filter", width=16),
                    color="blue",
                    fullWidth=True,
                    variant="filled"
                )
            ]
        )
    ]
)

# Main Data Grid
def create_data_grid():
    columnDefs = []
    
    for col in df_wide.columns:
        columnDef = {
            'field': col,
            'headerName': col.replace('_', ' ').title(),
            'filter': True,
            'floatingFilter': True,
            'minWidth': 150,
            'resizable': True,
            'sortable': True
        }
        
        if col in df_wide.select_dtypes(include=['int', 'float']).columns:
            if 'rate' in col.lower() or 'score' in col.lower():
                columnDef['valueFormatter'] = {"function": "d3.format('.4f')(params.value)"}
            else:
                columnDef['valueFormatter'] = {"function": "d3.format(',.0f')(params.value)"}
            columnDef['type'] = 'rightAligned'
            
        columnDefs.append(columnDef)
    
    return dmc.Paper(
        p="md",
        withBorder=True,
        radius="md",
        shadow="sm",
        style={'backgroundColor': colors['card_bg']},
        children=[
            dmc.Stack(
                children=[
                    dmc.Group(
                        justify="apart",
                        children=[
                            dmc.Stack(
                                gap=0,
                                children=[
                                    dmc.Title('📋 Airline Safety Dataset', order=3, c=colors['text_primary']),
                                    dmc.Text(
                                        "Explore comprehensive airline safety data with advanced filtering and sorting", 
                                        c=colors['text_secondary'],
                                        size="sm"
                                    )
                                ]
                            ),
                            dmc.Button(
                                "Export Data",
                                leftSection=DashIconify(icon="mdi:download", width=16),
                                variant="outline",
                                color="blue"
                            )
                        ]
                    ),
                    dag.AgGrid(
                        id='airline-safety-grid',
                        columnDefs=columnDefs,
                        rowData=df_wide.to_dict('records'),
                        defaultColDef={
                            "filter": True,
                            "floatingFilter": True,
                            "resizable": True,
                            "sortable": True,
                            "editable": False
                        },
                        dashGridOptions={
                            "pagination": True,
                            "paginationPageSize": 15,
                            "animateRows": True,
                            "rowSelection": "multiple"
                        },
                        columnSize="sizeToFit",
                        style={"height": "500px", "width": "100%", "borderRadius": "8px"}
                    )
                ]
            )
        ]
    )

# Detailed Data Table for df_long
def create_detailed_table():
    columnDefs = []
    
    for col in df_long.columns:
        columnDef = {
            'field': col,
            'headerName': col.replace('_', ' ').title(),
            'filter': True,
            'floatingFilter': True,
            'minWidth': 150,
            'resizable': True,
            'sortable': True
        }
        
        if col in df_long.select_dtypes(include=['int', 'float']).columns:
            columnDef['valueFormatter'] = {"function": "d3.format(',.0f')(params.value)"}
            columnDef['type'] = 'rightAligned'
            
        columnDefs.append(columnDef)
    
    return dmc.Paper(
        p="md",
        withBorder=True,
        radius="md",
        shadow="sm",
        style={'backgroundColor': colors['card_bg']},
        children=[
            dmc.Stack(
                children=[
                    dmc.Group(
                        justify="apart",
                        children=[
                            dmc.Stack(
                                gap=0,
                                children=[
                                    dmc.Title('📊 Detailed Safety Records', order=3, c=colors['text_primary']),
                                    dmc.Text(
                                        "Detailed view of all safety incidents and metrics across time periods", 
                                        c=colors['text_secondary'],
                                        size="sm"
                                    )
                                ]
                            )
                        ]
                    ),
                    dag.AgGrid(
                        id='detailed-safety-grid',
                        columnDefs=columnDefs,
                        rowData=df_long.to_dict('records'),
                        defaultColDef={
                            "filter": True,
                            "floatingFilter": True,
                            "resizable": True,
                            "sortable": True,
                            "editable": False
                        },
                        dashGridOptions={
                            "pagination": True,
                            "paginationPageSize": 20,
                            "animateRows": True,
                            "rowSelection": "multiple"
                        },
                        columnSize="sizeToFit",
                        style={"height": "500px", "width": "100%", "borderRadius": "8px"}
                    )
                ]
            )
        ]
    )

# Analytics Tabs Component
analytics_tabs = dmc.Tabs(
    [
        dmc.TabsList(
            [
                dmc.TabsTab("📋 Detailed Data", value="detailed_data"),
                dmc.TabsTab("📊 Incident Trends", value="incident_trends"),
                dmc.TabsTab("💀 Fatalities Analysis", value="fatalities_analysis"),
                dmc.TabsTab("📈 Safety Metrics", value="safety_metrics"),
                dmc.TabsTab("🔥 Risk Analysis", value="risk_analysis"),
                dmc.TabsTab("🔄 Improvement Tracking", value="improvement_tracking"),
            ],
            grow=True
        ),
        dmc.TabsPanel(
            dmc.Container(
                create_detailed_table(),
                fluid=True, px=0
            ),
            value="detailed_data"
        ),
        dmc.TabsPanel(
            dmc.Container(
                dcc.Graph(id="incident-trends-chart"),
                fluid=True, px=0
            ),
            value="incident_trends"
        ),
        dmc.TabsPanel(
            dmc.Container(
                dcc.Graph(id="fatalities-analysis-chart"),
                fluid=True, px=0
            ),
            value="fatalities_analysis"
        ),
        dmc.TabsPanel(
            dmc.Container(
                dcc.Graph(id="safety-metrics-chart"),
                fluid=True, px=0
            ),
            value="safety_metrics"
        ),
        dmc.TabsPanel(
            dmc.Container(
                dcc.Graph(id="risk-analysis-chart"),
                fluid=True, px=0
            ),
            value="risk_analysis"
        ),
        dmc.TabsPanel(
            dmc.Container(
                dcc.Graph(id="improvement-tracking-chart"),
                fluid=True, px=0
            ),
            value="improvement_tracking"
        ),
    ],
    color="blue",
    variant="pills",
    value="detailed_data",
    id="analytics-tabs"
)

# Main Layout
app.layout = dmc.MantineProvider(
    forceColorScheme="light",
    children=[
        dmc.Container(
            fluid=True,
            size="xl",
            style={'minHeight': '100vh', 'backgroundColor': colors['background'], 'padding': '20px 0'},
            children=[
                header,
                
                # Key Metrics Cards
                create_metrics_cards(),
                
                dmc.Space(h=20),
                
                dmc.Grid(
                    children=[
                        # Filters Column
                        dmc.GridCol(
                            span=3,
                            children=[filters_card]
                        ),
                        
                        # Main Content Column
                        dmc.GridCol(
                            span=9,
                            children=[
                                dmc.Stack(
                                    children=[
                                        create_data_grid(),
                                        
                                        dmc.Paper(
                                            p="md",
                                            withBorder=True,
                                            radius="md",
                                            shadow="sm",
                                            style={'backgroundColor': colors['card_bg']},
                                            children=[
                                                dmc.Stack(
                                                    children=[
                                                        dmc.Stack(
                                                            gap=0,
                                                            children=[
                                                                dmc.Title('📈 Advanced Analytics', order=3, c=colors['text_primary']),
                                                                dmc.Text(
                                                                    'Deep dive into airline safety trends, risk patterns, and improvement metrics',
                                                                    c=colors['text_secondary'],
                                                                    size="sm"
                                                                )
                                                            ]
                                                        ),
                                                        analytics_tabs
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ],
                    gutter="lg"
                )
            ]
        )
    ]
)

# Callbacks for interactive charts
@app.callback(
    [Output("incident-trends-chart", "figure"),
     Output("fatalities-analysis-chart", "figure"),
     Output("safety-metrics-chart", "figure"),
     Output("risk-analysis-chart", "figure"),
     Output("improvement-tracking-chart", "figure")],
    [Input("apply-filters", "n_clicks")],
    [Input("time-period", "value"),
     Input("airlines-filter", "value"),
     Input("improvement-status", "value"),
     Input("risk-category", "value"),
     Input("metric-type", "value")]
)
def update_charts(n_clicks, selected_periods, selected_airlines, improvement_status, risk_categories, metric_types):
    # Filter data based on selections
    filtered_df = df_long.copy()
    
    if selected_periods:
        filtered_df = filtered_df[filtered_df['period'].isin(selected_periods)]
    if selected_airlines:
        filtered_df = filtered_df[filtered_df['airline'].isin(selected_airlines)]
    if improvement_status:
        filtered_df = filtered_df[filtered_df['improvement_status'].isin(improvement_status)]
    if risk_categories:
        filtered_df = filtered_df[filtered_df['risk_category'].isin(risk_categories)]
    if metric_types:
        filtered_df = filtered_df[filtered_df['metric_type'].isin(metric_types)]
    
    # Chart 1: Incident Trends
    incident_df = filtered_df[filtered_df['metric_type'] == 'incidents']
    fig1 = px.bar(
        incident_df,
        x="airline", y="value", color="period",
        barmode="group",
        title="✈️ Incident Trends Comparison (1985-1999 vs 2000-2014)",
        labels={'value': 'Number of Incidents', 'airline': 'Airline'},
        color_discrete_sequence=[colors['primary'], colors['accent']],
        height=500
    )
    fig1.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': colors['text_primary']},
        xaxis_tickangle=-45
    )
    
    # Chart 2: Fatalities Analysis
    fatalities_df = filtered_df[filtered_df['metric_type'] == 'fatalities']
    fig2 = px.bar(
        fatalities_df,
        x="airline", y="value", color="period",
        barmode="group",
        title="💀 Fatalities Analysis (1985-1999 vs 2000-2014)",
        labels={'value': 'Number of Fatalities', 'airline': 'Airline'},
        color_discrete_sequence=[colors['danger'], colors['warning']],
        height=500
    )
    fig2.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': colors['text_primary']},
        xaxis_tickangle=-45
    )
    
    # Chart 3: Safety Metrics Heatmap
    pivot_data = filtered_df.pivot_table(
        index="airline", 
        columns=["period", "metric_type"], 
        values="value", 
        aggfunc="sum"
    ).fillna(0)
    
    if not pivot_data.empty:
        fig3 = px.imshow(
            pivot_data,
            aspect="auto",
            title="🔥 Safety Metrics Heatmap by Airline",
            color_continuous_scale="Blues",
            height=600
        )
        fig3.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': colors['text_primary']}
        )
    else:
        fig3 = go.Figure()
        fig3.update_layout(
            title="No data available for selected filters",
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
    
    # Chart 4: Risk Analysis
    risk_analysis = filtered_df.groupby(['airline', 'risk_category'])['value'].sum().reset_index()
    if not risk_analysis.empty:
        fig4 = px.treemap(
            risk_analysis,
            path=['risk_category', 'airline'],
            values='value',
            title='⚠️ Risk Distribution Across Airlines',
            color='value',
            color_continuous_scale='RdYlGn_r',
            height=500
        )
        fig4.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': colors['text_primary']}
        )
    else:
        fig4 = go.Figure()
        fig4.update_layout(
            title="No data available for selected filters",
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
    
    # Chart 5: Improvement Tracking
    improvement_data = filtered_df.groupby(['airline', 'improvement_status'])['value'].sum().reset_index()
    if not improvement_data.empty:
        fig5 = px.sunburst(
            improvement_data,
            path=['improvement_status', 'airline'],
            values='value',
            title='🔄 Safety Improvement Tracking',
            height=500,
            color_discrete_sequence=[colors['success'], colors['warning'], colors['danger'], colors['secondary'], colors['primary']]
        )
        fig5.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': colors['text_primary']}
        )
    else:
        fig5 = go.Figure()
        fig5.update_layout(
            title="No data available for selected filters",
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
    
    return fig1, fig2, fig3, fig4, fig5

if __name__ == "__main__":
    app.run(debug=True, port=6030)