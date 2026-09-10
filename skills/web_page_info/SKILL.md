---
name: web-page-info
description: >
  Get basic information about the currently opened webpage.
  Use when the user asks for the page title or URL.
---

# Web Page Info

## Workflow

1. Check that a browser page is open.
2. Get the page title.
3. Get the current URL.
4. Return the information to the user.

## Rules

- Do not navigate to another page.
- Do not click anything.
- Do not modify the webpage.

## Tools

Use:
- browser.get_title
- browser.get_url