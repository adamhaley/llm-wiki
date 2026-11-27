// n8n Code node "Build digest" in "LLM Wiki Daily Digest".
// Maps `wiki_tool.py digest` JSON (the SSH node's stdout) onto the generic
// Send Digest Email shape (n8n/digest-email/README.md). Presentation lives in
// that sub-workflow; this node only decides what to say.

const run = $input.first().json;
if (run.code !== 0) throw new Error(`Digest failed (exit ${run.code}): ${run.stdout || run.stderr}`);
const d = JSON.parse(run.stdout);

const VAULT = 'wiki';
const STALE_DAYS = 14;
const QUIET_DAYS = 7;
const TODO_MAX_CHARS = 220;

const obsidian = path => `obsidian://open?vault=${VAULT}&file=${encodeURIComponent(path.replace(/\.md$/, ''))}`;
const clip = text => (text.length > TODO_MAX_CHARS ? text.slice(0, TODO_MAX_CHARS).replace(/\s+\S*$/, '') + '…' : text);
const plural = (n, word) => `${n} ${word}${n !== 1 ? 's' : ''}`;
const statusTone = { 'in-progress': 'blue', ready: 'green', planned: 'grey' };

function activityBadge(lastActivity) {
  if (!lastActivity) return { text: 'No activity logged', tone: 'neutral' };
  const days = Math.round((new Date(d.date) - new Date(lastActivity)) / 86400000);
  const text = days === 0 ? 'Active today' : `${days}d since last activity`;
  return { text, tone: days >= STALE_DAYS ? 'bad' : days >= QUIET_DAYS ? 'warn' : 'good' };
}

const planItem = (plan, slug) => ({ text: plan.title, href: obsidian(plan.path), tags: slug ? [slug] : [{ text: plan.status, tone: statusTone[plan.status] }] });
const plansWith = status => d.projects.flatMap(p => p.plans.filter(x => x.status === status).map(x => planItem(x, p.slug)));

const todoCount = d.projects.reduce((n, p) => n + p.todos.length, 0) + d.unsorted_todos.length;
const planCount = d.projects.reduce((n, p) => n + p.plans.length, 0);
const inProgress = plansWith('in-progress');

const needsYou = {
  title: 'Needs you',
  groups: [
    { label: 'Pickup list', items: d.pickup },
    { label: 'Research that failed (set status: queued to retry)', items: d.research.failed.map(r => ({ text: r.title, href: obsidian(r.path) })) },
    { label: 'Plans ready to run', items: plansWith('ready') },
    { label: 'Plans in progress', items: inProgress },
  ],
};

const today = new Date(`${d.date}T12:00:00`).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });

return [{
  json: {
    title: 'Daily Digest',
    subject: `Daily Digest: ${plural(todoCount, 'to-do')}, ${inProgress.length} plans in progress · ${today}`,
    subtitle: `${plural(todoCount, 'open to-do')} · ${plural(planCount, 'open plan')} · ${plural(d.projects.length, 'project')} · ${today}`,
    sections: [
      { tone: 'attention', cards: needsYou.groups.some(g => g.items.length) ? [needsYou] : [] },
      {
        heading: 'New research',
        cards: d.research.answered.length
          ? [{ title: plural(d.research.answered.length, 'answered question'), groups: [{ items: d.research.answered.map(r => ({ text: r.title, href: obsidian(r.path) })) }] }]
          : [],
      },
      {
        heading: 'Projects, most recently active first',
        cards: [
          ...d.projects.map(p => ({
            title: p.slug,
            badge: activityBadge(p.last_activity),
            tags: [plural(p.todos.length, 'to-do'), plural(p.plans.length, 'open plan')],
            groups: [
              { label: 'Plans', items: p.plans.map(x => planItem(x)) },
              { label: 'To-dos', items: p.todos.map(clip) },
            ],
          })),
          ...(d.unsorted_todos.length ? [{ title: 'No project', groups: [{ items: d.unsorted_todos.map(clip) }] }] : []),
        ],
      },
    ],
    footer: 'From the second brain (wiki/todo.md, project plans, research) · LLM Wiki Daily Digest in n8n',
  },
}];
