---
title: "Trying Out Typst"
date: 2023-11-23T00:51:22-05:00
draft: true
tags: ["markup", "latex", "typst"]
---

Recently, I came across a new project, [Typst](https://typst.app/). From their GitHub, "Typst is a new markup-based typesetting system that is designed to be as powerful as LaTeX while being much easier to learn and use". It's written in Rust which I was immediately a fan of, and I was super interested in an alternative to LaTeX as I use it heavily for school papers, and while it's super powerful, it can be annoying to set up and the compile times can start to get slow when you start compiling 70 page documents. I started checking out their examples, and I couldn't find an APA template, so I figured that was a great way to start learning.

![Showcase of basic typst document](/img/blog/typst_showcase.png)

# Similarities and Differences from LaTeX
I first noticed a few things that really set Typst aside from LaTeX. The first thing was how all of the packages I needed were just built in to Typst. For the APA paper I was recreating, I needed to import 8 packages, some of which need to be manually installed by the person compiling the document. With Typst, I just needed to import the Cetz package for more advanced graphing stuff, as my paper included bar charts. The Cetz package is also included within Typst, so I didn't have to install any extra dependencies. I also noticed that commands in Typst start with #, as opposed to LaTeX where they start with \\. Typst has different elements like figures, blocks, and text, and the styling of these can be overridden with the show command. This can also be used very easily to dynamically override element styles. For example, the APA spec requires a specific and different type of heading for each different heading level (1: centered + bold, 2: align left + bold, 3: align left + italic, ...). This is different from the set command which allows you to configure different elements, for example, setting the global text size/font, or setting the spacing around lines. Below is an example of the usage of the show command to create APA headings.

![APA headings implemented in Typst](/img/blog/typst_apa_headings.png)


In my LaTeX paper, I was able to set the document class to APA, which provided me with macros to create the title, such as author, affiliation, course, due date, etc. 

<!-- cetz vs tikz and cetz trouble -->

<!-- bibliography styles/trouble -->

<!-- errors  -->
<!-- easier scripting? -->

<!-- little things? (syntax highlighting, faster build times, no aux files) -->

<!-- what id like added; doublespace -->