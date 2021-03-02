import numpy as np
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
import json

import data_handler as dh

##### Preliminary setup ########################################################
data_options = [
    {'label':'Stability Time', 'value':0},
    {'label': 'LI', 'value': 1},
    {'label': 'LEI', 'value': 2},
    {'label': 'RE', 'value': 3},
    {'label': 'REI', 'value': 4},
    {'label': 'SALI', 'value': 5},
    {'label': 'GALI', 'value': 6},
    {'label': 'MEGNO', 'value': 7},
    {'label': 'Frequency Map', 'value': 8},
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
    dh.FQ_data_handler
]
################################################################################


##### DASH Framework ###########################################################
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
application = app.server
################################################################################


##### LAYOUT PARAMETERS ########################################################
TAB_1_PADDING = 3
TAB_2_PADDING = 2
TAB_3_PADDING = 2
################################################################################


##### TAB1 LAYOUT ##############################################################
blocks = [
    dbc.Col([
        dbc.Row(
            dcc.Graph(
                id={
                    'type': 'figure',
                    'index': i
                },
                figure=go.Figure()
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                children="Plot options",
                            ),
                            dcc.Checklist(
                                id={
                                    'type': 'plot_options',
                                    'index': i
                                },
                                options=[
                                    {'label': ' Log10 scale', 'value': 'log10'},
                                ],
                                value=[]
                            ),
                        ]
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                id={
                                    'type': 'data_picker',
                                            'index': i
                                },
                                children="Data visualizer {}".format(i),
                            ),
                            dcc.Dropdown(
                                id={
                                    'type': 'main_dropdown',
                                            'index': i
                                },
                                options=data_options,
                                value=0,
                                multi=False,
                                clearable=False
                            ),
                        ]
                    )
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                id={
                                    'type': 'label_0',
                                    'index': i
                                },
                                children="parameter_0",
                            ),
                            dcc.Dropdown(
                                id={
                                    'type': 'dropdown_0',
                                    'index': i
                                },
                                options=[],
                                multi=False,
                                clearable=False
                            ),
                        ]
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                id={
                                    'type': 'label_1',
                                    'index': i
                                },
                                children="parameter_1",
                            ),
                            dcc.Dropdown(
                                id={
                                    'type': 'dropdown_1',
                                    'index': i
                                },
                                options=[],
                                multi=False,
                                clearable=False
                            ),
                        ]
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                id={
                                    'type': 'label_2',
                                    'index': i
                                },
                                children="parameter_2",
                            ),
                            dcc.Dropdown(
                                id={
                                    'type': 'dropdown_2',
                                    'index': i
                                },
                                options=[],
                                multi=False,
                                clearable=False
                            ),
                        ]
                    )
                ),
            ],
            form=True,
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                id={
                                    'type': 'label_3',
                                    'index': i
                                },
                                children="parameter_3",
                            ),
                            dcc.Dropdown(
                                id={
                                    'type': 'dropdown_3',
                                    'index': i
                                },
                                options=[],
                                multi=False,
                                clearable=False
                            ),
                        ]
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                id={
                                    'type': 'label_4',
                                    'index': i
                                },
                                children="parameter_4",
                            ),
                            dcc.Dropdown(
                                id={
                                    'type': 'dropdown_4',
                                    'index': i
                                },
                                options=[],
                                multi=False,
                                clearable=False
                            ),
                        ]
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                id={
                                    'type': 'label_5',
                                    'index': i
                                },
                                children="parameter_5",
                            ),
                            dcc.Dropdown(
                                id={
                                    'type': 'dropdown_5',
                                    'index': i
                                },
                                options=[],
                                multi=False,
                                clearable=False
                            ),
                        ]
                    )
                ),
            ],
        ),
    ])
for i in range(TAB_1_PADDING)
]

################################################################################

##### TAB2 LAYOUT ##############################################################
tab_2_content = [
    dbc.Col([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id={
                    'type': 'corr_figure',
                    'index': i
                },
                figure=go.Figure()
            )
        ]),
        dbc.Col([
            dcc.Graph(
                id={
                    'type': 'corr_figure_bis',
                    'index': i
                },
                figure=go.Figure()
            ),
            dbc.Row([
                dbc.Col(dbc.FormGroup([
                    dbc.Label(
                        children="X N_Bins"
                    ),
                    dcc.Input(
                        id={
                            'type': 'corr_figure_bis_x_bin',
                            'index': i
                        },
                        type="number",
                        placeholder="X n_bins",
                        value=50
                    )
                ])),
                dbc.Col(dbc.FormGroup([
                    dbc.Label(
                        children="Y N_Bins"
                    ),
                    dcc.Input(
                        id={
                            'type': 'corr_figure_bis_y_bin',
                            'index': i
                        },
                        type="number",
                        placeholder="Y n_bins",
                        value=50
                    )
                ])),
                dbc.Col(
                    dcc.Checklist(
                        id={
                            'type': 'corr_figure_bis_options',
                                    'index': i
                        },
                        options=[
                            {'label': ' Log10 scale (for density)', 'value': 'log10'},
                        ],
                        value=[]
                    ),
                )
            ])
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    children="Data options X axis",
                                ),
                                dcc.Checklist(
                                    id={
                                        'type': 'plot_options',
                                        'index': i
                                    },
                                    options=[
                                        {'label': ' Log10 scale',
                                            'value': 'log10'},
                                    ],
                                    value=[]
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'data_picker',
                                        'index': i
                                    },
                                    children="Data to place on X axis",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'main_dropdown',
                                        'index': i
                                    },
                                    options=data_options,
                                    value=0,
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_0',
                                        'index': i
                                    },
                                    children="parameter_0",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_0',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_1',
                                        'index': i
                                    },
                                    children="parameter_1",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_1',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_2',
                                        'index': i
                                    },
                                    children="parameter_2",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_2',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                ],
                form=True,
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_3',
                                        'index': i
                                    },
                                    children="parameter_3",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_3',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_4',
                                        'index': i
                                    },
                                    children="parameter_4",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_4',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_5',
                                        'index': i
                                    },
                                    children="parameter_5",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_5',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                ],
            ) ]),
        dbc.Col([
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    children="Data options Y Axis",
                                ),
                                dcc.Checklist(
                                    id={
                                        'type': 'plot_options',
                                        'index': i + 1
                                    },
                                    options=[
                                        {'label': ' Log10 scale',
                                            'value': 'log10'},
                                    ],
                                    value=[]
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'data_picker',
                                        'index': i + 1
                                    },
                                    children="Data to place on Y axis",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'main_dropdown',
                                        'index': i + 1
                                    },
                                    options=data_options,
                                    value=0,
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_0',
                                        'index': i + 1
                                    },
                                    children="parameter_0",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_0',
                                        'index': i + 1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_1',
                                        'index': i + 1
                                    },
                                    children="parameter_1",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_1',
                                        'index': i + 1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_2',
                                        'index': i + 1
                                    },
                                    children="parameter_2",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_2',
                                        'index': i + 1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                ],
                form=True,
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_3',
                                        'index': i + 1
                                    },
                                    children="parameter_3",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_3',
                                        'index': i + 1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_4',
                                        'index': i + 1
                                    },
                                    children="parameter_4",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_4',
                                        'index': i + 1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_5',
                                        'index': i + 1
                                    },
                                    children="parameter_5",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_5',
                                        'index': i + 1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                ],
            ), ]),
    ])
    ])
for i in range(TAB_1_PADDING, TAB_2_PADDING + TAB_1_PADDING, 2)]
################################################################################


##### TAB3 LAYOUT ##############################################################
comparison_blocks = [
    dbc.Col(dbc.Row([
        dbc.Col([
            dbc.Row(
                dcc.Graph(
                    id={
                        'type': 'figure',
                        'index': i
                    },
                    figure=go.Figure()
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    children="Plot options",
                                ),
                                dcc.Checklist(
                                    id={
                                        'type': 'plot_options',
                                        'index': i
                                    },
                                    options=[
                                        {'label': ' Log10 scale',
                                            'value': 'log10'},
                                    ],
                                    value=[]
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'data_picker',
                                        'index': i
                                    },
                                    children="Data visualizer {}".format(i),
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'main_dropdown',
                                        'index': i
                                    },
                                    options=data_options,
                                    value=0,
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_0',
                                        'index': i
                                    },
                                    children="parameter_0",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_0',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_1',
                                        'index': i
                                    },
                                    children="parameter_1",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_1',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_2',
                                        'index': i
                                    },
                                    children="parameter_2",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_2',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                ],
                form=True,
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_3',
                                        'index': i
                                    },
                                    children="parameter_3",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_3',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_4',
                                        'index': i
                                    },
                                    children="parameter_4",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_4',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_5',
                                        'index': i
                                    },
                                    children="parameter_5",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_5',
                                        'index': i
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                ],
            )
        ]),
        dbc.Col([
            dbc.Row(
                dcc.Graph(
                    id={
                        'type': 'figure',
                        'index': i+1
                    },
                    figure=go.Figure()
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    children="Plot options",
                                ),
                                dcc.Checklist(
                                    id={
                                        'type': 'plot_options',
                                        'index': i+1
                                    },
                                    options=[
                                        {'label': ' Log10 scale',
                                            'value': 'log10'},
                                    ],
                                    value=[]
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'data_picker',
                                        'index': i+1
                                    },
                                    children="Data visualizer {}".format(i+1),
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'main_dropdown',
                                        'index': i+1
                                    },
                                    options=data_options,
                                    value=0,
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_0',
                                        'index': i+1
                                    },
                                    children="parameter_0",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_0',
                                        'index': i+1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_1',
                                        'index': i+1
                                    },
                                    children="parameter_1",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_1',
                                        'index': i+1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_2',
                                        'index': i+1
                                    },
                                    children="parameter_2",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_2',
                                        'index': i+1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                ],
                form=True,
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_3',
                                        'index': i+1
                                    },
                                    children="parameter_3",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_3',
                                        'index': i+1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_4',
                                        'index': i+1
                                    },
                                    children="parameter_4",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_4',
                                        'index': i+1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    id={
                                        'type': 'label_5',
                                        'index': i+1
                                    },
                                    children="parameter_5",
                                ),
                                dcc.Dropdown(
                                    id={
                                        'type': 'dropdown_5',
                                        'index': i+1
                                    },
                                    options=[],
                                    multi=False,
                                    clearable=False
                                ),
                            ]
                        )
                    ),
                ],
            )
        ]),
        dbc.Col([
            dbc.Row(
                dcc.Graph(
                    id={
                        'type': 'figure_diff',
                        'index': i
                    },
                    figure=go.Figure()
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    children="Diff plot options",
                                ),
                                dcc.Checklist(
                                    id={
                                        'type': 'plot_options_diff',
                                        'index': i
                                    },
                                    options=[
                                        {'label': ' Log10 scale',
                                            'value': 'log10'},
                                        {'label': ' Absolute value',
                                            'value': 'absolute'},
                                        {'label': ' Relative difference',
                                            'value': 'relative'},
                                    ],
                                    value=[]
                                ),
                            ]
                        )
                    ),
                ]
            )
        ]),
    ]))
for i in range(TAB_1_PADDING + TAB_2_PADDING, TAB_1_PADDING + TAB_2_PADDING + TAB_3_PADDING, 2)]

################################################################################


##### FINAL LAYOUT #############################################################
app.layout = html.Div([
    dbc.Toast(
        [html.P("Plot(s) updated!", className="mb-0")],
        id="notification-toast",
        header="Notification",
        icon="primary",
        dismissable=True,
        is_open=False,
        duration=4000,
        style={"position": "fixed-top", "top": 66, "right": 10, "width": 350},
    ),
    dbc.Tabs([
        dbc.Tab(
            [
                dbc.Row(blocks[0:3]),
                #dbc.Row(blocks[3:6]),
                #dbc.Row(blocks[6:9])
            ],
            label="Heatmaps",
        ),
        dbc.Tab(
            [
                dbc.Row(tab_2_content[0]),
                #dbc.Row(tab_2_content[1]),
            ],
            label="Correlation plot",
        ),
        dbc.Tab(
            [
                dbc.Row(comparison_blocks[0]),
                #dbc.Row(comparison_blocks[1]),
            ],
            label="Heatmap Comparison"
        )
    ])
])
################################################################################


##### CALLBACKS ################################################################

#### Options update ####

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

#### Grab data and create figure ####

@app.callback(
    Output({'type': 'figure', 'index': MATCH}, 'figure'),
    [
        Input({'type': 'dropdown_0', 'index': MATCH}, 'value'),
        Input({'type': 'dropdown_1', 'index': MATCH}, 'value'),
        Input({'type': 'dropdown_2', 'index': MATCH}, 'value'),
        Input({'type': 'dropdown_3', 'index': MATCH}, 'value'),
        Input({'type': 'dropdown_4', 'index': MATCH}, 'value'),
        Input({'type': 'dropdown_5', 'index': MATCH}, 'value'),
        Input({'type': 'plot_options', 'index': MATCH}, 'value'),
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


#### Same thing but for the correlation plot ###
def exe_update_correlation_plot(*args):
    handler_1 = handler_list[args[14]]
    handler_2 = handler_list[args[15]]

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


@app.callback(
    Output({'type': 'corr_figure', 'index': TAB_1_PADDING}, 'figure'),
    [
        Input({'type': 'dropdown_0', 'index': TAB_1_PADDING}, 'value'),    # 0
        Input({'type': 'dropdown_1', 'index': TAB_1_PADDING}, 'value'),    # 1
        Input({'type': 'dropdown_2', 'index': TAB_1_PADDING}, 'value'),    # 2
        Input({'type': 'dropdown_3', 'index': TAB_1_PADDING}, 'value'),    # 3
        Input({'type': 'dropdown_4', 'index': TAB_1_PADDING}, 'value'),    # 4
        Input({'type': 'dropdown_5', 'index': TAB_1_PADDING}, 'value'),    # 5
        Input({'type': 'plot_options', 'index': TAB_1_PADDING}, 'value'),  # 6
        Input({'type': 'dropdown_0', 'index': TAB_1_PADDING+1}, 'value'),    # 7
        Input({'type': 'dropdown_1', 'index': TAB_1_PADDING+1}, 'value'),    # 8
        Input({'type': 'dropdown_2', 'index': TAB_1_PADDING+1}, 'value'),    # 9
        Input({'type': 'dropdown_3', 'index': TAB_1_PADDING+1}, 'value'),    # 10
        Input({'type': 'dropdown_4', 'index': TAB_1_PADDING+1}, 'value'),    # 11
        Input({'type': 'dropdown_5', 'index': TAB_1_PADDING+1}, 'value'),    # 12
        Input({'type': 'plot_options', 'index': TAB_1_PADDING+1}, 'value')   # 13
    ],
    [
        State({'type': 'main_dropdown', 'index': TAB_1_PADDING}, 'value'),  # 14
        State({'type': 'main_dropdown', 'index': TAB_1_PADDING+1}, 'value')  # 15
    ]
)
def update_correlation_plot(*args):
    return exe_update_correlation_plot(*args)


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
    """
    fig = go.Figure(
        data = go.Contour(
            z=histo,
            x=(xedj[:-1] + xedj[1:]) / 2,
            y=(yedj[:-1] + yedj[1:]) / 2,
            hoverongaps=False,
            line_smoothing=0.85,
            connectgaps=True,
            colorscale="Viridis"
        )
    )
    """
    fig.update_layout(
        title="Correlation Density Plot " + ("[log10 scale]" if "log10" in args[16] else "[linear scale]")
    )

    return fig


@app.callback(
    Output({'type': 'corr_figure_bis', 'index': TAB_1_PADDING}, 'figure'),
    [
        Input({'type': 'dropdown_0', 'index': TAB_1_PADDING}, 'value'),    # 0
        Input({'type': 'dropdown_1', 'index': TAB_1_PADDING}, 'value'),    # 1
        Input({'type': 'dropdown_2', 'index': TAB_1_PADDING}, 'value'),    # 2
        Input({'type': 'dropdown_3', 'index': TAB_1_PADDING}, 'value'),    # 3
        Input({'type': 'dropdown_4', 'index': TAB_1_PADDING}, 'value'),    # 4
        Input({'type': 'dropdown_5', 'index': TAB_1_PADDING}, 'value'),    # 5
        Input({'type': 'plot_options', 'index': TAB_1_PADDING}, 'value'),  # 6
        Input({'type': 'dropdown_0', 'index': TAB_1_PADDING+1}, 'value'),    # 7
        Input({'type': 'dropdown_1', 'index': TAB_1_PADDING+1}, 'value'),    # 8
        Input({'type': 'dropdown_2', 'index': TAB_1_PADDING+1}, 'value'),    # 9
        Input({'type': 'dropdown_3', 'index': TAB_1_PADDING+1}, 'value'),    # 10
        Input({'type': 'dropdown_4', 'index': TAB_1_PADDING+1}, 'value'),    # 11
        Input({'type': 'dropdown_5', 'index': TAB_1_PADDING+1}, 'value'),    # 12
        Input({'type': 'plot_options', 'index': TAB_1_PADDING+1}, 'value'),  # 13
        Input({'type': 'corr_figure_bis_x_bin', 'index': TAB_1_PADDING}, 'value'),  # 14
        Input({'type': 'corr_figure_bis_y_bin', 'index': TAB_1_PADDING}, 'value'),  # 15
        Input({'type': 'corr_figure_bis_options', 'index': TAB_1_PADDING}, 'value'),# 16
    ],
    [
        State({'type': 'main_dropdown', 'index': TAB_1_PADDING}, 'value'),  # 17
        State({'type': 'main_dropdown', 'index': TAB_1_PADDING+1}, 'value')  # 18
    ]
)
def update_correlation_plot_bis(*args):
    return exe_update_correlation_plot_bis(*args)


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
    Output({'type': 'figure_diff', 'index': TAB_1_PADDING+TAB_2_PADDING}, 'figure'),
    [
        Input({'type': 'dropdown_0', 'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),    # 0
        Input({'type': 'dropdown_1', 'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),    # 1
        Input({'type': 'dropdown_2', 'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),    # 2
        Input({'type': 'dropdown_3', 'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),    # 3
        Input({'type': 'dropdown_4', 'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),    # 4
        Input({'type': 'dropdown_5', 'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),    # 5
        Input({'type': 'plot_options', 'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),  # 6
        Input({'type': 'dropdown_0', 'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value'),    # 7
        Input({'type': 'dropdown_1', 'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value'),    # 8
        Input({'type': 'dropdown_2', 'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value'),    # 9
        Input({'type': 'dropdown_3', 'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value'),    # 10
        Input({'type': 'dropdown_4', 'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value'),    # 11
        Input({'type': 'dropdown_5', 'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value'),    # 12
        Input({'type': 'plot_options', 'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value'),  # 13
        Input({'type': 'plot_options_diff', 'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),  # 14
    ],
    [
        State({'type': 'main_dropdown', 'index': TAB_1_PADDING+TAB_2_PADDING}, 'value'),  # 15
        State({'type': 'main_dropdown', 'index': TAB_1_PADDING+TAB_2_PADDING+1}, 'value')  # 16
    ]
)
def update_diff_plot(*args):
    return exe_update_diff_plot(*args)


@app.callback(
    Output("notification-toast", "is_open"),
    [
        Input({'type': 'corr_figure_bis', 'index': TAB_1_PADDING}, 'figure'),
        Input({'type': 'figure', 'index': ALL}, 'figure'),
    ]
)
def update_toast(*p):
    return True

################################################################################


##### RUN THE SERVER ###########################################################
if __name__ == '__main__':
    app.run_server(port=8080, debug=True)
################################################################################
