// n8n Code node "Render" in the "Send Digest Email" sub-workflow.
// Turns the generic digest shape (see README.md in this folder) into an HTML
// email in the retired Upwork digest's style. Knows nothing about the caller.

const DEFAULT_TO = 'adamhaley@gmail.com';
const SAFE_HREF = /^(https?:|mailto:|obsidian:)/i;

const doc = $input.first().json;
if (!doc.title || !Array.isArray(doc.sections)) {
  throw new Error('Send Digest Email: input needs `title` and a `sections` array (see README).');
}
const sections = doc.sections.filter(s => Array.isArray(s.cards) && s.cards.length);
if (!sections.length) return [];

// ── Helpers ────────────────────────────────────────────────────────────────

function esc(text) {
  return String(text ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// Keep link text, drop link targets, show `code`.
function inlineMd(text) {
  const plain = String(text ?? '')
    .replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, '$2')
    .replace(/\[\[([^\]]+)\]\]/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
  return esc(plain).replace(/`([^`]+)`/g, '<code>$1</code>');
}

function link(href, html) {
  return href && SAFE_HREF.test(href) ? `<a href="${esc(href)}">${html}</a>` : html;
}

const badgeColors = { good: '#16a34a', warn: '#d97706', bad: '#dc2626', neutral: '#64748b' };

function tags(list) {
  return (list ?? []).map(t => {
    const tag = typeof t === 'string' ? { text: t } : t;
    return `<span class="tag ${esc(tag.tone ?? '')}">${esc(tag.text)}</span>`;
  }).join('');
}

function item(entry) {
  const it = typeof entry === 'string' ? { text: entry } : entry;
  return `<li>${tags(it.tags)}${link(it.href, inlineMd(it.text))}</li>`;
}

// ── CSS (from the Upwork digest) ───────────────────────────────────────────

const css = `
  body { margin:0; padding:0; background:#f1f5f9; font-family:'Helvetica Neue',Arial,sans-serif; }
  .wrapper { max-width:680px; margin:32px auto; background:#fff; border-radius:12px;
             box-shadow:0 2px 8px rgba(0,0,0,.08); overflow:hidden; }
  .header { background:#14532d; padding:28px 32px; }
  .header h1 { margin:0; color:#fff; font-size:22px; font-weight:700; }
  .header p  { margin:6px 0 0; color:#bbf7d0; font-size:13px; }
  .section { padding:24px 32px 4px; }
  .section h2 { margin:0 0 14px; font-size:13px; letter-spacing:.06em; text-transform:uppercase; color:#64748b; }
  .card { border:1px solid #e2e8f0; border-radius:10px; padding:18px 20px; margin-bottom:16px; background:#fff; }
  .card.attention { border-color:#fcd34d; background:#fffbeb; }
  .card-header { display:flex; justify-content:space-between; align-items:flex-start; gap:12px; }
  .card-title { font-size:16px; font-weight:700; color:#1e293b; margin:0; flex:1; }
  .card-title a { color:#1e293b; }
  .badge { flex-shrink:0; font-size:12px; font-weight:700; color:#fff; padding:3px 9px; border-radius:20px; white-space:nowrap; }
  .meta { margin:10px 0 4px; }
  .tag { display:inline-block; font-size:12px; background:#f1f5f9; color:#475569; padding:3px 10px; border-radius:20px; margin:0 6px 6px 0; }
  .tag.green { background:#dcfce7; color:#166534; }
  .tag.blue  { background:#dbeafe; color:#1e40af; }
  .tag.amber { background:#fef3c7; color:#92400e; }
  .body { font-size:14px; color:#475569; line-height:1.6; margin:12px 0; }
  ul { margin:8px 0 0; padding-left:18px; }
  li { font-size:14px; color:#475569; line-height:1.55; margin-bottom:6px; }
  li a { color:#15803d; }
  code { font-size:12px; background:#f1f5f9; padding:1px 4px; border-radius:4px; }
  .sub { font-size:12px; font-weight:700; color:#94a3b8; text-transform:uppercase; letter-spacing:.05em; margin:14px 0 0; }
  .button { display:inline-block; margin-top:14px; background:#15803d; color:#fff !important; text-decoration:none;
            padding:9px 20px; border-radius:8px; font-size:13px; font-weight:600; }
  .footer { background:#f8fafc; border-top:1px solid #e2e8f0; padding:16px 32px; text-align:center; margin-top:12px; }
  .footer p { margin:0; font-size:12px; color:#94a3b8; }
`;

// ── Cards and sections ─────────────────────────────────────────────────────

function card(c, tone) {
  const badge = c.badge
    ? `<span class="badge" style="background:${badgeColors[c.badge.tone] ?? badgeColors.neutral}">${esc(c.badge.text)}</span>`
    : '';
  const groups = (c.groups ?? []).filter(g => (g.items ?? []).length).map(g =>
    `${g.label ? `<p class="sub">${esc(g.label)}</p>` : ''}<ul>${g.items.map(item).join('')}</ul>`).join('');
  const button = c.button && SAFE_HREF.test(c.button.href ?? '')
    ? `<a class="button" href="${esc(c.button.href)}">${esc(c.button.text)}</a>` : '';
  return `
    <div class="card ${tone === 'attention' ? 'attention' : ''}">
      <div class="card-header">
        <p class="card-title">${link(c.href, esc(c.title))}</p>
        ${badge}
      </div>
      ${c.tags?.length ? `<div class="meta">${tags(c.tags)}</div>` : ''}
      ${c.body ? `<p class="body">${esc(c.body)}</p>` : ''}
      ${groups}${button}
    </div>`;
}

const sectionHtml = sections.map(s => `
  <div class="section">
    ${s.heading ? `<h2>${esc(s.heading)}</h2>` : ''}
    ${s.cards.map(c => card(c, s.tone)).join('')}
  </div>`).join('');

// ── Assemble email ─────────────────────────────────────────────────────────

const today = new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric', timeZone: 'America/Los_Angeles' });

const htmlBody = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>${esc(doc.title)}</title>
  <style>${css}</style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <h1>${esc(doc.title)}</h1>
      ${doc.subtitle ? `<p>${esc(doc.subtitle)}</p>` : ''}
    </div>
    ${sectionHtml}
    ${doc.footer ? `<div class="footer"><p>${esc(doc.footer)}</p></div>` : ''}
  </div>
</body>
</html>`;

return [{
  json: {
    to: doc.to || DEFAULT_TO,
    subject: doc.subject || `${doc.title} · ${today}`,
    htmlBody,
  },
}];
