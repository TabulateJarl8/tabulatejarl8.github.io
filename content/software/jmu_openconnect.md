---
title: JMU OpenConnect
weight: 40
draft: false
nav: false
featured: true
status: "warning"
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

This is a wrapper script around openconnect to help with authentication for the JMU VPN on Linux. Openconnect used to work fine until Ivanti purchased Pulse Secure, and then that broke something. This script opens up a web browser to allow the user to authenticate with Duo, and then grabs the DSID cookie to use for openconnect authentication.
