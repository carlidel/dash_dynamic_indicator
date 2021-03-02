import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from wsgi import app
from layouts import layout_1, layout_2, layout_3, layout_4
import callbacks

index_layout = html.Div([
    html.H1("INDEX"),
    html.Br(),
    dcc.Link('Go to Heatmap dashboard', href='/apps/heatmaps'),
    html.Br(),
    dcc.Link('Go to Correlation Plots dashboard', href='/apps/correlations'),
    html.Br(),
    dcc.Link('Go to Heatmap comparison dashboard', href='/apps/differences'),
    html.Br(),
    dcc.Link('Go to Resonance plots dashboard', href='/apps/resonance'),
    html.Br(),
    dcc.Link('Go to Confusion plots dashboard', href='/apps/confusion'),
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=index_layout)
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/heatmaps':
        return html.Div([
            dbc.Toast(
                "Plot(s) Updated!",
                id="notification-toast-1",
                header="Notification",
                icon="primary",
                is_open=False,
                dismissable=True,
                duration=4000,
                # top: 66 positions the toast below the navbar
                style={"position": "fixed", "top": 5,
                       "right": 10, "width": 350},
            ),
            html.H1("Heatmaps Dashboard"),
            html.H3("General dashboard for visualizing differend indicators on a single webpage."),
            html.Br(),
            dcc.Link("Go back to index.", href="/"),
            html.Br(),
            layout_1
        ])
    elif pathname == '/apps/correlations':
        return html.Div([
            dbc.Toast(
                "Plot(s) Updated!",
                id="notification-toast-2",
                header="Notification",
                icon="primary",
                is_open=False,
                dismissable=True,
                duration=4000,
                # top: 66 positions the toast below the navbar
                style={"position": "fixed", "top": 5,
                       "right": 10, "width": 350},
            ),
            html.H1("Correlation dashboard"),
            html.H3(
                "Choose two different dynamic (or generic) indicators and observe the resulting correlation plots."),
            html.Br(),
            dcc.Link("Go back to index.", href="/"),
            html.Br(),
            layout_2
        ])
    elif pathname == '/apps/differences':
        return html.Div([
            dbc.Toast(
                "Plot(s) Updated!",
                id="notification-toast-3",
                header="Notification",
                icon="primary",
                is_open=False,
                dismissable=True,
                duration=4000,
                # top: 66 positions the toast below the navbar
                style={"position": "fixed", "top": 5,
                       "right": 10, "width": 350},
            ),
            html.H1("Heatmaps Comparison Dashboard"),
            html.H3(
                "Choose two similar heatmpas and observe the resulting difference on a third heatmap."),
            html.Br(),
            dcc.Link("Go back to index.", href="/"),
            html.Br(),
            layout_3
        ])
    elif pathname == '/apps/resonance':
        return html.Div([
            dbc.Toast(
                "Plot(s) Updated!",
                id="notification-toast-4",
                header="Notification",
                icon="primary",
                is_open=False,
                dismissable=True,
                duration=4000,
                # top: 66 positions the toast below the navbar
                style={"position": "fixed", "top": 5,
                       "right": 10, "width": 350},
            ),
            html.H1("Resonance Dashboard"),
            html.H3(
                "General dashboard for visualizing resonances both in the action space and in the frequency space."),
            html.Br(),
            dcc.Link("Go back to index.", href="/"),
            html.Br(),
            layout_4
        ])
    else:
        return index_layout


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8080)
