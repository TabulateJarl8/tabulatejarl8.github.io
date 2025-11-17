---
title: "Trying Out Typst"
date: 2023-12-05T00:51:22-05:00
draft: false
tags: ["markup", "latex", "typst"]
---

Recently, I came across a new project, [Typst](https://typst.app/). From their GitHub, "Typst is a new markup-based typesetting system that is designed to be as powerful as LaTeX while being much easier to learn and use". It's written in Rust which I was immediately a fan of, and I was super interested in an alternative to LaTeX as I use it heavily for school papers, and while it's super powerful, it can be annoying to set up and the compile times can start to get slow when you start compiling 70 page documents. I started checking out their examples, and I couldn't find an APA template, so I figured that was a great way to start learning.

![Showcase of basic typst document](/img/blog/typst_showcase.png)

# Similarities and Differences from LaTeX

I first noticed a few things that really set Typst aside from LaTeX. The first thing was how all of the packages I needed were just built in to Typst. For the APA paper I was recreating, I needed to import 8 packages, some of which need to be manually installed by the person compiling the document. With Typst, I just needed to import the Cetz package for more advanced graphing stuff, as my paper included bar charts. The Cetz package is also included within Typst, so I didn't have to install any extra dependencies. I also noticed that commands in Typst start with #, as opposed to LaTeX where they start with \\. Typst has different elements like figures, blocks, and text, and the styling of these can be overridden with the show command. This can also be used very easily to dynamically override element styles. For example, the APA spec requires a specific and different type of heading for each different heading level (1: centered + bold, 2: align left + bold, 3: align left + italic, ...). This is different from the set command which allows you to configure different elements, for example, setting the global text size/font, or setting the spacing around lines. Below is an example of the usage of the show command to create APA headings.

![APA headings implemented in Typst](/img/blog/typst_apa_headings.png)

In my LaTeX paper, I was able to set the document class to APA, which provided me with macros to create the title, such as author, affiliation, course, due date, etc. In Typst, I had to implement this myself since, obviously, there wasn't any other template. However, scripting in Typst is much easier than in LaTeX and I'll talk about that a little bit more later.

# Graphs

One of the main components of my original APA paper was graphs that I created to showcase the research I did. Looking into what Typst had built in, there was some rudimentary graphing stuff, but I needed to import a 3rd package, [Cetz](https://github.com/johannes-wolf/cetz), that comes pre-bundled with Typst in order to get more complicated graphics, however it's the exact same in LaTeX so that's fine. A wrote a quick rule in my template to format figures according to the APA spec, and then started reimplementing my graphs. Graphs using Cetz are much more readable than graphs using Tikz/Pgfplots in LaTeX.

![Cetz graph code](/img/blog/cetz_graph_code.png)

However, I noticed something strange after I finished writing the code. There was a lot of left padding on the graph, and it was difficult to fit some bigger graphs. I started an issue ([johannes-wolf/cetz#341](https://github.com/johannes-wolf/cetz/issues/341)) asking the developer about this issue, and he explained to me that he was currently in the process of rewriting the ColumnChart to be a wrapper around the Plot API. This would allow users to manually adjust the `x-min` and `x-max` values, solving the issue with the extra padding. This library needs a bit of work because of how new it is, but I could see it very easily evolving into a suitable replacement for Tikz.

# Bibliography Issues

Next step was to complete the bibliography, and fortunately Typst has tons of bibliography formats built in, APA being one of them. The Typst developers have made an alternative format to BibTeX, called [Hayagriva](https://github.com/typst/hayagriva), which is just YAML. However, they also fully support using legacy BibTeX files from your old documents, and since many automatic citation generators and other tools don't support their newer format yet. After constructing a bibliography, I noticed another issue. When an author is missing, the APA style guidelines say that the source should be referenced from the source title, and when missing a date, it should include "(n.d.)". There are a few issues that I was experiencing:

1. When provided an author but not a date, (n.d.) was missing
2. When provided a date but not an author, the source title was missing
3. When neither an author nor a date is provided, the source was missing but (n.d.) is provided

After asking about this issue in the Typst Discord server, one of the maintainers of Hayagriva reached out and asked a few questions. Afterwards I was referred to an existing issue ([typst/typst#2762](https://github.com/typst/typst/issues/2762)). This issue documents my exact issue, and it's currently being resolved, which is nice to see.

# Indentation Issues

Typst has a known issue where the first paragraph under headings ignore the indentation rules set by `par(first-line-indent: size)`. This issue is currently being tracked ([typst/typst#311](https://github.com/typst/typst/issues/311)), but in the meantime, I needed a workaround. After looking through the issue, I found some people who made workarounds, but there were issues with all of them. The closest one was pretty simple, but it added a bit of vertical spacing underneath each header. To counter this, I just added some negative vertical space right next to the added horizontal space. The following code snippet loops through all headings that are levels 1-3, and adds a 0.5in indent and -0.67in of vertical space:

![Typst Indentation Fix](/img/blog/typst_indentation_fix.png)

# Small Things

Theres a few small things that are nice about Typst, and since they're not big enough for their own section, I'll just list them all here.

- Typst has really nice errors. Coming from LaTeX that's really not a high bar to pass, but it's still nice nevertheless. They're clear and concise, and point out the exact line that the issue lies on.
- Typst scripting is much easier than scripting in LaTeX. As you can see from the few screenshots I've included, the code is readable and easy to understand, which is great for maintainability.
- Typst has syntax highlighting. Not just this, but it also has inline syntax highlighting which is really nice.
- Typst build times are much faster than build times in LaTeX.
- There are no auxiliary files in Typst like in LaTeX. When I would compile a LaTeX document, I would get tons of auxiliary files, like `.aux`, `.bbl`, `.blg`, `.fls`, `.out`, and `.log` to name a few. Typst just has your `.typ` markup file, your bibliography if you have one, and then it generates a PDF without any of the extra junk that LaTeX uses.

# Final Thoughts

Typst seems like a really nice tool and I'm excited to see how it matures. It definitely needs some refinement as you saw from the types of issues that were open, but it's nothing that's unfixable. They could also do with some more commands to reduce boilerplate, such as the `\doublespacing` command from LaTeX. In Typst, you need to implement double spacing yourself, and while it's not too difficult and it's only 2 lines of code, it would still be more friendly to beginners to add more commands like that. If you have a paper you need to write, or if you're just curious, give Typst a try. My completed APA template can be found in my random-junk repository for now, until I decide if I want to put this into it's own Typst package. [https://github.com/TabulateJarl8/random-junk/blob/master/typst/apa.typ](https://github.com/TabulateJarl8/random-junk/blob/master/typst/apa.typ).

