# Chapter 1: What Is Software Defined Radio?

## 1.1 What is a radio?

Before trying to understand Software Defined Radio, let's first
think about what an ordinary radio actually does.

## 1.2 Traditional radio

A traditional radio uses electronic circuits to perform operations
such as:

- filtering
- amplification
- mixing
- modulation
- demodulation

## 1.3 Software Defined Radio

In an SDR, many of these operations are performed in software.

### A simple SDR chain

A basic receiver can be represented as:

Antenna → RF Front End → ADC → Digital Processing → Information

## 1.4 A little mathematics

A sinusoidal signal can be written as

$$
x(t)=A\cos(2\pi ft+\phi)
$$

where:

- $A$ is amplitude
- $f$ is frequency
- $\phi$ is phase

## 1.5 Our first GNU Radio experiment

In this experiment, we will generate our first signal using GNU Radio.