# Chapter 15: Bits, Symbols and Digital Communication

## Main Question

**How can zeros and ones eventually become a radio waveform?**

In Chapters 12 through 14, the message varied continuously.

AM allowed a continuously varying message to change carrier amplitude. FM allowed it to change instantaneous frequency. Even when we added noise or changed modulation conditions, the underlying message was still an analog quantity that could take many values.

Digital communication begins differently.

We may start with a sequence such as

```text
1 0 1 1 0 0 1 0
```

These are **bits**.

But a bit is an abstract piece of information. An antenna cannot radiate the idea of `0` or `1`. Somewhere in the transmitter, those bits must become numerical signal states, sampled waveforms, voltages, currents, and eventually electromagnetic fields.

The path therefore looks roughly like this:

`Bits → Groups of Bits → Symbols → Physical Signal States → Waveform`

This chapter develops the first half of that path.

We will not yet build BPSK, QPSK, QAM, or PAM. First we need a clean understanding of bits, symbols, bit rate, symbol rate, and mapping. Once those ideas are clear, the modulation schemes that follow become much easier to understand.

## 15.1 A Bit Is Information, Not a Voltage

A bit has two possible values:

```text
0
1
```

That sounds simple, but one distinction is worth making immediately.

The bit is the **information**. The voltage, phase, frequency, amplitude, or I/Q point used to represent it is a **signal representation**.

Those are not the same thing.

The sequence

```text
1 0 1 1 0 0 1 0
```

does not inherently mean

```text
1 volt, 0 volts, 1 volt, ...
```

A particular system might choose such a representation, but another system may represent the same bits using two phases, two frequencies, or two complex constellation points.

Inside GNU Radio, the bits also need some numerical container. In our first experiments, they are carried in byte-sized stream items whose values happen to be only `0` and `1`.

So even before modulation, three ideas are already separate:

- the information bit;
- the numerical value stored in a GNU Radio item;
- the physical waveform that will eventually represent the information.

The experiments in this chapter keep those distinctions visible.

## 15.2 Experiment 15.1: Bits as a Sampled Waveform

Start with the known sequence

```text
1 0 1 1 0 0 1 0
```

A known pattern is useful because every part of the Time Sink display can be predicted before running the flowgraph.

![GNU Radio flowgraph for representing a known bit sequence as a sampled waveform](../figures/ch15/ch15-exp1-bit-waveform-flowgraph.png)

Use:

| Parameter | Value |
|---|---:|
| Sample rate | `32k` samples/s |
| Bit rate | `1k` bit/s |
| Samples per bit | `32` |
| Vector Source | `[1, 0, 1, 1, 0, 0, 1, 0]` |
| Repeat | Yes |
| Time Sink points | `512` |

The Vector Source produces byte values. We deliberately restrict them to `0` and `1` because those values represent our binary information.

The **UChar to Float** block changes only the data type:

```text
byte 0 -> float 0.0
byte 1 -> float 1.0
```

No modulation has happened.

The next block, **Repeat**, gives each bit a visible duration in the sampled waveform.

With

$$
f_s=32000\text{ samples/s}
$$

and

$$
R_b=1000\text{ bit/s},
$$

the number of waveform samples per bit is

$$
N_{\text{samples/bit}}=\frac{f_s}{R_b}=\frac{32000}{1000}=32.
$$

So each input bit value is repeated for 32 output samples.

![Known binary sequence represented using 32 samples per bit](../figures/ch15/ch15-exp1-bit-waveform.png)

At a bit rate of 1000 bit/s, one bit lasts

$$
T_b=\frac{1}{R_b}=\frac{1}{1000}=1\text{ ms}.
$$

The Time Sink displays 512 samples. At 32 kS/s, the visible interval is

$$
T_{\text{display}}=\frac{512}{32000}=16\text{ ms}.
$$

Since each bit lasts 1 ms, the display contains 16 bit intervals, which is two repetitions of the eight-bit pattern.

This experiment gives us one of the most useful distinctions in digital communication:

> **A bit is a unit of information. A sample is one numerical description of a waveform at one instant. One bit may be represented by many samples.**

The rectangular shape here is only a teaching representation. Later, pulse shaping will replace these abrupt transitions with a waveform better suited to communication systems.

## 15.3 Experiment 15.2: Changing the Bit Rate

Bit rate tells us how many information bits pass through the system each second.

Its reciprocal is the bit duration:

$$
T_b=\frac{1}{R_b}.
$$

To make that relationship visible, keep the sample rate fixed at 32 kS/s and vary the bit rate from 500 to 4000 bit/s.

The samples-per-bit relationship remains

$$
N_{\text{samples/bit}}=\frac{f_s}{R_b}.
$$

At our fixed sample rate:

| Bit Rate | Bit Duration | Samples per Bit |
|---:|---:|---:|
| 500 bit/s | 2 ms | 64 |
| 1000 bit/s | 1 ms | 32 |
| 2000 bit/s | 0.5 ms | 16 |
| 4000 bit/s | 0.25 ms | 8 |

The Time Sink still shows a 16 ms window.

At 500 bit/s:

![Binary waveform at 500 bit/s](../figures/ch15/ch15-exp2-bit-rate-500.png)

Each bit lasts 2 ms, so eight bit intervals fit in the display.

At 2000 bit/s:

![Binary waveform at 2000 bit/s](../figures/ch15/ch15-exp2-bit-rate-2000.png)

Each bit now lasts only 0.5 ms, so 32 bit intervals fit in the same window.

The information alphabet has not changed. The source still contains only zeros and ones.

Only the rate has changed.

At a fixed waveform sample rate, increasing the bit rate also means that fewer samples are available to represent each bit. That relationship will matter later when we discuss symbol timing, interpolation, pulse shaping, and receiver synchronization.

## 15.4 Experiment 15.3: Grouping Bits into Symbols

So far, every bit has been treated separately.

There is no requirement to keep doing that.

Take the same bit sequence and group it in pairs:

```text
1 0 | 1 1 | 0 0 | 1 0
```

There are four possible two-bit patterns:

```text
00
01
10
11
```

We can assign each pattern a **symbol index**.

For this experiment, the Repack Bits block uses **MSB-first** endianness, so the mapping is

| Bit Group | Symbol Index |
|---|---:|
| `00` | 0 |
| `01` | 1 |
| `10` | 2 |
| `11` | 3 |

The flowgraph is:

![GNU Radio flowgraph for grouping bits into two-bit symbols](../figures/ch15/ch15-exp3-bits-to-symbols-flowgraph.png)

Repack Bits is configured with one relevant input bit and two relevant output bits.

For our sequence,

```text
Bits:           1 0 | 1 1 | 0 0 | 1 0
Two-bit groups:  10 |  11 |  00 |  10
Symbol indices:   2 |   3 |   0 |   2
```

The result is:

![Two-bit groups represented as symbol indices](../figures/ch15/ch15-exp3-symbol-indices.png)

The values `0`, `1`, `2`, and `3` are labels for the four possible symbol choices.

They are not yet transmitted amplitudes.

In particular, symbol index `3` does not mean 3 volts, amplitude 3, phase 3 radians, or frequency 3 Hz.

It means only: **the bit pattern associated with symbol index 3 occurred**.

One timing detail is also worth keeping clear. In this particular flowgraph, the grouped symbols are repeated for the same `samples_per_bit` value used earlier. The purpose of Experiment 15.3 is therefore to make the **grouping and indexing** visible, not to establish the correct symbol duration for a fixed bit rate.

The next experiment handles the bit-rate and symbol-rate timing relationship explicitly.

## 15.5 Bits per Symbol

If each symbol represents \(k\) bits, then the number of possible bit patterns is

$$
M=2^k.
$$

For example:

| Bits per Symbol \(k\) | Possible Symbols \(M\) |
|---:|---:|
| 1 | 2 |
| 2 | 4 |
| 3 | 8 |
| 4 | 16 |
| 6 | 64 |
| 8 | 256 |

Conversely,

$$
k=\log_2(M).
$$

This is why modulation names often contain numbers such as 2, 4, 8, 16, 64, or 256. For an \(M\)-ary modulation with \(M\) equal to a power of two, each symbol can represent an integer number of bits.

But grouping more bits into each symbol changes another important quantity: **symbol rate**.

## 15.6 Experiment 15.4: Bit Rate vs Symbol Rate

Keep the information bit rate fixed at

$$
R_b=1000\text{ bit/s}.
$$

Now compare three groupings:

```text
1 bit per symbol
2 bits per symbol
4 bits per symbol
```

The flowgraph creates three parallel branches from the same bit source.

![GNU Radio flowgraph comparing one, two, and four bits per symbol](../figures/ch15/ch15-exp4-bit-vs-symbol-rate-flowgraph.png)

The sample rate remains 32 kS/s.

At 1000 bit/s, one bit occupies

$$
\frac{32000}{1000}=32
$$

samples.

A one-bit symbol therefore occupies 32 samples.

A two-bit symbol represents two bit intervals, so it occupies 64 samples.

A four-bit symbol represents four bit intervals, so it occupies 128 samples.

The flowgraph implements exactly those three durations.

![Comparison of bit rate and symbol rate for different numbers of bits per symbol](../figures/ch15/ch15-exp4-bit-vs-symbol-rate.png)

For one bit per symbol,

$$
R_s=1000\text{ symbols/s}.
$$

For two bits per symbol,

$$
R_s=500\text{ symbols/s}.
$$

For four bits per symbol,

$$
R_s=250\text{ symbols/s}.
$$

The general relationship is

$$
R_b=kR_s.
$$

Since

$$
k=\log_2(M),
$$

we can also write

$$
R_b=R_s\log_2(M).
$$

Here:

- \(R_b\) is bit rate in bit/s;
- \(R_s\) is symbol rate in symbols/s;
- \(k\) is the number of bits represented by one symbol;
- \(M\) is the number of possible symbol states.

### Baud Is a Symbol Rate

Symbol rate is measured in **baud**.

One baud means one symbol per second.

So:

```text
1000 bit/s with 1 bit/symbol -> 1000 baud
1000 bit/s with 2 bits/symbol ->  500 baud
1000 bit/s with 4 bits/symbol ->  250 baud
```

Bit/s and baud are equal only when each symbol represents one bit.

This distinction becomes increasingly important once we move to QPSK and QAM, where one symbol commonly represents several bits.

## 15.7 Experiment 15.5: Mapping Bits to Symbol Indices

Grouping tells us which bits belong together.

**Mapping** tells us which symbol label or signal state is associated with each possible bit group.

For our MSB-first two-bit experiment:

```text
00 -> 0
01 -> 1
10 -> 2
11 -> 3
```

The next flowgraph displays the original bits and the mapped two-bit symbol indices over the same time interval.

![GNU Radio flowgraph for comparing original bits with mapped symbol indices](../figures/ch15/ch15-exp5-bit-to-symbol-mapping-flowgraph.png)

The bit branch repeats each bit for 32 samples.

The two-bit symbol branch repeats each symbol for

$$
2\times32=64
$$

samples.

The Time Sinks show 256 samples at 32 kS/s:

$$
T_{\text{display}}=\frac{256}{32000}=8\text{ ms}.
$$

At 1000 bit/s, that interval contains eight bits, or four two-bit symbols.

![Original binary data and the corresponding two-bit symbol indices](../figures/ch15/ch15-exp5-bit-to-symbol-mapping.png)

The sequence can be read as

```text
Bits:     1 0 | 1 1 | 0 0 | 1 0
Symbols:   2  |  3  |  0  |  2
```

Each bit lasts 1 ms.

Each two-bit symbol lasts 2 ms.

The experiment now connects grouping, mapping, and timing correctly in one view.

But the symbol indices are still abstract.

We have decided that `10` maps to symbol index `2`, but we have not decided what physical waveform symbol `2` should produce.

That comes next in the book.

## 15.8 Experiment 15.6: Random Bits to Symbols

A fixed sequence is ideal for learning because every output can be predicted.

Real communication systems, however, process data that changes.

For the final experiment, replace the Vector Source with a Random Source.

Configure it as:

```text
Minimum: 0
Maximum: 2
Number of Samples: 1000
Repeat: Yes
```

GNU Radio's Random Source generates values in the interval

$$
[\text{Minimum},\text{Maximum}),
$$

so `Minimum = 0` and `Maximum = 2` produce only

```text
0
1
```

The flowgraph keeps the same two branches used in Experiment 15.5:

- one branch displays the bits;
- the other groups them in pairs with MSB-first Repack Bits and displays symbol indices from 0 to 3.

![Random binary data and the resulting two-bit symbol indices](../figures/ch15/ch15-exp6-random-bits-to-symbols.png)

There is one implementation detail worth knowing.

The GNU Radio Random Source used here generates a fixed pseudo-random vector of `1000` items and repeats that vector because `Repeat = Yes`.

So it is not producing an entirely new random value forever. Within the displayed windows, however, it gives us an arbitrary-looking binary sequence that is useful for exercising the bit-to-symbol processing chain.

The rule remains unchanged:

`Binary Data → Group Two Bits → Symbol Index 0, 1, 2, or 3`

Unlike Experiment 15.5, separate live Time Sinks may be showing different positions in the repeating pseudo-random sequence at the instant a screenshot is captured. The purpose here is therefore not to verify every visible bit pair against every visible symbol.

Experiment 15.5 already provided that controlled comparison.

This experiment shows that the same processing logic works on a longer, non-hand-picked bit stream.

## 15.9 Bits, Bytes, Samples, and Stream Items

Digital GNU Radio flowgraphs make several layers of representation visible at once.

When we say a stream contains bits, we are describing the **information**.

GNU Radio still needs a data type to carry those values.

In our experiments, a bit value such as

```text
1
```

was stored inside a byte-sized stream item.

That does not mean the bit itself is eight information bits. It means one byte-sized container is currently carrying one useful bit.

After Repack Bits groups two useful bits into each output item, the possible numerical values become

```text
0, 1, 2, 3
```

while the output items are still byte-sized containers.

Then, after UChar to Float and Repeat, those symbol labels are converted into floating-point waveform samples for visualization.

So four different questions can arise:

1. How many information bits are present?
2. How many bits are grouped into one symbol?
3. What numerical value labels that symbol?
4. What GNU Radio data type carries that value?

Those questions are related, but they are not interchangeable.

Keeping them separate prevents many confusing errors later when flowgraphs contain packed bytes, unpacked bits, symbol indices, floats, and complex samples at the same time.

## 15.10 A Symbol Is Still Not a Radio Waveform

We can now take

```text
1 0 1 1 0 0 1 0
```

group it as

```text
10 | 11 | 00 | 10
```

and map those groups to

```text
2 | 3 | 0 | 2
```

But we still have not created a radio waveform.

The numbers are only symbol indices.

The transmitter must still associate each possible symbol with a distinguishable **signal state**.

Earlier chapters gave us several physical signal properties that can be changed:

- amplitude;
- frequency;
- phase;
- I and Q together.

Digital modulation chooses from a discrete set of allowed states of those properties.

That produces families such as ASK, FSK, PSK, PAM, and QAM.

The conceptual difference from analog modulation is important:

> **Analog modulation lets a signal property follow a continuously varying message. Digital modulation selects from a discrete set of signal states according to the current symbol.**

That is the bridge between the analog chapters and the digital communication chapters.

## 15.11 Why Symbols Are Useful

Why group bits at all?

The main reason is that one transmitted symbol can represent more than one information bit.

With two possible symbols,

$$
M=2,
$$

each symbol represents

$$
\log_2(2)=1
$$

bit.

With four possible symbols,

$$
M=4,
$$

each symbol represents

$$
\log_2(4)=2
$$

bits.

With sixteen possible symbols,

$$
M=16,
$$

each symbol represents

$$
\log_2(16)=4
$$

bits.

At a fixed bit rate, carrying more bits per symbol reduces the required symbol rate.

But there is a cost.

More symbol states usually means that the receiver must distinguish among more closely spaced possibilities. Noise, distortion, timing error, carrier error, and other impairments can therefore make decisions harder.

We will see that trade-off much more clearly once the symbols become actual amplitude levels and constellation points.

For now, the main idea is enough:

> **A symbol is one choice from a defined alphabet, and that one choice may represent several bits of information.**

## 15.12 GNU Radio Toolbox

The chapter introduces a few blocks that will appear repeatedly in the digital communication chapters.

| GNU Radio Block | Role in This Chapter |
|---|---|
| Vector Source | Generates a known teaching sequence of byte values `0` and `1` |
| Random Source | Generates a fixed pseudo-random vector of binary values for testing |
| UChar to Float | Converts byte-valued items into float-valued items for waveform display |
| Repeat | Repeats each input item to create a chosen number of waveform samples per bit or symbol |
| Repack Bits | Changes how useful bits are grouped into output items |
| QT GUI Time Sink | Displays bit values and symbol indices over time |
| Throttle | Controls the rate of the software-only simulation |

### Repeat

Repeat outputs each input item `Interpolation` times.

In Experiment 15.1,

```text
Interpolation = 32
```

turns each bit value into 32 waveform samples.

In the fixed-bit-rate symbol experiments, the interpolation increases with the number of bits per symbol so that the symbol duration matches the amount of information grouped into that symbol.

### Repack Bits

Repack Bits changes how useful bits are packed into output bytes.

For our two-bit experiments:

```text
Bits per input byte: 1
Bits per output byte: 2
Endianness: MSB
```

The explicit MSB setting is important. It gives the mapping used throughout this chapter:

```text
00 -> 0
01 -> 1
10 -> 2
11 -> 3
```

A different endianness convention can assign different numerical indices to the same arriving bit order.

### Random Source

With

```text
Minimum = 0
Maximum = 2
```

the Random Source produces binary values because its range is `[Minimum, Maximum)`.

In this experiment it pre-generates 1000 pseudo-random items and repeats them.

That behaviour is sufficient for the present demonstration, but it is useful to remember that a repeating pseudo-random test source is not the same thing as an infinite sequence of newly generated independent bits.

## 15.13 Explore Further

The chapter's relationships are simple enough to predict before changing the flowgraph.

1. In Experiment 15.2, set the bit rate to 4000 bit/s. Predict the bit duration and samples per bit before running.

2. Keep the sample rate at 32 kS/s and choose a bit rate that does not divide it exactly. Consider what an integer Repeat factor can and cannot represent.

3. Change Experiment 15.3 from MSB-first to LSB-first Repack Bits. Observe how the numerical symbol indices assigned to bit pairs change.

4. In Experiment 15.4, keep \(R_b=1000\) bit/s and calculate the symbol rate for 3 bits per symbol.

5. Extend the symbol grouping to 4 bits per symbol and predict the possible index range.

6. In Experiment 15.5, replace the source sequence with another eight-bit pattern and work out the expected symbol indices by hand before running.

7. In Experiment 15.6, increase `Number of Samples` in the Random Source. The repetition period of the pseudo-random pattern should become longer.

The useful habit is the same one we have used throughout the book: predict first, run second, then explain any difference.

## 15.14 What We Learned

A **bit** is a unit of binary information.

It is not inherently a voltage, sample, byte, or waveform level.

The bit rate \(R_b\) tells us how many information bits pass through the system each second, and the bit duration is

$$
T_b=\frac{1}{R_b}.
$$

In an SDR waveform, one bit may be represented by many samples.

Several bits can be grouped into one **symbol**.

If each symbol represents \(k\) bits, the number of possible symbols is

$$
M=2^k.
$$

The bit rate and symbol rate are related by

$$
R_b=kR_s=R_s\log_2(M).
$$

Symbol rate is measured in baud.

Bit/s and baud are equal only when each symbol represents one bit.

**Mapping** defines the association between a bit group and a symbol label or signal state.

In our MSB-first two-bit experiments,

```text
00 -> 0
01 -> 1
10 -> 2
11 -> 3
```

but those numerical indices are still only labels.

The radio waveform comes later.

We also separated several implementation concepts that are easy to mix together:

- information bits;
- byte-sized GNU Radio items;
- grouped symbol indices;
- waveform samples;
- physical signal states.

The transmitter-side path is now clearer:

`Bits → Bit Groups → Symbol Indices → Physical Signal States → Waveform`

In this chapter, we reached the symbol indices.

## 15.15 Connecting to the Next Chapter

We now know how to group binary information into symbols.

The next step is to give those symbols physical signal values.

The simplest place to begin is amplitude.

A binary system could assign two amplitude levels to its two symbols. A four-symbol system could choose four allowed levels.

Once noise is added, however, the received amplitude will not always land exactly on one of those ideal values.

The receiver must decide which symbol was most likely transmitted.

That takes us to Chapter 16, **Pulse Amplitude Modulation**, where abstract symbol indices become amplitude levels and the receiver begins making real symbol decisions.