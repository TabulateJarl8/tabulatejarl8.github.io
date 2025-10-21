---
title: "Rewriting the randfacts duplicate facts test"
date: 2024-11-18T14:44:19-05:00
draft: false
tags: ["randfacts", "rust", "python"]
---

Recently, I was working on a Python web backend project for work, and I noticed something strange with the LSP I was using, Pyright. For some reason, it couldn't automatically detect and import modules that I referenced. This seemed like a pretty standard and basic feature, so after a quick search, I stumbled upon [microsoft/pyright#4263](https://github.com/microsoft/pyright/issues/4263). Someone posted an issue asking Microsoft about why this feature wasn't available in Pyright, and they responded with this:

> This is a language service feature that is included in pylance, Microsoft's premium Python language server for VS Code. We don't have plans to port it to pyright. If you want this functionality, please switch to pylance.

This was pretty annoying, as I have switched to Neovim as my primary editor, and I didn't want to switch back to VSCode. Fortunately, I learned about basedpyright in the same issue, and the author commented that they had pushed an update to the LSP which added this feature. Along with this, it also seemed to give more warnings about typing issues in the code, so I started going through some of my projects and transitioning them to be fully typed. Eventually, I got to my randfacts Python module and this is where the story really begins.

## Some Background

Randfacts is a Python module that I created with a very simple purpose, which is to provide a developer with an easy-to-use interface to a database of random facts. I had made this for a Discord bot, as nothing else existed at the time, and I wasn't expecting it to actually be anything. At the same time, I was also starting to learn about publishing PyPI modules, so I figured I'd throw it up on there to learn how the whole publishing process worked. After a while, however, I noticed that the downloads started going up a lot more than I expected, so I started maintaining the project some more, and I eventually got to where I am today. At the time of writing this, the module has about 1.2 million downloads, which isn't a ton compared to some other modules, but it's pretty cool to me.

## The checkduplicates test

After a while of maintaining the module, I noticed a problem. Since the facts were being scraped off of the web, I inevitably ended up with some duplicates. To address this, I wrote a test in Python that would go through all of the facts and use the Levenshtein distance algorithm to compute the similarity between the two strings. On top of Levenshtein distance, I used a token sort ratio preprocessor, which tokenizes each string by converting it to lowercase and removing any punctuation because this usually gave more accurate results. With this method of string similarity checking, I could accurately match strings with the same meaning but different wording, such as "Jupiter is the biggest planet in the solar system" and "The biggest planet in the solar system is Jupiter". This test worked fine for a while, but every time I added another fact, it needed to be compared with every fact before it. With the current list of over 7,000 facts, the test needs to compute about 27.5 million string comparisons. The Python version of the test could compute about 400k-500k string comparisons per second, which ended up taking a bit over a minute just to check for duplicate facts.

In comes Rust. When I was first learning Rust, I started to rewrite this test, as I thought using a compiled language would at least provide a small benefit in computation time, but this doesn't address the underlying problem of why the test is so slow. When I came back to randfacts with my new LSP, I rediscovered this half-finished implementation and decided that it would be fun to finish now that I know more about Rust.

## Finishing the Rewrite

My goal was for the Rust test to have similar, if not the same functionality as the Python test.

### Algorithm Optimizations

The first problem I addressed was the efficiency of the Levenshtein distance algorithm. Since this is originally a mathematical equation and wasn't designed for programming, it isn't particularly efficient. This is where Wagner-Fischer comes in. Wagner-Fischer is an implementation of Levenshtein distance that uses dynamic programming to avoid redundant calculations. Levenshtein distance is also recursive, which Wagner-Fischer is not, avoiding that extra recursive overhead. I chose to go with a Wagner-Fischer implementation that only uses two arrays instead of a full matrix to hopefully get even better performance. The full algorithm is below:

```rs
#[inline(always)]
fn wagner_fischer_2row(s1: &[char], s2: &[char]) -> usize {
    // Ensure s1 is the shorter sequence for optimization
    let (s1, s2) = if s1.len() < s2.len() {
        (s1, s2)
    } else {
        (s2, s1)
    };

    let len1 = s1.len();
    let len2 = s2.len();

    // handle empty string cases
    if len1 == 0 {
        return len2;
    }
    if len2 == 0 {
        return len1;
    }

    // Initialize two rows for the dynamic programming matrix
    let mut prev_row = vec![0; len2 + 1];
    let mut curr_row = vec![0; len2 + 1];

    // Initialize first row with incremental values
    (0..=len2).for_each(|i| {
        prev_row[i] = i;
    });

    // Fill the matrix using only two rows
    for (i, c1) in s1.iter().enumerate() {
        curr_row[0] = i + 1;

        for (j, c2) in s2.iter().enumerate() {
            curr_row[j + 1] = if c1 == c2 {
                // No edit needed
                prev_row[j]
            } else {
                // Take minimum of three possible operations (insert, delete, substitute)
                1 + prev_row[j].min(prev_row[j + 1]).min(curr_row[j])
            };
        }

        // Swap rows using mem::swap for better performance
        std::mem::swap(&mut prev_row, &mut curr_row);
    }

    prev_row[len2]

}
```

### Tokenization Optimizations

To speed it up a bit more, I added the following check to the `token_sort_ratio` function:

```rs
if (len1 as f64 / len2 as f64) < 0.5 || (len2 as f64 / len1 as f64) < 0.5 {
    return 0.0;
}
```

This snippet will check if the length of the strings we're comparing differ by more than half. If they do, we could reasonably assume that the strings are different. While this may not always present to be true, the performance gain is great enough to justify it being in the algorithm. This makes it so that on some comparisons we can just completely skip the Wagner-Fischer computations, which is an O(m\*n) algorithm, with m and n being the lengths of the strings.

### Iteration Optimizations

Other than the algorithm implementation, this may be the most important part to focus on. There are so many different ways to iterate over every combination of facts, so choosing the correct way is crucial to a fast algorithm. Let's take a look at the iteration line by line:

```rs
// Generate all possible indices combinations
let indices: Vec<_> = (0..all_facts.len())
    .flat_map(|i| ((i + 1)..all_facts.len()).map(move |j| (i, j)))
    .collect();
```

Instead of generating an iterable structure that contains all of the facts pre-paired, we can generate all pairs of indices instead. The `all_facts` array contains a struct with information about the fact, such as the fact itself and the line number in the file where the fact can be located. The fact itself isn't just a `String`, but rather an `Arc<String>`. This allows us to have cheaper clones which is crucial for performance. Next, we can look at how these indices are used:

```rs {hl_lines=["3-4"]}
// Process combinations in parallel
indices
    .into_par_iter()
    .progress_with(pb)
    .filter_map(|(i, j)| {
        let facts = &all_facts;
        let fact1 = &facts[i];
        let fact2 = &facts[j];

        let ratio = token_sort_ratio(&fact1.fact, &fact2.fact);
        if ratio > SIMILARITY_THRESHOLD {
            Some((fact1.clone(), fact2.clone(), ratio))
        } else {
            None
        }
    })
    .collect()
```

If we take a look at this first part, we can see where a huge amount of the improved performance lies. I'm using a Rust library called [Rayon](https://github.com/rayon-rs/rayon) which makes it incredibly easy to convert a sequential iterator into a parallel iterator. This means that instead of doing one string comparison at a time, I can take advantage of all of my CPU cores and do many computations at once, drastically speeding up the time it takes to find duplicate facts.

```rs {hl_lines=["6-10"]}
// Process combinations in parallel
indices
    .into_par_iter()
    .progress_with(pb)
    .filter_map(|(i, j)| {
        let facts = &all_facts;
        let fact1 = &facts[i];
        let fact2 = &facts[j];

        let ratio = token_sort_ratio(&fact1.fact, &fact2.fact);
        if ratio > SIMILARITY_THRESHOLD {
            Some((fact1.clone(), fact2.clone(), ratio))
        } else {
            None
        }
    })
    .collect()
```

The next part is pretty simple. We can take references of the facts to avoid copying/cloning, and calculate the similarity ratio. If it's above the threshold, add it to the removal list and continue. I found a good threshold with this particular algorithm is 82.5.

### CI Caching

The one downfall of the Rust version is that it takes time to compile which can slow down the CI, and that defeats the purpose of having a faster test. To solve this issue, I used GitHub's [actions/cache](https://github.com/actions/cache) action. Here's the relevant section of the CI:

```yml {hl_lines=[3,"5-7",12,"14-15",18]}
- name: Cache checkduplicates binary
        uses: actions/cache@v4
        id: cache
        with:
          path: |
            tests/checkduplicates/target/release/checkduplicates
          key: ${{ runner.os }}-cargo-${{ hashFiles('tests/checkduplicates/Cargo.lock', 'tests/checkduplicates/Cargo.toml', 'tests/checkduplicates/src/**') }}
          restore-keys: |
            ${{ runner.os }}-cargo-

      - name: Build checkduplicates test
        if: steps.cache.outputs.cache-hit != 'true'
        run: |
          cd tests/checkduplicates
          cargo build --release

      - name: Check for duplicate facts
        run: ./tests/checkduplicates/target/release/checkduplicates
```

To explain this simply, the cache action will check if `Cargo.toml`, `Cargo.lock`, or anything in `src/**` have changed. If it has, we'll assume that the cache is expired and the test should be rebuilt, which you can see in lines 12, 14-15. If the cache is not expired, we place the cached `checkduplicates` binary in appropriate place. After building, or if building is skipped, we then run the resulting binary. This allows us to skip the build time if nothing has changed in the test, while still letting it automatically build if something has changed.

## Conclusion

After all of this work, was it worth it? Let's let the number speak for themselves.

|                            | Python Test | Rust Test  |
| -------------------------- | ----------- | ---------- |
| Approximate iterations/sec | 550,000     | 2,200,000  |
| Time Taken                 | 48 seconds  | 12 seconds |

This benchmark was performed on my Framework 16 Laptop. I have a Ryzen 7 7840HS @ 3.8GHz, 16GB of DDR5-5600 RAM, and I was using the "Performance" profile with power profiles daemon on Arch Linux. In this case, the Rust version of the test performed 4&times; faster than the Python version of the test.

This metric, along with the CI caching, led to a huge performance gain in the duplicate fact checking. That's all I have for now so hopefully you learned something or just enjoyed this post. The full source code for the new test can be found below, just note that I've pinned the commit so there may be a more up to date version on the master branch.

<https://github.com/TabulateJarl8/randfacts/tree/5e6786e8b536efc2895880ce5f0e88a8f442454b/tests/checkduplicates>
