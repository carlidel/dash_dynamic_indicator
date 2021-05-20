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
import matplotlib.cm
import scipy.ndimage
from numba import njit, prange

from layouts import layout_1, layout_2, layout_3, layout_4, layout_5, layout_6, layout_7, layout_8

import plot_maker as pm

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
    dcc.Link('Go to Convolution dashboard', href='/apps/convolution'),
    html.Br(),
    dcc.Link('Go to Threshold evolution dashboard', href='/apps/threshold'),
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
    elif pathname == '/apps/threshold':
        return html.Div([
            dbc.Toast(
                "Plot(s) Updated!",
                id="notification-toast-8",
                header="Notification",
                icon="primary",
                is_open=False,
                dismissable=True,
                duration=4000,
                # top: 66 positions the toast below the navbar
                style={"position": "fixed", "top": 5,
                       "right": 10, "width": 350},
            ),
            html.H1("Threshold evolution Dashboard"),
            html.H3(
                "General dashboard for visualizing the variation of the best threshold (accuracy-wise) for a given dynamic indicator, considering the varying number of turns considered for computing it."),
            html.Br(),
            dcc.Link("Go back to index.", href="/"),
            html.Br(),
            layout_8
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
    {'label': 'Simple radial distance', 'value': 9},
    {'label': 'Radial distance', 'value': 10}
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
    dh.radius_data_handler,
    dh.EVO_RAD_data_handler
]
name_options = ['Stability Time', 'LI', 'LEI', 'RE', 'REI', 'SALI', 'GALI', 'MEGNO', 'Frequency Map', 'Simple radial distance', 'Radial distance']

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

#### Plots update ##############################################################


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

################################################################################


def update_correlation_plot(
    d_00, d_01, d_02, d_03, d_04, d_05, linked_options_0,
    d_10, d_11, d_12, d_13, d_14, d_15, linked_options_1,
    x_bin, y_bin, fig_options, md_0, md_1
):
    d_0 = (d_00, d_01, d_02, d_03, d_04, d_05)
    d_1 = (d_10, d_11, d_12, d_13, d_14, d_15)
    handler_1 = handler_list[md_0]
    handler_2 = handler_list[md_1]

    param_list_1 = handler_1.get_param_list()
    param_dict_1 = {}
    for i in range(len(param_list_1)):
        param_dict_1[param_list_1[i]] = d_0[i]
    data_1 = handler_1.get_data(param_dict_1)

    param_list_2 = handler_2.get_param_list()
    param_dict_2 = {}
    for i in range(len(param_list_2)):
        param_dict_2[param_list_2[i]] = d_1[i]
    data_2 = handler_2.get_data(param_dict_2)

    fig1 = pm.correlation_plot(
        data_1, data_2,
        log10_x='log10' in linked_options_0,
        log10_y='log10' in linked_options_1
    )
    fig2 = pm.correlation_plot_bis(
        data_1, data_2,
        x_bin, y_bin,
        log10_x='log10' in linked_options_0,
        log10_y='log10' in linked_options_1,
        log10_hist='log10' in fig_options)

    return [fig1, fig2]


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
def cb_corr_1(*args):
    return update_correlation_plot(*args)


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
def cb_corr_2(*args):
    return update_correlation_plot(*args)


def update_difference_plot(
    d_00, d_01, d_02, d_03, d_04, d_05, linked_options_0,
    d_10, d_11, d_12, d_13, d_14, d_15, linked_options_1,
    plot_options, md_0, md_1
):
    d_0 = (d_00, d_01, d_02, d_03, d_04, d_05)
    d_1 = (d_10, d_11, d_12, d_13, d_14, d_15)
    handler_1 = handler_list[md_0]
    handler_2 = handler_list[md_1]

    param_list_1 = handler_1.get_param_list()
    param_dict_1 = {}
    for i in range(len(param_list_1)):
        param_dict_1[param_list_1[i]] = d_0[i]
    data_1 = handler_1.get_data(param_dict_1)

    param_list_2 = handler_2.get_param_list()
    param_dict_2 = {}
    for i in range(len(param_list_2)):
        param_dict_2[param_list_2[i]] = d_1[i]
    data_2 = handler_2.get_data(param_dict_2)

    fig = pm.diff_plot(
        data_1, data_2,
        log10_x="log10" in linked_options_0,
        log10_y="log10" in linked_options_1,
        relative_plot='relative' in plot_options,
        absolute_plot='absolute' in plot_options,
        log10_plot='log10' in plot_options
    )
    return [fig]


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
def cd_diff_plot_1(*args):
    return update_difference_plot(*args)


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
def cd_diff_plot_2(*args):
    return update_difference_plot(*args)


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

################################################################################

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
def confusion_plot(
    d_00, d_01, d_02, d_03, d_04, d_05, linked_options,
    stab_time, input_negative, input_samples, md_0
):
    d_0 = (d_00, d_01, d_02, d_03, d_04, d_05)
    handler = handler_list[md_0]
    param_list = handler.get_param_list()
    param_dict = {}
    for i in range(len(param_list)):
        param_dict[param_list[i]] = d_0[i]
    stab_param = {
        'epsilon': param_dict["epsilon"],
        'mu': param_dict["mu"],
        'kick': 'no_kick'
    }
    stab_data = dh.stability_data_handler.get_data(stab_param).flatten()
    ind_data = np.asarray(handler.get_data(param_dict)).flatten()

    fig, fig_adv, table = pm.confusion_plot_single(
        stab_data, ind_data, 
        log10_ind="log10" in linked_options,
        stab_thresh=stab_time,
        sampling=input_samples,
        reverse="reverse" in linked_options
    )

    iterable = handler.get_data_all_turns(param_dict)
    fig_final = pm.confusion_plot_multiple(
        stab_data,
        iterable,
        log10_ind="log10" in linked_options,
        stab_thresh=stab_time,
        sampling=input_samples,
        reverse="reverse" in linked_options
    )

    return [fig, fig_adv, table, fig_final]


################################################################################

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
def evolution_plot(
    d_00, d_01, d_02, d_03, d_04, d_05, linked_options,
    min_turns, max_turns, sample_skip, md_0
):
    d_0 = (d_00, d_01, d_02, d_03, d_04, d_05)
    handler = handler_list[md_0]
    param_list = handler.get_param_list()
    param_dict = {}
    for i in range(len(param_list)):
        param_dict[param_list[i]] = d_0[i]
    stab_param = {
        'epsilon': param_dict["epsilon"],
        'mu': param_dict["mu"],
        'kick': 'no_kick'
    }
    stab_data = dh.stability_data_handler.get_data(stab_param)
    iterable = handler.get_data_all_turns(param_dict)

    fig = pm.evolution_plot(
        stab_data,
        iterable,
        min_turns,
        max_turns,
        sample_skip,
        log10='log10' in linked_options,
        filter_data='filter' in linked_options
    )
    return [fig]

################################################################################

@app.callback(
    [
        Output({'type': 'linked_stab_figure', 'index': MATCH}, 'figure'),
        Output({'type': 'conv_avg_figure', 'index': MATCH}, 'figure'),
        Output({'type': 'conv_std_figure', 'index': MATCH}, 'figure'),
        Output({'type': 'corr_plot_standard_fig', 'index': MATCH}, 'figure'),
        Output({'type': 'corr_plot_avg_fig', 'index': MATCH}, 'figure'),
        Output({'type': 'corr_plot_std_fig', 'index': MATCH}, 'figure'),
        Output({'type': 'fig_avg_main_confusion', 'index': MATCH}, 'figure'),
        Output({'type': 'fig_avg_advanced_confusion', 'index': MATCH}, 'figure'),
        Output({'type': 'tab_avg_confusion', 'index': MATCH}, 'children'),
        Output({'type': 'fig_std_main_confusion', 'index': MATCH}, 'figure'),
        Output({'type': 'fig_std_advanced_confusion', 'index': MATCH}, 'figure'),
        Output({'type': 'tab_std_confusion', 'index': MATCH}, 'children'),
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
        Input({'type': 'stability_time', 'index': MATCH}, 'value'),  # 10
        Input({'type': 'input_negative', 'index': MATCH}, 'value'),  # 11
        Input({'type': 'input_samples', 'index': MATCH}, 'value'),  # 12
    ],
    [
        State({'type': 'main_dropdown', 'index': MATCH}, 'value')   # 13
    ]
)
@cache.memoize(timeout=CACHE_TIMEOUT)
def convolution_plots(
    d_00, d_01, d_02, d_03, d_04, d_05, linked_options,
    kernel_size, x_bin, y_bin, stab_time, input_negative, input_samples, md_0
):
    d_0 = (d_00, d_01, d_02, d_03, d_04, d_05)
    handler = handler_list[md_0]
    param_list = handler.get_param_list()
    param_dict = {}
    for i in range(len(param_list)):
        param_dict[param_list[i]] = d_0[i]
    stab_param = {
        'epsilon': param_dict["epsilon"],
        'mu': param_dict["mu"],
        'kick': 'no_kick'
    }

    stab_data = dh.stability_data_handler.get_data(stab_param)
    ind_data = np.asarray(handler.get_data(param_dict))
    
    fig_just_stab = pm.simple_heatmap(
        stab_data,
        log10=True,
        title="Stability time"
    )

    if 'log10' in linked_options:
        ind_data = np.log10(ind_data)
    
    avg_convolution = avg_convolve(
        ind_data,
        kernel_size,
        (True if "color_invert" in linked_options else False)
    ) 
    std_convolution = std_convolve(
        ind_data,
        kernel_size,
        (True if "color_invert" in linked_options else False)
    ) 

    fig_img_avg = pm.simple_heatmap(
        avg_convolution,
        log10=False,
        title="Uniform filter",
        reversescale=(True if "color_invert" in linked_options else False)
    )

    fig_img_std = pm.simple_heatmap(
        std_convolution,
        log10=False,
        title="Uniform filter",
        reversescale=(True if "color_invert" in linked_options else False)
    )

    stab_data = stab_data.flatten()
    avg_convolution = avg_convolution.flatten()
    std_convolution = std_convolution.flatten()
    ind_data_flat = ind_data.flatten()

    fig_histo_standard = pm.correlation_plot_bis(
        stab_data,
        ind_data_flat,
        x_bin,
        y_bin,
        log10_x=True,
        log10_y=False,
        log10_hist="log10_histo" in linked_options
    )

    fig_histo_avg = pm.correlation_plot_bis(
        stab_data,
        avg_convolution,
        x_bin,
        y_bin,
        log10_x=True,
        log10_y=False,
        log10_hist="log10_histo" in linked_options
    )

    fig_histo_std = pm.correlation_plot_bis(
        stab_data,
        std_convolution,
        x_bin,
        y_bin,
        log10_x=True,
        log10_y=False,
        log10_hist="log10_histo" in linked_options
    )

    fig_histo_standard.update_layout(
        title="Correlation density plot for standard data " +
        ("[log10 scale]" if "log10_histo" in linked_options else "[linear scale]"),
        yaxis_title="Dynamic indicator",
        xaxis_title="Stability time [log10]"
    )

    fig_histo_avg.update_layout(
        title="Correlation density plot for uniform filter " +
        ("[log10 scale]" if "log10_histo" in linked_options else "[linear scale]"),
        yaxis_title="Dynamic indicator",
        xaxis_title="Stability time [log10]"
    )

    fig_histo_std.update_layout(
        title="Correlation density plot for standard deviation filter " +
        ("[log10 scale]" if "log10_histo" in linked_options else "[linear scale]"),
        yaxis_title="Dynamic indicator",
        xaxis_title="Stability time [log10]"
    )

    
    fig_conf_main_avg, fig_conf_adv_avg, table_cond_avg = pm.confusion_plot_single(
        stab_data,
        avg_convolution,
        log10_ind=False,
        stab_thresh=stab_time,
        sampling=input_samples,
        reverse="reverse" in linked_options
    )

    fig_conf_main_std, fig_conf_adv_std, table_cond_std = pm.confusion_plot_single(
        stab_data,
        std_convolution,
        log10_ind=False,
        stab_thresh=stab_time,
        sampling=input_samples,
        reverse="reverse" in linked_options
    )

    fig_conf_main_avg.update_layout(
        title="Threshold evaluation (average convolution)",
        xaxis_title="Threshold position",
        yaxis_title="Samples"
    )
    fig_conf_main_avg.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    fig_conf_main_std.update_layout(
        title="Threshold evaluation (standard deviation convolution)",
        xaxis_title="Threshold position",
        yaxis_title="Samples"
    )
    fig_conf_main_std.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    return [
        fig_just_stab, fig_img_avg, fig_img_std,
        fig_histo_standard, fig_histo_avg, fig_histo_std,
        fig_conf_main_avg, fig_conf_adv_avg, table_cond_avg,
        fig_conf_main_std, fig_conf_adv_std, table_cond_std
    ]


@app.callback(
    Output({'type': 'fig_combo_confusion', 'index': MATCH}, 'figure'),
    [
        Input({'type': 'dropdown_0', 'index': MATCH}, 'value'),     # 0
        Input({'type': 'dropdown_1', 'index': MATCH}, 'value'),     # 1
        Input({'type': 'dropdown_2', 'index': MATCH}, 'value'),     # 2
        Input({'type': 'dropdown_3', 'index': MATCH}, 'value'),     # 3
        Input({'type': 'dropdown_4', 'index': MATCH}, 'value'),     # 4
        Input({'type': 'dropdown_5', 'index': MATCH}, 'value'),     # 5
        Input({'type': 'linked_options', 'index': MATCH}, 'value'),  # 6
        Input({'type': 'stability_time', 'index': MATCH}, 'value'),  # 7
        Input({'type': 'input_negative', 'index': MATCH}, 'value'),  # 8
        Input({'type': 'input_samples', 'index': MATCH}, 'value'),  # 9
        Input({'type': 'convolution_picker', 'index': MATCH}, 'value'),  # 10
        Input({'type': 'input_kernel', 'index': MATCH}, 'value'),  # 11
    ],
    [
        State({'type': 'main_dropdown', 'index': MATCH}, 'value')   # 12
    ]
)
@cache.memoize(timeout=CACHE_TIMEOUT)
def threshold_plots(
    d_00, d_01, d_02, d_03, d_04, d_05, linked_options,
    stability_time, input_negative, input_samples,
    convolution_picker, input_kernel, md_0
):
    d_0 = (d_00, d_01, d_02, d_03, d_04, d_05)
    handler = handler_list[md_0]
    param_list = handler.get_param_list()
    param_dict = {}
    for i in range(len(param_list)):
        param_dict[param_list[i]] = d_0[i]
    stab_param = {
        'epsilon': param_dict["epsilon"],
        'mu': param_dict["mu"],
        'kick': 'no_kick'
    }
    stab_data = dh.stability_data_handler.get_data(stab_param).flatten()
    iterable = handler.get_data_all_turns(param_dict)
    
    conv = ("avg" if "avg" in convolution_picker else (
        "std" if "std" in convolution_picker else None))
    conv_kernel = None if conv is None else input_kernel
    conv_options = ["reverse"] if "reverse" in linked_options else []

    final_fig = pm.confusion_plot_multiple(
        stab_data,
        iterable,
        log10_ind="log10" in linked_options,
        stab_thresh=stability_time,
        sampling=input_samples,
        reverse="reverse" in linked_options,
        convolution=conv,
        convolution_kernel=conv_kernel,
        convolution_options=conv_options
    )
    return final_fig

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
