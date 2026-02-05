---
title: "More Randfacts Testing"
date: 2026-02-04T15:57:04-05:00
draft: false
tags: ["randfacts", "rust", "python", "math"]
---

I've covered this topic before in a [previous post]({{< ref "blog/randfacts_checkduplicates" >}}), but I've recently gotten back into improving [randfacts](https://github.com/TabulateJarl8/randfacts) after switching it from poetry to uv. I'm really not sure why, but after improving the unit tests, I had an urge to see how much faster I could make the checkduplicates test.

As a brief historical overview, the checkduplicates test finds any facts that are duplicated in the dataset. This sounds easy at first, but I originally wanted it to work for facts with different phrasings but the same meaning. From this, I stumbled across the [Levenshtein Distance](https://en.wikipedia.org/wiki/Levenshtein_distance) algorithm. As of the time I'm writing this, there have been four major iterations of this test, listed below:

- **Python**: I implemented this first version with the [`fuzzywuzzy`](https://github.com/seatgeek/fuzzywuzzy) module, but this was pretty slow because it's all Python.
- **Python/C++**: After a few years of using this, I rewrote it to use [`rapidfuzz`](https://github.com/rapidfuzz/RapidFuzz), which is a much faster C++ based implementation of Levenshtein. This worked decently well for a while, but I again got tired of the slowdown.
- **Rust #1**: The third time around I had recently learned Rust and wanted to try that out, so I did. However, if I remember correctly it was actually originally slower than the C++ version, probably because there's not much speedup you can do when using a recursive algorithm. This is when I discovered [Wagner-Fischer](https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm), which is a dynamic programming approach to Levenshtein distance. My initial implementation was already drastically faster, and I go over the particular optimizations that I did in [my other blog post]({{< ref "blog/randfacts_checkduplicates" >}}).
- **Rust #2**: This is my fourth and most recent development, and on my personal desktop I've increased the speed from ~17.10s to ~165.52ms, which is about a 196% increase in speed, and this ratio seems to be similar on my laptop.

## Dice-S&#248;rensen

There were a few main optimizations that I made. Firstly, I completely switched algorithms. I found a formula called the [Dice-S&#248;rensen coefficient](https://en.wikipedia.org/wiki/Dice-S%C3%B8rensen_coefficient) which is used for calculating the similarity between two samples. It's defined as follows:

$$DSC=\frac{2\left|X\cap Y\right|}{\left|X\right| + \left|Y\right|}$$

Between two sets, it computes the ratio of twice the number of items in their intersection to the sum of their lengths. For example, if you have two sets of `{i, love, programming}` and `{programming, is, what, i, love}`, their intersection is `{i, programming, love}` of length three, giving us:

$$\frac{2\cdot 3}{3+5}=0.75$$

Once we establish a similarity threshold that works best (turned out to be `0.70` for me), then we can just use this to compare similarity without having to do recursion or complex matrix edit distance calculations.

The actual base algorithm itself ended up being fairly simple, as it is provided a sorted array of `u64`s (we'll discuss why/how `u64` in a moment), so we're able to calculate the intersection in one linear pass:

```rs
#[inline(always)]
fn dice_sorensen_sorted(set1: &[u64], set2: &[u64]) -> f64 {
    let len1 = set1.len();
    let len2 = set2.len();

    let mut intersect = 0;
    let mut i = 0;
    let mut j = 0;

    // calculate the intersection of the two sorted vecs of tokens:
    while i < len1 && j < len2 {
        let x = set1[i];
        let y = set2[j];

        if x == y {
            intersect += 1;
            i += 1;
            j += 1;
        } else if x < y {
            i += 1;
        } else {
            j += 1;
        }
    }

    // DSC = (2|X intersect Y|)/(|X| + |Y|)
    (2.0 * intersect as f64) / ((len1 + len2) as f64) * 100.0
}
```

## Hashing/Tokenizing

I mentioned in the last section that the algorithm is provided a list (set) of `u64`s. This is another reason why it can run so must faster. Since integer comparisons are so much quicker compared to full string comparisons, why not just tokenize the string (which we were already doing) and hash each word? This allows us to just store a vector of each hash and check if numbers are equal (\(O(1)\)) instead of checking if strings are equal (\(O(n)\)). In this same normalization pass, I also added "stop word" removal. This is a term from natural language processing that describes words such as "i", "was", "a", "or", "at", or anything else like that that doesn't really contribute "meaning" to a sample. By removing all of these words from the set of tokens, we can construct a set that more closely represents the core "subject" of the fact.

## Length Difference Ratio Termination

The other huge optimization that this approach allowed us to do is the fact that we're now able to calculate the mathematical limit at which two facts could not possibly be considered similar if their lengths differ by \(x\) amount. This was a little bit complex to do but I'll try to annotate the math here:

We already know the following formula for calculating the coefficient:

$$DSC=\frac{2\left|X\cap Y\right|}{\left|X\right| + \left|Y\right|}$$

Since this is a ratio against the sum of the lengths of the sets, we should be able to derive at what length of \(Y\) (given \(|X|\)) will the ratio not surpass the set threshold. We know that the list is sorted from least to greatest by length, and from that, we know that as we traverse from start to finish (comparing every \(X\) against everything after it), \(|X| \leq |Y|\). This tells us that the maximum possible intersection length between the two sets is \(|X|\). From this, we can construct an inequality representing this maximum case:

$$
\begin{aligned}
\frac{2\cdot |X|}{|X| + |Y|} & \geq \text{threshold} \\
2\cdot |X| & \geq \text{threshold}\cdot\left(|X|+|Y|\right) \\
2\cdot |X| & \geq \text{threshold}\cdot|X| + \text{threshold}\cdot|Y| \\
2\cdot |X| - \text{threshold}\cdot |X| & \geq \text{threshold}\cdot|Y| \\
|X|\left(2 - \text{threshold}\right) & \geq \text{threshold}\cdot|Y| \\
\frac{|X|\left(2 - \text{threshold}\right)}{\text{threshold}} & \geq |Y| \\
\end{aligned}
$$

In my final Rust implementation, I was able to use this formula to break off processing once we've reached this limit, shown here:

```rust {hl_lines=["2-5","14-15","18-19","21-25"]}
// ...
// this would take 70.0 and make it into 0.7
let fractional_ratio = SIMILARITY_THRESHOLD / 100.0;
// use the formula we just calculated
let length_diff_ratio = (2.0 - fractional_ratio) / fractional_ratio;

// Process facts in parallel
facts
    .par_iter()
    .enumerate()
    .progress_with(pb)
    .flat_map(|(i, f1)| {
        let mut matches = vec![];
        // here is the length of X, or |X|
        let len1 = f1.token_hashes.len();

        for f2 in &facts[i + 1..] {
            // here is the length of the fact we're comparing against, or |Y|
            let len2 = f2.token_hashes.len();

            // if lengths are too different to possibly be the same, don't try any of the
            // remaining facts
            if (len2 as f64) > (len1 as f64) * length_diff_ratio {
                break;
            }

            let ratio = dice_sorensen_sorted(&f1.token_hashes, &f2.token_hashes);
            if ratio > SIMILARITY_THRESHOLD {
                matches.push((f1.original.clone(), f2.original.clone(), ratio));
            }
        }

        matches
    })
    .collect()
```

## Speed Comparison and Conclusion

|                               | Python                        | C++/Python                 | Wagner-Fischer Rust        | Dice-S&#248;rensen Rust    |
| ----------------------------- | ----------------------------- | -------------------------- | -------------------------- | -------------------------- |
| Runtime (seconds)             | 419.22 seconds (6m59s)        | 68.34 seconds (1m08s)      | 17.1 seconds               | 0.165 seconds              |
| Approximate Iterations/second | ~60,000-70,000                | ~400,000                   | ~1,550,000                 | ~50,000[^1]                |
| Source Code Permalink         | [Link][python test permalink] | [Link][c++ test permalink] | [Link][old rust permalink] | [Link][new rust permalink] |

I found this comparison kind of interesting because the new Rust version is so fast, but it by far has the least number of iterations/second. While this may seem like it'd be slower at first, the speed is due to the test having far less comparisons to do than any of the other implementations because of the new ability to only compare facts that could possibly be similar. I've actually found this new implementation to have picked up duplicate facts that the Levenshtein and Wagner-Fischer implementations missed, while also having almost no false positives. Overall, this has been a very worthwhile investment and I had a lot of fun learning about this new algorithm.

[python test permalink]: https://github.com/TabulateJarl8/randfacts/blob/021bd555f1b1931343acc7dfe7e0746af9003afe/tests/checkduplicates.py
[c++ test permalink]: https://github.com/TabulateJarl8/randfacts/blob/de5f66ff1eb4545de82c14c62405fd33c7cd07e7/tests/checkduplicates.py
[old rust permalink]: https://github.com/TabulateJarl8/randfacts/blob/4c56325c1c8a529c12cca2eebfdc2a2eac6307d0/tests/checkduplicates/src/main.rs
[new rust permalink]: https://github.com/TabulateJarl8/randfacts/blob/94029d363bb7a3a5e8e15c70a8eec16864f5f7aa/tests/checkduplicates/src/main.rs

[^1]: This is kind of difficult to measure because of how fast it runs, but manually calculating it gives around this. The quick flash of the progress bar also shows something around this
