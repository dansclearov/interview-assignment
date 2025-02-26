# Security Vulnerability Assessment and Fixes

This repository contains my solutions for a three-part security assignment focusing on identifying, analyzing, and backporting vulnerabilities in popular JavaScript libraries.

## Overview

The assessment covers three distinct CVEs across different npm packages:

1. **[CVE-2023-45857: Axios CSRF Vulnerability](./part_1/)**
   Analysis of a cross-site request forgery vulnerability in Axios where XSRF tokens were leaked across origins.

2. **[CVE-2020-36604: Hoek Prototype Pollution](./part_2/)**
   Investigation into why Hoek 6.1.3 is unexpectedly immune to a prototype pollution vulnerability despite lacking explicit protections.

3. **[CVE-2021-23434: Object-Path Type Confusion](./part_3/)**
   Fixing a type confusion vulnerability that allowed bypassing previous prototype pollution protections.

## Technologies

All vulnerabilities involve JavaScript/Node.js libraries and focus on common web security issues:
- CSRF protections
- Prototype pollution
- Type confusion

## Approach

For each vulnerability, I:
1. Analyzed the root cause
2. Examined the official fix
3. Backported the fix to earlier versions
4. Created patches or documented the necessary code changes

## Challenges & Assumptions

- **Hoek 6.1.3**: The unexpected immunity required some debugging and a deeper investigation of JavaScript property assignment behaviors

Each subdirectory contains detailed README files with specific findings and solutions.
