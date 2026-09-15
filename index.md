# Learn Software Defined Radio by Building, Observing, and Experimenting

**SDR with GNU Radio** is a practical introduction to Software Defined Radio, digital signal processing, and digital communication.

The book develops each topic by connecting three things: the underlying signal-processing idea, a GNU Radio experiment, and the behaviour we can actually observe. Mathematics is introduced where it helps explain what the experiment is showing.

:::: {.columns}

::: {.column width="33%"}

### BUILD

![](figures/ch18/ch18-exp1-rectangular-symbol-bandwidth-flowgraph.png)

Build signals, channels, and communication systems in GNU Radio.

:::

::: {.column width="33%"}

### EXPLORE

![](figures/ch18/ch18-exp6-rrc-rolloff-spectrum.png)

Change parameters and observe how the waveform and spectrum respond.

:::

::: {.column width="34%"}

### ANALYZE

![](figures/ch19/ch19-exp3-high-snr-constellation.png)

Use spectra, eye diagrams, and constellations to understand what the receiver is seeing.

:::

::::

## About the Book

The book starts with signals, sampling, complex numbers, I/Q representation, frequency-domain analysis, filtering, and modulation.

From there, it moves into digital communication: bits and symbols, PAM, QPSK and QAM, pulse shaping, matched filtering, wireless-channel impairments, equalization, carrier synchronization, symbol timing, frame detection, and a complete single-carrier receiver.

The current OFDM section begins by asking why multicarrier communication is useful and how orthogonal subcarriers can overlap in frequency without necessarily interfering.

The aim is not to treat GNU Radio as a collection of blocks to memorize. Each flowgraph is used to answer an engineering question and to connect the visible result back to the underlying DSP.

## How the Chapters Work

Most chapters begin with a question or problem.

We first build a small experiment, predict what should happen, and then examine the result using the most useful view for that problem, such as a time-domain plot, spectrum, eye diagram, constellation, or numerical measurement.

The theory is then developed around what the experiment revealed.

As the book progresses, the individual ideas are combined into larger communication systems rather than remaining isolated demonstrations.

## What the Experiments Include

The examples use GNU Radio flowgraphs together with a small number of supporting Python scripts where a separate calculation or visualization is useful.

The experiments cover both successful operation and deliberate failure cases. Seeing what happens when carrier recovery, timing recovery, equalization, or frame synchronization is missing is an important part of understanding what each receiver stage actually does.

## About the Author

**Dhrubjun Nath Saikia** is the author of *SDR with GNU Radio*.

The book grew from a hands-on approach to learning signal processing and communication systems: build the system, observe its behaviour, and then explain why it behaves that way.

## Source Code and Experiments

The GNU Radio flowgraphs, supporting scripts, figures, and Markdown source used throughout the book are available in the project repository.

[View the project on GitHub](https://github.com/dhrubjun/sdr-with-gnu-radio)