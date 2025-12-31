---
title: "pub_source"
draft: false
nav: false
featured: false
status: "success"
logo: /img/showcase/pub_source/logo.svg
buttons:
  - get:
    text: crates.io
    button_color: secondary
    href: https://crates.io/crates/pub_source
    newtab: false
  - source:
    text: Source Code
    button_color: primary
    href: https://github.com/TabulateJarl8/pub_source
    newtab: false
software_page: true
---

A Rust proc macro to make everything public.

`pub_source` provides a macro which rewrites a block of Rust source code so that all top level items become public.

This macro rewrites the following kinds of items to `pub`:

- functions
- structs and all of their fields
- enums
- type aliases
- constants and statics
- traits
- modules (recursively)
- impl blocks (functions, consts, type items inside them)
- unions

This crate also denies the use of `unwrap`, `expect`, and `panic!()`.

This was originally written to be injected around user-submitted code in a code runner so that unit tests could access everything the user wrote. There may be other uses but I'm not quite sure what they might be yet.
