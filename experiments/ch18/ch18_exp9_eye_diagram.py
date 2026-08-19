import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# Experiment parameters
# ---------------------------------------------------------

samp_rate = 32000
sps = 32
eye_len = 2 * sps
skip = 20 * sps
n_traces = 120


# ---------------------------------------------------------
# Eye-diagram plotting function
# ---------------------------------------------------------

def plot_eye(input_file, output_file, title):
    samples = np.fromfile(input_file, dtype=np.float32)

    # Remove the initial TX/RX filter transient
    x = samples[skip:]

    windows = []

    for k in range(n_traces):
        start = k * sps
        end = start + eye_len

        if end <= len(x):
            windows.append(x[start:end])

    windows = np.asarray(windows)

    # Two symbol periods = 2 ms for Rs = 1 ksymbol/s
    t_ms = np.arange(eye_len) / samp_rate * 1000

    plt.figure(figsize=(10, 6))

    for window in windows:
        plt.plot(
            t_ms,
            window,
            linewidth=0.8,
            alpha=0.22
        )

    # Correct symbol sampling instant
    plt.axvline(
        1.0,
        linestyle="--",
        linewidth=1.2,
        label="Sampling instant"
    )

    plt.title(title)
    plt.xlabel("Time (ms)")
    plt.ylabel("Amplitude")

    plt.xlim(0, 2)
    plt.ylim(-2, 2)

    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        output_file,
        dpi=220,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Created: {output_file}")


# ---------------------------------------------------------
# Generate both Chapter 18 eye diagrams
# ---------------------------------------------------------

plot_eye(
    "ch18-eye-clean.dat",
    "../../figures/ch18/ch18-exp9-eye-no-noise.png",
    "BPSK Eye Diagram After RRC Matched Filtering"
)

plot_eye(
    "ch18-eye-05.dat",
    "../../figures/ch18/ch18-exp9-eye-noise-05.png",
    "BPSK Eye Diagram with Noise After RRC Matched Filtering"
)