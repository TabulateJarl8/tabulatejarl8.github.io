---
title: "More Randfacts Testing"
date: 2026-02-04T15:57:04-05:00
draft: true
tags: ["randfacts", "rust", "python"]
---

I've covered this topic before in a [previous post]({{< ref "blog/randfacts_checkduplicates" >}}), but I've recently gotten back into improving [randfacts](https://github.com/TabulateJarl8/randfacts) after switching it from poetry to uv. I'm really not sure why, but after improving the unit tests, I had an urge to see how much faster I could make the checkduplicates test.

As a brief historical overview, the checkduplicates test finds any facts that are duplicated in the dataset. This sounds easy at first, but I originally wanted it to work for facts with different phrasings but the same meaning. From this, I stumbled across the [Levenshtein Distance](https://en.wikipedia.org/wiki/Levenshtein_distance) algorithm. As of the time I'm writing this, there have been four major iterations of this test, listed below:

- **Python**: I implemented this first version with the [`fuzzywuzzy`](https://github.com/seatgeek/fuzzywuzzy) module, but this was pretty slow because it's all Python.
- **Python/C++**: After a few years of using this, I rewrote it to use [`rapidfuzz`](https://github.com/rapidfuzz/RapidFuzz), which is a much faster C++ based implementation of Levenshtein. This worked decently well for a while, but I again got tired of the slowdown.
- **Rust #1**: The third time around I had recently learned Rust and wanted to try that out, so I did. However, if I remember correctly it was actually originally slower than the C++ version, probably because there's not much speedup you can do when using a recursive algorithm. This is when I discovered [Wagner-Fischer](https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm), which is a dynamic programming approach to Levenshtein distance. My initial implementation was already drastically faster, and I go over the particular optimizations that I did in [my other blog post]({{< ref "blog/randfacts_checkduplicates" >}}).
- **Rust #2**: This is my fourth and most decent development, and on my personal laptop I've increased the speed from ~12.7s to ~90ms, which is about a 197% increase in speed.

## New Algorithm

There were five main optimizations that I made. Firstly, I completely switched algorithms. I found a formula called the [Dice-S&#248;rensen coefficient](https://en.wikipedia.org/wiki/Dice-S%C3%B8rensen_coefficient) which is used for calculating the similarity between two samples. It's defined as follows:

$$DSC=\frac{2\left|X\cap Y\right|}{\left|X\right| + \left|Y\right|}$$

Between two sets, it computes the ratio of twice the number of items in their intersection to the sum of their lengths. For example, if you have two sets of `{i, love, programming}` and `{programming, is, what, i, love}`, their intersection is `{i, programming, love}` of length three, giving us:

$$\frac{2\cdot 3}{3+5}=0.75$$

Once we establish a similarity threshold that works best (turned out to be `0.70` for me), then we can just use this to compare similarity without having to do recursion or complex matrix edit distance calculations.

- stop words
- hashing/tokenizing for integer comparison
- linear intersect calculation with sorting
- length diff ratio
