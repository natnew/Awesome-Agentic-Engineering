#!/usr/bin/env node
// Find entries whose `Last reviewed: <Month YYYY>` marker is older than
// FRESHNESS_MONTHS, and entries under tracked paths that have no marker.
//
// Pure Node (no deps). Emits a Markdown report to stdout.
//
// Usage:
//   node .github/scripts/find-stale-entries.mjs
//   FRESHNESS_MONTHS=12 node .github/scripts/find-stale-entries.mjs

import { readFile, readdir, stat } from 'node:fs/promises';
import { join, relative } from 'node:path';

const ROOT = process.cwd();
const FRESHNESS_MONTHS = Number(process.env.FRESHNESS_MONTHS ?? 9);
const TRACKED = ['README.md', 'appendix'];

const MONTHS = {
  january: 0, february: 1, march: 2, april: 3, may: 4, june: 5,
  july: 6, august: 7, september: 8, october: 9, november: 10, december: 11,
};

async function walk(path) {
  const out = [];
  const st = await stat(path).catch(() => null);
  if (!st) return out;
  if (st.isFile()) {
    if (path.endsWith('.md')) out.push(path);
    return out;
  }
  const entries = await readdir(path, { withFileTypes: true });
  for (const e of entries) {
    if (e.name.startsWith('.') || e.name === 'node_modules') continue;
    out.push(...(await walk(join(path, e.name))));
  }
  return out;
}

function parseReviewed(text) {
  const m = text.match(/Last reviewed:\s*([A-Za-z]+)\s+(\d{4})/);
  if (!m) return null;
  const month = MONTHS[m[1].toLowerCase()];
  const year = Number(m[2]);
  if (month === undefined || Number.isNaN(year)) return null;
  return new Date(Date.UTC(year, month, 1));
}

function monthsBetween(a, b) {
  return (b.getUTCFullYear() - a.getUTCFullYear()) * 12
    + (b.getUTCMonth() - a.getUTCMonth());
}

async function main() {
  const now = new Date();
  const files = [];
  for (const p of TRACKED) files.push(...(await walk(join(ROOT, p))));

  const stale = [];
  const missing = [];

  for (const abs of files) {
    const rel = relative(ROOT, abs).replaceAll('\\', '/');
    const content = await readFile(abs, 'utf8');
    const reviewed = parseReviewed(content);
    if (!reviewed) {
      missing.push(rel);
      continue;
    }
    const age = monthsBetween(reviewed, now);
    if (age > FRESHNESS_MONTHS) {
      stale.push({ file: rel, reviewed, age });
    }
  }

  const lines = [];
  lines.push(`# Freshness audit — ${now.toISOString().slice(0, 10)}`);
  lines.push('');
  lines.push(`Threshold: **${FRESHNESS_MONTHS} months** since last review.`);
  lines.push('');

  lines.push('## Stale entries');
  lines.push('');
  if (stale.length === 0) {
    lines.push('_None._');
  } else {
    lines.push('| File | Last reviewed | Age (months) |');
    lines.push('| --- | --- | --- |');
    for (const s of stale.sort((a, b) => b.age - a.age)) {
      const rev = s.reviewed.toLocaleString('en-US', { month: 'long', year: 'numeric', timeZone: 'UTC' });
      lines.push(`| \`${s.file}\` | ${rev} | ${s.age} |`);
    }
  }
  lines.push('');

  lines.push('## Files missing a `Last reviewed:` marker');
  lines.push('');
  if (missing.length === 0) {
    lines.push('_None._');
  } else {
    for (const f of missing.sort()) lines.push(`- \`${f}\``);
  }
  lines.push('');

  process.stdout.write(lines.join('\n'));

  // Exit code signals "action needed" to the workflow.
  process.exit(stale.length > 0 || missing.length > 0 ? 1 : 0);
}

main().catch((err) => {
  console.error(err);
  process.exit(2);
});
