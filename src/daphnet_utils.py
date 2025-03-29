import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def do_plot(data: np.ndarray, target: np.ndarray, time=None):
    """
    Plota os sinais de aceleração e destaca as regiões com FoG (label=2).
    
    Parameters:
    - data: array (n_samples, 9) com sinais multicanais
    - target: array (n_samples,) com os rótulos (0, 1, 2)
    - time: array opcional com timestamps (mesmo tamanho de target)
    """
    n_channels = data.shape[1]
    index = time if time is not None else np.arange(len(target))

    # Cria DataFrame para facilitar com seaborn
    df_signals = pd.DataFrame(data, columns=[f"acc_{i+1}" for i in range(n_channels)])
    df_signals["time"] = index
    df_signals["FoG"] = target

    # Melt para usar com seaborn
    df_melted = df_signals.melt(id_vars=["time", "FoG"], var_name="Canal", value_name="Valor")

    plt.figure(figsize=(14, 6))
    sns.lineplot(data=df_melted, x="time", y="Valor", hue="Canal", linewidth=1)

    # Sombreamento onde há congelamento (label=2)
    fog_regions = df_signals["FoG"] == 2
    if fog_regions.any():
        plt.fill_between(df_signals["time"], df_melted["Valor"].min(), df_melted["Valor"].max(),
                         where=fog_regions, color="red", alpha=0.1, label="FoG")

    plt.title("Sinais de Aceleração com Detecção de Freezing of Gait (FoG)")
    plt.xlabel("Tempo")
    plt.ylabel("Aceleração (mg)")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()


def x_numerical_integration(signal: np.ndarray, fs: float = 64.0) -> float:
    dt = 1.0 / fs
    return np.trapz(signal, dx=dt)


def x_count_transitions(labels: np.ndarray) -> int:
    return np.sum(labels[1:] != labels[:-1])


def x_fi(window: np.ndarray) -> np.ndarray:
    means = np.mean(window, axis=0)
    stds = np.std(window, axis=0)
    mins = np.min(window, axis=0)
    maxs = np.max(window, axis=0)
    return np.concatenate([means, stds, mins, maxs])


def do_test(model, X_test: np.ndarray, y_test: np.ndarray):
    y_pred = model.predict(X_test)
    acc = np.mean(y_pred == y_test)
    print(f"Acurácia: {acc * 100:.2f}%")
    return acc


def load_daphnet_file(path):
    df = pd.read_csv(path, sep=r"\s+", engine="python", header=None)
    df.columns = ["time"] + [f"acc_{i}" for i in range(1, 10)] + ["label"]
    return df


def extract_labeled_windows(df, window_size=128, step_size=64, freeze_label=2, threshold=0.5):
    signals = df[[f"acc_{i}" for i in range(1, 10)]].values
    labels = df["label"].values

    X, y = [], []
    for start in range(0, len(df) - window_size + 1, step_size):
        end = start + window_size
        window = signals[start:end]
        label_window = labels[start:end]

        features = x_fi(window)
        freezing_ratio = np.mean(label_window == freeze_label)
        label = int(freezing_ratio >= threshold)

        X.append(features)
        y.append(label)

    return np.array(X), np.array(y)


def load_full_dataset(folder_path: Path, window_size=128, step_size=64):
    X_all, y_all = [], []
    for file in sorted(folder_path.glob("*.txt")):
        df = load_daphnet_file(file)
        X, y = extract_labeled_windows(df, window_size, step_size)
        X_all.append(X)
        y_all.append(y)
    return np.concatenate(X_all), np.concatenate(y_all)
