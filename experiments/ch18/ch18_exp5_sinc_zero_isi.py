import numpy as np
import matplotlib.pyplot as plt

# Symbol sequence
symbols = np.array([1, -1, 1, 1, -1])

# Normalized symbol period
Ts = 1.0

# Symbol sampling instants
symbol_times = np.arange(len(symbols)) * Ts

# Time axis
t = np.linspace(-2, 6, 4000)

# Store individual pulse contributions
pulses = []

# Create one shifted sinc pulse for each symbol
for ak, tk in zip(symbols, symbol_times):
    pulse = ak * np.sinc((t - tk) / Ts)
    pulses.append(pulse)

# Sum all pulse contributions
total_waveform = np.sum(pulses, axis=0)

# Plot
plt.figure(figsize=(12, 7))

# Individual shifted sinc pulses
for i, pulse in enumerate(pulses):
    plt.plot(
        t,
        pulse,
        linewidth=1.2,
        alpha=0.65,
        label=f"Pulse from symbol {i + 1}"
    )

# Total transmitted waveform
plt.plot(
    t,
    total_waveform,
    linewidth=2.5,
    label="Sum of all pulses"
)

# Ideal symbol values at sampling instants
plt.scatter(
    symbol_times,
    symbols,
    s=70,
    zorder=5,
    label="Symbol sampling points"
)

# Vertical lines marking symbol sampling instants
for tk in symbol_times:
    plt.axvline(tk, linewidth=0.8, alpha=0.25, linestyle="--")

plt.axhline(0, linewidth=0.8)

plt.title("Overlapping Sinc Pulses and the Nyquist Zero-ISI Idea")
plt.xlabel("Time / Symbol Period")
plt.ylabel("Amplitude")

plt.xlim(-1.5, 5.5)
plt.ylim(-1.8, 2.0)

plt.grid(True, alpha=0.3)
plt.legend(loc="upper right")
plt.tight_layout()
plt.show()