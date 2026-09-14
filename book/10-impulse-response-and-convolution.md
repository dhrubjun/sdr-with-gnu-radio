# Chapter 10: Impulse Response and Convolution

In the previous chapter, we used filters to keep some frequencies and suppress others. We changed cutoff frequencies, transition widths, filter taps, and sample rates, and we watched the spectrum change.

That gave us a useful frequency-domain view of filtering. But one question is still open:

> What is an FIR filter actually doing to the individual samples?

To answer it, we will approach filtering from the time domain. We will begin with one of the simplest discrete-time signals, an impulse, and use it to reveal the behaviour of a small FIR filter.

From there, we will delay the impulse, scale it, use several impulses, allow their responses to overlap, and finally replace the obvious impulses with an ordinary short sequence.

By the time we reach the convolution equation, the equation will describe a process we have already seen happen in GNU Radio.

## 10.1 From a Filter to a System

A system takes an input and produces an output. For a discrete-time system, we normally write the input as $x[n]$ and the output as $y[n]$.

An FIR filter is one example of such a system. Its behaviour is controlled by a finite set of coefficients called **taps**.

In Chapter 9, we mainly asked which frequencies those taps allowed through and which frequencies they attenuated. Here we ask a different question:

> If we know the taps, how are the output samples actually formed?

The answer begins with the impulse.

## 10.2 The Discrete-Time Impulse and Impulse Response

The discrete-time impulse is defined by

$$
\delta[n]=\begin{cases}1,&n=0\\0,&n\neq0\end{cases}
$$

As a sequence, it begins

$$
[1,\;0,\;0,\;0,\;0,\ldots]
$$

The impulse may look almost trivial, but it is extremely useful. If we apply an impulse to a system and observe the output, that output is called the **impulse response** of the system.

We normally denote the impulse response by

$$
h[n]
$$

For an FIR filter configured with the taps

$$
[1,\;0.5,\;0.25]
$$

we expect an input impulse to reveal those same values at the output. Our first experiment checks that directly.

## 10.3 Experiment 1: Observing an FIR Impulse Response

We use a Vector Source to generate one impulse followed by zeros, and pass the same stream to a Time Sink and a Decimating FIR Filter. A second Time Sink observes the filter output.

![GNU Radio flowgraph for observing the impulse response of an FIR filter](../figures/ch10/ch10-exp1-impulse-response-flowgraph.png)

Use the following main settings:

```text
samp_rate = 1k

Vector Source
Output Type: Float
Vector: (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
Tags: []
Repeat: Yes
Vector Length: 1

Decimating FIR Filter
Type: Float -> Float (Real Taps)
Decimation: 1
Taps: (1, 0.5, 0.25)
Sample Delay: 0

QT GUI Time Sink
Number of Points: 32
Sample Rate: samp_rate
Autoscale: Yes
```

With

$$
f_s=1000\text{ samples/s}
$$

the sample interval is

$$
T_s=\frac{1}{f_s}=1\text{ ms}
$$

Visible sample markers are useful here because we are interested in individual discrete-time values.

The Vector Source repeats the 16-sample sequence so that the impulse appears continuously in the display. Conceptually, however, the impulse response is the response to one impulse. The impulses are separated by enough zeros that the three-sample response finishes before the next impulse arrives.

Our input is

$$
x[n]=\delta[n]
$$

and the filter taps are

$$
h[n]=[1,\;0.5,\;0.25]
$$

If the taps describe the impulse response, the filter output should contain those three values.

![Impulse response of the FIR filter](../figures/ch10/ch10-exp1-impulse-response.png)

That is exactly what we observe. The non-zero output samples are

$$
1,\quad0.5,\quad0.25
$$

so for this causal FIR filter,

$$
\boxed{h[n]=[1,\;0.5,\;0.25]}
$$

The experiment gives us our first central result:

$$
\boxed{\text{FIR taps}=\text{impulse response}}
$$

## 10.4 Delay, Scaling, and Superposition

The next experiments keep the same FIR filter and change only the input. Together they reveal why impulse response is so useful for linear time-invariant systems.

### Experiment 2: Delay the Impulse

Move the impulse four samples to the right:

```text
(0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
```

The input is now

$$
x[n]=\delta[n-4]
$$

![Response to a delayed impulse](../figures/ch10/ch10-exp2-delayed-impulse.png)

The output has exactly the same shape as before, but it also begins four samples later:

$$
\delta[n-4]\longrightarrow h[n-4]
$$

The filter has not changed its behaviour simply because the impulse arrived later. This is the basic idea of **time invariance**.

### Experiment 3: Scale the Impulse

Keep the impulse at the delayed position, but change its amplitude from 1 to 2:

```text
(0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
```

Now

$$
x[n]=2\delta[n-4]
$$

If a unit impulse produces $h[n-4]$, doubling the impulse should double the complete response:

$$
2\delta[n-4]\longrightarrow2h[n-4]
$$

Since

$$
h[n]=[1,\;0.5,\;0.25]
$$

we expect

$$
2h[n]=[2,\;1,\;0.5]
$$

![Response to a scaled impulse](../figures/ch10/ch10-exp3-scaled-impulse.png)

GNU Radio gives exactly those values. Scaling the input scales the output by the same factor. This is one part of **linearity**.

### Experiment 4: Use Two Separate Impulses

Now use

```text
(1, 0, 0, 0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
```

The input is

$$
x[n]=\delta[n]+0.5\delta[n-4]
$$

The first impulse creates

$$
h[n]=[1,\;0.5,\;0.25]
$$

The second creates a half-sized copy four samples later:

$$
0.5h[n-4]
$$

so

$$
y[n]=h[n]+0.5h[n-4]
$$

![Response to two impulses](../figures/ch10/ch10-exp4-two-impulses.png)

Over one period, the samples are

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| $x[n]$ | 1 | 0 | 0 | 0 | 0.5 | 0 | 0 | 0 |
| $y[n]$ | 1 | 0.5 | 0.25 | 0 | 0.5 | 0.25 | 0.125 | 0 |

Each non-zero input sample has produced its own shifted and scaled copy of the impulse response.

### Experiment 5: Let the Responses Overlap

Move the second impulse closer:

```text
(1, 0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
```

Now

$$
x[n]=\delta[n]+0.5\delta[n-2]
$$

The first impulse contributes

$$
[1,\;0.5,\;0.25]
$$

and the second contributes

$$
[0.5,\;0.25,\;0.125]
$$

starting at $n=2$.

| $n$ | 0 | 1 | 2 | 3 | 4 |
|---:|---:|---:|---:|---:|---:|
| From $\delta[n]$ | 1 | 0.5 | 0.25 | 0 | 0 |
| From $0.5\delta[n-2]$ | 0 | 0 | 0.5 | 0.25 | 0.125 |
| **Total $y[n]$** | **1** | **0.5** | **0.75** | **0.25** | **0.125** |

At $n=2$, both responses contribute:

$$
y[2]=0.25+0.5=0.75
$$

Therefore,

$$
y[n]=[1,\;0.5,\;0.75,\;0.25,\;0.125]
$$

![Overlapping impulse responses](../figures/ch10/ch10-exp5-overlapping-impulse-responses.png)

The value 0.75 did not appear in either individual response. It appears because overlapping contributions add.

We now have almost the complete intuition behind convolution:

> Each input sample creates a shifted and scaled copy of the impulse response, and overlapping copies add.

## 10.5 Any Sequence Can Be Built from Impulses

The previous inputs were deliberately written as obvious impulses. An ordinary sequence follows exactly the same idea.

Consider

$$
x[n]=[1,\;2,\;1]
$$

We can write it as

$$
x[n]=\delta[n]+2\delta[n-1]+\delta[n-2]
$$

The first sample is a unit impulse at $n=0$. The second is an impulse of amplitude 2 at $n=1$. The third is a unit impulse at $n=2$.

More generally, a discrete-time sequence can be expressed as

$$
x[n]=\sum_{k=-\infty}^{\infty}x[k]\delta[n-k]
$$

This representation is the bridge between the impulse experiments and convolution.

## 10.6 Experiment 6: Convolution of Two Short Sequences

Keep the FIR impulse response

$$
h[n]=[1,\;0.5,\;0.25]
$$

and set the Vector Source to

```text
(1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
```

The non-zero input is

$$
x[n]=[1,\;2,\;1]
$$

Because the repeated vector contains enough trailing zeros, the filter response to one copy finishes before the next copy begins. This lets us compare the visible samples directly with the ordinary finite-length linear convolution of $x[n]$ and $h[n]$.

The first input sample contributes

$$
1h[n]=[1,\;0.5,\;0.25]
$$

starting at $n=0$.

The second contributes

$$
2h[n]=[2,\;1,\;0.5]
$$

starting at $n=1$.

The third contributes

$$
1h[n]=[1,\;0.5,\;0.25]
$$

starting at $n=2$.

Aligning the contributions gives

| $n$ | 0 | 1 | 2 | 3 | 4 |
|---:|---:|---:|---:|---:|---:|
| From $x[0]=1$ | 1 | 0.5 | 0.25 | 0 | 0 |
| From $x[1]=2$ | 0 | 2 | 1 | 0.5 | 0 |
| From $x[2]=1$ | 0 | 0 | 1 | 0.5 | 0.25 |
| **Total $y[n]$** | **1** | **2.5** | **2.25** | **1** | **0.25** |

Therefore,

$$
\boxed{y[n]=[1,\;2.5,\;2.25,\;1,\;0.25]}
$$

![Convolution of two simple sequences](../figures/ch10/ch10-exp6-convolution-simple-sequences.png)

GNU Radio produces the same sequence.

We have just performed **convolution**.

For every input sample, we took a copy of the impulse response, scaled it by the input value, shifted it to the sample position, and added all overlapping contributions.

We write this compactly as

$$
\boxed{y[n]=x[n]*h[n]}
$$

where $*$ denotes convolution.

## 10.7 The Convolution Equation

For discrete-time signals, convolution is written as

$$
\boxed{y[n]=\sum_{k=-\infty}^{\infty}x[k]h[n-k]}
$$

The equation describes exactly the process we just carried out.

The variable $n$ identifies the output sample being calculated. The variable $k$ runs through the input samples that can contribute to that output.

For our example,

$$
x[n]=[1,\;2,\;1]
$$

and

$$
h[n]=[1,\;0.5,\;0.25]
$$

### Calculating $y[0]$

$$
y[0]=x[0]h[0]+x[1]h[-1]+x[2]h[-2]
$$

Since the causal impulse response is zero for negative indices,

$$
y[0]=(1)(1)+(2)(0)+(1)(0)=1
$$

### Calculating $y[1]$

$$
y[1]=x[0]h[1]+x[1]h[0]+x[2]h[-1]
$$

so

$$
y[1]=(1)(0.5)+(2)(1)+(1)(0)=2.5
$$

### Calculating $y[2]$

$$
y[2]=x[0]h[2]+x[1]h[1]+x[2]h[0]
$$

which gives

$$
y[2]=(1)(0.25)+(2)(0.5)+(1)(1)=2.25
$$

### Calculating $y[3]$ and $y[4]$

$$
y[3]=x[0]h[3]+x[1]h[2]+x[2]h[1]=(1)(0)+(2)(0.25)+(1)(0.5)=1
$$

$$
y[4]=x[0]h[4]+x[1]h[3]+x[2]h[2]=(1)(0)+(2)(0)+(1)(0.25)=0.25
$$

Putting the samples together gives the same output as before:

$$
\boxed{y[n]=[1,\;2.5,\;2.25,\;1,\;0.25]}
$$

The equation has not introduced a new operation. It is simply a compact mathematical description of the shifted, scaled, and added impulse responses we already observed.

### Why Does $h[n-k]$ Appear Reversed?

For a fixed output index $n$, increasing $k$ makes the argument $n-k$ decrease.

For example, while calculating $y[2]$,

$$
h[2-k]\rightarrow h[2],\;h[1],\;h[0]
$$

as $k$ moves through 0, 1, and 2.

This is where the familiar **flip-and-slide** interpretation comes from.

For understanding an FIR filter, however, the impulse-response viewpoint is often more intuitive: every input sample launches a shifted and scaled copy of $h[n]$, and the copies add.

Both viewpoints describe the same convolution.

### Length of a Finite Convolution

If two finite sequences have lengths $L_x$ and $L_h$, their full linear convolution has length

$$
\boxed{L_y=L_x+L_h-1}
$$

Here,

$$
L_x=3,\qquad L_h=3
$$

so

$$
L_y=3+3-1=5
$$

which matches our result.

## 10.8 FIR Filtering Is Convolution

Suppose an FIR filter has $M$ taps:

$$
h[0],h[1],\ldots,h[M-1]
$$

A causal FIR filter can calculate each output sample as

$$
y[n]=\sum_{k=0}^{M-1}h[k]x[n-k]
$$

This is the finite FIR form of convolution.

The GNU Radio Decimating FIR Filter therefore applies the supplied taps as FIR coefficients while processing the incoming stream. With `Decimation = 1`, no sample-rate reduction occurs, so the block behaves as an ordinary FIR filter.

The connection is now direct:

$$
\boxed{\text{FIR taps}=h[n]}
$$

and

$$
\boxed{\text{FIR output}=x[n]*h[n]}
$$

## 10.9 Experiments 7 and 8: Changing the Impulse Response

So far we kept the same three taps. Now we keep the input fixed and change the system itself.

### Experiment 7: Change the Taps

Keep

$$
x[n]=[1,\;2,\;1]
$$

but change the FIR taps to

```text
(1, -1)
```

The new impulse response is

$$
h[n]=[1,\;-1]
$$

The shifted contributions are

| $n$ | 0 | 1 | 2 | 3 |
|---:|---:|---:|---:|---:|
| From $x[0]=1$ | 1 | -1 | 0 | 0 |
| From $x[1]=2$ | 0 | 2 | -2 | 0 |
| From $x[2]=1$ | 0 | 0 | 1 | -1 |
| **Total $y[n]$** | **1** | **1** | **-1** | **-1** |

Therefore,

$$
\boxed{y[n]=[1,\;1,\;-1,\;-1]}
$$

![Changing the impulse response](../figures/ch10/ch10-exp7-change-impulse-response.png)

The input did not change. Only $h[n]$ changed, and the output changed with it. Changing the taps means changing the system.

### Experiment 8: Reverse the Taps

Return to

$$
h[n]=[1,\;0.5,\;0.25]
$$

and then manually enter the reversed sequence

```text
(0.25, 0.5, 1)
```

The new impulse response is

$$
h_r[n]=[0.25,\;0.5,\;1]
$$

For the same input $x[n]=[1,2,1]$, the contributions become

| $n$ | 0 | 1 | 2 | 3 | 4 |
|---:|---:|---:|---:|---:|---:|
| From $x[0]=1$ | 0.25 | 0.5 | 1 | 0 | 0 |
| From $x[1]=2$ | 0 | 0.5 | 1 | 2 | 0 |
| From $x[2]=1$ | 0 | 0 | 0.25 | 0.5 | 1 |
| **Total $y[n]$** | **0.25** | **1** | **2.25** | **2.5** | **1** |

Thus,

$$
\boxed{y[n]=[0.25,\;1,\;2.25,\;2.5,\;1]}
$$

![Effect of reversing the FIR taps](../figures/ch10/ch10-exp8-reversed-fir-taps.png)

This experiment resolves a common source of confusion. The term $h[n-k]$ in the convolution equation does **not** mean that we should reverse the desired taps before entering them into GNU Radio.

If the intended impulse response is

$$
[1,\;0.5,\;0.25]
$$

those are the taps we enter. Supplying

$$
[0.25,\;0.5,\;1]
$$

defines a different impulse response and therefore a different filter.

## 10.10 Linearity, Time Invariance, and Why the Impulse Response Is Enough

The experiments have quietly demonstrated the two properties behind an **LTI system**.

A system is **time invariant** if delaying the input delays the output by the same amount without changing its shape. Experiment 2 showed

$$
\delta[n]\longrightarrow h[n]
$$

and

$$
\delta[n-4]\longrightarrow h[n-4]
$$

A system is **linear** if scaling and adding inputs produces the same scaling and addition in the outputs. Experiments 3, 4, and 5 demonstrated this behaviour with scaled and multiple impulses.

These two properties explain why the impulse response is so powerful.

Any discrete-time input can be written as a sum of shifted and scaled impulses:

$$
x[n]=\sum_{k=-\infty}^{\infty}x[k]\delta[n-k]
$$

Time invariance tells us that the response to $\delta[n-k]$ is $h[n-k]$. Linearity tells us that the response can be scaled by $x[k]$ and that all contributions can be added.

Therefore,

$$
y[n]=\sum_{k=-\infty}^{\infty}x[k]h[n-k]
$$

which is convolution.

For an LTI system, knowing $h[n]$ is enough to predict the response to any input for which the convolution is defined.

## 10.11 Connecting Time-Domain and Frequency-Domain Filtering

Chapter 9 and this chapter have examined the same FIR filter from two complementary viewpoints.

In the time domain,

$$
\boxed{y[n]=x[n]*h[n]}
$$

Filtering appears as convolution.

In the frequency domain, the corresponding relationship is

$$
\boxed{Y(e^{j\omega})=X(e^{j\omega})H(e^{j\omega})}
$$

or, when using a generic frequency variable,

$$
Y(f)=X(f)H(f)
$$

The impulse response $h[n]$ and frequency response $H(e^{j\omega})$ are Fourier-transform pairs.

So the taps we used in the time-domain calculations and the filter shape we observed in Chapter 9 are two descriptions of the same FIR system.

This is a central DSP connection:

> Convolution in time corresponds to multiplication in frequency.

## 10.12 GNU Radio Toolbox

This chapter relied on only a few blocks, but used them in a way that exposed the sample-by-sample behaviour of an FIR filter.

| GNU Radio block | Role in this chapter |
|---|---|
| Vector Source | Generates short, known sequences such as impulses and hand-verifiable test vectors |
| Decimating FIR Filter | Applies the FIR taps; with decimation set to 1, no sample-rate reduction occurs |
| QT GUI Time Sink | Displays the input and output sample sequences |
| Variable | Defines shared values such as `samp_rate = 1k` |

For the Vector Source, `Vector Length = 1` produces an ordinary scalar stream, while `Repeat = Yes` repeats the supplied sequence. This is useful for continuously displaying short experiments.

For the Decimating FIR Filter, the **Taps** field contains the FIR coefficients. With `Decimation = 1`, the output sample rate is unchanged.

## 10.13 Explore Further

The same small flowgraph can answer several useful questions.

Try changing the taps to

```text
(0.5, 0.5)
```

and predict the response to an impulse before running the flowgraph. Then try a difference-like filter such as

```text
(1, -1)
```

with a slowly changing input sequence and observe which parts of the input become emphasized.

It is also useful to move two non-zero input samples closer together and predict exactly where their impulse-response copies will overlap.

Finally, shorten the repeating Vector Source period until one filter response begins to overlap the next repeated input period. This demonstrates why the long run of zeros in our main experiments was important when comparing the streaming GNU Radio output with a single finite linear-convolution calculation.

## 10.14 What We Learned

We began with one impulse and used it to expose the behaviour of a small FIR filter.

An impulse reveals the system's impulse response:

$$
\delta[n]\longrightarrow h[n]
$$

For the FIR filters used here, the taps are the impulse-response samples.

A delayed impulse produces a delayed response:

$$
\delta[n-k]\longrightarrow h[n-k]
$$

A scaled impulse produces a scaled response:

$$
A\delta[n-k]\longrightarrow Ah[n-k]
$$

Multiple input samples create multiple shifted and scaled copies of the impulse response. When those copies overlap, their contributions add.

An arbitrary discrete-time sequence can be represented as shifted and scaled impulses:

$$
x[n]=\sum_{k=-\infty}^{\infty}x[k]\delta[n-k]
$$

For an LTI system, this leads directly to convolution:

$$
\boxed{y[n]=x[n]*h[n]}
$$

or

$$
\boxed{y[n]=\sum_{k=-\infty}^{\infty}x[k]h[n-k]}
$$

For finite sequences of lengths $L_x$ and $L_h$, the full linear-convolution length is

$$
L_y=L_x+L_h-1
$$

We also saw that reversing the tap list manually does not implement the same filter in another way. It defines a different impulse response and therefore a different system.

Most importantly, the FIR filtering we used in Chapter 9 now has a clear sample-by-sample interpretation. Filtering is not a mysterious block operation. It is convolution with the filter's impulse response.

## 10.15 Connecting to the Next Chapter

Convolution answers the question

> What does this system do to the input signal?

The next chapter asks a different but closely related question:

> Does a known signal appear somewhere inside what we received?

A radar receiver may search for a delayed echo of a transmitted pulse. A digital receiver may search for a known preamble. A receiver may need to find a weak known pattern inside noise.

To solve that problem, we will reuse many of the ideas developed here, especially shifting, multiplying, summing, and comparing known signal shapes.

That leads to **Chapter 11: Correlation, Matched Filtering and Signal Detection**.
