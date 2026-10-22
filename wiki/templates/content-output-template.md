---
title: <% tp.file.title %>
type: output
slug: <% tp.file.title.split("--")[0] %>
channel: <% tp.file.title.split("--")[1] || "" %>
status: scheduled
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
published:
url:
tags:
  - content
---

# <% tp.file.title %>

Draft: [<% tp.file.title.split("--")[0] %>](../drafts/<% tp.file.title.split("--")[0] %>.md)

## Final Copy

## Publication Notes

- 
