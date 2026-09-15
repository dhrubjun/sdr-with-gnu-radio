# SDR with GNU Radio

**SDR with GNU Radio** is a practical book about Software Defined Radio, digital signal processing, and communication systems.

The book develops the topics through intuition, GNU Radio experiments, visual observation, and supporting mathematics. The aim is not only to learn how to use GNU Radio blocks, but to understand what the signals are doing and why a communication system behaves the way it does.

## Read the Book

The book is available online:

**https://dhrubjun.github.io/sdr-with-gnu-radio/**

## What the Book Covers

The chapters progress from the fundamentals to complete digital communication systems, including:

- signals, sampling, and aliasing;
- complex numbers and I/Q signals;
- FFTs, filtering, convolution, and correlation;
- analog and digital modulation;
- PAM, BPSK, QPSK, and QAM;
- pulse shaping and matched filtering;
- wireless-channel impairments and multipath;
- channel equalization;
- carrier and symbol timing synchronization;
- frame synchronization and packet detection;
- a complete single-carrier digital receiver;
- multicarrier communication and OFDM.

The OFDM section begins by developing the motivation for orthogonal subcarriers before moving toward an IFFT-based implementation.

## Repository Structure

```text
book/         Book chapters in Markdown
experiments/  GNU Radio experiments and supporting files
figures/      Figures used in the book
scripts/      Supporting Python scripts
data/         Experiment data where required
docs/         Supporting documentation
tools/        Project utilities
```

The Quarto configuration is stored in `_quarto.yml`, and `index.md` is the homepage of the published book.

## Running the Experiments

Most experiments are built with **GNU Radio**. Some chapters also use small **Python** scripts for calculations, plots, or payload processing.

To work with the repository locally:

```bash
git clone https://github.com/dhrubjun/sdr-with-gnu-radio.git
cd sdr-with-gnu-radio
```

The exact GNU Radio blocks and parameters used in each experiment are described in the corresponding chapter.

## Learning Approach

The book follows a simple pattern:

**Build → Observe → Experiment → Explain**

Whenever possible, the experiments also include failure cases. For example, receiver stages are deliberately disabled to show what happens when carrier recovery, timing recovery, equalization, or frame synchronization is missing.

This makes the plots useful for understanding and diagnosing real communication systems rather than treating them only as illustrations.


## Author

**Dhrubjun Nath Saikia**

This project is being developed as a practical learning resource for Software Defined Radio, DSP, and digital communication using GNU Radio.
