---
name: save-project-assets
description: Use proactively when user confirms something works ("it works", "verified", "已修复"), before session ends / context compaction, or when user explicitly asks ("save assets", "save project", "保存资产", "update docs", "update memory"). Do NOT trigger on every git commit — only when there is new knowledge worth persisting.
---

# Save Project Assets

<!-- ─────────────────────────────────────────────
  CONFIG — optional overrides only.
  All values are auto-detected from git if not set here.
  ───────────────────────────────────────────── -->
<!--
  GITHUB_REPO = owner/repo   (override only — auto-detected from git remote)
  DOCS_DIR    = docs/        (override only — auto-detected by checking ./docs/)
  BRANCH      = main         (override only — auto-detected from git branch)
-->

## Overview

Capture and persist all knowledge generated in this session: engineering lessons, feature status, fixed issues, ideas, lessons learned, and memory updates.

**Language / 语言:** Auto-detect the working language — match the project's existing docs (TECH_LOG/CHANGELOG), falling back to the user's conversation language. Write each entry in that **single** language. The bilingual headers shown in the templates below are illustrative; emit only the detected language, not both.

**Announce at start:** "Saving project assets… / 正在保存项目资产…"

---

### Trigger Conditions — When to Run

**✅ Run proactively (without being asked):**
| Signal | Example |
|--------|---------|
| User confirms something works | "it works", "verified", "test passed", "已修复", "验证通过" |
| Session ending / context nearing full | Before `/compact`, before long pause |
| Feature branch merged to main | After `git merge` or PR merged |

**✅ Run on explicit request:**
| Phrase | Intent |
|--------|--------|
| "save assets" / "save project" / "保存资产" | Full 7-step save |
| "update docs" / "更新文档" | Steps 2-3-7 only |
| "update memory" / "更新记忆" | Step 6 only |
| "/save-project-assets" | Direct invocation |

**❌ Do NOT trigger on:**
- Every `git commit` or `git push` — too disruptive, Step 7 itself commits docs
- Generic "save" / "record" / "记录" without clear intent — too ambiguous
- Test failures or work-in-progress — nothing confirmed yet
- Small refactor / formatting commits — no new knowledge

---

**Session start:** Silently load MEMORY.md to restore context. Do not announce unless asked.

---

## Step 0: Content Check (fast gate)

Before doing anything, answer these questions:

- Did this session produce **new** engineering lessons, fixes, or architectural decisions?
- Did the user **confirm** something works?
- Are there **new** ideas or status changes not yet in docs/memory?

**If all answers are NO → stop immediately.** Say: "Nothing new to save this session."

Only continue to Step 1 if at least one answer is YES.

---

## Step 0b: Auto-Detect Project Context

Before writing anything, resolve these values (use CONFIG overrides if set, otherwise detect):

```bash
# GitHub repo  (e.g. owner/repo)
git remote get-url origin
# → parse: https://github.com/owner/repo.git  OR  git@github.com:owner/repo.git
# → extract: owner/repo
# → also note HOST: github.com / gitlab.com / bitbucket.org …

# Current branch
git branch --show-current

# Docs directory — check in order:
# 1. docs/   2. doc/   3. ./ (project root)
ls docs/ 2>/dev/null || ls doc/ 2>/dev/null || echo "use project root"
```

Store the resolved values as:
- `GITHUB_REPO` = e.g. `myorg/myrepo`
- `GIT_HOST` = host parsed from the remote URL (e.g. `github.com`, `gitlab.com`)
- `BRANCH` = e.g. `main` or `feature/xyz`
- `DOCS_DIR` = e.g. `docs/` or `./`

Use these in all subsequent steps.
- If `git remote get-url origin` fails (no remote), skip Step 4 (GitHub comments) silently.
- If `GIT_HOST` is **not** `github.com` (e.g. GitLab, Bitbucket, Gitea), skip Step 4 silently — `gh` only works with GitHub.

---

## Step 1: Harvest Session Knowledge

Before writing anything, collect from this session:

| Category | Source | Target |
|----------|--------|--------|
| Engineering lessons | Bugs fixed, root causes, architectural decisions | `docs/TECH_LOG.md` |
| Feature status | Built / tested / merged | `docs/CHANGELOG.md` |
| Fixed issues | Confirmed working by user | GitHub issue comments |
| Ideas / future work | Noticed but not implemented | `docs/IDEAS.md` |
| Lessons learned | Pitfalls, mistakes, what to avoid next time | `docs/LESSONS.md` |
| Persistent facts | Architecture, preferences, constraints | Memory files |
| README summary | New features shipped, fixed issues, install changes | `README.md` |

**Only write new entries** — never duplicate existing content.

---

## Step 2: Update TECH_LOG.md (Lessons & Experiences / 经验教训)

File: `docs/TECH_LOG.md`

Add at the **top** (newest first):

```markdown
## {YYYY-MM-DD}: {Brief title} (Issue #{N})
<!-- 中文：## {YYYY-MM-DD}：{简短标题}（Issue #{N}） -->

### Problem / 问题
{What was wrong or the challenge}

### Root Cause / 根因
{Why it happened — name the specific code/API/behavior}

### Fix / 修复方案
{What was done; include key code snippets if instructive}

### Lessons / 经验总结
- **Rule / 规则**: {actionable rule for the future}
- **Why / 原因**: {reason this matters}
```

**Skip** if no new engineering lessons this session.

---

## Step 3: Update CHANGELOG.md (Feature Status / 功能状态)

File: `docs/CHANGELOG.md`

- New feature/fix completed → add or update `[version-dev]` section at top
- Format: `### 🐛 Fix` · `### 🚀 Feature` · `### 📐 Refactor`
- Include issue numbers, key behavior changes, test counts
- **Never** repeat existing entries

---

## Step 3b: Update README.md (User-Facing Summary / 用户摘要)

File: `README.md` (project root)

Update only the sections that changed this session:

- **Features / 功能列表**: add newly shipped features
- **Changelog / 变更记录**: if README contains a short changelog block, append the latest entry
- **Known issues / 已知问题**: remove issues fixed this session; add newly discovered ones
- **Installation / 安装**: update if install steps or requirements changed

**Rules / 规则:**
- Edit only what changed — do not rewrite the entire README
- Keep changes minimal and user-facing; omit internal implementation details
- **Skip / 跳过** if no README sections are affected by this session's work

---

## Step 4: Comment on Fixed GitHub Issues / 评论已修复的 Issue

For each issue the user confirmed working this session:

```bash
gh issue comment {N} --repo {GITHUB_REPO} --body "## ✅ Fixed / 已修复

{2-3 sentences: root cause + fix approach + how it was verified}

Status: **fixed**"
```

**Only comment if the user explicitly confirmed it works.** No speculation.

---

## Step 5: Update IDEAS.md (Future Work / 未来工作)

File: `docs/IDEAS.md`

New ideas, improvements, or "noticed but not done" items:

```markdown
## {Feature area / 功能方向}

- [ ] {Specific idea} — {why it's worth doing / 为什么值得做}
```

**Skip** if nothing new.

---

## Step 5b: Update LESSONS.md (Lessons Learned / 教训)

File: `docs/LESSONS.md`

Pitfalls hit, mistakes made, what to avoid next time — distinct from TECH_LOG (a running journal); LESSONS captures the takeaway:

```markdown
## {Topic / 主题}

- **Lesson / 教训:** {what went wrong / 踩了什么坑}
  - **Why / 原因:** {root cause / 根因}
  - **Avoid / 规避:** {how to not repeat it / 下次怎么避免}
```

**Skip** if nothing new.

---

## Step 6: Update Persistent Memory / 更新持久记忆

Memory location: auto-detected by Claude Code at `~/.claude/projects/{sanitized-cwd}/memory/`

### 6a. Update MEMORY.md index
- Add pointer for any new memory file
- Update changed facts (new test count, new branch, new version, new lesson)

### 6b. Write/update memory files as needed

**When to create a new memory file:**
- New architectural pattern discovered
- Engineering lesson with future applicability
- Project status change (new branch, feature shipped, new issue pattern)
- User preference or workflow correction

**Memory file format:**
```markdown
---
name: {topic}
description: {one-line description for relevance matching}
type: project | feedback | user | reference
---

{Content}
**Why:** {motivation}
**How to apply:** {when this matters}
```

### 6c. Key facts to keep current
- Active branch and its purpose
- Latest test count
- Latest release version/artifact name
- Fixed issues list (append newly fixed)
- New engineering lessons

---

## Step 7: Commit Docs / 提交文档

If `docs/` files were modified:

```bash
git add docs/TECH_LOG.md docs/CHANGELOG.md docs/IDEAS.md docs/LESSONS.md README.md
git commit -m "docs: {brief description of what was recorded}"
# Push ONLY if direct pushes to this branch are allowed.
# On protected / review-required branches, stop after commit and
# let the user push or open a PR instead.
git push origin {current-branch}
```

---

## Session Start Protocol / 会话开始协议

On the first message of a new session:

1. Claude Code auto-loads MEMORY.md — silently absorb the facts
2. Note: active branch, open issues, recent lessons, last test count
3. Be ready to answer project-state questions without re-reading source files
4. If user references recent work, confirm context: "I have context from the previous session: {key facts}."

---

## Asset Locations (all auto-detected)

| Asset | Auto-detected path |
|-------|-------------------|
| Tech lessons | `{DOCS_DIR}/TECH_LOG.md` |
| Changelog | `{DOCS_DIR}/CHANGELOG.md` |
| Ideas | `{DOCS_DIR}/IDEAS.md` |
| Lessons | `{DOCS_DIR}/LESSONS.md` |
| Architecture | `{DOCS_DIR}/ARCHITECTURE.md` |
| Memory | `~/.claude/projects/{sanitized-cwd}/memory/MEMORY.md` |
| GitHub repo | parsed from `git remote get-url origin` |
| Branch | from `git branch --show-current` |

---

## Checklist

- [ ] TECH_LOG updated (or confirmed nothing new)
- [ ] CHANGELOG updated (or confirmed nothing new)
- [ ] README.md updated (or confirmed nothing new)
- [ ] Fixed GitHub issues commented
- [ ] IDEAS.md updated (or confirmed nothing new)
- [ ] LESSONS.md updated (or confirmed nothing new)
- [ ] Memory files updated with current facts
- [ ] Docs committed and pushed
