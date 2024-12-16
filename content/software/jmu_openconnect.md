---
title: JMU OpenConnect
weight: 40
draft: false
nav: false
featured: true
status: "danger"
logo: "/img/showcase/jmu_openconnect/logo_static.svg"
images:
  - "/img/showcase/jmu_openconnect/logo_static.svg"
alts:
  - JMU OpenConnect logo
buttons:
  - source:
    text: Source Code
    button_color: primary
    href: https://github.com/TabulateJarl8/jmu-openconnect
    newtab: false
  - pypi:
    text: PyPI Page
    button_color: secondary
    href: https://pypi.org/project/jmu-openconnect/
    newtab: false
layout: "software_page"
---

Wrapper script around openconnect for JMU VPN authentication on Linux.

> ## IMPORTANT:
>
> This project is based on Ivanti Pulse Secure, which JMU no longer uses as of January 6th, 2025. Now that JMU has switched to GlobalProtect, you can switch to using [yuezk/GlobalProtect-openconnect](https://github.com/yuezk/GlobalProtect-openconnect) if needed. While the GUI frontend has some weird licensing restrictions, the CLI component will always be free, and you could just make a GUI wrapper around that if needed.

This is a wrapper script around openconnect to help with authentication for the JMU VPN on Linux. Openconnect used to work fine until Ivanti purchased Pulse Secure, and then that broke something. This script opens up a web browser to allow the user to authenticate with Duo, and then grabs the DSID cookie to use for openconnect authentication.
