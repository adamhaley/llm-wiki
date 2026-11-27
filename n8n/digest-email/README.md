# Send Digest Email (n8n sub-workflow)

One reusable n8n workflow that turns a small JSON document into an HTML email in the style of
the retired Upwork job digest (green header, white cards, pill tags, coloured badge, button) and
sends it. Any workflow can send Adam a digest by building this shape and calling it with an
**Execute Workflow** node. The sub-workflow knows nothing about where the data came from.

- n8n: workflow **Send Digest Email**, folder Obsidian.
- Renderer source: [`render.js`](render.js) (the Code node, kept in sync by hand).
- First caller: **LLM Wiki Daily Digest**, which builds its input in
  [`../daily-digest-build.js`](../daily-digest-build.js).

## Input shape

Send one item whose `json` is:

```jsonc
{
  "to": "someone@example.com",     // optional; defaults to Adam
  "subject": "…",                  // optional; defaults to "<title> · <today>"
  "title": "Daily Digest",         // required: header text
  "subtitle": "83 to-dos · Friday, November 27, 2026", // optional: line under the header
  "sections": [                    // required, may be empty
    {
      "heading": "Needs you",      // optional: small caps label above the cards
      "tone": "attention",         // optional: "attention" = amber cards; default white
      "cards": [
        {
          "title": "ahmedia",      // required
          "href": "https://…",     // optional: makes the title a link
          "badge": { "text": "2d since last activity", "tone": "good" },
                                   // optional; tone: good | warn | bad | neutral
          "tags": ["16 to-dos", { "text": "in-progress", "tone": "blue" }],
                                   // optional pills; string or {text, tone}; tone: green | blue | amber | grey
          "body": "Plain paragraph text.",   // optional
          "groups": [              // optional: labelled bullet lists
            {
              "label": "Plans",    // optional
              "items": [
                "plain item",      // string, or:
                { "text": "Item with `code` and [link text](url)", "href": "obsidian://…", "tags": ["planned"] }
              ]
            }
          ],
          "button": { "text": "View Job →", "href": "https://…" }  // optional
        }
      ]
    }
  ],
  "footer": "Where this came from"  // optional
}
```

Text fields are escaped. Item `text` supports a small slice of markdown: `` `code` `` and links
(`[text](url)`, `[[wikilink]]`), rendered as their text only. `href` values must be `https:`,
`http:`, `mailto:` or `obsidian:` links; anything else is dropped.

An input with no cards at all sends nothing, so callers can skip their own "is there anything
to send" check.

## Changing the format

Edit `render.js` and paste it into the **Render** Code node. Keep the input shape
backward-compatible: add optional fields rather than renaming existing ones, because every
caller depends on it.
