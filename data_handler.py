import plotly.graph_objects as go
import numpy as np
import h5py
import os


def faddeev_leverrier(m, grade=1):
    assert grade > 0
    step = 1
    B = m.copy()
    p = np.trace(B)
    while step != grade:
        step += 1
        B = np.matmul(m, B - np.identity(B.shape[-1]) * p)
        p = np.trace(B) * (1 / step)
    return p * ((-1) ** (grade + 1))


v_faddeev_leverrier = np.vectorize(
    faddeev_leverrier, signature="(n,m),(1)->(1)")


class data_handler(object):
    def __init__(self, filename_standard, param_dict, f_data, f_plot, f_data_all_turns=None):
        self.filename_standard = filename_standard
        self.param_dict = param_dict
        self.f_data = f_data
        self.f_plot = f_plot
        self.f_data_all_turns = f_data_all_turns

    def get_param_list(self):
        return list(self.param_dict.keys())

    def get_param_options(self, param):
        if param not in self.param_dict:
            raise ValueError("param not in dictionary")
        else:
            return self.param_dict[param]

    def get_data(self, parameters):
        return self.f_data(parameters)

    def get_plot(self, parameters, log_scale=False):
        return self.f_plot(parameters, log_scale)

    def get_data_all_turns(self, parameters):
        return self.f_data_all_turns(parameters)


### Data location on EOS
data_path = "/mnt/volume"

#### DATASET STANDARD ####

# FULL SET
# mu_list = [0.0, 0.2, -0.2, 1.0, -1.0]
# epsilon_list = [0.0, 1.0, 2.0, 4.0, 16.0, 32.0, 64.0]

# REDUCED SET
mu_list = [0.0, 0.2, 1.0]
epsilon_list = [0.0, 4.0, 16.0, 32.0, 64.0]

turn_samples = [10, 100, 1000, 10000, 100000]

def eml(epsilon, mu):
    epsilon = float(epsilon)
    mu = float(mu)
    return "eps_{:.2}_mu_{:.2}_".format(epsilon, mu).replace(".", "_")


def init_filename_standard(epsilon, mu):
    return (
        "henon_4d_init_"
        + eml(epsilon, mu)
        + "id_basic.hdf5"
    )


def get_raw_coordinates(parameters):
    filename = init_filename_standard(parameters["epsilon"], parameters["mu"])
    with h5py.File(os.path.join(data_path, filename), mode="r") as f:
        x  = f["coords/x"][...]
        px = f["coords/px"][...]
        y  = f["coords/y"][...]
        py = f["coords/py"][...]
    return x, px, y, py
    

#### RADIUS ####

radius_param_dict = {
    "mu": mu_list,
    "epsilon": epsilon_list
}

def radius_get_data(parameters):
    filename = init_filename_standard(parameters["epsilon"], parameters["mu"])
    with h5py.File(os.path.join(data_path, filename), mode="r") as f:
        data = np.sqrt(
            + np.power(f["coords/x"][...], 2)
            + np.power(f["coords/px"][...], 2)
            + np.power(f["coords/y"][...], 2)
            + np.power(f["coords/py"][...], 2)
        )
    return data


def radius_get_plot(parameters, log_scale=False):
    data = radius_get_data(parameters)
    if log_scale:
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
        title="Radial distance from center " +
        (" [linear scale]" if not log_scale else " [log10 scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


radius_data_handler = data_handler(
    init_filename_standard,
    radius_param_dict,
    radius_get_data,
    radius_get_plot
)

#### STABILITY ####

stability_param_dict = {
    "kick": ["no_kick", "1e-4", "1e-8", "1e-12"],
    "mu": mu_list,
    "epsilon": epsilon_list
}

def stability_filename_standard(kick, mu, epsilon):
    return (
        "henon_4d_long_track_"
        + ("" if kick=="no_kick" else "wkick_")
        + eml(epsilon, mu)
        + "id_basic"
        + ("" if kick=="no_kick" else "_subid_" + kick)
        + ".hdf5"
    )

def stability_get_data(parameters):
    filename = stability_filename_standard(parameters["kick"], parameters["mu"], parameters["epsilon"])
    with h5py.File(os.path.join(data_path, filename), mode="r") as f:
        data = f["stability_time"][...]
    return data


def stability_get_plot(parameters, log_scale=False):
    data = stability_get_data(parameters)
    if log_scale:
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
        title="Stability time " +
        (" [linear scale]" if not log_scale else " [log10 scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


stability_data_handler = data_handler(
    stability_filename_standard,
    stability_param_dict,
    stability_get_data,
    stability_get_plot
)


#### LI ####

LI_param_dict = {
    "turns": turn_samples,
    "displacement": [1e-12],
    "mu": mu_list,
    "epsilon": epsilon_list
}


def LI_filename_standard(displacement, mu, epsilon):
    return (
        "henon_4d_displacement_"
        + eml(epsilon, mu)
        + "id_basic"
        + "_subid_{}".format(displacement)
        + ".hdf5"
    )

def LI_get_data(parameters):
    filename = LI_filename_standard(parameters["displacement"], parameters["mu"], parameters["epsilon"])
    idx = str(parameters["turns"])
    with h5py.File(os.path.join(data_path, filename), mode="r") as f:
        sample = f[idx]
        data = np.log10(np.sqrt(
            np.power(sample["x"][0] - sample["x"][1], 2) +
            np.power(sample["px"][0] - sample["px"][1], 2) +
            np.power(sample["y"][0] - sample["y"][1], 2) +
            np.power(sample["py"][0] - sample["py"][1], 2)
        ) / f.attrs["displacement"]) / parameters["turns"]
    return data


def LI_get_data_all_turns(parameters):
    filename = LI_filename_standard(
        parameters["displacement"], parameters["mu"], parameters["epsilon"])
    f = h5py.File(os.path.join(data_path, filename), mode="r")
    all_turns = list(f)
    for t in all_turns:
        sample = f[t]
        data = np.log10(np.sqrt(
            np.power(sample["x"][0] - sample["x"][1], 2) +
            np.power(sample["px"][0] - sample["px"][1], 2) +
            np.power(sample["y"][0] - sample["y"][1], 2) +
            np.power(sample["py"][0] - sample["py"][1], 2)
        ) / f.attrs["displacement"]) / parameters["turns"]
        yield int(t), data


def LI_get_plot(parameters, log_scale=False):
    data = LI_get_data(parameters)
    if log_scale:
        data = np.log10(data)
    fig = go.Figure(
        data=go.Heatmap(
            z=data,
            x=np.linspace(0, 1, 500),
            y=np.linspace(0, 1, 500),
            hoverongaps=False,
            colorscale="Viridis",
            reversescale=True
        )
    )
    fig.update_layout(
        title="LI (Fast Lyapunov Indicator) " +
        (" [linear scale]" if not log_scale else " [log10 scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


LI_data_handler = data_handler(
    LI_filename_standard,
    LI_param_dict,
    LI_get_data,
    LI_get_plot,
    LI_get_data_all_turns
)


#### LEI ####

LEI_param_dict = {
    "grade": [1, 2, 3, 4, 5, 6],
    "turns": turn_samples,
    "displacement": [1e-12],
    "mu": mu_list,
    "epsilon": epsilon_list
}


def LEI_filename_standard(displacement, mu, epsilon):
    return (
        "henon_4d_LEI_"
        + eml(epsilon, mu)
        + "id_basic"
        + "_subid_{}".format(displacement)
        + ".hdf5"
    )


def LEI_get_data(parameters):
    filename = LEI_filename_standard(parameters["displacement"], parameters["mu"], parameters["epsilon"])
    f = h5py.File(os.path.join(data_path, filename), mode="r")
    return f[str(parameters["turns"])][str(parameters["grade"])]


def LEI_get_data_all_turns(parameters):
    filename = LEI_filename_standard(
        parameters["displacement"], parameters["mu"], parameters["epsilon"])
    f = h5py.File(os.path.join(data_path, filename), mode="r")
    all_turns = list(f)
    for t in all_turns:
        data = f[t][str(parameters["grade"])][...]
        yield int(t), data


def LEI_get_plot(parameters, log_scale=False):
    data = LEI_get_data(parameters)
    if log_scale:
        data = np.log10(data)
    fig = go.Figure(
        data=go.Heatmap(
            z=data,
            x=np.linspace(0, 1, 500),
            y=np.linspace(0, 1, 500),
            hoverongaps=False,
            colorscale="Viridis",
            reversescale=True
        )
    )
    fig.update_layout(
        title="LEI (Invariant Lyapunov Indicatr) " +
        (" [linear scale]" if not log_scale else " [log10 scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


LEI_data_handler = data_handler(
    LEI_filename_standard,
    LEI_param_dict,
    LEI_get_data,
    LEI_get_plot,
    LEI_get_data_all_turns
)

#### RE ####

RE_param_dict = {
    "turns": turn_samples,
    "kicks": ["no_kick", "uniform (1e-12)", "gaussian (1e-12, 1e-13)", "uniform forward only (1e-12)", "gaussian forward only (1e-12, 1e-13)"],
    "mu": mu_list,
    "epsilon": epsilon_list
}


def RE_filename_standard(kicks, mu, epsilon):
    if kicks == "no_kick":
        kick_label = "_subid_no_kick"
    elif kicks == "uniform (1e-12)":
        kick_label = "_subid_unif_kick"
    elif kicks == "gaussian (1e-12, 1e-13)":
        kick_label = "_subid_gauss_kick"
    elif kicks == "uniform forward only (1e-12)":
        kick_label = "_subid_unif_kick_forward"
    elif kicks == "gaussian forward only (1e-12, 1e-13)":
        kick_label = "_subid_gauss_kick_forward"
    else:
        print("Something is weird!!!")
        kick_label = ""
    
    return (
        "henon_4d_inverse_tracking_"
        + eml(epsilon, mu)
        + "id_basic"
        + kick_label
        + ".hdf5"
    )


def RE_get_data(parameters):
    filename0 = init_filename_standard(parameters["epsilon"], parameters["mu"])
    filename1 = RE_filename_standard(parameters["kicks"], parameters["mu"], parameters["epsilon"])
    idx = str(parameters["turns"])
    f0 = h5py.File(os.path.join(data_path, filename0), mode="r")
    f1 = h5py.File(os.path.join(data_path, filename1), mode="r")
    data = np.sqrt(
        + np.power(f0["coords/x"][...] - f1[idx]["x"][...], 2)
        + np.power(f0["coords/px"][...] - f1[idx]["px"][...], 2)
        + np.power(f0["coords/y"][...] - f1[idx]["y"][...], 2)
        + np.power(f0["coords/py"][...] - f1[idx]["py"][...], 2)
    )
    f0.close()
    f1.close()
    return data


def RE_get_data_all_turns(parameters):
    filename0 = init_filename_standard(parameters["epsilon"], parameters["mu"])
    filename1 = RE_filename_standard(parameters["kicks"], parameters["mu"], parameters["epsilon"])
    f0 = h5py.File(os.path.join(data_path, filename0), mode="r")
    f1 = h5py.File(os.path.join(data_path, filename1), mode="r")

    all_turns = list(f1)
    for t in all_turns:
        data = np.sqrt(
            + np.power(f0["coords/x"][...] - f1[t]["x"][...], 2)
            + np.power(f0["coords/px"][...] - f1[t]["px"][...], 2)
            + np.power(f0["coords/y"][...] - f1[t]["y"][...], 2)
            + np.power(f0["coords/py"][...] - f1[t]["py"][...], 2)
        )
        yield int(t), data



def RE_get_plot(parameters, log_scale=False):
    data = RE_get_data(parameters)
    if log_scale:
        data = np.log10(data)
    fig = go.Figure(
        data=go.Heatmap(
            z=data,
            x=np.linspace(0, 1, 500),
            y=np.linspace(0, 1, 500),
            hoverongaps=False,
            colorscale="Viridis",
            reversescale=True
        )
    )
    fig.update_layout(
        title="RE (Reversibility error) " +
        (" [linear scale]" if not log_scale else " [log10 scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


RE_data_handler = data_handler(
    RE_filename_standard,
    RE_param_dict,
    RE_get_data,
    RE_get_plot,
    RE_get_data_all_turns
)


#### REI ####

REI_param_dict = {
    "grade": [1, 2, 3, 4, 5, 6],
    "turns": turn_samples,
    "kicks": ["no_kick", "uniform (1e-12)", "gaussian (1e-12, 1e-13)", "uniform forward only (1e-12)", "gaussian forward only (1e-12, 1e-13)"],
    "mu": mu_list,
    "epsilon": epsilon_list
}


def REI_filename_standard(kicks, mu, epsilon):
    if kicks == "no_kick":
        kick_label = "_subid_no_kick"
    elif kicks == "uniform (1e-12)":
        kick_label = "_subid_unif_kick"
    elif kicks == "gaussian (1e-12, 1e-13)":
        kick_label = "_subid_gauss_kick"
    elif kicks == "uniform forward only (1e-12)":
        kick_label = "_subid_unif_kick_forward"
    elif kicks == "gaussian forward only (1e-12, 1e-13)":
        kick_label = "_subid_gauss_kick_forward"
    else:
        print("Something is weird!!!")
        kick_label = ""

    return (
        "henon_4d_REI_"
        + eml(epsilon, mu)
        + "id_basic"
        + kick_label
        + ".hdf5"
    )


def make_REI_matrix(x0, px0, y0, py0, x, px, y, py):
    d_x = x - x0
    d_px = px - px0
    d_y = y - y0
    d_py = py - py0
    return np.transpose(np.array([
        [d_x * d_x, d_x * d_px, d_x * d_y, d_x * d_py],
        [d_px * d_x, d_px * d_px, d_px * d_y, d_px * d_py],
        [d_y * d_x, d_y * d_px, d_y * d_y, d_y * d_py],
        [d_py * d_x, d_py * d_px, d_py * d_y, d_py * d_py],
    ]), axes=(2, 3, 0, 1))


def REI_get_data(parameters):
    filename1 = REI_filename_standard(
        parameters["kicks"], parameters["mu"], parameters["epsilon"])
    f = h5py.File(os.path.join(data_path, filename1), mode="r")    
    return f[str(parameters["turns"])][str(parameters["grade"])][...]


def REI_get_data_all_turns(parameters):
    filename1 = REI_filename_standard(
        parameters["kicks"], parameters["mu"], parameters["epsilon"])
    f = h5py.File(os.path.join(data_path, filename1), mode="r")
    all_turns = list(f)
    for t in all_turns:
        data = f[t][str(parameters["grade"])][...]
        yield int(t), data


def REI_get_plot(parameters, log_scale=False):
    data = REI_get_data(parameters)
    if log_scale:
        data = np.log10(data)
    fig = go.Figure(
        data=go.Heatmap(
            z=data,
            x=np.linspace(0, 1, 500),
            y=np.linspace(0, 1, 500),
            hoverongaps=False,
            colorscale="Viridis",
            reversescale=True
        )
    )
    fig.update_layout(
        title="REI (Invariant reversibility error) " +
        (" [linear scale]" if not log_scale else " [log10 scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


REI_data_handler = data_handler(
    REI_filename_standard,
    REI_param_dict,
    REI_get_data,
    REI_get_plot,
    REI_get_data_all_turns
)

#### SALI ####

SALI_param_dict = {
    "turns": turn_samples,
    "mu": mu_list,
    "epsilon": epsilon_list
}


def SALI_filename_standard(mu, epsilon):
    return(
        "henon_4d_sali_"
        + eml(epsilon, mu)
        + "id_basic.hdf5"
    )


def SALI_get_data(parameters):
    filename = SALI_filename_standard(parameters["mu"], parameters["epsilon"])
    idx = str(parameters["turns"])
    with h5py.File(os.path.join(data_path, filename), mode="r") as f:
        data = f[idx][...]
    return data


def SALI_get_data_all_turns(parameters):
    filename = SALI_filename_standard(parameters["mu"], parameters["epsilon"])
    f = h5py.File(os.path.join(data_path, filename), mode="r")
    all_turns = list(f)
    for t in all_turns:
        data = f[t][...]
        yield int(t), data


def SALI_get_plot(parameters, log_scale=False):
    data = SALI_get_data(parameters)
    if log_scale:
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
        title="SALI " +
        (" [linear scale]" if not log_scale else " [log10 scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


SALI_data_handler = data_handler(
    SALI_filename_standard,
    SALI_param_dict,
    SALI_get_data,
    SALI_get_plot,
    SALI_get_data_all_turns
)


#### GALI ####

GALI_param_dict = {
    "n_dimensions" : ["gali2", "gali3", "gali4"],
    "turns": turn_samples,
    "mu": mu_list,
    "epsilon": epsilon_list
}


def GALI_filename_standard(mu, epsilon):
    return(
        "henon_4d_gali_"
        + eml(epsilon, mu)
        + "id_basic.hdf5"
    )


def GALI_get_data(parameters):
    filename = GALI_filename_standard(parameters["mu"], parameters["epsilon"])
    idx = str(parameters["turns"])
    with h5py.File(os.path.join(data_path, filename), mode="r") as f:
        data = f[parameters["n_dimensions"]][idx][...]
    return data


def GALI_get_data_all_turns(parameters):
    filename = GALI_filename_standard(parameters["mu"], parameters["epsilon"])
    f = h5py.File(os.path.join(data_path, filename), mode="r")
    all_turns = list(f)
    for t in all_turns:
        data = f[parameters["n_dimensions"]][t][...]
        yield int(t), data


def GALI_get_plot(parameters, log_scale=False):
    data = GALI_get_data(parameters)
    if log_scale:
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
        title="GALI " +
        (" [linear scale]" if not log_scale else " [log10 scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


GALI_data_handler = data_handler(
    GALI_filename_standard,
    GALI_param_dict,
    GALI_get_data,
    GALI_get_plot,
    GALI_get_data_all_turns
)

#### MEGNO ####

MEGNO_param_dict = {
    "turns": turn_samples,
    "mu": mu_list,
    "epsilon": epsilon_list
}


def MEGNO_filename_standard(mu, epsilon):
    return(
        "henon_4d_megno_"
        + eml(epsilon, mu)
        + "id_basic.hdf5"
    )


def MEGNO_get_data(parameters):
    filename = MEGNO_filename_standard(parameters["mu"], parameters["epsilon"])
    idx = str(parameters["turns"])
    with h5py.File(os.path.join(data_path, filename), mode="r") as f:
        data = f[idx][...]
    return data


def MEGNO_get_data_all_turns(parameters):
    filename = MEGNO_filename_standard(parameters["mu"], parameters["epsilon"])
    f = h5py.File(os.path.join(data_path, filename), mode="r")
    all_turns = list(f)
    for t in all_turns:
        data = f[t][...]
    return data


def MEGNO_get_plot(parameters, log_scale=False):
    data = MEGNO_get_data(parameters)
    if log_scale:
        data = np.log10(data)
    fig = go.Figure(
        data=go.Heatmap(
            z=data,
            x=np.linspace(0, 1, 500),
            y=np.linspace(0, 1, 500),
            hoverongaps=False,
            colorscale="Viridis",
            reversescale=True
        )
    )
    fig.update_layout(
        title="MEGNO " +
        (" [linear scale]" if not log_scale else " [log10 scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


MEGNO_data_handler = data_handler(
    MEGNO_filename_standard,
    MEGNO_param_dict,
    MEGNO_get_data,
    MEGNO_get_plot,
    MEGNO_get_data_all_turns
)


#### FREQUENCY MAP ####


FQ_param_dict = {
    "turns": [2**11, 2**12, 2**13, 2**14],
    "mu": mu_list,
    "epsilon": epsilon_list
}


def FQ_filename_standard(mu, epsilon):
    return(
        "henon_4d_fft_"
        + eml(epsilon, mu)
        + "id_basic.hdf5"
    )


def FQ_get_data(parameters):
    filename = FQ_filename_standard(parameters["mu"], parameters["epsilon"])
    idx = str(int(np.log2(parameters["turns"])) - 1)
    with h5py.File(os.path.join(data_path, filename), mode="r") as f:
        data = np.sqrt(
            +np.power(f[idx]["tune_x"][0] - f[idx]["tune_x"][1], 2)
            + np.power(f[idx]["tune_y"][0] - f[idx]["tune_y"][1], 2)
        )
    return data


def FQ_get_data_all_turns(parameters):
    filename = FQ_filename_standard(parameters["mu"], parameters["epsilon"])
    f = h5py.File(os.path.join(data_path, filename), mode="r")
    all_turns = list(f)
    for t in all_turns:
        data = np.sqrt(
            +np.power(f[t]["tune_x"][0] - f[t]["tune_x"][1], 2)
            + np.power(f[t]["tune_y"][0] - f[t]["tune_y"][1], 2)
        )
        yield 2**int(t), data


def FQ_get_plot(parameters, log_scale=False):
    data = FQ_get_data(parameters)
    if log_scale:
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
        title="Frequency Map " +
        (" [linear scale]" if not log_scale else " [log10 scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


FQ_data_handler = data_handler(
    FQ_filename_standard,
    FQ_param_dict,
    FQ_get_data,
    FQ_get_plot,
    FQ_get_data_all_turns
)


#### TUNE ####

TUNE_param_dict = {
    "turns": [2**10, 2**11, 2**12, 2**13, 2**14],
    "mu": mu_list,
    "epsilon": epsilon_list
}


def TUNE_X_get_data(parameters):
    filename = FQ_filename_standard(parameters["mu"], parameters["epsilon"])
    idx = str(int(np.log2(parameters["turns"])))
    with h5py.File(os.path.join(data_path, filename), mode="r") as f:
        data = f[idx]["tune_x"][0]
    return data


def TUNE_Y_get_data(parameters):
    filename = FQ_filename_standard(parameters["mu"], parameters["epsilon"])
    idx = str(int(np.log2(parameters["turns"])))
    with h5py.File(os.path.join(data_path, filename), mode="r") as f:
        data = f[idx]["tune_y"][0]
    return data


def TUNE_X_get_plot(parameters, log_scale=False):
    data = TUNE_X_get_data(parameters)
    if log_scale:
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
        title="Tune X " +
        (" [linear scale]" if not log_scale else " [log10 scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


def TUNE_Y_get_plot(parameters, log_scale=False):
    data = TUNE_Y_get_data(parameters)
    if log_scale:
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
        title="Tune X " +
        (" [linear scale]" if not log_scale else " [log10 scale]"),
        xaxis_title="X_0",
        yaxis_title="Y_0"
    )
    return fig


TUNE_X_data_handler = data_handler(
    FQ_filename_standard,
    TUNE_param_dict,
    TUNE_X_get_data,
    TUNE_X_get_plot
)

TUNE_Y_data_handler = data_handler(
    FQ_filename_standard,
    TUNE_param_dict,
    TUNE_Y_get_data,
    TUNE_Y_get_plot
)
