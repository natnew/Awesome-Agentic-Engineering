# Benchmark and Evidence Policy

> Audience: maintainers · Evidence class: official

Last reviewed: March 2026

Canonical resources are trusted in this repository because they define what counts as evidence. A source is strong when it makes a capability, interface, benchmark, or operational claim falsifiable.

## Source Priority

Use sources in roughly this order when curating or revising entries:

1. Official docs, architecture guides, specifications, and first-party repositories.
2. Benchmark repos, evaluation papers, and methodology write-ups tied to a named workload.
3. Field reports such as engineering blogs, postmortems, incident write-ups, and operator notes.
4. Author assessment after reviewing the materials above against this repository's rubric.

Marketing pages, launch threads, GitHub stars, and product announcements can help with discovery, but they are not enough on their own for substantive claims.

## Evidence Tags

Tag substantive claims with one of these labels:

| Tag | Meaning |
| --- | --- |
| `[official]` | Official docs, architecture guides, specs, benchmark documentation, or first-party repositories. |
| `[benchmark]` | Published benchmark runs, evaluation papers, or benchmark repos tied to a named workload. |
| `[field report]` | Production write-ups, incident reports, engineering blogs, or operator notes about real deployments. |
| `[author assessment]` | This repository's synthesis after reviewing the sources above. |

## Benchmark Performance vs. Production Maturity

Keep these as separate judgments:

- Benchmark performance describes behaviour on a defined task, dataset, or benchmark harness.
- Production maturity describes operability, reliability, governance fit, safety posture, observability, and surrounding operator knowledge.
- A benchmark result can support workload fit. It does not by itself prove production readiness.
- When benchmark evidence is used, name the workload or benchmark rather than implying a generic win.

## Rapidly Changing Sections

Sections that depend on vendor releases, product packaging, or fast-moving capabilities must include a visible `Last reviewed: Month YYYY` marker.

Apply this especially to:

- Product lists and vendor capability summaries.
- API or SDK surface comparisons.
- Operational guidance tied to current releases, policies, or benchmark availability.

If a rapidly changing section has an old review date, treat it as historical until it is refreshed.

## Contribution Rules

- Prefer official docs, architecture guides, papers, benchmark repos, or first-party code repositories.
- Use `[field report]` for claims about real-world deployment behaviour, not for vendor promises.
- Keep benchmark evidence separate from ecosystem maturity, governance fit, or workload suitability.
- Use `[author assessment]` when the repository is making a synthesis or tradeoff judgment rather than restating a source.
