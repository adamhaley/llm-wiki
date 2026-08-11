# CRM

Use this directory for person records that need both relationship context and practical contact information.

Create one markdown file per person and keep [index.md](index.md) alphabetized with short summaries.

Each CRM note should reserve frontmatter fields for emails, phones, websites, social profiles, preferred contact method, location, company, role, follow-up dates, and future sync IDs. Leave unknown values explicit; do not invent contact details.

The markdown note is the context layer. A future database-backed CRM can become the structured operational layer, linked through `crm_external_id` and `crm_sync_status`.
