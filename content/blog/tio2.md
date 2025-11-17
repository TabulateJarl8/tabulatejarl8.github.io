---
title: "TiO2"
date: 2023-10-20T00:29:03-04:00
draft: false
tags: ["programming", "parsing", "rust", "python"]
---

Some of you may know of my TI-BASIC to Python transpiler, [ti842py](/software/ti842py). While not very practical, this project was pretty fun for me to work on because I was having to find all of these different ways to implement TI-BASIC functions in Python. This project was based on a project that I found by [thenaterhood](https://github.com/thenaterhood) called basically-ti-basic, which could decompile and (almost) compile the TI calculator .8XP files. He did a lot of the hard work of reverse engineering the bytecode, and his program helped me out a lot. I forked his project, reverse engineered some instructions that he missed, and then packaged it for PyPI so I could more easily use it in ti842py.

# The Problem

My program worked fine for a while, and I implemented many features such as matrices support, `Goto`/`Lbl`, `getKey`, and many others. However, it was the goto support that eventally broke everything. I had been using a [fork](https://github.com/snoack/python-goto/pull/23) of snoack's `goto-statement` Python module which modified the Python bytecode to allow for jumping to labels, and after some recent Python update, they changed how their internal instructions work and it broke the goto module. Someone did fork the project to add support for Python 3.11, however if I switched to this fork, I would lose a nice feature from the fork I was using: goto into blocks. While it probably didn't matter too much, I figured that this wasn't maintainable and I should look for another solution.

# The Solution

Since I'm a huge fan of Rust, I decided that I should rewrite my project in Rust, but do it better and do things correctly this time. I created a new project, and with the help of [a friend](https://turbowafflz.gitlab.io), named it TiO2. The name is a play on "TI" from Texas Instruments, and the "Oxidize" trend in naming Rust projects, as the element TiO2 is Titanium Dioxide. I've been working on this project a lot for the past few weeks, and I'm excited seeing how far it's come. At this point, I've completely rewritten the basically-ti-basic project in Rust, including fixing the compiler. This means that TiO2 will be able to both decompile .8XP files as well as compile to them from plain text (this is a lot harder than it sounds, barely any of the 8XP bytecode is documented). Since 2/3 features are completely, I've now moved on to the most difficult and largest part of the project, which is building the interpreter. I've opted to go with a bytecode interpreter rather than a plaintext interpreter or transpiling to a different language, as I feel that this is the most maintainable route to go. TI-BASIC can be represented in plaintext in too many different ways, and other programming languages can change, but the bytecode is going to remain the same, so if I implement it once, I (hopefully) never have to look at it again.

![Debug output from compiling a small program](/img/blog/tio2_compile_debug_output.png)

# Where I Am Now

Currently, I'm trying to figure out the best way to implement the parser. If I was able to somehow parse the bytecode into postfix notation, that would be really helpful, however that sounds pretty difficult. I may take inspiration from postfix though, as it does seem like a smart idea if it was able to be done. I'm about to stop programming for the night, however the last thing that I was stuck on was trying to figure out a way to gather tokens together, such as in a number or a string. Since each number or character is only one byte, I need to find a way to group the tokens together that are all part of one object, such as the number `-3.56` or the text in the command `Disp "HELLO WORLD"`. I might come up with a list of which bytes represent functions, and if the interpreter comes across a function, it will add the following bytes to the top argument in an argument stack until a comma is reached, which signifies the end of an argument and the beginning of a new one. Once the end of the line or, in some cases, a closing parenthesis is reached, the arguments will be popped back into the function and then evaluted. That's just one idea I have, but I suppose we'll have to see what works out.

![A screenshot of the tokens.rs file](/img/blog/tio2_tokens_rs_nvim.png)

