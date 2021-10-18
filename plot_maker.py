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
#from numba import njit, prange


def simple_heatmap(data, log10=False, title="", reversescale=False):
    if log10:
        data = np.log10(data)
    fig = go.Figure()
    fig.add_trace(
        go.Heatmap(
            z=data,
            x=np.linspace(0, 1, 500),
            y=np.linspace(0, 1, 500),
            hoverongaps=False,
            colorscale="Viridis",
            reversescale=reversescale
        )
    )
    fig.update_layout(
        title=title + ("[log10 scale]" if log10 else ""),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


def correlation_plot(data_1, data_2, log10_x=False, log10_y=False):
    if log10_x:
        data_1 = np.log10(data_1)
    if log10_y:
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


def correlation_plot_bis(data_1, data_2, n_bins_x, n_bins_y, log10_x=False, log10_y=False, log10_hist=True):
    if log10_x:
        data_1[data_1 == 0] = np.nan
        data_1 = np.log10(data_1)

    if log10_y:
        data_2[data_2 == 0] = np.nan
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
        bins=[n_bins_x, n_bins_y],
        range=[[data_1.min(), data_1.max()], [data_2.min(), data_2.max()]]
    )

    histo[histo == 0] = np.nan
    if log10_hist:
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
        ("[log10 scale]" if log10_hist else "[linear scale]")
    )

    return fig


def diff_plot(data_1, data_2, log10_x=False, log10_y=False, relative_plot=False, absolute_plot=False, log10_plot=False):
    if log10_x:
        data_1 = np.log10(data_1)
    if log10_y:
        data_2 = np.log10(data_2)

    # make plot
    data = data_1 - data_2
    if relative_plot:
        data = data / data_1
    if absolute_plot:
        data = np.absolute(data)
    if log10_plot:
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
        + ("[absolute value] " if absolute_plot else "")
        + ("[log10 scale]" if log10_plot else "[linear scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


def confusion_data(stab_data, ind_data, log10_ind=False, stab_thresh=1e7,sampling=100, reverse=False):
    stab_data = stab_data.flatten()
    ind_data = ind_data.flatten()

    if log10_ind:
        ind_data[ind_data == 0] = np.nan
        ind_data = np.log10(ind_data)
    max_ind = np.nanmax(ind_data)
    min_ind = np.nanmin(ind_data)
    samples = np.linspace(min_ind, max_ind, sampling+2)[1:-1]

    tp = np.empty(sampling)
    tn = np.empty(sampling)
    fp = np.empty(sampling)
    fn = np.empty(sampling)

    for i, v in enumerate(samples):
        if reverse:
            tp[i] = np.count_nonzero(stab_data[ind_data >= v] >= stab_thresh)
            tn[i] = np.count_nonzero(stab_data[ind_data < v] < stab_thresh)
            fp[i] = np.count_nonzero(stab_data[ind_data < v] >= stab_thresh)
            fn[i] = np.count_nonzero(stab_data[ind_data >= v] < stab_thresh)
        else:
            tp[i] = np.count_nonzero(stab_data[ind_data < v] >= stab_thresh)
            tn[i] = np.count_nonzero(stab_data[ind_data >= v] < stab_thresh)
            fp[i] = np.count_nonzero(stab_data[ind_data >= v] >= stab_thresh)
            fn[i] = np.count_nonzero(stab_data[ind_data < v] < stab_thresh)

    accuracy = (tp+tn)/(tp+tn+fp+fn)
    precision = tp/(tp+fp)
    sensitivity = tp/(tp+fn)
    specificity = tn/(tn+fp)

    max_accuracy_idx = np.nanargmax(accuracy)
    max_accuracy = accuracy[max_accuracy_idx]
    best_threshold = samples[max_accuracy_idx]

    return(
        samples,
        tp, tn, fp, fn,
        accuracy, precision, sensitivity, specificity,
        max_accuracy_idx, max_accuracy, best_threshold
    )


def confusion_plot_single(stab_data, ind_data, log10_ind=False, stab_thresh=1e7, sampling=100, reverse=False):

    samples,\
    tp, tn, fp, fn,\
    accuracy, precision, sensitivity, specificity,\
    max_accuracy_idx, max_accuracy, best_threshold = confusion_data(
        stab_data, ind_data, log10_ind, 
        stab_thresh, sampling, reverse
    )

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

    fig.update_layout(
        title="Threshold evaluation",
        xaxis_title="Threshold position",
        yaxis_title="Samples"
    )

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
        best_threshold,
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
        html.Td("{:2e}".format(samples[max_accuracy_idx]))
    ])
    row3 = html.Tr([
        html.Td("Accuracy (all correct / all)"),
        html.Td("{:.2f}%".format((max_accuracy*100)))
    ])
    row2 = html.Tr([
        html.Td("Precision (true positives / predicted positives)"),
        html.Td("{:.2f}%".format((precision[max_accuracy_idx]*100)))
    ])
    row4 = html.Tr([
        html.Td("Sensitivity (true positives / all actual positives)"),
        html.Td("{:.2f}%".format((sensitivity[max_accuracy_idx]*100)))
    ])
    row5 = html.Tr([
        html.Td("Specificity (true negatives / all actual negatives)"),
        html.Td("{:.2f}%".format((specificity[max_accuracy_idx]*100)))
    ])

    table_body = [html.Tbody([row1, row2, row3, row4, row5])]
    table = table_header + table_body

    return fig, fig_adv, table


def confusion_plot_multiple (stab_data, ind_data_iterable, log10_ind=False, stab_thresh=1e7, sampling=100, reverse=False, convolution=None, convolution_kernel=None, convolution_options=[]):
    if ind_data_iterable is None:
        return go.Figure()
    else:
        times = []
        thresholds = []
        accuracies = []
        valid_conditions = []
        for block in ind_data_iterable:
            t, ind_data = block
            if convolution == "avg":
                ind_data = avg_convolve(
                    ind_data,
                    convolution_kernel,
                    (False if "reverse" in convolution_options else True)
                )
            elif convolution == "std":
                ind_data = std_convolve(
                    ind_data,
                    convolution_kernel,
                    (False if "reverse" in convolution_options else True)
                )
            ind_data = ind_data.flatten()
            times.append(t)
            valid_conditions.append(
                np.count_nonzero(np.logical_not(np.isnan(ind_data)))
            )
            samples,\
            tp, tn, fp, fn,\
            accuracy, precision, sensitivity, specificity,\
            max_accuracy_idx, max_accuracy, best_threshold = confusion_data(
                stab_data, ind_data, log10_ind,
                stab_thresh, sampling, reverse
            )
            thresholds.append(best_threshold)
            accuracies.append(max_accuracy)

        thresholds = [x for _, x in sorted(zip(times, thresholds))]
        accuracies = [x for _, x in sorted(zip(times, accuracies))]
        valid_conditions = [x for _, x in sorted(zip(times, valid_conditions))]
        times = [x for x in sorted(times)]

        final_fig = go.Figure()
        final_fig.add_trace(
            go.Scatter(
                x=times,
                y=thresholds,
                name="Best Thresholds (accuracy-wise)",
                mode="lines"
            ),
        )
        final_fig.add_trace(
            go.Scatter(
                x=times,
                y=accuracies,
                name="Accuracy",
                mode="lines",
                yaxis="y2"
            ),
        )
        final_fig.add_trace(
            go.Scatter(
                x=times,
                y=valid_conditions,
                name="Valid initial conditions",
                mode="lines",
                yaxis="y3"
            ),
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
            title="Theshold evolution")
        final_fig.update_xaxes(
            title_text="N turns used for computing indicator",
            type="log"
        )
        final_fig.update_layout(
            xaxis=dict(
                domain=[0.3, 0.85]
            ),
            yaxis=dict(
                title="Threshold value"
            ),
            yaxis2=dict(
                title="Accuracy value",
                side="right",
                overlaying="y",
            ),
            yaxis3=dict(
                title="Valid initial conditions (particles not lost)",
                side="left",
                position=0.15,
                overlaying="y",
            )
        )
        return final_fig


def evolution_plot(stab_data, iterable, min_turns, max_turns, sample_skip, log10=False, filter_data=False):
    stab_data = np.log10(stab_data).flatten()
    if iterable is None:
        return go.Figure()
    
    t_list = []
    values = []
    
    for t, v in iterable:
        t_list.append(t)
        values.append(v.flatten())

    values = [x for _, x in sorted(zip(t_list, values))]
    t_list = [x for x in sorted(t_list)]

    t_list = np.array(t_list)
    values = np.array(values)

    if log10:
        values = np.log10(values)

    cmap = matplotlib.cm.get_cmap('viridis')

    fig = go.Figure()
    min_lim = -np.inf if min_turns == 0.0 else np.log10(min_turns)
    max_lim = np.log10(max_turns)
    for i in range(0, values.shape[1], int(sample_skip)):
        if not filter_data or not (stab_data[i] < min_lim or stab_data[i] > max_lim):
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
    return fig


#@njit(parallel=True)
def avg_convolve_core(padded_array, result, ks, take_top=True):
    ks = ks // 2
    if take_top:
        replacement = np.nanmax(padded_array)
    else:
        replacement = np.nanmin(padded_array)
    for i in range(len(result)):
        for j in range(len(result[i])):
            if np.isnan(padded_array[i + ks, j + ks]):
                result[i, j] = np.nan
            else:
                sample = padded_array[i: i + 1 +
                                      ks * 2, j: j + 1 + ks * 2].copy()
                for a in range(ks):
                    for b in range(ks):
                        if np.isnan(sample[a, b]):
                            sample[a, b] = replacement
                result[i, j] = np.nanmean(sample)
    return result


def avg_convolve(array, ks, take_top=True):
    len_pad = ks // 2
    return avg_convolve_core(
        np.pad(array, ((len_pad, len_pad), (len_pad, len_pad)), 'reflect'),
        np.empty_like(array),
        ks,
        take_top
    )


#@njit(parallel=True)
def std_convolve_core(padded_array, result, ks, take_top=True):
    ks = ks // 2
    if take_top:
        replacement = np.nanmax(padded_array)
    else:
        replacement = np.nanmin(padded_array)
    for i in range(len(result)):
        for j in range(len(result[i])):
            if np.isnan(padded_array[i + ks, j + ks]):
                result[i, j] = np.nan
            else:
                sample = padded_array[i: i + 1 +
                                      ks * 2, j: j + 1 + ks * 2].copy()
                for a in range(ks):
                    for b in range(ks):
                        if np.isnan(sample[a, b]):
                            sample[a, b] = replacement
                result[i, j] = np.nanstd(sample)
    return result


def std_convolve(array, ks, take_top=True):
    len_pad = ks // 2
    return std_convolve_core(
        np.pad(array, ((len_pad, len_pad), (len_pad, len_pad)), 'reflect'),
        np.empty_like(array),
        ks,
        take_top
    )


