# Chapter 25: Why OFDM?

## Main Question

**Why divide one high-rate data stream among many slower orthogonal subcarriers instead of transmitting everything on one fast carrier?**

Chapter 24 completed the single-carrier part of the receiver.

We combined pulse shaping, synchronization, equalization, symbol decisions, frame detection, and payload recovery into one end-to-end QPSK system. That receiver could compensate for several important impairments, but the multipath experiment also exposed a deeper difficulty.

As the symbol rate of a single-carrier system increases, the symbol duration becomes shorter. A physical echo delay that was small compared with one long symbol can become a large fraction of a shorter symbol.

The resulting intersymbol interference becomes harder to manage.

A different approach is to divide the high-rate information stream into several slower parallel streams and transmit them on different subcarriers.

That is the starting point of multicarrier communication.

But simply adding many carriers creates another problem. If they are kept far apart, spectrum is wasted. If they are moved closer together without any special structure, they interfere.

OFDM solves both problems by using many **orthogonal** subcarriers.

Their spectra can overlap, yet the receiver can still separate them when the frequencies and observation interval satisfy the required orthogonality relationship.

This chapter develops that idea experimentally before introducing the IFFT.

## 25.1 The Problem with One Very Fast Carrier

For a single-carrier system with symbol rate $R_s$, the symbol duration is

$$
T_s=\frac{1}{R_s}
$$

Increasing the symbol rate therefore reduces the time occupied by each symbol.

That can increase the information rate, but the physical propagation channel has not changed.

A reflected signal may still arrive with the same absolute delay.

If that delay is small compared with $T_s$, its effect may be manageable.

If $T_s$ becomes shorter, the same delay occupies a larger fraction of the symbol interval.

![A fixed multipath delay occupies a larger fraction of the symbol interval as the symbol rate increases.](../figures/ch25/ch25_symbol_rate_fixed_echo_delay_concept.png)

The important quantity is therefore not simply the echo delay or the symbol rate by itself.

It is the relationship between **channel delay spread and symbol duration**.

## 25.2 Experiment 25.1: Symbol Rate and Multipath

We now observe this effect with a single-carrier QPSK signal.

The sample rate is

$$
F_s=32000\text{ samples/s}
$$

and the first case uses

$$
sps=32
$$

so

$$
R_s=\frac{F_s}{sps}=\frac{32000}{32}=1000\text{ symbols/s}
$$

The transmitter uses QPSK with root-raised-cosine pulse shaping.

The channel contains a direct path and one delayed copy.

| Parameter | Value |
|---|---:|
| Sample rate | `32 ksample/s` |
| Samples per symbol | `32` initially |
| Symbol rate | `1 ksymbol/s` initially |
| RRC roll-off factor | `0.35` |
| Filter span | `8` symbols |
| Number of taps | `257` |
| Echo delay | `8` samples |
| Echo gain | `0.5` |

![GNU Radio flowgraph for the single-carrier symbol-rate and multipath experiment.](../figures/ch25/ch25_exp01_symbol_rate_multipath_flowgraph.png)

The echo delay is kept fixed while the symbol rate is changed.

This is important.

The channel is not being made worse between runs. The same physical delay is being compared with different symbol durations.

![Comparison of the effect of a fixed multipath delay at different single-carrier symbol rates.](../figures/ch25/ch25_exp01_symbol_rate_multipath_comparison.png)

At the lower symbol rate, the eye and constellation remain comparatively well behaved.

As the symbol rate increases, the same 8-sample echo occupies a larger fraction of one symbol interval. The eye closes further and the constellation becomes more distorted.

A higher symbol rate is not inherently bad.

The difficulty appears when the symbol duration becomes short relative to the channel delay spread.

This suggests a different strategy: instead of one very fast stream, divide the information among several slower streams.

## 25.3 From One Fast Stream to Several Slower Streams

Suppose a high-rate stream is divided among four parallel subcarriers.

Each subcarrier then carries only part of the total information rate.

Its symbol rate can therefore be lower, giving a longer symbol duration.

For the same physical multipath delay, a longer symbol duration means the delayed energy occupies a smaller fraction of one symbol interval.

That is the fundamental **multicarrier** idea.

There is, however, an immediate cost.

If the subcarriers are widely separated so that their spectra do not overlap, significant frequency space can be left unused.

A practical system therefore wants two things at once:

- relatively slow symbols on each subcarrier;
- efficient packing of those subcarriers in frequency.

Orthogonality is what makes both possible.

## 25.4 Experiment 25.2: Building a Simple Multicarrier Signal

Before introducing OFDM, we manually build a four-subcarrier waveform from ordinary GNU Radio blocks.

Each branch generates QPSK symbols, pulse shapes them at a lower symbol rate, shifts the complex signal to a chosen subcarrier frequency, and contributes to the final sum.

The subcarriers are initially placed near

```text
-6 kHz
-2 kHz
+2 kHz
+6 kHz
```

so the spacing is approximately 4 kHz.

![GNU Radio flowgraph used to construct the four-subcarrier multicarrier signal.](../figures/ch25/ch25_exp02_multicarrier_signal_flowgraph.png)

The combined spectrum contains four distinct pulse-shaped regions.

![Spectrum of the manually constructed four-subcarrier multicarrier signal.](../figures/ch25/ch25_exp02_four_subcarrier_multicarrier_spectrum.png)

This demonstrates the multicarrier principle.

Several slower streams can coexist in different frequency regions.

But the large gaps also reveal the weakness of this simple arrangement.

If a system used hundreds of subcarriers with similar guard spacing, much of the available spectrum would remain unused.

We therefore want to move the subcarriers closer together.

The next question is whether overlapping subcarrier spectra must necessarily interfere.

## 25.5 What Does Orthogonal Mean?

A familiar example comes from vectors.

Consider

$$
\mathbf{x}=[1,0]
$$

and

$$
\mathbf{y}=[0,1]
$$

A vector compared with itself gives

$$
\mathbf{x}\cdot\mathbf{x}=1
$$

while the dot product between the two different vectors is

$$
\mathbf{x}\cdot\mathbf{y}=0
$$

The vectors are orthogonal.

Signals can have an analogous relationship.

Instead of comparing two short vectors, we compare two waveforms over a specified time interval.

For normalized signals,

$$
C_{ii}=1
$$

for a signal compared with itself, while two different orthogonal signals satisfy

$$
C_{ij}=0,\qquad i\neq j
$$

over the chosen observation interval.

That zero cross-correlation is exactly what we want between different OFDM subcarriers.

## 25.6 Experiment 25.3: Demonstrating Subcarrier Orthogonality

We now use two simple complex carriers without data modulation so that the orthogonality itself is visible.

| Parameter | Value |
|---|---:|
| Sample rate, $F_s$ | `32 ksample/s` |
| Number of samples, $N$ | `32` |
| Useful interval, $T_u$ | `1 ms` |
| First carrier, $f_1$ | `1 kHz` |
| Second carrier, $f_2$ | variable |

The useful observation interval is

$$
T_u=\frac{N}{F_s}=\frac{32}{32000}=0.001\text{ s}=1\text{ ms}
$$

so

$$
\frac{1}{T_u}=1000\text{ Hz}
$$

The two carriers are combined with Multiply Conjugate.

A Moving Average then averages the complex result over exactly 32 samples:

```text
Length: 32
Scale: 0.03125
```

Complex to Mag converts the result into a correlation magnitude.

![GNU Radio flowgraph for measuring the correlation between two subcarriers over the useful interval.](../figures/ch25/ch25_exp03_subcarrier_orthogonality_flowgraph.png)

### Relative Rotation

The easiest way to understand the result is to think of the complex carriers as rotating arrows.

Let

$$
f_1=1000\text{ Hz}
$$

and

$$
f_2=2000\text{ Hz}
$$

Their relative frequency is

$$
\Delta f=f_2-f_1=1000\text{ Hz}
$$

A 1 kHz relative rotation completes one full cycle in

$$
\frac{1}{1000}=1\text{ ms}
$$

which is exactly $T_u$.

During the averaging interval, the relative phasor therefore makes one complete revolution.

Its directions cancel over the full cycle, so the correlation magnitude approaches zero.

The two carriers are orthogonal over that interval.

### Non-Orthogonal 750 Hz Spacing

Now keep

$$
f_1=1000\text{ Hz}
$$

and use

$$
f_2=1750\text{ Hz}
$$

Then

$$
\Delta f=750\text{ Hz}
$$

and during $T_u=1$ ms,

$$
\Delta fT_u=750(0.001)=0.75
$$

The relative phasor completes only three quarters of a cycle.

The directions therefore do not cancel completely.

The measured correlation magnitude is approximately

$$
|C|\approx0.300377
$$

which is nonzero.

The carriers are not orthogonal over this interval.

### Two Complete Rotations

We also test

$$
f_2=3000\text{ Hz}
$$

with $f_1=1000$ Hz.

Now

$$
\Delta f=2000\text{ Hz}
$$

so the relative phasor completes exactly two rotations in 1 ms.

Two complete rotations also average to zero.

![Comparison of non-orthogonal and orthogonal subcarrier spacings.](../figures/ch25/ch25_exp03_subcarrier_orthogonality_comparison.png)

The general condition is

$$
\Delta f=\frac{k}{T_u},\qquad k=1,2,3,\ldots
$$

or equivalently,

$$
\Delta fT_u=k
$$

where $k$ is a nonzero integer.

### Why OFDM Uses the Smallest Orthogonal Spacing

If $2/T_u$, $3/T_u$, and larger integer multiples are also orthogonal, why is

$$
\Delta f=\frac{1}{T_u}
$$

the familiar OFDM spacing?

Because it is the smallest nonzero orthogonal spacing.

For $T_u=1$ ms:

| Spacing | $\Delta fT_u$ | Orthogonal? | Interpretation |
|---:|---:|---|---|
| 750 Hz | 0.75 | No | nonzero cross-correlation |
| 1 kHz | 1 | Yes | closest orthogonal spacing |
| 2 kHz | 2 | Yes | orthogonal but more widely separated |
| 3 kHz | 3 | Yes | orthogonal but wastes more spacing |

OFDM normally uses adjacent spacing

$$
\Delta f=\frac{1}{T_u}
$$

because it preserves orthogonality while packing the subcarriers as closely as possible in this ideal model.

### What the GUI Displays Mean

The Frequency Sink after Multiply Conjugate shows the **relative frequency** between the two carriers.

For example, with $f_1=1$ kHz and $f_2=2$ kHz, the displayed component appears near $-1$ kHz because of the multiplication order.

That spectral line does not by itself prove orthogonality.

The decisive measurement is the complex average over the complete useful interval.

When that cross-correlation approaches zero, the two carriers are orthogonal over $T_u$.

## 25.7 Why Orthogonality Matters to a Receiver

Zero cross-correlation becomes useful when different subcarriers carry different data.

Suppose Subcarrier 1 carries symbol $A_1$ and Subcarrier 2 carries symbol $A_2$.

If the receiver detects Subcarrier 1, we want the desired carrier to survive while the other carrier contributes nothing.

For normalized carriers,

$$
C_{11}=1
$$

and for an orthogonal neighbour,

$$
C_{21}=0
$$

The detected contribution is then

$$
A_1C_{11}+A_2C_{21}=A_1(1)+A_2(0)=A_1
$$

The desired symbol remains.

The orthogonal neighbour cancels in the corresponding correlation operation.

This is the practical reason orthogonality matters.

## 25.8 Experiment 25.4: Recovering Data from Orthogonal Subcarriers

We now transmit independent QPSK data on two subcarriers and attempt to recover Subcarrier 1.

Two spacings are compared:

- 1 kHz, which is orthogonal over $T_u=1$ ms;
- 750 Hz, which is not.

Unlike Experiment 25.2, we do not use RRC pulse shaping here.

Each QPSK symbol is held constant for exactly 32 samples using Repeat.

With

$$
F_s=32000\text{ samples/s}
$$

and

$$
N=32
$$

each symbol occupies

$$
T_u=\frac{32}{32000}=1\text{ ms}
$$

This rectangular finite-duration symbol interval is intentional because it gives us the same common interval used in the orthogonality experiment.

The main values are

| Parameter | Value |
|---|---:|
| Sample rate | `32 ksample/s` |
| $N$ | `32` samples |
| $T_u$ | `1 ms` |
| $f_1$ | `1 kHz` |
| $f_2$ | `2 kHz` for orthogonal case |
| $f_2$ | `1.75 kHz` for non-orthogonal case |

At the receiver, the combined signal is multiplied by the conjugate of a 1 kHz reference, averaged over 32 samples, and reduced to one recovered complex value per symbol interval.

![GNU Radio flowgraph for recovering one QPSK subcarrier from the two-subcarrier signal.](../figures/ch25/ch25_exp04_orthogonal_subcarrier_recovery_flowgraph.png)

### Orthogonal Case

For

$$
f_1=1000\text{ Hz}
$$

and

$$
f_2=2000\text{ Hz}
$$

the spacing is

$$
\Delta f=1000\text{ Hz}=\frac{1}{T_u}
$$

The detected symbol is

$$
A_1C_{11}+A_2C_{21}=A_1
$$

because the second subcarrier has zero cross-correlation with the first over the useful interval.

The recovered constellation therefore contains the expected four QPSK points.

### Non-Orthogonal Case

Now use

$$
f_2=1750\text{ Hz}
$$

so

$$
\Delta f=750\text{ Hz}
$$

The cross-correlation is no longer zero.

The detected symbol becomes

$$
\hat{A}_1=A_1+C_{21}A_2
$$

Part of Subcarrier 2 therefore leaks into the detection of Subcarrier 1.

Because $A_2$ is itself changing among QPSK values, each desired constellation point can be displaced in several different directions.

![Comparison of recovered Subcarrier 1 for orthogonal and non-orthogonal subcarrier spacing.](../figures/ch25/ch25_exp04_orthogonal_vs_nonorthogonal_recovery.png)

The orthogonal case produces four clean constellation points.

The non-orthogonal case produces several displaced points.

This unwanted interaction is **inter-carrier interference**, or ICI.

The conclusion should be stated carefully.

A non-orthogonal pair is not necessarily impossible to decode with every conceivable receiver.

What this experiment shows is that orthogonal subcarriers can ideally be separated by the corresponding correlation operation without mutual interference, whereas loss of orthogonality introduces unwanted coupling between the detected subcarrier values.

## 25.9 Spectral Overlap Is Not the Same as Interference

A simple multicarrier system can avoid interference by leaving large gaps between subcarriers.

That works, but it wastes spectrum.

![Widely separated subcarriers leave unused spectrum between neighboring channels.](../figures/ch25/ch25_widely_separated_multicarrier_concept.png)

OFDM takes a different approach.

The individual subcarrier spectra are allowed to overlap.

The frequencies are chosen so that the waveforms remain orthogonal over the common useful symbol interval.

That leads to one of the central ideas of the chapter:

> **Overlapping spectra do not automatically imply inter-carrier interference. What matters is whether the subcarriers remain orthogonal over the receiver's observation interval.**

This allows OFDM to combine relatively slow subcarrier symbols with efficient frequency packing.

## 25.10 Why OFDM Helps with Multipath

We can now return to the problem that started the chapter.

A high-rate single-carrier stream requires short symbols.

A fixed physical multipath delay can therefore occupy a large fraction of one symbol interval.

Multicarrier transmission divides the same overall data stream among many slower subcarriers.

Each subcarrier can use a longer symbol duration.

The physical propagation delay has not disappeared, but it now occupies a smaller fraction of the useful symbol interval.

This makes multipath easier to manage.

OFDM does not magically eliminate multipath.

Later we will still need a guard interval or cyclic prefix, channel estimation, and equalization.

The important point is more fundamental:

> **Many slower subcarriers create longer symbol intervals, reducing the relative severity of a fixed channel delay spread.**

Orthogonality then allows those subcarriers to be packed closely in frequency.

## 25.11 Choosing the Orthogonal Frequencies

A practical OFDM design begins with the useful symbol duration $T_u$.

The minimum adjacent orthogonal spacing is

$$
\Delta f=\frac{1}{T_u}
$$

The subcarrier frequencies can therefore be written as

$$
f_k=f_0+\frac{k}{T_u}
$$

where $k$ is an integer.

The value $f_0$ shifts the complete set in frequency.

The relative spacing determines the orthogonality over the common interval.

For

$$
T_u=1\text{ ms}
$$

we obtain

$$
\Delta f=1\text{ kHz}
$$

A possible baseband set is therefore

```text
...  -2 kHz  -1 kHz   0   +1 kHz  +2 kHz  ...
```

Now suppose one useful OFDM symbol contains $N$ time-domain samples at sample rate $F_s$.

Then

$$
T_u=\frac{N}{F_s}
$$

and

$$
\Delta f=\frac{1}{T_u}=\frac{F_s}{N}
$$

But $F_s/N$ is exactly the spacing between DFT frequency bins.

This is the bridge between the manually constructed subcarriers in this chapter and the FFT/IFFT implementation used by practical OFDM systems.

## 25.12 GNU Radio Toolbox

Several familiar GNU Radio blocks take on new roles in the multicarrier experiments.

| GNU Radio Block | Role in This Chapter |
|---|---|
| Signal Source | creates complex subcarrier references |
| Multiply | shifts a complex QPSK stream to a subcarrier frequency |
| Add | combines several subcarrier waveforms |
| Multiply Conjugate | exposes the relative phase and frequency between two subcarriers |
| Moving Average | averages the relative phasor over exactly one useful interval |
| Complex to Mag | converts the complex cross-correlation result to a magnitude |
| Repeat | holds each QPSK value constant for the complete useful symbol interval in Experiment 25.4 |
| Keep 1 in N | selects one recovered complex value per useful symbol interval |
| QT GUI Frequency Sink | displays subcarrier spectra and relative-frequency components |
| QT GUI Constellation Sink | shows whether one subcarrier has been recovered cleanly |

### Moving Average as the Correlation Window

In Experiment 25.3,

```text
Length: 32
Scale: 1.0/32
```

makes the Moving Average calculate a normalized average over one 1 ms useful interval.

Its meaning here is therefore more specific than generic smoothing.

It is the integration window over which orthogonality is tested.

### Repeat in the Data-Recovery Experiment

The Repeat block in Experiment 25.4 deliberately creates a rectangular 1 ms symbol interval.

That is not presented as a practical final OFDM pulse-shaping solution.

It is a controlled teaching construction that lets the data experiment use the same $T_u$ and orthogonality condition developed in Experiment 25.3.

## 25.13 Explore Further

The experiments can be extended without changing their basic structure.

1. Keep `f1 = 1 kHz` and `Tu = 1 ms`, then test `f2 = 1.5`, `2.0`, `2.5`, `3.0`, and `4.0 kHz`. Calculate $\Delta fT_u$ before looking at the Number Sink.

2. Test negative frequency differences as well as positive ones. Orthogonality depends on the integer number of relative rotations, not on the sign alone.

3. Keep the subcarrier spacing fixed at 1 kHz and change the averaging interval. Observe that a spacing can be orthogonal for one interval and non-orthogonal for another.

4. In Experiment 25.4, replace the 1 kHz spacing with 750 Hz and predict the constellation locations before running the flowgraph.

5. Compare 1 kHz and 2 kHz orthogonal spacing. Both should separate ideally, but one uses frequency space more efficiently.

6. Increase the number of manually constructed subcarriers and observe how quickly the flowgraph becomes cumbersome. This motivates the IFFT implementation directly.

7. Return to Experiment 25.1 and compare a fixed physical echo with several symbol durations. Relate the observed eye closure to the ratio between echo delay and symbol duration.

## 25.14 What We Learned

This chapter developed the motivation for OFDM from the communication problem rather than beginning with an OFDM block.

A high symbol rate shortens the single-carrier symbol duration.

A fixed multipath delay therefore becomes more significant relative to each symbol as the symbol rate increases.

This motivates dividing a high-rate stream among several slower parallel streams.

The manually constructed four-subcarrier experiment showed the multicarrier idea directly, but wide carrier spacing used the available spectrum inefficiently.

Orthogonality provides the solution.

For normalized carriers, a subcarrier correlated with itself gives

$$
C_{ii}=1
$$

while two different orthogonal subcarriers satisfy

$$
C_{ij}=0,\qquad i\neq j
$$

over the common useful interval.

Experiment 25.3 showed this physically through relative rotation.

With $T_u=1$ ms, 1 kHz spacing produced one complete relative revolution and approximately zero cross-correlation.

A 750 Hz spacing produced only 0.75 of a revolution and a measured correlation magnitude of approximately 0.300377.

A 2 kHz spacing produced two complete revolutions and again gave approximately zero cross-correlation.

The general condition is

$$
\Delta f=\frac{k}{T_u}
$$

for nonzero integer $k$.

OFDM normally uses

$$
\Delta f=\frac{1}{T_u}
$$

because it is the smallest nonzero orthogonal spacing.

Experiment 25.4 then showed why that zero cross-correlation matters to actual data.

For orthogonal subcarriers, detection of Subcarrier 1 produced

$$
A_1(1)+A_2(0)=A_1
$$

so the other QPSK stream did not contribute to the recovered symbol in the ideal correlation model.

When the spacing was changed to 750 Hz, the second subcarrier leaked into the first and produced ICI.

The key distinction is that **spectral overlap is not automatically the same as interference**.

Orthogonal subcarrier spectra can overlap while remaining ideally separable over the correct observation interval.

Finally, the relationship

$$
\Delta f=\frac{1}{T_u}=\frac{F_s}{N}
$$

showed that the orthogonal subcarrier spacing is exactly the DFT-bin spacing for an $N$-sample useful symbol.

That is the bridge to the IFFT.

## 25.15 Connecting to the Next Chapter

We now understand why OFDM uses many slow, closely spaced, orthogonal subcarriers.

Our experiments constructed those subcarriers manually with separate oscillators, multipliers, and adders.

That approach is useful for two or four carriers because every operation remains visible.

It does not scale well to dozens, hundreds, or thousands of subcarriers.

The DFT relationship developed in this chapter gives us a better method.

If the desired complex data symbols are placed directly into orthogonal frequency bins, the inverse discrete Fourier transform can generate the complete time-domain multicarrier waveform in one operation.

The FFT and IFFT therefore do more than analyze OFDM.

They provide the computational structure that makes practical OFDM possible.

The next chapter develops that idea directly.

That leads to **Chapter 26: Building an OFDM Signal with the IFFT**.