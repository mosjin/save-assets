# save-assets

> Proactively save all project knowledge at commit time or on demand.

[中文](README.md)

A [Claude Code](https://claude.ai/code) skill that automatically persists all knowledge generated during a session:

- 📋 **TECH_LOG** — Engineering lessons & root-cause analyses
- 📝 **CHANGELOG** — Feature status & fix records
- 💬 **GitHub Issues** — Auto-comment confirmed fixes
- 💡 **IDEAS** — Future work & improvement notes
- 🧠 **Memory** — Persistent cross-session context

Three variants: **中文 (zh)** · **English (en)** · **auto-detect (default)**

---

## Install

Hosted as a Claude Code plugin marketplace on GitHub.

### Recommended: Plugin install (2 commands)

**Step 1: Add the marketplace**

```
/plugin marketplace add mosjin/save-assets
```

**Step 2: Install the plugin**

```
/plugin install save-assets
```

Done. The skill is now available in your Claude Code session.

### Alternative B: one-command script

```bash
git clone https://github.com/mosjin/save-assets
cd save-assets
python install.py
```

Then run `/reload-plugins` inside Claude Code. To uninstall: `python install.py --remove`.

### Alternative C: manual JSON

Add to `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "save-assets": {
      "source": { "source": "github", "repo": "mosjin/save-assets" }
    }
  },
  "enabledPlugins": {
    "save-assets@save-assets": true
  }
}
```

Then `/reload-plugins`.

---

## Usage

```
/save-assets        # auto language
/save-assets-zh     # Chinese
/save-assets-en     # English
```

**Auto-triggers** (no command needed) when you say: `save assets` · `update docs` · `update memory`

---

## Workflow (7 steps)

| Step | Action |
|------|--------|
| 0 | Content check — exit immediately if nothing new |
| 1 | Harvest session knowledge |
| 2 | Update `docs/TECH_LOG.md` with lessons |
| 3 | Update `docs/CHANGELOG.md` with feature status |
| 4 | Comment on confirmed-fixed GitHub issues |
| 5 | Update `docs/IDEAS.md` with new ideas |
| 6 | Update Claude Code auto-memory (MEMORY.md) |
| 7 | `git add docs/ && git commit && git push` |

---

## Trigger Conditions

**Proactive (no explicit request needed):**

| Signal | Example |
|--------|---------|
| User confirms something works | "it works", "verified", "test passed" |
| Session ending / context nearing full | Before `/compact` |
| Feature branch merged to main | After PR merge |

**Do NOT trigger on:** every `git commit` (too disruptive — Step 7 itself commits docs), generic "save"/"record" without clear intent, test failures, small formatting commits.

---

## Configuration (optional)

All values are **auto-detected from git** — no configuration required in most cases.

The skill automatically detects:
- **GitHub repo** — from `git remote get-url origin`
- **Remote host** — parsed from the remote URL (`github.com` / `gitlab.com` / …)
- **Current branch** — from `git branch --show-current`
- **Docs directory** — checks `docs/`, then `doc/`, then project root

> 🌐 Non-GitHub repos (GitLab / Bitbucket / Gitea) **skip the Issue-comment step automatically** — `gh` only works with GitHub.
> 🈳 The default variant **auto-detects the working language** (from existing docs / conversation) and writes in a single language — no forced bilingual output.

To override, open the installed SKILL.md and uncomment the CONFIG block:

```markdown
<!-- CONFIG — optional overrides only
  GITHUB_REPO = owner/repo   (override only — auto-detected from git remote)
  DOCS_DIR    = docs/        (override only — auto-detected by checking ./docs/)
  BRANCH      = main         (override only — auto-detected from git branch)
-->
```

> 📄 Doc filenames (`TECH_LOG.md` / `CHANGELOG.md` / `IDEAS.md`) are conventions — rename them in SKILL.md if your project already uses different names.

Memory path is auto-detected by Claude Code — no setup needed.

---

## Optional: Hooks

Copy entries from `hooks/settings-example.json` into `~/.claude/settings.json`:

- **SessionStart hook** — injects a skill reminder into Claude's context every session
- **Stop hook** — reminds Claude to save when the session ends

---

## Directory Structure

```
save-assets/
├── install.py                              ← fallback one-command installer
├── .claude-plugin/
│   ├── plugin.json                         ← plugin metadata
│   └── marketplace.json                    ← GitHub marketplace manifest
├── .claude/skills/
│   ├── save-assets/SKILL.md        ← bilingual default
│   ├── save-assets-zh/SKILL.md     ← Chinese
│   └── save-assets-en/SKILL.md     ← English
├── hooks/settings-example.json             ← hook configuration example
├── README.md                               ← 中文文档
└── README_EN.md                            ← English docs (this file)
```

---

## Requirements

- [Claude Code](https://claude.ai/code) CLI
- `gh` CLI (for GitHub issue comments, optional)
- `git`
- A `docs/` folder in your project (or adjust paths in SKILL.md)

---

## License

MIT

---

*Extracted from real-world usage on [DiskCleaner](https://github.com/mosjin/DiskCleanerSimple).*
