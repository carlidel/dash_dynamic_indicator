import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash
import numpy as np
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State, MATCH, ALL
import data_handler as dh
from data_handler import TUNE_X_data_handler, TUNE_Y_data_handler
from plotly.subplots import make_subplots
from flask_caching import Cache
import os
import glob
from datetime import datetime
from tqdm import tqdm
import matplotlib.cm
import scipy.ndimage

from layouts import layout_1, layout_2, layout_3, layout_4, layout_5, layout_6, layout_7

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
application = app.server


cache = Cache(app.server, config={
    'CACHE_TYPE': 'SimpleCache',
})
# For security... let's just clean the cache every 48 hours.
CACHE_TIMEOUT = 48 * 60 * 60

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
    html.Br(),
    dcc.Link('Go to Time Evolution dashboard', href='/apps/evolution'),
    html.Br(),
    dcc.Link('Go to Convoltuion dashboard', href='/apps/convolution'),
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
                "Choose two similar heatmaps and observe the resulting difference on a third heatmap."),
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
    elif pathname == '/apps/confusion':
        return html.Div([
            dbc.Toast(
                "Plot(s) Updated!",
                id="notification-toast-5",
                header="Notification",
                icon="primary",
                is_open=False,
                dismissable=True,
                duration=4000,
                # top: 66 positions the toast below the navbar
                style={"position": "fixed", "top": 5,
                       "right": 10, "width": 350},
            ),
            html.H1("Confusion Dashboard"),
            html.H3(
                "General dashboard for visualizing confusion data (true positive, false positive, etc.)."),
            html.Br(),
            dcc.Link("Go back to index.", href="/"),
            html.Br(),
            layout_5
        ])
    elif pathname == '/apps/evolution':
        return html.Div([
            dbc.Toast(
                "Plot(s) Updated!",
                id="notification-toast-6",
                header="Notification",
                icon="primary",
                is_open=False,
                dismissable=True,
                duration=4000,
                # top: 66 positions the toast below the navbar
                style={"position": "fixed", "top": 5,
                       "right": 10, "width": 350},
            ),
            html.H1("Evolution Dashboard"),
            html.H3(
                "General dashboard for visualizing the evolution of dynamic indicators."),
            html.Br(),
            dcc.Link("Go back to index.", href="/"),
            html.Br(),
            layout_6
        ])
    elif pathname == '/apps/convolution':
        return html.Div([
            dbc.Toast(
                "Plot(s) Updated!",
                id="notification-toast-7",
                header="Notification",
                icon="primary",
                is_open=False,
                dismissable=True,
                duration=4000,
                # top: 66 positions the toast below the navbar
                style={"position": "fixed", "top": 5,
                       "right": 10, "width": 350},
            ),
            html.H1("Convolution Dashboard"),
            html.H3(
                "General dashboard for visualizing the indicators considering a customizable convolution kernel (average and standard deviation)."),
            html.Br(),
            dcc.Link("Go back to index.", href="/"),
            html.Br(),
            layout_7
        ])
    else:
        return index_layout

################################################################################
##### LAYOUT PARAMETERS ########################################################
TAB_1_PADDING = 9
TAB_2_PADDING = 4
TAB_3_PADDING = 4

T4_FIGURE_HEIGHT = 800
T4_FIGURE_WIDTH = 900
COLORS = ["red", "blue", "green", "orange", "cyan"]
################################################################################

##### Preliminary setup ########################################################
data_options = [
    {'label': 'Stability Time', 'value': 0},
    {'label': 'LI', 'value': 1},
    {'label': 'LEI', 'value': 2},
    {'label': 'RE', 'value': 3},
    {'label': 'REI', 'value': 4},
    {'label': 'SALI', 'value': 5},
    {'label': 'GALI', 'value': 6},
    {'label': 'MEGNO', 'value': 7},
    {'label': 'Frequency Map', 'value': 8},
    {'label': 'Simple radial distance', 'value': 9}
]
handler_list = [
    dh.stability_data_handler,
    dh.LI_data_handler,
    dh.LEI_data_handler,
    dh.RE_data_handler,
    dh.REI_data_handler,
    dh.SALI_data_handler,
    dh.GALI_data_handler,
    dh.MEGNO_data_handler,
    dh.FQ_data_handler,
    dh.radius_data_handler
]
name_options = ['Stability Time', 'LI', 'LEI', 'RE', 'REI', 'SALI', 'GALI', 'MEGNO', 'Frequency Map', 'Simple radial distance']

################################################################################


#### Option update ####


@app.callback(
    [
        Output({'type': 'dropdown_0', 'index': MATCH}, 'options'),
        Output({'type': 'dropdown_0', 'index': MATCH}, 'value'),
        Output({'type': 'label_0', 'index': MATCH}, 'children'),
        Output({'type': 'dropdown_1', 'index': MATCH}, 'options'),
        Output({'type': 'dropdown_1', 'index': MATCH}, 'value'),
        Output({'type': 'label_1', 'index': MATCH}, 'children'),
        Output({'type': 'dropdown_2', 'index': MATCH}, 'options'),
        Output({'type': 'dropdown_2', 'index': MATCH}, 'value'),
        Output({'type': 'label_2', 'index': MATCH}, 'children'),
        Output({'type': 'dropdown_3', 'index': MATCH}, 'options'),
        Output({'type': 'dropdown_3', 'index': MATCH}, 'value'),
        Output({'type': 'label_3', 'index': MATCH}, 'children'),
        Output({'type': 'dropdown_4', 'index': MATCH}, 'options'),
        Output({'type': 'dropdown_4', 'index': MATCH}, 'value'),
        Output({'type': 'label_4', 'index': MATCH}, 'children'),
        Output({'type': 'dropdown_5', 'index': MATCH}, 'options'),
        Output({'type': 'dropdown_5', 'index': MATCH}, 'value'),
        Output({'type': 'label_5', 'index': MATCH}, 'children'),
    ],
    Input({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
@cache.memoize(timeout=CACHE_TIMEOUT)
def update_dropdown_and_labels(value):
    value = handler_list[value]
    outputs = []

    for i in range(len(value.get_param_list())):
        outputs.append(
            [{'label': str(s), 'value': s} for s in
                value.get_param_options(value.get_param_list()[i])]
        )
        outputs.append(outputs[-1][0]['value'])
        outputs.append(value.get_param_list()[i])

    for i in range(len(value.get_param_list()), 6):
        outputs.append([])
        outputs.append(None)
        outputs.append("parameter_{}".format(i))

    return outputs

#### Plots update ####


@app.callback(
    Output({'type': 'linked_figure', 'index': MATCH}, 'figure'),
    [
        Input({'type': 'dropdown_0', 'index': MATCH}, 'value'),
        Input({'type': 'dropdown_1', 'index': MATCH}, 'value'),
        Input({'type': 'dropdown_2', 'index': MATCH}, 'value'),
        Input({'type': 'dropdown_3', 'index': MATCH}, 'value'),
        Input({'type': 'dropdown_4', 'index': MATCH}, 'value'),
        Input({'type': 'dropdown_5', 'index': MATCH}, 'value'),
        Input({'type': 'linked_options', 'index': MATCH}, 'value'),
    ],
    State({'type': 'main_dropdown', 'index': MATCH}, 'value')
)
@cache.memoize(timeout=CACHE_TIMEOUT)
def update_figure(*args):
    handler = handler_list[args[7]]
    param_list = handler.get_param_list()
    param_dict = {}
    for i in range(len(param_list)):
        param_dict[param_list[i]] = args[i]
    log_scale = True if 'log10' in args[6] else False
    return handler.get_plot(param_dict, log_scale)


def exe_update_correlation_plot(*args):
    handler_1 = handler_list[args[17]]
    handler_2 = handler_list[args[18]]

    param_list_1 = handler_1.get_param_list()
    param_dict_1 = {}
    for i in range(len(param_list_1)):
        param_dict_1[param_list_1[i]] = args[i]
    data_1 = handler_1.get_data(param_dict_1)
    if 'log10' in args[6]:
        data_1 = np.log10(data_1)

    param_list_2 = handler_2.get_param_list()
    param_dict_2 = {}
    for i in range(len(param_list_2)):
        param_dict_2[param_list_2[i]] = args[i + 7]
    data_2 = handler_2.get_data(param_dict_2)
    if 'log10' in args[13]:
        data_2 = np.log10(data_2)

    # make plot
    data_1 = data_1.flatten()
    data_2 = data_2.flatten()

    fig = go.Figure(
        data=go.Scattergl(
            x=data_1,
            y=data_2,
            mode='markers'
        )
    )

    fig.update_layout(
        title="Correlation Scatter Plot"
    )

    return fig


@cache.memoize(timeout=CACHE_TIMEOUT)
def exe_update_correlation_plot_bis(*args):
    handler_1 = handler_list[args[17]]
    handler_2 = handler_list[args[18]]

    param_list_1 = handler_1.get_param_list()
    param_dict_1 = {}
    for i in range(len(param_list_1)):
        param_dict_1[param_list_1[i]] = args[i]
    data_1 = handler_1.get_data(param_dict_1)
    if 'log10' in args[6]:
        data_1 = np.log10(data_1)

    param_list_2 = handler_2.get_param_list()
    param_dict_2 = {}
    for i in range(len(param_list_2)):
        param_dict_2[param_list_2[i]] = args[i + 7]
    data_2 = handler_2.get_data(param_dict_2)
    if 'log10' in args[13]:
        data_2 = np.log10(data_2)

    # make plot
    data_1 = data_1.flatten()
    data_2 = data_2.flatten()

    bool_mask = np.logical_and(
        np.logical_not(np.isnan(data_1)),
        np.logical_not(np.isnan(data_2)),
    )
    data_1 = data_1[bool_mask]
    data_2 = data_2[bool_mask]

    histo, xedj, yedj = np.histogram2d(
        data_1,
        data_2,
        bins=[args[14], args[15]],
        range=[[data_1.min(), data_1.max()], [data_2.min(), data_2.max()]]
    )

    histo[histo == 0] = np.nan
    if "log10" in args[16]:
        histo = np.log10(histo)

    fig = go.Figure(
        data=go.Heatmap(
            z=np.transpose(histo),
            x=xedj,
            y=yedj,
            hoverongaps=False,
            colorscale="Viridis",
        )
    )
    fig.update_layout(
        title="Correlation Density Plot " +
        ("[log10 scale]" if "log10" in args[16] else "[linear scale]")
    )

    return fig


@app.callback(
    [
        Output({'type': 'lay_2_figure', 'index': TAB_1_PADDING}, 'figure'),
        Output({'type': 'lay_2_figure_bis', 'index': TAB_1_PADDING}, 'figure'),
    ],
    [
        Input({'type': 'dropdown_0', 'index': TAB_1_PADDING}, 'value'),    # 0
        Input({'type': 'dropdown_1', 'index': TAB_1_PADDING}, 'value'),    # 1
        Input({'type': 'dropdown_2', 'index': TAB_1_PADDING}, 'value'),    # 2
        Input({'type': 'dropdown_3', 'index': TAB_1_PADDING}, 'value'),    # 3
        Input({'type': 'dropdown_4', 'index': TAB_1_PADDING}, 'value'),    # 4
        Input({'type': 'dropdown_5', 'index': TAB_1_PADDING}, 'value'),    # 5
        Input({'type': 'linked_options', 'index': TAB_1_PADDING}, 'value'),  # 6
        Input({'type': 'dropdown_0', 'index': TAB_1_PADDING+1}, 'value'),    # 7
        Input({'type': 'dropdown_1', 'index': TAB_1_PADDING+1}, 'value'),    # 8
        Input({'type': 'dropdown_2', 'index': TAB_1_PADDING+1}, 'value'),    # 9
        Input({'type': 'dropdown_3', 'index': TAB_1_PADDING+1}, 'value'),    # 10
        Input({'type': 'dropdown_4', 'index': TAB_1_PADDING+1}, 'value'),    # 11
        Input({'type': 'dropdown_5', 'index': TAB_1_PADDING+1}, 'value'),    # 12
        Input({'type': 'linked_options', 'index': TAB_1_PADDING+1}, 'value'),  # 13
        Input({'type': 'lay_2_x_bin',
               'index': TAB_1_PADDING}, 'value'),  # 14
        Input({'type': 'lay_2_y_bin',
               'index': TAB_1_PADDING}, 'value'),  # 15
        Input({'type': 'lay_2_fig_options',
               'index': TAB_1_PADDING}, 'value'),  # 16
    ],
    [
        State({'type': 'main_dropdown', 'index': TAB_1_PADDING}, 'value'),  # 17
        State({'type': 'main_dropdown', 'index': TAB_1_PADDING+1}, 'value')  # 18
    ]
)
def update_correlation_plot(*args):
    return [
        exe_update_correlation_plot(*args),
        exe_update_correlation_plot_bis(*args)
    ]


@app.callback(
    [
        Output({'type': 'lay_2_figure', 'index': TAB_1_PADDING+2}, 'figure'),
        Output({'type': 'lay_2_figure_bis', 'index': TAB_1_PADDING+2}, 'figure'),
    ],
    [
        Input({'type': 'dropdown_0', 'index': TAB_1_PADDING+2}, 'value'),    # 0
        Input({'type': 'dropdown_1', 'index': TAB_1_PADDING+2}, 'value'),    # 1
        Input({'type': 'dropdown_2', 'index': TAB_1_PADDING+2}, 'value'),    # 2
        Input({'type': 'dropdown_3', 'index': TAB_1_PADDING+2}, 'value'),    # 3
        Input({'type': 'dropdown_4', 'index': TAB_1_PADDING+2}, 'value'),    # 4
        Input({'type': 'dropdown_5', 'index': TAB_1_PADDING+2}, 'value'),    # 5
        Input({'type': 'linked_options', 'index': TAB_1_PADDING+2}, 'value'),  # 6
        Input({'type': 'dropdown_0', 'index': TAB_1_PADDING+3}, 'value'),    # 7
        Input({'type': 'dropdown_1', 'index': TAB_1_PADDING+3}, 'value'),    # 8
        Input({'type': 'dropdown_2', 'index': TAB_1_PADDING+3}, 'value'),    # 9
        Input({'type': 'dropdown_3', 'index': TAB_1_PADDING+3}, 'value'),    # 10
        Input({'type': 'dropdown_4', 'index': TAB_1_PADDING+3}, 'value'),    # 11
        Input({'type': 'dropdown_5', 'index': TAB_1_PADDING+3}, 'value'),    # 12
        Input({'type': 'linked_options', 'index': TAB_1_PADDING+3}, 'value'),  # 13
        Input({'type': 'lay_2_x_bin',
               'index': TAB_1_PADDING+2}, 'value'),  # 14
        Input({'type': 'lay_2_y_bin',
               'index': TAB_1_PADDING+2}, 'value'),  # 15
        Input({'type': 'lay_2_fig_options',
               'index': TAB_1_PADDING+2}, 'value'),  # 16
    ],
    [
        State({'type': 'main_dropdown', 'index': TAB_1_PADDING+2}, 'value'),  # 17
        State({'type': 'main_dropdown', 'index': TAB_1_PADDING+3}, 'value')  # 18
    ]
)
def update_correlation_plot_2(*args):
    return [
        exe_update_correlation_plot(*args),
        exe_update_correlation_plot_bis(*args)
    ]


@cache.memoize(timeout=CACHE_TIMEOUT)
def exe_update_diff_plot(*args):
    handler_1 = handler_list[args[15]]
    handler_2 = handler_list[args[16]]

    param_list_1 = handler_1.get_param_list()
    param_dict_1 = {}
    for i in range(len(param_list_1)):
        param_dict_1[param_list_1[i]] = args[i]
    data_1 = handler_1.get_data(param_dict_1)
    if 'log10' in args[6]:
        data_1 = np.log10(data_1)

    param_list_2 = handler_2.get_param_list()
    param_dict_2 = {}
    for i in range(len(param_list_2)):
        param_dict_2[param_list_2[i]] = args[i + 7]
    data_2 = handler_2.get_data(param_dict_2)
    if 'log10' in args[13]:
        data_2 = np.log10(data_2)

    # make plot
    data = data_1 - data_2
    if 'relative' in args[14]:
        data = data / data_1
    if 'absolute' in args[14]:
        data = np.absolute(data)
    if 'log10' in args[14]:
        data = np.log10(data)

    fig = go.Figure(
        data=go.Heatmap(
            z=data,
            x=np.linspace(0, 1, 500),
            y=np.linspace(0, 1, 500),
            hoverongaps=False,
            colorscale="Viridis"
        )
    )
    fig.update_layout(
        title="Difference "
        + ("[absolute value] " if "absolute" in args[14] else "")
        + ("[log10 scale]" if "log10" in args[14] else "[linear scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


@app.callback(
    [
        Output({'type': 'figure_diff',
                'index': TAB_1_PADDING+TAB_2_PADDING}, 'figure')
    ],
    [
        Input({'type': 'dropdown_0',
               'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),      # 0
        Input({'type': 'dropdown_1',\
               'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),      # 1
        Input({'type': 'dropdown_2',\
               'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),      # 2
        Input({'type': 'dropdown_3',\
               'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),      # 3
        Input({'type': 'dropdown_4',\
               'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),      # 4
        Input({'type': 'dropdown_5',\
               'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),      # 5
        Input({'type': 'linked_options',\
               'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),      # 6
        Input({'type': 'dropdown_0',\
               'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value'),    # 7
        Input({'type': 'dropdown_1',\
               'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value'),    # 8
        Input({'type': 'dropdown_2',\
               'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value'),    # 9
        Input({'type': 'dropdown_3',\
               'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value'),    # 10
        Input({'type': 'dropdown_4',\
               'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value'),    # 11
        Input({'type': 'dropdown_5',\
               'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value'),    # 12
        Input({'type': 'linked_options',\
               'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value'),    # 13
        Input({'type': 'plot_options_diff',\
               'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),      # 14
    ],
    [
        State({'type': 'main_dropdown',\
               'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),      # 15
        State({'type': 'main_dropdown',\
               'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value')     # 16
    ]
)
def update_diff_plot(*args):
    return [exe_update_diff_plot(*args)]


@app.callback(
    [
        Output({'type': 'figure_diff',
                'index': TAB_1_PADDING+TAB_2_PADDING+2}, 'figure')
    ],
    [
        Input({'type': 'dropdown_0',
               'index': TAB_1_PADDING+TAB_2_PADDING+2}, 'value'),    # 0
        Input({'type': 'dropdown_1',\
               'index': TAB_1_PADDING+TAB_2_PADDING+2}, 'value'),    # 1
        Input({'type': 'dropdown_2',\
               'index': TAB_1_PADDING+TAB_2_PADDING+2}, 'value'),    # 2
        Input({'type': 'dropdown_3',\
               'index': TAB_1_PADDING+TAB_2_PADDING+2}, 'value'),    # 3
        Input({'type': 'dropdown_4',\
               'index': TAB_1_PADDING+TAB_2_PADDING+2}, 'value'),    # 4
        Input({'type': 'dropdown_5',\
               'index': TAB_1_PADDING+TAB_2_PADDING+2}, 'value'),    # 5
        Input({'type': 'linked_options',\
               'index': TAB_1_PADDING+TAB_2_PADDING+2}, 'value'),    # 6
        Input({'type': 'dropdown_0',\
               'index': TAB_1_PADDING+TAB_2_PADDING+3}, 'value'),    # 7
        Input({'type': 'dropdown_1',\
               'index': TAB_1_PADDING+TAB_2_PADDING+3}, 'value'),    # 8
        Input({'type': 'dropdown_2',\
               'index': TAB_1_PADDING+TAB_2_PADDING+3}, 'value'),    # 9
        Input({'type': 'dropdown_3',\
               'index': TAB_1_PADDING+TAB_2_PADDING+3}, 'value'),    # 10
        Input({'type': 'dropdown_4',\
               'index': TAB_1_PADDING+TAB_2_PADDING+3}, 'value'),    # 11
        Input({'type': 'dropdown_5',\
               'index': TAB_1_PADDING+TAB_2_PADDING+3}, 'value'),    # 12
        Input({'type': 'linked_options',\
               'index': TAB_1_PADDING+TAB_2_PADDING+3}, 'value'),    # 13
        Input({'type': 'plot_options_diff',\
               'index': TAB_1_PADDING+TAB_2_PADDING+2}, 'value'),    # 14
    ],
    [
        State({'type': 'main_dropdown',\
               'index': TAB_1_PADDING+TAB_2_PADDING+2}, 'value'),    # 15
        State({'type': 'main_dropdown',\
               'index': TAB_1_PADDING+TAB_2_PADDING+3}, 'value')     # 16
    ]
)
def update_diff_plot_2(*args):
    return [exe_update_diff_plot(*args)]


################### RESONANCE PLOTS ############################################

@app.callback(
    Output('fig_action', 'figure'),
    [
        Input('drop_epsilon', 'value'),         # 0
        Input('drop_mu', 'value'),              # 1
        Input('drop_nturns', 'value'),          # 2
        Input('input_tolerance', 'value'),      # 3
        Input('input_minres', 'value'),         # 4
        Input('input_maxres', 'value'),         # 5
        Input('xtune', 'value'),                # 6
        Input('ytune', 'value'),                # 7
    ]
)
@cache.memoize(timeout=CACHE_TIMEOUT)
def update_action_plot(*args):
    parameters = {
        "mu": args[1],
        "epsilon": args[0],
        "turns": args[2],
    }
    data_x = TUNE_X_data_handler.get_data(parameters)
    data_y = TUNE_Y_data_handler.get_data(parameters)
    data = np.empty((500, 500)) * np.nan
    extra_data_x = np.zeros((500, 500))
    extra_data_y = np.zeros((500, 500))

    for i in list(range(args[4], args[5] + 1)):
        for j in range(0, i+1):
            nx = j
            ny = i - j

            bool_mask = np.modf(
                np.absolute(+ nx * data_x + ny * data_y))[0] < args[3]
            data[bool_mask] = i
            extra_data_x[bool_mask] = nx
            extra_data_y[bool_mask] = ny

            bool_mask = np.modf(
                np.absolute(+ nx * data_x - ny * data_y))[0] < args[3]
            data[bool_mask] = i
            extra_data_x[bool_mask] = nx
            extra_data_y[bool_mask] = -ny

    actual_max_res = int(np.nanmax(data))
    actual_min_res = int(np.nanmin(data))
    n_resonances = (actual_max_res - actual_min_res) + 1
    interval = 1 / (n_resonances)
    colorscale = []
    for i, j in enumerate(range(actual_min_res, actual_max_res + 1)):
        colorscale.append([interval * i, COLORS[j % len(COLORS)]])
        colorscale.append([interval * (i + 1), COLORS[(j) % len(COLORS)]])

    fig = go.Figure({
        'data': [{
            'z': data,
            'x': np.linspace(0, 1, 500),
            'y': np.linspace(0, 1, 500),
            'hoverongaps': False,
            'type': 'heatmap',
            'customdata': np.dstack((
                [extra_data_x, extra_data_y]
            )),
            'hovertemplate': "<br>".join([
                "Resonance Order: %{z}",
                "n_x: %{customdata[0]}",
                "n_y: %{customdata[1]}"
            ]),
            'colorscale': colorscale,
            'colorbar':dict(
                dtick=1
            )
        }]
    })

    fig.update_layout(
        title="Resonance plot - Action space - resonance order in colorbar",
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    fig.update_layout(width=int(T4_FIGURE_WIDTH))
    fig.update_layout(height=int(T4_FIGURE_HEIGHT))
    return fig


def filter_01(x, y):
    mask = np.logical_and(
        np.logical_and(x >= -0.01, x <= 1.01),
        np.logical_and(y >= -0.01, y <= 1.01)
    )
    return x[mask], y[mask]


@app.callback(
    Output('fig_frequency', 'figure'),
    [
        Input('drop_epsilon', 'value'),         # 0
        Input('drop_mu', 'value'),              # 1
        Input('drop_nturns', 'value'),          # 2
        Input('input_tolerance', 'value'),      # 3
        Input('input_minres', 'value'),         # 4
        Input('input_maxres', 'value'),         # 5
        Input('xtune', 'value'),                # 6
        Input('ytune', 'value'),                # 7
        Input('freq_coloring_options', 'value')  # 8
    ],
    [
        State('fig_frequency', 'relayoutData')  # 9
    ]
)
@cache.memoize(timeout=CACHE_TIMEOUT)
def update_frequency_plot(*args):
    parameters = {
        "mu": args[1],
        "epsilon": args[0],
        "turns": args[2],
    }
    data_x = TUNE_X_data_handler.get_data(parameters)
    data_y = TUNE_Y_data_handler.get_data(parameters)

    color_data_stab = np.log10(dh.stability_data_handler.get_data({
        "mu": args[1],
        "epsilon": args[0],
        "kick": "no_kick"
    }).flatten())
    color_data_stab[np.isnan(data_x.flatten())] = np.nan
    color_data_stab[np.isnan(data_y.flatten())] = np.nan

    color_data_rad = dh.radius_data_handler.get_data({
        "mu": args[1],
        "epsilon": args[0]
    }).flatten()
    color_data_rad[np.isnan(data_x.flatten())] = np.nan
    color_data_rad[np.isnan(data_y.flatten())] = np.nan

    r_x, r_px, r_y, r_py = dh.get_raw_coordinates(parameters)

    customdata = np.dstack((
        r_x.flatten(),
        r_px.flatten(),
        r_y.flatten(),
        r_py.flatten(),
        color_data_stab
    ))[0]

    fig = go.Figure()

    if 'black' in args[8]:
        fig.add_trace(
            go.Scattergl(
                x=data_x.flatten(),
                y=data_y.flatten(),
                name="data",
                mode="markers",
                marker_color="black",
                customdata=customdata,
                hovertemplate="<br>".join([
                    "X_0: %{customdata[0]:.3f}",
                    "PX_0: %{customdata[1]:.3f}",
                    "Y_0: %{customdata[2]:.3f}",
                    "PY_0: %{customdata[3]:.3f}",
                    "Stability time [log10]: %{customdata[4]:.3f}",
                ])
            )
        )
    else:
        if 'stab' in args[8]:
            marker = dict(
                color=color_data_stab,
                colorscale='Viridis',
                showscale=True
            )
        elif 'radial' in args[8]:
            marker = dict(
                color=color_data_rad,
                colorscale='Viridis',
                showscale=True
            )
        else:
            marker = None
        fig.add_trace(
            go.Scattergl(
                x=data_x.flatten(),
                y=data_y.flatten(),
                name="data",
                mode="markers",
                marker=marker,
                customdata=customdata,
                hovertemplate="<br>".join([
                    "X_0: %{customdata[0]:.3f}",
                    "PX_0: %{customdata[1]:.3f}",
                    "Y_0: %{customdata[2]:.3f}",
                    "PY_0: %{customdata[3]:.3f}",
                    "Stability time [log10]: %{customdata[4]:.3f}",
                ])
            )
        )
        fig.update_layout(legend_orientation="h")

    x = np.linspace(0, 1, 1000)
    for i in list(range(args[4], args[5] + 1)):
        for j in range(1, i):
            nx = j
            ny = i - j
            for q in range(0, i+1):
                newx, y = filter_01(x, q/ny - nx / ny * x)
                fig.add_trace(go.Scattergl(
                    x=newx,
                    y=y,
                    mode='lines',
                    marker_color=COLORS[i % len(COLORS)],
                    name="Resonance {}".format(i),
                    showlegend=(True if q == 0 and j == 1 else False),
                    hoverinfo="skip"
                ))
                newx, y = filter_01(x, q/(-ny) - nx / (-ny) * x)
                fig.add_trace(go.Scattergl(
                    x=newx,
                    y=y,
                    mode='lines',
                    marker_color=COLORS[i % len(COLORS)],
                    name="Resonance {} - {} - bis".format(i, q),
                    showlegend=False,
                    hoverinfo="skip"
                ))
                newx, y = filter_01(x, q/ny - (-nx) / ny * x)
                fig.add_trace(go.Scattergl(
                    x=newx,
                    y=y,
                    mode='lines',
                    marker_color=COLORS[i % len(COLORS)],
                    name="Resonance {} - {} - ter".format(i, q),
                    showlegend=False,
                    hoverinfo="skip"
                ))
                newx, y = filter_01(x, q/(-ny) - (-nx) / (-ny) * x)
                fig.add_trace(go.Scattergl(
                    x=newx,
                    y=y,
                    mode='lines',
                    marker_color=COLORS[i % len(COLORS)],
                    name="Resonance {} - {} - quater".format(i, q),
                    showlegend=False,
                    hoverinfo="skip"
                ))
        for j in range(i+1):
            fig.add_vline(j/i, line_color=COLORS[i % len(COLORS)])
            fig.add_hline(j/i, line_color=COLORS[i % len(COLORS)])

    fig.add_trace(go.Scattergl(
        x=x,
        y=np.ones_like(x) * args[7],
        name="Working Frequency",
        mode='lines',
        line_color="grey",
        showlegend=True,
        hoverinfo="skip"
    ))
    fig.add_vline(args[6], line_color="grey")

    fig.update_layout(width=int(T4_FIGURE_WIDTH))
    fig.update_layout(height=int(T4_FIGURE_HEIGHT))

    fig.update_layout(
        title="Resonance plot - Frequency space",
        xaxis_title="X tune [2pi units]",
        yaxis_title="Y tune [2pi units]"
    )

    if args[9] is None:
        fig.update_xaxes(range=[0.0, 1.0])
        fig.update_yaxes(range=[0.0, 1.0])
    else:
        if "xaxis.range[0]" in args[9]:
            fig.update_xaxes(range=[
                args[9]["xaxis.range[0]"],
                args[9]["xaxis.range[1]"],
            ])
        else:
            fig.update_xaxes(range=[0.0, 1.0])
        if "yaxis.range[0]" in args[9]:
            fig.update_yaxes(range=[
                args[9]["yaxis.range[0]"],
                args[9]["yaxis.range[1]"],
            ])
        else:
            fig.update_xaxes(range=[0.0, 1.0])

    return fig


@app.callback(
    [
        Output({'type': 'fig_main_confusion', 'index': MATCH}, 'figure'),
        Output({'type': 'fig_advanced_confusion', 'index': MATCH}, 'figure'),
        Output({'type': 'tab_confusion', 'index': MATCH}, 'children'),
        Output({'type': 'fig_thresh_evolution', 'index': MATCH}, 'figure'),
    ],
    [
        Input({'type': 'dropdown_0', 'index': MATCH}, 'value'),     # 0
        Input({'type': 'dropdown_1', 'index': MATCH}, 'value'),     # 1
        Input({'type': 'dropdown_2', 'index': MATCH}, 'value'),     # 2
        Input({'type': 'dropdown_3', 'index': MATCH}, 'value'),     # 3
        Input({'type': 'dropdown_4', 'index': MATCH}, 'value'),     # 4
        Input({'type': 'dropdown_5', 'index': MATCH}, 'value'),     # 5
        Input({'type': 'linked_options', 'index': MATCH}, 'value'), # 6
        Input({'type': 'stability_time', 'index': MATCH}, 'value'),  # 7
        Input({'type': 'input_negative', 'index': MATCH}, 'value'), # 8
        Input({'type': 'input_samples', 'index': MATCH}, 'value'),  # 9
    ],
    [
        State({'type': 'main_dropdown', 'index': MATCH}, 'value')   # 10       
    ]
)
@cache.memoize(timeout=CACHE_TIMEOUT)
def confusion_plot(*args):
    handler = handler_list[args[10]]
    param_list = handler.get_param_list()
    param_dict = {}
    for i in range(len(param_list)):
        param_dict[param_list[i]] = args[i]
    stab_param = {
        'epsilon': param_dict["epsilon"],
        'mu': param_dict["mu"],
        'kick': 'no_kick'
    }
    stab_data = dh.stability_data_handler.get_data(stab_param).flatten()
    ind_data = np.asarray(handler.get_data(param_dict)).flatten()

    if "log10" in args[6]:
        ind_data[ind_data == 0] = np.nan
        ind_data = np.log10(ind_data)
    max_ind = np.nanmax(ind_data)
    min_ind = np.nanmin(ind_data)
    samples = np.linspace(min_ind, max_ind, args[9]+2)[1:-1]

    tp = np.empty(args[9])
    tn = np.empty(args[9])
    fp = np.empty(args[9])
    fn = np.empty(args[9])

    for i, v in enumerate(samples):
        if "reverse" in args[6]:
            tp[i] = np.count_nonzero(stab_data[ind_data >= v] >= args[7])
            tn[i] = np.count_nonzero(stab_data[ind_data < v] < args[7])
            fp[i] = np.count_nonzero(stab_data[ind_data < v] >= args[7])
            fn[i] = np.count_nonzero(stab_data[ind_data >= v] < args[7])
        else:
            tp[i] = np.count_nonzero(stab_data[ind_data < v] >= args[7])
            tn[i] = np.count_nonzero(stab_data[ind_data >= v] < args[7])
            fp[i] = np.count_nonzero(stab_data[ind_data >= v] >= args[7])
            fn[i] = np.count_nonzero(stab_data[ind_data < v] < args[7])

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=samples,
            y=tp,
            name="True Positive",
            mode='lines',
            marker_color="red"
        ))
    fig.add_trace(
        go.Scatter(
            x=samples,
            y=tn,
            name="True Negative",
            mode='lines',
            marker_color="orange"
        ))
    fig.add_trace(
        go.Scatter(
            x=samples,
            y=fp,
            name="False Positive",
            mode='lines',
            marker_color="blue"
        ))
    fig.add_trace(
        go.Scatter(
            x=samples,
            y=fn,
            name="False Negative",
            mode='lines',
            marker_color="cyan"
        ))

    max_accuracy = np.nanargmax((tp + tn) / (tp + tn + fn + fp))

    fig.update_layout(
        title="Threshold evaluation",
        xaxis_title="Threshold position",
        yaxis_title="Samples"
    )

    accuracy = (tp+tn)/(tp+tn+fp+fn)
    precision = tp/(tp+fp)
    sensitivity = tp/(tp+fn)
    specificity = tn/(tn+fp)

    fig_adv = go.Figure()
    fig_adv.add_trace(
        go.Scatter(
            x=samples,
            y=accuracy,
            name="Accuracy",
            mode='lines'
        )
    )
    fig_adv.add_trace(
        go.Scatter(
            x=samples,
            y=precision,
            name="Precision",
            mode="lines"
        )
    )
    fig_adv.add_trace(
        go.Scatter(
            x=samples,
            y=sensitivity,
            name="Sensitivity",
            mode="lines"
        )
    )
    fig_adv.add_trace(
        go.Scatter(
            x=samples,
            y=specificity,
            name="Specificity",
            mode='lines'
        )
    )
    fig_adv.add_vline(
        samples[max_accuracy],
        annotation_text="Max accuracy",
        annotation_position="bottom right"
    )
    fig_adv.update_layout(
        xaxis_title="Threshold position",
        yaxis_title="Value"
    )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig_adv.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(hovermode="x")
    fig_adv.update_layout(hovermode="x")

    table_header = [
    html.Thead(html.Tr([html.Th("Parameter"), html.Th("Value")]))
    ]

    row1 = html.Tr([
        html.Td("Best Threshold (accuracy-wise)"), 
        html.Td("{:2e}".format(samples[max_accuracy]))
    ])
    row3 = html.Tr([
        html.Td("Accuracy"),
        html.Td("{:.2f}%".format((accuracy[max_accuracy]*100)))
    ])
    row2 = html.Tr([
        html.Td("Precision"),
        html.Td("{:.2f}%".format((precision[max_accuracy]*100)))
    ])
    row4 = html.Tr([
        html.Td("Sensitivity"),
        html.Td("{:.2f}%".format((sensitivity[max_accuracy]*100)))
    ])
    row5 = html.Tr([
        html.Td("Specificity"),
        html.Td("{:.2f}%".format((specificity[max_accuracy]*100)))
    ])
    
    table_body = [html.Tbody([row1, row2, row3, row4, row5])]

    iterable = handler.get_data_all_turns(param_dict)
    if iterable is None or 'full_scan' not in args[6]:
        final_fig = go.Figure()
    else:
        times = []
        thresholds = []
        accuracies = []
        for block in iterable:
            t, ind_data = block
            ind_data = ind_data.flatten()
            times.append(t)
            if "log10" in args[6]:
                ind_data[ind_data==0] = np.nan
                ind_data = np.log10(ind_data)
            max_ind = np.nanmax(ind_data)
            min_ind = np.nanmin(ind_data)
            samples = np.linspace(min_ind, max_ind, args[9]+2)[1:-1]

            for i, v in enumerate(samples):
                if "reverse" in args[6]:
                    tp[i] = np.count_nonzero(stab_data[ind_data >= v] == 10000000)
                    tn[i] = np.count_nonzero(stab_data[ind_data < v] != 10000000)
                    fp[i] = np.count_nonzero(stab_data[ind_data < v] == 10000000)
                    fn[i] = np.count_nonzero(stab_data[ind_data >= v] != 10000000)
                else:
                    tp[i] = np.count_nonzero(stab_data[ind_data < v] == 10000000)
                    tn[i] = np.count_nonzero(stab_data[ind_data >= v] != 10000000)
                    fp[i] = np.count_nonzero(stab_data[ind_data >= v] == 10000000)
                    fn[i] = np.count_nonzero(stab_data[ind_data < v] != 10000000)
            accuracy = (tp+tn)/(tp+tn+fp+fn)
            max_accuracy = np.nanargmax(accuracy)
            thresholds.append(samples[max_accuracy])
            accuracies.append(accuracy[max_accuracy])

        thresholds = [x for _, x in sorted(zip(times, thresholds))]
        accuracies = [x for _, x in sorted(zip(times, accuracies))]
        times = [x for x in sorted(times)]

        final_fig = make_subplots(specs=[[{"secondary_y": True}]])
        final_fig.add_trace(
            go.Scatter(
                x=times,
                y=thresholds,
                name="Best Thresholds (accuracy-wise)",
                mode="lines"
            ),
            secondary_y=False,
        )
        final_fig.add_trace(
            go.Scatter(
                x=times,
                y=accuracies,
                name="Accuracy",
                mode="lines"
            ),
            secondary_y=True,
        )
        final_fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
        final_fig.update_layout(hovermode="x")
        final_fig.update_layout(
            title="Theshold evolution for " + name_options[args[10]])
        final_fig.update_xaxes(
            title_text="N turns used for computing indicator",
            type="log"
            )
        final_fig.update_yaxes(title_text="Threshold value", secondary_y=False)
        final_fig.update_yaxes(title_text="Accuracy value", secondary_y=True)

    return [fig, fig_adv, table_header + table_body, final_fig]


@app.callback(
    [
        Output({'type': 'fig_evolution', 'index': MATCH}, 'figure'),
    ],
    [
        Input({'type': 'dropdown_0', 'index': MATCH}, 'value'),     # 0
        Input({'type': 'dropdown_1', 'index': MATCH}, 'value'),     # 1
        Input({'type': 'dropdown_2', 'index': MATCH}, 'value'),     # 2
        Input({'type': 'dropdown_3', 'index': MATCH}, 'value'),     # 3
        Input({'type': 'dropdown_4', 'index': MATCH}, 'value'),     # 4
        Input({'type': 'dropdown_5', 'index': MATCH}, 'value'),     # 5
        Input({'type': 'linked_options', 'index': MATCH}, 'value'),  # 6
        Input({'type': 'min_turns', 'index': MATCH}, 'value'),  # 7
        Input({'type': 'max_turns', 'index': MATCH}, 'value'),  # 8
        Input({'type': 'sample_skip', 'index': MATCH}, 'value'),  # 9
    ],
    [
        State({'type': 'main_dropdown', 'index': MATCH}, 'value')   # 10
    ]
)
@cache.memoize(timeout=CACHE_TIMEOUT)
def evolution_plot(*args):
    handler = handler_list[args[10]]
    param_list = handler.get_param_list()
    param_dict = {}
    for i in range(len(param_list)):
        param_dict[param_list[i]] = args[i]
    stab_param = {
        'epsilon': param_dict["epsilon"],
        'mu': param_dict["mu"],
        'kick': 'no_kick'
    }
    stab_data = np.log10(dh.stability_data_handler.get_data(stab_param).flatten())
    iterable = handler.get_data_all_turns(param_dict)
    if iterable is None:
        return [go.Figure()]
    t_list = []
    values = []
    for t, v in iterable:
        t_list.append(t)
        values.append(v.flatten())

    values = [x for _, x in sorted(zip(t_list, values))]
    t_list = [x for x in sorted(t_list)]

    t_list = np.array(t_list)
    values = np.array(values)

    bool_mask = np.logical_and(
        t_list >= args[7],
        t_list <= args[8]
    )

    t_list = t_list[bool_mask]
    values = values[bool_mask]

    if "log10" in args[6]:
        values = np.log10(values)

    cmap = matplotlib.cm.get_cmap('viridis')
    fig = go.Figure()
    for i in tqdm(range(0, values.shape[1], int(args[9]))):
        if "filter" in args[6]:
            if np.any(np.isnan(values[:,i])):
                continue
        color = cmap(stab_data[i]/7)
        color = 'rgb({},{},{})'.format(
            int(color[0]*255), int(color[1]*255), int(color[2]*255),)
        fig.add_trace(
            go.Scattergl(
                x=t_list,
                y=values[:, i],
                line=dict(
                    color=color,
                    width=1.0
                ),
                mode='lines+markers',
                showlegend=False,
            )
        )
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        name="Stability time [log10]",
        mode='markers',
        marker=dict(
            colorscale='Viridis',
            showscale=True,
            cmin=np.nanmin(stab_data),
            cmax=np.nanmax(stab_data),
        ),
        hoverinfo='none'
    ))

    fig.update_xaxes(type="log")
    fig.update_layout(height=1200)
    fig.update_layout(
        title="Evolution plot",
        xaxis_title="Turns executed",
        yaxis_title="Dynamic indicator value"
    )
    return [fig]


@app.callback(
    [
        Output({'type': 'linked_stab_figure', 'index': MATCH}, 'figure'),
        Output({'type': 'conv_avg_figure', 'index': MATCH}, 'figure'),
        Output({'type': 'conv_std_figure', 'index': MATCH}, 'figure'),
        Output({'type': 'corr_plot_standard_fig', 'index': MATCH}, 'figure'),
        Output({'type': 'corr_plot_avg_fig', 'index': MATCH}, 'figure'),
        Output({'type': 'corr_plot_std_fig', 'index': MATCH}, 'figure'),
    ],
    [
        Input({'type': 'dropdown_0', 'index': MATCH}, 'value'),     # 0
        Input({'type': 'dropdown_1', 'index': MATCH}, 'value'),     # 1
        Input({'type': 'dropdown_2', 'index': MATCH}, 'value'),     # 2
        Input({'type': 'dropdown_3', 'index': MATCH}, 'value'),     # 3
        Input({'type': 'dropdown_4', 'index': MATCH}, 'value'),     # 4
        Input({'type': 'dropdown_5', 'index': MATCH}, 'value'),     # 5
        Input({'type': 'linked_options', 'index': MATCH}, 'value'),  # 6
        Input({'type': 'kernel_size', 'index': MATCH}, 'value'),  # 7
        Input({'type': 'x_bins', 'index': MATCH}, 'value'),  # 8
        Input({'type': 'y_bins', 'index': MATCH}, 'value'),  # 9
    ],
    [
        State({'type': 'main_dropdown', 'index': MATCH}, 'value')   # 10
    ]
)
@cache.memoize(timeout=CACHE_TIMEOUT)
def convolution_plots(*args):
    handler = handler_list[args[10]]
    param_list = handler.get_param_list()
    param_dict = {}
    for i in range(len(param_list)):
        param_dict[param_list[i]] = args[i]
    stab_param = {
        'epsilon': param_dict["epsilon"],
        'mu': param_dict["mu"],
        'kick': 'no_kick'
    }

    stab_data = np.log10(dh.stability_data_handler.get_data(stab_param))
    
    fig_just_stab = go.Figure()
    fig_just_stab.add_trace(
        go.Heatmap(
            z=stab_data,
            x=np.linspace(0, 1, 500),
            y=np.linspace(0, 1, 500),
            hoverongaps=False,
            colorscale="Viridis"
        )
    )
    fig_just_stab.update_layout(
        title="Stability time [log10 scale]",
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )

    stab_data = stab_data.flatten()
    
    ind_data = np.asarray(handler.get_data(param_dict))
    
    if 'log10' in args[6]:
        ind_data = np.log10(ind_data)

    avg_convolution = scipy.ndimage.generic_filter(
        ind_data,
        lambda x: np.nanmean(x),
        size=args[7],
        mode='reflect'
    )
    std_convolution = scipy.ndimage.generic_filter(
        ind_data,
        lambda x : np.nanstd(x),
        size=args[7],
        mode='reflect'
    )

    fig_img_avg = go.Figure()
    fig_img_avg.add_trace(go.Heatmap(
        z=avg_convolution,
        x=np.linspace(0, 1, 500),
        y=np.linspace(0, 1, 500),
        hoverongaps=False,
        colorscale="Viridis",
        reversescale=(True if "color_invert" in args[6] else False)
    ))
    fig_img_avg.update_layout(
        title="Uniform filter",
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )

    fig_img_std = go.Figure()
    fig_img_std.add_trace(go.Heatmap(
        z=std_convolution,
        x=np.linspace(0, 1, 500),
        y=np.linspace(0, 1, 500),
        hoverongaps=False,
        colorscale="Viridis",
        reversescale=(True if "color_invert" in args[6] else False)
    ))
    fig_img_std.update_layout(
        title="Standard deviation filter",
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    avg_convolution = avg_convolution.flatten()
    std_convolution = std_convolution.flatten()
    ind_data_flat = ind_data.flatten()

    bool_mask = np.logical_and(
        np.logical_not(np.isnan(stab_data)),
        np.logical_not(np.isnan(ind_data_flat))
    )
    stab_data_temp = stab_data[bool_mask]
    ind_data_flat = ind_data_flat[bool_mask]
    histo_standard, xedj_standard, yedj_standard = np.histogram2d(
        stab_data_temp,
        ind_data_flat,
        bins=[args[8], args[9]],
        range=[[stab_data_temp.min(), stab_data_temp.max()], [
            ind_data_flat.min(), ind_data_flat.max()]]
    )
    histo_standard[histo_standard == 0] = np.nan
    if "log10_histo" in args[6]:
        histo_standard = np.log10(histo_standard)
    fig_histo_standard = go.Figure()
    fig_histo_standard.add_trace(
        go.Heatmap(
            z=np.transpose(histo_standard),
            x=xedj_standard,
            y=yedj_standard,
            hoverongaps=False,
            colorscale="Viridis",
        )
    )
    fig_histo_standard.update_layout(
        title="Correlation density plot for standard data " +
        ("[log10 scale]" if "log10_histo" in args[6] else "[linear scale]"),
        xaxis_title="Dynamic indicator",
        yaxis_title="Stability time [log10]"
    )

    bool_mask = np.logical_and(
        np.logical_not(np.isnan(stab_data)),
        np.logical_not(np.isnan(avg_convolution)),
    )
    stab_data = stab_data[bool_mask]
    avg_convolution = avg_convolution[bool_mask]
    std_convolution = std_convolution[bool_mask]

    histo_avg, xedj_avg, yedj_avg = np.histogram2d(
        stab_data,
        avg_convolution,
        bins=[args[8], args[9]],
        range=[[stab_data.min(), stab_data.max()], [
            avg_convolution.min(), avg_convolution.max()]]
    )
    histo_avg[histo_avg == 0] = np.nan
    if "log10_histo" in args[6]:
        histo_avg = np.log10(histo_avg)

    histo_std, xedj_std, yedj_std = np.histogram2d(
        stab_data,
        std_convolution,
        bins=[args[8], args[9]],
        range=[[stab_data.min(), stab_data.max()], [
            std_convolution.min(), std_convolution.max()]]
    )
    histo_std[histo_std == 0] = np.nan
    if "log10_histo" in args[6]:
        histo_std = np.log10(histo_std)

    fig_histo_avg = go.Figure()
    fig_histo_avg.add_trace(
        go.Heatmap(
            z=np.transpose(histo_avg),
            x=xedj_avg,
            y=yedj_avg,
            hoverongaps=False,
            colorscale="Viridis",
        )
    )
    fig_histo_avg.update_layout(
        title="Correlation density plot for uniform filter " +
        ("[log10 scale]" if "log10_histo" in args[6] else "[linear scale]"),
        xaxis_title="Dynamic indicator",
        yaxis_title="Stability time [log10]"
    )

    fig_histo_std = go.Figure()
    fig_histo_std.add_trace(
        go.Heatmap(
            z=np.transpose(histo_std),
            x=xedj_std,
            y=yedj_std,
            hoverongaps=False,
            colorscale="Viridis",
        )
    )
    fig_histo_std.update_layout(
        title="Correlation density plot for standard deviation filter " +
        ("[log10 scale]" if "log10_histo" in args[6] else "[linear scale]"),
        xaxis_title="Dynamic indicator",
        yaxis_title="Stability time [log10]"
    )

    return [fig_just_stab, fig_img_avg, fig_img_std, fig_histo_standard, fig_histo_avg, fig_histo_std]


################################################################################

@app.callback(
    Output("notification-toast-1", "is_open"),
    [
        Input({'type': 'linked_figure', 'index': ALL}, 'figure'),
    ]
)
def update_toast_1(*p):
    return True


@app.callback(
    Output("notification-toast-2", "is_open"),
    [
        Input({'type': 'lay_2_figure', 'index': ALL}, 'figure'),
    ]
)
def update_toast_2(*p):
    return True


@app.callback(
    Output("notification-toast-3", "is_open"),
    [
        Input({'type': 'figure_diff',
               'index': ALL}, 'figure'),
        Input({'type': 'linked_figure', 'index': ALL}, 'figure'),
    ]
)
def update_toast_3(*p):
    return True


@app.callback(
    Output("notification-toast-4", "is_open"),
    [
        Input('fig_frequency', 'figure'),
        Input('fig_action', 'figure'),
    ]
)
def update_toast_4(*p):
    return True


@app.callback(
    Output("notification-toast-5", "is_open"),
    [
        Input({'type': 'fig_main_confusion',
                'index': ALL}, 'figure'),
    ]
)
def update_toast_5(*p):
    return True


################################################################################
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8080, debug=True)
