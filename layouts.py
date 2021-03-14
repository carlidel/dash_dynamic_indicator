import numpy as np
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
import json

from data_handler import stability_data_handler, FQ_data_handler

##### LAYOUT PARAMETERS ########################################################
TAB_1_PADDING = 9
TAB_2_PADDING = 4
TAB_3_PADDING = 4
TAB_5_PADDING = 4
TAB_6_PADDING = 2
TAB_7_PADDING = 2
TAB_8_PADDING = 6

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

##### TAB1 LAYOUT ##############################################################
blocks = [
    dbc.Col([
        dbc.Row(
            dcc.Graph(
                id={
                    'type': 'linked_figure',
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
                                    'type': 'linked_options',
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

layout_1 = html.Div([
    dbc.Row(blocks[0:3]),
    dbc.Row(blocks[3:6]),
    dbc.Row(blocks[6:9]),
])

################################################################################

##### TAB2 LAYOUT ##############################################################
layout_2 = html.Div([
    dbc.Col([
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id={
                        'type': 'lay_2_figure',
                        'index': i
                    },
                    figure=go.Figure()
                )
            ]),
            dbc.Col([
                dcc.Graph(
                    id={
                        'type': 'lay_2_figure_bis',
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
                                'type': 'lay_2_x_bin',
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
                                'type': 'lay_2_y_bin',
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
                                'type': 'lay_2_fig_options',
                                'index': i
                            },
                            options=[
                                {'label': ' Log10 scale (for density)',
                                 'value': 'log10'},
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
                                            'type': 'linked_options',
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
                )]),
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
                                            'type': 'linked_options',
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
    for i in range(TAB_1_PADDING, TAB_2_PADDING + TAB_1_PADDING, 2)
])
################################################################################

##### TAB3 LAYOUT ##############################################################
layout_3 = html.Div([
    dbc.Col(dbc.Row([
        dbc.Col([
            dbc.Row(
                dcc.Graph(
                    id={
                        'type': 'linked_figure',
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
                                        'type': 'linked_options',
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
                        'type': 'linked_figure',
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
                                        'type': 'linked_options',
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
    for i in range(TAB_1_PADDING + TAB_2_PADDING, TAB_1_PADDING + TAB_2_PADDING + TAB_3_PADDING, 2)
])

################################################################################

#### TAB 4 LAYOUT ##############################################################
layout_4 = html.Div([
    dbc.Col([
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="fig_action",
                    figure=go.Figure()
                )
            ]),
            dbc.Col([
                dcc.Graph(
                    id="fig_frequency",
                    figure=go.Figure()
                )
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label(
                    children="Epsilon"
                ),
                dcc.Dropdown(
                    id="drop_epsilon",
                    options=[{'label': str(s), 'value': s} for s in stability_data_handler.get_param_options(
                        "epsilon")],
                    value=stability_data_handler.get_param_options("epsilon")[
                        0],
                    multi=False,
                    clearable=False
                ),
                dbc.Label(
                    children="Mu"
                ),
                dcc.Dropdown(
                    id="drop_mu",
                    options=[{'label': str(s), 'value': s} for s in stability_data_handler.get_param_options(
                        "mu")],
                    value=stability_data_handler.get_param_options("mu")[0],
                    multi=False,
                    clearable=False
                ),
                dbc.Label(
                    children="N turns"
                ),
                dcc.Dropdown(
                    id="drop_nturns",
                    options=[{'label': str(s), 'value': s} for s in FQ_data_handler.get_param_options(
                        "turns")],
                    value=FQ_data_handler.get_param_options("turns")[0],
                    multi=False,
                    clearable=False
                )
            ]),
            dbc.Col(dbc.FormGroup([
                dbc.Row([
                    dbc.Label(
                        children="Tolerance"
                    ),
                    dcc.Input(
                        id="input_tolerance",
                        type="number",
                        value=2.5e-3
                    )
                ]),
                dbc.Row([
                    dbc.Label(
                        children="Min resonance"
                    ),
                    dcc.Input(
                        id="input_minres",
                        type="number",
                        value=3
                    ),
                    dbc.Label(
                        children="Max resonance"
                    ),
                    dcc.Input(
                        id="input_maxres",
                        type="number",
                        value=6
                    )
                ]),
                dbc.Row([
                    dbc.Label(
                        children="Known X tune"
                    ),
                    dcc.Input(
                        id="xtune",
                        type="number",
                        value=0.168
                    ),
                    dbc.Label(
                        children="Known Y tune"
                    ),
                    dcc.Input(
                        id="ytune",
                        type="number",
                        value=0.201
                    )
                ]),
                dbc.Row([
                    dbc.Col(dbc.Label(
                        children="Coloring options in resonance plot data (freq. space)"
                    )),
                    dbc.Col(dcc.Dropdown(
                        id="freq_coloring_options",
                        options=[
                            {'label': 'Just Black', 'value': 'black'},
                            {'label': 'Stability Time [log10 scale]', 'value': 'stab'},
                            {'label': 'Radial Distance', 'value': 'radial'},
                        ],
                        value='black',
                        multi=False,
                        clearable=False
                    ))
                ])
            ])),
        ])
    ])
])

########## TAB 5 ###############################################################

confusion_block = [dbc.Col([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id={
                    "type": "fig_main_confusion",
                    'index': i
                },
                figure=go.Figure()
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id={
                    'type': "fig_advanced_confusion",
                    'index': i
                },
                figure=go.Figure()
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Table(
                id={
                    'type': 'tab_confusion',
                    'index': i
                },
                bordered=True
            )
        ]),
        dbc.Col([
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    children="Options",
                                ),
                                dcc.Checklist(
                                    id={
                                        'type': 'linked_options',
                                        'index': i
                                    },
                                    options=[
                                        {'label': ' Execute threshold sampling on a log10space',
                                            'value': 'log10'},
                                        {'label': ' Invert the classification method',
                                            'value': 'reverse'},
                                        {'label': ' Plot a full threshold analysis down below',
                                            'value': 'full_scan'
                                        },
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
                                    children="Data selector",
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
            dbc.Row([
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                children="N Turns to consider 'stable'",
                            ),
                            dcc.Input(
                                id={
                                    'type': "stability_time",
                                    'index': i
                                },
                                value=1.0e7,
                                type="number"
                            ),
                            html.Br(),
                            dbc.Label(
                                children="placeholder_2",
                            ),
                            dcc.Input(
                                id={
                                    'type': "input_negative",
                                    'index': i
                                },
                                value=1.0,
                                type="number"
                            ),
                        ]
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                children="N samples",
                            ),
                            dcc.Input(
                                id={
                                    'type': "input_samples",
                                    'index': i
                                },
                                value=100,
                                type="number"
                            ),
                        ]
                    )
                )
            ])
        ])
    ])
    ])
    for i in range(TAB_1_PADDING + TAB_2_PADDING + TAB_3_PADDING, TAB_1_PADDING + TAB_2_PADDING + TAB_3_PADDING + TAB_5_PADDING)
]

confusion_block_2 = [dbc.Col([
        dcc.Graph(
            id={
                "type": "fig_thresh_evolution",
                        'index': i
            },
            figure=go.Figure()
        )
    ])
    for i in range(TAB_1_PADDING + TAB_2_PADDING + TAB_3_PADDING, TAB_1_PADDING + TAB_2_PADDING + TAB_3_PADDING + TAB_5_PADDING)
]

layout_5 = dbc.Col([
    dbc.Row([
        confusion_block[0],
        confusion_block[1],
    ]), 
    dbc.Row([
        confusion_block[2],
        confusion_block[3],
    ]),
    html.H2("Threshold position over time"),
    dbc.Row([
        confusion_block_2[0],
        confusion_block_2[1]
    ]),
    dbc.Row([
        confusion_block_2[2],
        confusion_block_2[3]
    ])
])

################################################################################

#### TAB 6 #####################################################################

block_6 = [dbc.Row([
        dbc.Col([
            dcc.Graph(
                id={
                    'type': 'fig_evolution',
                    'index': i
                },
                figure=go.Figure()
            )
        ], width=9),
        dbc.Col([
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
                                        'type': 'linked_options',
                                        'index': i
                                    },
                                    options=[
                                        {'label': 'Filter unstable particles',
                                            'value': 'filter'
                                         },
                                        {'label': 'Log scale (indicator value)',
                                            'value': 'log10'
                                         },
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
                                    children="Data selector",
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
            dbc.Row([
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                children="Min turns to visualize",
                            ),
                            dcc.Input(
                                id={
                                    'type': "min_turns",
                                    'index': i
                                },
                                value=0,
                                type="number"
                            ),
                            html.Br(),
                            dbc.Label(
                                children="Max turns to visualize",
                            ),
                            dcc.Input(
                                id={
                                    'type': "max_turns",
                                    'index': i
                                },
                                value=10000000,
                                type="number"
                            ),
                            html.Br(),
                            dbc.Label(
                                children="Samples to skip",
                            ),
                            dcc.Input(
                                id={
                                    'type': "sample_skip",
                                    'index': i
                                },
                                value=101,
                                type="number"
                            ),
                        ]
                    )
                )
            ])
        ], width=3)
    ])
for i in range(
    TAB_1_PADDING + TAB_2_PADDING + TAB_3_PADDING + TAB_5_PADDING,
    TAB_1_PADDING + TAB_2_PADDING + TAB_3_PADDING + TAB_5_PADDING + TAB_6_PADDING
    )
]

layout_6 = dbc.Col([
    block_6[0],
    block_6[1]
])

################################################################################

#### TAB 7 #####################################################################

block_7 = [
    [
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id={
                    'type': 'linked_figure',
                    'index': i
                },
                figure=go.Figure()
            ),
            dcc.Graph(
                id={
                    'type': 'linked_stab_figure',
                    'index': i
                },
                figure=go.Figure()
            )
        ], width=4),
        dbc.Col([
            dcc.Graph(
                id={
                    'type': 'conv_avg_figure',
                    'index': i
                },
                figure=go.Figure()
            ),
            dcc.Graph(
                id={
                    'type': 'conv_std_figure',
                    'index': i
                },
                figure=go.Figure()
            )
        ], width=5),
        dbc.Col([
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
                                        'type': 'linked_options',
                                        'index': i
                                    },
                                    options=[
                                        {'label': 'Log scale (for visualizing the indicator values and perform the samplings in the conufusion matrix)',
                                            'value': 'log10'
                                         },
                                         {'label': 'Invert the colorscale in the Heatmaps',
                                            'value': 'color_invert'
                                         },
                                        {'label': 'Toggle Log scale for the correlation',
                                            'value': 'log10_histo'
                                         },
                                        {'label': ' Invert the classification method for the confusion matrix',
                                            'value': 'reverse'},
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
                                    children="Data selector",
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
            dbc.Row([
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                children="Kernel size for convolutions",
                            ),
                            dcc.Input(
                                id={
                                    'type': "kernel_size",
                                    'index': i
                                },
                                value=3,
                                type="number"
                            ),
                            html.Br(),
                            dbc.Label(
                                children="X Bins (correlation plots)",
                            ),
                            dcc.Input(
                                id={
                                    'type': "x_bins",
                                    'index': i
                                },
                                value=50,
                                type="number"
                            ),
                            html.Br(),
                            dbc.Label(
                                children="Y Bins (correlation plots)",
                            ),
                            dcc.Input(
                                id={
                                    'type': "y_bins",
                                    'index': i
                                },
                                value=25,
                                type="number"
                            ),
                            html.Br(),
                            dbc.Label(
                                children="N Turns to consider 'stable'",
                            ),
                            dcc.Input(
                                id={
                                    'type': "stability_time",
                                    'index': i
                                },
                                value=1.0e7,
                                type="number"
                            ),
                            html.Br(),
                            dbc.Label(
                                children="placeholder_2",
                            ),
                            dcc.Input(
                                id={
                                    'type': "input_negative",
                                    'index': i
                                },
                                value=1.0,
                                type="number"
                            ),
                            html.Br(),
                            dbc.Label(
                                children="N samples",
                            ),
                            dcc.Input(
                                id={
                                    'type': "input_samples",
                                    'index': i
                                },
                                value=100,
                                type="number"
                            ),
                        ]
                    )
                )
            ])
        ], width=3),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id={
                    'type': 'corr_plot_standard_fig',
                    'index': i
                },
                figure=go.Figure()
            )
        ]),
        dbc.Col([
            dcc.Graph(
                id={
                    'type': 'corr_plot_avg_fig',
                    'index': i
                },
                figure=go.Figure()
            )
        ]),
        dbc.Col([
            dcc.Graph(
                id={
                    'type': 'corr_plot_std_fig',
                    'index': i
                },
                figure=go.Figure()
            )
        ]),
    ])
    ]
for i in range(
    TAB_1_PADDING+TAB_2_PADDING+TAB_3_PADDING +
        TAB_5_PADDING+TAB_6_PADDING,
    TAB_1_PADDING+TAB_2_PADDING+TAB_3_PADDING +
        TAB_5_PADDING+TAB_6_PADDING+TAB_7_PADDING
)]


extra_block_7 = [
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id={
                    "type": "fig_main_confusion",
                    'index': i
                },
                figure=go.Figure()
            ),
            dcc.Graph(
                id={
                    'type': "fig_advanced_confusion",
                    'index': i
                },
                figure=go.Figure()
            ),
            dbc.Table(
                id={
                    'type': 'tab_confusion',
                    'index': i
                },
                bordered=True
            )
        ]),
        dbc.Col([
            dcc.Graph(
                id={
                    "type": "fig_avg_main_confusion",
                    'index': i
                },
                figure=go.Figure()
            ),
            dcc.Graph(
                id={
                    'type': "fig_avg_advanced_confusion",
                    'index': i
                },
                figure=go.Figure()
            ),
            dbc.Table(
                id={
                    'type': 'tab_avg_confusion',
                    'index': i
                },
                bordered=True
            )
        ]),
        dbc.Col([
            dcc.Graph(
                id={
                    "type": "fig_std_main_confusion",
                    'index': i
                },
                figure=go.Figure()
            ),
            dcc.Graph(
                id={
                    'type': "fig_std_advanced_confusion",
                    'index': i
                },
                figure=go.Figure()
            ),
            dbc.Table(
                id={
                    'type': 'tab_std_confusion',
                    'index': i
                },
                bordered=True
            )
        ]),
    ])

    for i in range(
        TAB_1_PADDING+TAB_2_PADDING+TAB_3_PADDING +
            TAB_5_PADDING+TAB_6_PADDING,
        TAB_1_PADDING+TAB_2_PADDING+TAB_3_PADDING +
            TAB_5_PADDING+TAB_6_PADDING+TAB_7_PADDING
)]


dummy_block_7 = [html.Div(dbc.Col([
    dcc.Graph(
        id={
            "type": "fig_thresh_evolution",
            'index': i
        },
        figure=go.Figure()
    )
]), hidden=True)
    for i in range(
    TAB_1_PADDING+TAB_2_PADDING+TAB_3_PADDING +
    TAB_5_PADDING+TAB_6_PADDING,
    TAB_1_PADDING+TAB_2_PADDING+TAB_3_PADDING +
    TAB_5_PADDING+TAB_6_PADDING+TAB_7_PADDING
)
]

layout_7 = dbc.Col([
    block_7[0][0],
    block_7[0][1],
    extra_block_7[0],
    dummy_block_7[0],
    block_7[1][0],
    block_7[1][1],
    extra_block_7[1],
    dummy_block_7[1]
])

################################################################################

#### TAB 7 #####################################################################

block_8 = [
    dbc.Col([
        dcc.Graph(
            id={
                'type': 'fig_combo_confusion',
                'index': i
            },
            figure=go.Figure()
        ),
        dbc.Row([
            dbc.Col(
                dbc.FormGroup([
                    dbc.Label(
                        children="Options",
                    ),
                    dcc.Checklist(
                        id={
                            'type': 'linked_options',
                            'index': i
                        },
                        options=[
                            {'label': ' Execute threshold sampling on a log10space',
                                'value': 'log10'},
                            {'label': ' Invert the classification method',
                                'value': 'reverse'},
                        ],
                        value=[]
                    ),
                ])
            ),
            dbc.Col(
                dbc.FormGroup([
                    dbc.Label(
                        id={
                            'type': 'data_picker',
                            'index': i
                        },
                        children="Data selector",
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
                    dbc.Label(
                        children="Convolution procedure to apply"
                    ),
                    dcc.Dropdown(
                        id={
                            'type': 'convolution_picker',
                            'index': i
                        },
                        options=[
                            {'label': 'Original data (no convolution)', 'value': 'none'},
                            {'label': 'Pick average value in kernel', 'value': 'avg'},
                            {'label': 'Pick standard deviation in kernel', 'value': 'std'},
                        ],
                        value='none',
                        multi=False,
                        clearable=False
                    ),
                    dbc.Label(
                        children="Kernel size (if picked)"
                    ),
                    dcc.Input(
                        id={
                            'type': "input_kernel",
                                    'index': i
                        },
                        value=7.0,
                        type="number"
                    )
                ])
            )
        ]),
        dbc.Row([
            dbc.Col(
                dbc.FormGroup([
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
                ])
            ),
            dbc.Col(
                dbc.FormGroup([
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
                ])
            ),
            dbc.Col(
                dbc.FormGroup([
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
                ])
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
        dbc.Row([
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                children="N Turns to consider 'stable'",
                            ),
                            dcc.Input(
                                id={
                                    'type': "stability_time",
                                    'index': i
                                },
                                value=1.0e7,
                                type="number"
                            ),
                            html.Br(),
                            dbc.Label(
                                children="placeholder_2",
                            ),
                            dcc.Input(
                                id={
                                    'type': "input_negative",
                                    'index': i
                                },
                                value=1.0,
                                type="number"
                            ),
                        ]
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label(
                                children="N samples",
                            ),
                            dcc.Input(
                                id={
                                    'type': "input_samples",
                                    'index': i
                                },
                                value=100,
                                type="number"
                            ),
                        ]
                    )
                )
                ])
    ])
    for i in range(
        TAB_1_PADDING+TAB_2_PADDING+TAB_3_PADDING+
        TAB_5_PADDING+TAB_6_PADDING+TAB_7_PADDING,
        TAB_1_PADDING+TAB_2_PADDING+TAB_3_PADDING+
        TAB_5_PADDING+TAB_6_PADDING+TAB_7_PADDING+TAB_8_PADDING
    )
]
 
layout_8 = dbc.Col([
    dbc.Row([block_8[0],block_8[1]]),
    dbc.Row([block_8[2],block_8[3]]),
    dbc.Row([block_8[4],block_8[5]]),
])
################################################################################
