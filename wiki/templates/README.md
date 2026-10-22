# Templates

Starter templates for each note type. These stay tracked in git even though most `wiki/` content does not.

Applied via the Templater plugin, not by copy/paste. `title`/`created`/`updated` auto-fill from the new note itself.

**Folder templates were inert until 2026-10-21.** Templater's `enable_folder_templates` and `trigger_on_file_creation` were both absent from `.obsidian/plugins/templater-obsidian/data.json` — i.e. at their default of `false` — so none of the configured folder templates had ever fired on new-note creation, despite being correctly configured. Both are now `true`. If a folder template stops firing again, check those two settings first (Templater → Folder templates → "Trigger Templater on new file creation") before suspecting the template itself.

- `crm/`, `topics/`, `pages/`, and `patterns/` each auto-insert their template on file creation (Templater folder templates, configured in `.obsidian/plugins/templater-obsidian/data.json`).
- `journal/` gets its template from the core Daily Notes plugin instead (see `.obsidian/daily-notes.json`), so it's deliberately left out of Templater's folder-template list to avoid double-inserting.
- `pages/` is mixed-type (page, entity, source, synthesis) — its folder default is the generic `page-template`; for the other three, use the command palette's "Templater: Insert template" and pick manually.
- `content/ideas/`, `content/drafts/`, and `content/output/` each auto-insert their own stage template. These are the only templates that derive frontmatter from the *filename* rather than just stamping dates: `slug` auto-fills from the file's name (and `channel` from the part after `--`, for outputs), precisely so the naming convention in `wiki/content/README.md` can't drift from the frontmatter by hand. The draft and output templates also pre-write the link back to the previous stage. Because all three stages share a basename, those are relative markdown links, not `[[wikilinks]]` — a bare `[[slug]]` would be ambiguous across the stage folders.
