# Inclusion Economics Handbook

Source for the IE Research Handbook — a living handbook for research staff at
[YIE](https://egc.yale.edu/ie), [IEIC](https://krea.edu.in/ieindia/), and
[IEN](https://govlab.com.np/).

> **Live site:** https://handbook.inclusioneconomics.org *(once deployed and
> domain configured)*

## Quick links

- **Read the handbook:** [https://&lt;ORG&gt;.github.io/&lt;REPO&gt;/](https://&lt;ORG&gt;.github.io/&lt;REPO&gt;/)
- **Suggest a change:** click _Edit this page_ on any handbook page
- **Contributing guide:** [`contributing.qmd`](./contributing.qmd) (also rendered on the site)
- **Page template:** [`templates/_page-template.qmd`](./templates/_page-template.qmd)

## Working locally

```bash
# Install Quarto (one-time)
brew install --cask quarto                   # macOS; see quarto.org for others

# Clone and preview
git clone https://github.com/hks-epod/inclusion-economics-handbook.git
cd inclusion-economics-handbook
quarto preview                                # live-reload at http://localhost:4848
```

## Deployment

A push to `main` triggers `.github/workflows/publish.yml`, which renders the
site and deploys to GitHub Pages.

To enable Pages on the repo:

1. **Settings → Pages → Source:** GitHub Actions.
2. Custom domain: add `CNAME` file at the repo root with your domain, then
   configure DNS to point at GitHub Pages.

## Pre-wired integrations

These are configured in `_quarto.yml` but commented out. Activate by replacing
the `REPLACE_ME` placeholders and uncommenting:

| Integration | Purpose                                  | Setup link                                          |
|---          |---                                       |---                                                  |
| Algolia DocSearch | Full-text search                   | https://docsearch.algolia.com/apply/                |
| Giscus      | Per-page comments via GitHub Discussions | https://giscus.app                                  |
| Umami       | Privacy-friendly analytics               | https://umami.is/  (cloud) or self-host             |
| Cloudflare Access | Gating before public launch        | https://www.cloudflare.com/products/zero-trust/access/ |

## Stale-content automation

A monthly cron in `.github/workflows/stale-pages.yml` runs
`scripts/check_stale_pages.py`, which opens a GitHub issue for any page whose
`last-reviewed` frontmatter is more than 365 days old. Adjust the threshold
via the `STALE_THRESHOLD_DAYS` env var in the workflow.

## Repo structure

```
.
├── _quarto.yml              # Site config: navbar, sidebar, integrations
├── _variables.yml           # Centralized links/emails (referenced via {{< meta var.x >}})
├── theme.scss               # Light theme overrides + status badge styles
├── theme-dark.scss          # Dark mode overrides
├── styles.scss              # Per-deployment customization (kept empty)
├── index.qmd                # Homepage
├── contributing.qmd         # How to contribute
├── glossary.qmd             # IE acronyms
├── about.qmd                # Handbook governance & stack
├── _partials/               # Reusable includes (status banner, analytics, feedback)
├── templates/_page-template.qmd  # Copy-paste skeleton for new pages
├── start-here/              # Role-based curated paths
├── working-at-ie/           # Lifecycle section index pages...
├── research-design/
├── field-planning/
├── implementation/
├── data-collection/
├── data-analysis/
├── project-management/
├── scripts/check_stale_pages.py
├── .github/workflows/       # publish.yml + stale-pages.yml
├── .github/CODEOWNERS       # Auto-review assignment
└── .github/PULL_REQUEST_TEMPLATE.md
```

## Page template basics

Every content page has YAML frontmatter:

```yaml
---
title: "Page title"
status: "draft"                 # draft | in-review | approved | archived
last-reviewed: "YYYY-MM-DD"
owner-role: "Role responsible"
hubs: ["YIE", "IEIC", "IEN"]
---

{{< include /_partials/_status-banner.qmd >}}

::: {.tldr}
Two to four sentences.
:::
```

See `templates/_page-template.qmd` for the full skeleton.

## License

Content: CC-BY-4.0 unless otherwise noted. Code (workflows, scripts, theme):
MIT.
