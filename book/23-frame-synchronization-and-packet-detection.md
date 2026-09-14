# Chapter 23: Frame Synchronization and Packet Detection

## Main Question

**How does a receiver determine where a frame or packet begins in a continuous stream of recovered symbols or bits?**

Chapter 22 recovered symbol timing. The receiver learned when to measure each symbol so that the transmitted constellation could be observed at useful decision instants.

But correct symbol timing does not tell us where a message begins.

A receiver may produce a continuous stream such as

```text
... 1 0 1 1 0 0 1 0 0 1 1 0 0 1 0 1 1 0 1 1 0 0 1 0 ...
```

and still need to answer several questions.

Where does one frame begin?

Which bits belong to the synchronization sequence?

Which bits belong to the payload?

That is the problem of **frame synchronization**.

In this chapter, we create repeated QPSK frames, insert a known preamble, detect it with correlation, study the effects of noise and threshold choice, compare different preamble sequences and lengths, and finally use GNU Radio stream tags to mark detected frame boundaries.

Carrier synchronization determines the correct phase and frequency reference. Timing synchronization determines when to sample the waveform. Frame synchronization determines where the structured message begins.

## 23.1 From a Continuous Stream to a Frame

A practical digital communication system usually organizes information into **frames** or **packets**.

A simple frame may contain

```text
Preamble | Payload
```

The **payload** contains the information we want to communicate.

The **preamble** is a known sequence deliberately inserted by the transmitter.

Sending known information may appear wasteful, but it gives the receiver a recognizable landmark. If every frame begins with the same sequence, the receiver can search the incoming stream for that pattern.

A more complete frame may also contain a header and an error-detection field, but we do not need that structure yet.

The central idea is simple:

> **A known preamble gives the receiver a way to locate an otherwise unknown frame boundary.**

In these experiments, packet detection and frame-boundary detection are closely related because the same known sequence provides both the evidence that a frame is present and the reference position for that frame.

## 23.2 Experiment 23.1: Creating a Repeated QPSK Frame

Before detecting a frame, we first create one.

The transmitted stream repeats the same basic structure:

```text
Preamble | Payload | Preamble | Payload | ...
```

![GNU Radio flowgraph for the repeated QPSK frame](../figures/ch23/ch23_exp01_flowgraph.png)

The modulation itself is familiar QPSK. The new element is the structure of the transmitted data.

The main settings are

| Parameter | Value |
|---|---:|
| Sample rate | `32 kS/s` |
| Symbol rate | `4 ksym/s` |
| Samples per symbol | `8` |
| RRC roll-off factor | `0.35` |
| RRC span | `8` symbols |
| Number of RRC taps | `65` |

Because the frame repeats, the preamble also appears periodically in the transmitted stream.

![Repeated QPSK frame](../figures/ch23/ch23_exp01_repeated_qpsk_frame.png)

At this stage, the receiver is not yet detecting anything.

The experiment simply creates a known sequence that appears repeatedly inside an otherwise continuous communication signal.

## 23.3 Searching for the Preamble with Correlation

The DSP operation we need was introduced in Chapter 11: **correlation**.

There, correlation measured how strongly a received signal matched a known reference.

Here, the same idea becomes a frame-synchronization tool.

Let the known preamble contain $N$ complex symbols. One form of sliding correlation is

$$
C[k]=\sum_{n=0}^{N-1}r[k+n]p^*[n]
$$

where $r[\cdot]$ is the received sequence and $p[\cdot]$ is the known preamble.

A detector can examine

$$
|C[k]|
$$

As the reference slides across unrelated payload symbols, the terms do not reinforce consistently.

When the received sequence aligns with the known preamble, the terms reinforce and a larger correlation response appears.

The important point is that correlation combines evidence from the **entire known sequence** rather than deciding from one sample alone.

## 23.4 Experiment 23.2: Detecting the Preamble with Correlation

We now search the repeated QPSK stream for the known preamble.

![GNU Radio flowgraph for preamble correlation](../figures/ch23/ch23_exp02_flowgraph.png)

Because the same preamble occurs once per frame, we expect strong correlation responses at regular intervals.

![Preamble correlation for the repeated frame](../figures/ch23/ch23_exp02_preamble_correlation.png)

That is what we observe.

The receiver does not need to know the payload. It only needs the known synchronization sequence.

Correlation has now changed from a general similarity measure into a practical synchronization mechanism.

## 23.5 Correlation in Noise

A simple noisy received signal can be written as

$$
r[n]=s[n]+w[n]
$$

Noise changes the individual received samples.

Correlation still has an advantage because it combines information from several known symbols. Random noise does not normally reinforce over the preamble in the same structured way as the correctly aligned sequence.

This does not make correlation immune to noise.

As the disturbance becomes stronger, genuine correlation peaks can shrink or fluctuate, while accidental responses from noise and payload data can become more significant.

## 23.6 Experiment 23.3: Preamble Detection in Noise

We now increase only the Channel Model noise voltage.

The experiment observes both the recovered QPSK symbols and the preamble-correlation response.

![Effect of noise on preamble correlation and recovered QPSK symbols](../figures/ch23/ch23_exp03_noise_comparison.png)

As the noise increases, the constellation spreads and the correlation response becomes more variable.

Useful preamble peaks remain recognizable over part of the tested range, but visual inspection is not enough for an automatic receiver.

The receiver needs a numerical rule that decides whether a correlation response is large enough to count as a detection.

That leads to a threshold.

## 23.7 Turning a Correlation Peak into a Detection

Suppose the receiver declares a preamble when

$$
|C[k]|>T
$$

where $T$ is the detection threshold.

A low threshold makes the detector more sensitive, but unrelated payload patterns or noise fluctuations are then more likely to cross it.

That can produce a **false detection**.

A high threshold makes the detector more selective, but a genuine preamble weakened by noise or distortion may fail to cross it.

That produces a **missed detection**.

There is therefore no universal best threshold.

The threshold expresses how much correlation evidence the receiver requires before it accepts that the preamble has been found.

## 23.8 Experiment 23.4: Effect of Detection Threshold

We compare three detection thresholds.

| Detection threshold | Observation |
|---:|---|
| 7 | sensitive; more values qualify |
| 11 | useful separation in this experiment |
| 14 | above the genuine observed peaks |

![Comparison of different preamble detection thresholds](../figures/ch23/ch23_exp04_threshold_comparison.png)

At threshold 7, the detector responds readily.

Around 11, the strongest preamble responses are separated more clearly from the lower values.

At 14, the genuine observed peaks no longer reach the decision level, so detections are missed.

For this experiment, **11** is a useful choice.

It is not a universal threshold. A useful value depends on signal scaling, preamble length and sequence, noise, channel conditions, and the acceptable tradeoff between false alarms and missed detections.

## 23.9 Experiment 23.5: Effect of Preamble Sequence and Length

Detection quality depends not only on the threshold but also on the sequence being searched for.

We compare:

1. the correct 8-symbol preamble;
2. a wrong 8-symbol sequence;
3. a shorter 4-symbol preamble.

For the retained comparison, the detection threshold is 7.

![Effect of the preamble sequence and length on correlation](../figures/ch23/ch23_exp05_preamble_comparison.png)

The correct 8-symbol preamble produces strong, clearly separated peaks.

For the wrong 8-symbol comparison, the reference sequence is

```text
[1+1j, 1-1j, -1-1j, -1+1j, 1+1j, 1-1j, -1-1j, -1+1j]
```

Its correlation response is weaker and less distinctive than the correct sequence.

The shorter 4-symbol preamble still produces periodic responses, but the peak magnitude is lower because fewer known symbols contribute to the correlation sum.

This gives two useful lessons.

First, **sequence choice matters**. A useful preamble should have correlation properties that make the desired alignment easy to distinguish from other alignments.

Second, **length creates a tradeoff**. A longer preamble can provide more detection evidence, but it also consumes more transmission overhead.

Longer is not automatically better. The sequence itself matters as well.

A constellation plot is not needed for this experiment because the question concerns preamble detection rather than modulation quality.

## 23.10 From Correlation Peaks to Receiver Events

A correlation plot is useful for understanding the detector, but a practical receiver needs machine-readable information saying that a frame landmark was found at a particular stream position.

GNU Radio can attach metadata to stream items using a **stream tag**.

The tag does not replace the data item. It adds information to that position in the stream.

For example, a receiver can create a tag with the key

```text
frame_start
```

when it detects the known access code.

Downstream blocks can then use that metadata to interpret the following data relative to the detected frame boundary.

## 23.11 Experiment 23.6: Detecting an Access Code and Creating Frame Tags

We now move from complex-symbol preamble correlation to a direct bit-stream experiment.

The repeated frame is

```text
Access code: 10110010
Payload:     01100101
```

The frame length is

$$
N_{\text{frame}}=8+8=16\text{ bits}
$$

GNU Radio's `Correlate Access Code - Tag` block searches for

```text
10110010
```

with the settings

```text
Access Code: 10110010
Threshold: 0
Tag Name: frame_start
```

`Tag Debug` is configured to display the `frame_start` tags.

![GNU Radio access-code detection](../figures/ch23/ch23_exp06_access_code_detection.png)

The observed tag offsets include

```text
8
24
40
56
72
88
104
120
```

The spacing is

$$
24-8=16
$$

which matches the 16-bit repeated frame.

### Where Is the Tag Placed?

The detector cannot know that the access code matched until the complete 8-bit pattern has arrived.

In this direct-bit experiment, the tag therefore appears immediately after the detected access code, at the first payload bit.

![Conceptual position of the detected frame tags](../figures/ch23/ch23_exp06_tag_offset_concept.png)

![Tag Debug output for repeated access-code detections](../figures/ch23/ch23_exp06_access_code_tags.png)

The receiver has now converted pattern detection into explicit stream metadata.

## 23.12 Two Different Meanings of Threshold

Two different threshold concepts appear in this chapter.

They must not be confused.

| Threshold | Meaning |
|---|---|
| Correlation detection threshold | minimum correlation evidence required for a detection |
| `Correlate Access Code - Tag` threshold | maximum number of access-code bit mismatches tolerated |

A correlation threshold of 11 and an access-code threshold of 1 are completely different quantities.

The first compares a continuous-valued correlation response with a decision level.

The second controls how many binary disagreements are allowed when matching the access code.

## 23.13 Experiment 23.7: Access-Code Error Tolerance

We deliberately corrupt one access-code bit.

With

```text
Threshold: 0
```

the access-code detector requires an exact match, so the corrupted pattern is rejected.

We then change only

```text
Threshold: 1
```

which allows one bit mismatch.

![Access-code detection with one tolerated bit error](../figures/ch23/ch23_exp07_access_code_error_tolerance.png)

The detector now creates `frame_start` tags.

In the retained output, the accepted one-bit mismatch is reported with

```text
Value: 1
```

Allowing access-code errors therefore creates another tradeoff.

A strict match reduces accidental detections but can miss a corrupted genuine code.

Greater tolerance can preserve detection when some access-code bits are wrong, but more unintended bit patterns may also qualify.

## 23.14 Putting Frame Detection into the QPSK Receiver

The direct bit-stream experiment isolated the access-code detector.

We now integrate it into the communication receiver.

The main processing stages are

**Pulse Shaping → Channel → Matched Filtering → Symbol Timing Recovery → QPSK Decisions → Bit Reconstruction → Access-Code Detection → `frame_start` Tags**

Frame synchronization does not replace timing synchronization.

Timing synchronization answers:

> **Where should each symbol be sampled?**

Frame synchronization answers:

> **Which recovered symbol or bit marks the beginning of the frame structure?**

The two stages solve different problems.

## 23.15 Experiment 23.8: QPSK Frame Detection

The complete frame-detection flowgraph combines the synchronization and decision stages needed to recover the repeated bit structure.

![Complete QPSK frame-detection flowgraph](../figures/ch23/ch23_exp08_flowgraph.png)

The main settings are

| Parameter | Value |
|---|---:|
| Sample rate | `32 kS/s` |
| Symbol rate | `4 ksym/s` |
| Samples per symbol | `8` |
| RRC roll-off factor | `0.35` |
| RRC span | `8` symbols |
| RRC taps | `65` |
| Access code | `10110010` |
| Access-code threshold | `0` |
| Tag name | `frame_start` |
| Head | `128` items |

The Symbol Sync configuration from Chapter 22 is retained:

```text
Timing Error Detector: Gardner
Samples per Symbol: 8
Expected TED Gain: 1
Loop Bandwidth: 0.045
Damping Factor: 1
Maximum Deviation: 1.5
Output Samples/Symbol: 1
Interpolating Resampler: MMSE, 8 tap FIR
```

The synchronized QPSK symbols are separated into I and Q components.

Binary Slicers produce bit decisions, and Interleave reconstructs the serial bit order used by the frame detector.

![Recovered QPSK symbols in the complete frame detector](../figures/ch23/ch23_exp08_recovered_qpsk.png)

The recovered constellation forms four compact QPSK clusters.

![Detected frame tags in the complete QPSK receiver](../figures/ch23/ch23_exp08_frame_tags.png)

The observed frame-tag offsets are

```text
22
38
54
70
86
102
118
```

Again,

$$
38-22=16
$$

so the tag spacing agrees with the 16-bit frame length.

### Why Did the Absolute Tag Offset Change?

The direct bit-stream experiment produced its first tag at offset 8.

The complete QPSK receiver produces the first retained tag at offset 22.

The difference is expected because the complete receiver contains filtering, timing recovery, and startup transients that were absent from the direct-bit experiment.

The absolute stream offset can therefore change.

The important repeated-frame observation is

$$
n_{k+1}-n_k=16
$$

The receiver processing changes latency, while the repeated spacing still reveals the correct frame structure.

## 23.16 Experiment 23.8 Continued: Frame Detection in Noise

We now increase the Channel Model noise voltage while leaving the access-code detector settings unchanged.

The retained comparison uses

```text
Noise Voltage: 0
Noise Voltage: 1.5
Noise Voltage: 2
```

![QPSK frame detection at noise voltages 0, 1.5, and 2](../figures/ch23/ch23_exp08_noise_frame_detection.png)

### Noise Voltage = 0

The constellation contains four compact clusters, and the detected tags are

```text
22
38
54
70
86
102
118
```

Frame synchronization works correctly.

### Noise Voltage = 1.5

The constellation spreads significantly.

The retained tag offsets are

```text
22
54
70
86
102
118
```

The expected tag at 38 is missing.

This is a **missed detection**.

The constellation is still recognizably QPSK, but frame-level synchronization has already begun to fail.

This is an important systems lesson: a receiver can still appear usable at the symbol level while a higher-level detection function is already making mistakes.

### Noise Voltage = 2

The constellation is much more dispersed.

The retained output includes offsets such as

```text
41
54
70
86
102
118
```

The expected periodic sequence is disrupted, and an unexpected detection appears at 41.

At this noise level, symbol and bit errors can destroy genuine access-code matches and can also create accidental bit patterns that resemble the access code.

The exact erroneous offsets depend on the particular noise realization.

The general conclusion is:

> **As bit decisions become unreliable, frame detection can suffer both missed detections and false detections.**

## 23.17 Why Not Simply Increase the Error Tolerance?

Allowing more access-code mismatches can reduce missed detections when the genuine code is corrupted.

But Experiment 23.7 showed the cost.

Greater tolerance also increases the number of unintended bit patterns that can qualify as a match.

There is therefore no free correction.

Useful access-code length, sequence, and tolerated mismatch count depend on the expected channel conditions and on how costly false detections and missed detections are for the system.

## 23.18 Preamble, Access Code, and `frame_start`

These terms are related but not interchangeable.

A **preamble** is a known sequence transmitted to help the receiver detect or synchronize to a frame.

An **access code** is the known binary pattern searched for by the bit-level access-code detector.

In our experiments, the access code is

```text
10110010
```

`frame_start` is different.

It is not transmitted through the channel.

It is a **GNU Radio stream-tag key created inside the receiver** after the access code has been detected.

The transmitter sends known structure. The receiver recognizes that structure and creates metadata describing the detected position.

## 23.19 Physical Meaning of Frame Synchronization

After carrier recovery and timing recovery, a receiver can still be producing an endless stream of symbols or bits.

Frame synchronization gives that stream structure.

The transmitter inserts a known landmark.

The channel distorts the signal.

The receiver recovers symbols or bits and searches for the landmark.

When the detector accepts a match, the receiver establishes a reference position from which the payload can be interpreted.

Frame synchronization therefore converts a continuous stream of decisions into structured communication.

## 23.20 Frame Synchronization Does Not Guarantee Correct Data

Detecting a frame boundary answers one question:

> **Where is the frame?**

It does not prove that every payload bit is correct.

A receiver can recover carrier phase, recover symbol timing, detect the access code, and still make payload bit errors because of noise or other impairments.

This creates another distinction.

| Receiver function | Main question |
|---|---|
| Frame synchronization | Where does the frame begin? |
| Error detection | Was the recovered frame corrupted? |
| Error correction | Can some corrupted information be recovered? |

Practical frames often contain an error-detection field such as a cyclic redundancy check, or CRC.

A CRC gives the receiver a way to test whether the recovered frame is consistent with the transmitted redundancy.

Some systems also use forward error correction, or FEC, which adds structured redundancy so that certain errors can be corrected rather than merely detected.

Those topics belong to the broader subject of channel coding and are beyond the experimental scope of this chapter.

The important point here is narrower:

> **Successful frame synchronization tells the receiver where the data is. It does not guarantee that the data is correct.**

## 23.21 Practical SDR Perspective

Real communication systems often use synchronization sequences chosen specifically for good detection properties rather than arbitrary bit patterns.

Important design considerations can include:

- autocorrelation behaviour;
- cross-correlation with other sequences;
- sequence length;
- false-alarm probability;
- detection probability;
- channel distortion;
- carrier offset;
- timing uncertainty;
- multipath;
- computational complexity.

Sequence families such as Barker sequences, Gold codes, and Zadoff-Chu sequences appear in different communication and ranging systems because synchronization performance depends strongly on sequence design.

We do not develop those families here.

The principle established by our experiments is enough for the current receiver:

> **A receiver can find structure in an unknown stream by searching for a known transmitted pattern.**

## 23.22 GNU Radio Toolbox

Several GNU Radio blocks take on important frame-synchronization roles in this chapter.

| GNU Radio Block | Role in This Chapter |
|---|---|
| Threshold | helps convert a continuous correlation response into a detection state |
| Correlate Access Code - Tag | searches a bit stream for a known binary code and creates a tag |
| Tag Debug | displays selected stream tags and offsets |
| Binary Slicer | converts recovered real-valued I or Q components into binary decisions |
| Interleave | reconstructs the serial bit sequence from I and Q decisions |
| Head | limits a repeating experiment to a finite number of output items |

### Threshold

The Threshold block operates on a continuous-valued input using low and high decision levels.

In the correlation experiment, it helps convert correlation evidence into a detection indication.

This is separate from the access-code mismatch threshold used later.

### Correlate Access Code - Tag

The retained settings are

```text
Access Code: 10110010
Threshold: 0
Tag Name: frame_start
```

For this block, `Threshold` specifies how many access-code bit mismatches may be tolerated.

### Tag Debug

Tag Debug displays stream-tag information in the GNU Radio console.

The retained configuration includes

```text
Name: Access Code Detection
Key Filter: frame_start
Display: On
```

The displayed offset identifies the tagged stream position.

### Binary Slicer

Binary Slicer converts a real-valued input into binary decisions.

In the QPSK receiver, the I and Q components are sliced separately.

### Interleave

Interleave combines the I and Q bit-decision streams in alternating order so that the serial frame bit sequence can be reconstructed.

### Head

The complete experiment uses

```text
Num Items: 128
```

to provide a finite observation interval.

Head does not perform synchronization. It only prevents the repeating source and Tag Debug output from running indefinitely.

## 23.23 Explore Further

The frame-detection experiments support several useful extensions.

1. Keep the transmitted frame unchanged and search for a different access code. Confirm that correct timing and a clean constellation do not help if the receiver is searching for the wrong pattern.

2. Restore the correct access code and increase the tolerated bit-error threshold. Observe the tradeoff between missed detections and accidental matches.

3. Increase the Channel Model noise gradually and identify where the first missed detection appears.

4. Change the payload while keeping the access code fixed. Check whether some payload patterns create more accidental access-code-like matches than others.

5. Increase the Head length and observe a longer sequence of frame tags.

6. Repeat the symbol-level correlation experiment with a shorter and longer preamble while keeping the signal scaling comparable.

7. Compare a low correlation threshold with a high one under the same noisy condition. Record both missed and extra detections rather than judging only the largest peak.

8. Change the preamble sequence while keeping its length fixed. Compare how distinct the correct-alignment correlation peak remains.

## 23.24 What We Learned

Timing synchronization and frame synchronization solve different problems.

Timing recovery determines when to sample each symbol.

Frame synchronization determines where structured data begins in the recovered stream.

A known preamble gives the receiver a recognizable landmark.

Correlation searches for that landmark by combining evidence across several known symbols.

Correlation can remain useful in noise, but sufficiently strong disturbance makes genuine and accidental responses harder to separate.

A correlation detection threshold trades sensitivity against false detections and missed detections.

The useful threshold depends on the actual sequence, scaling, channel, and receiver requirements.

Preamble sequence and length both matter. A shorter sequence reduces overhead but provides less correlation evidence in this experiment.

GNU Radio stream tags attach metadata to positions in a stream.

`Correlate Access Code - Tag` can detect a known binary pattern and create a `frame_start` tag.

Its threshold is a tolerated bit-mismatch count, not a correlation-magnitude threshold.

With access-code threshold 0, the one-bit-corrupted code was rejected.

With threshold 1, that one-bit mismatch was accepted in the retained experiment.

The direct repeated 16-bit frame produced tags separated by 16 items.

In the direct-bit experiment, the tag appeared after the detected access code.

Filtering, synchronization, and startup transients changed the absolute tag offsets in the complete QPSK receiver, while the repeated 16-item spacing remained.

The complete receiver recovered QPSK symbols, converted them into bits, detected the access code, and marked frame boundaries.

Increasing noise caused missed detections, and stronger noise also produced an unintended detection in the retained run.

Finally, frame synchronization identifies structure. It does not guarantee that the payload itself is error-free.

The receiver now understands more than waveform timing or constellation geometry. It has begun to recognize the organization of the transmitted information.

## 23.25 Connecting to the Next Chapter

The previous chapters developed the major functions of a single-carrier receiver one at a time.

Pulse shaping and matched filtering established the waveform.

The wireless channel introduced impairments.

Equalization addressed structured multipath distortion.

Carrier synchronization recovered phase and frequency.

Timing synchronization recovered the symbol-sampling instants.

This chapter identified frame boundaries.

These functions have been easier to understand separately, but a practical receiver must make them work together on the same received signal.

That raises the next question:

> **What happens when all of these receiver functions are combined into one end-to-end digital communication system?**

Chapter 24 answers that question.

We will integrate the receiver stages, recover actual transmitted information, and then deliberately disable important functions so that their failure signatures can be observed directly.

That leads to **Chapter 24: Building a Complete Single-Carrier Digital Receiver**.