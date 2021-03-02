import numpy as np
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State, MATCH, ALL
from app import app
import data_handler as dh
from data_handler import TUNE_X_data_handler, TUNE_Y_data_handler

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
        Input('freq_coloring_options', 'value') # 8
    ],
    [
        State('fig_frequency', 'relayoutData')  # 9
    ]
)
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
            marker=dict(
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
    Output("notification-toast-1", "is_open"),
    [
        #Input('fig_frequency', 'figure'),
        #Input('fig_action', 'figure'),
        #Input({'type': 'figure_diff',
        #       'index': ALL}, 'figure'),
        #Input({'type': 'lay_2_figure', 'index': ALL}, 'figure'),
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