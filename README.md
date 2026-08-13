# save-assets

> 在提交代码时或按需主动保存所有项目知识。

[English](README_EN.md)

一个 [Claude Code](https://claude.ai/code) skill，自动持久化 AI 助手在会话中产生的所有知识：

- 📋 **TECH_LOG** — 工程经验 & 根因分析
- 📝 **CHANGELOG** — 功能状态 & 修复记录
- 💬 **GitHub Issues** — 自动评论已修复 Issue
- 💡 **IDEAS** — 未来工作 & 改进想法
- ⚠️ **LESSONS** — 教训 & 避坑（踩过的坑、根因、规避）
- ✅ **VERIFIED_FACTS** — 已验证能力状态（事实 + 日期 + 证据 + 失效条件）
- 🧠 **Memory** — 跨会话持久上下文

支持三个版本：**中文 (zh)** · **English (en)** · **自动识别 (default)**

---

## 安装

save-assets 以 Claude Code 插件市场的形式托管在 GitHub 上。

### 推荐方式：Plugin 安装（两条命令）

**第一步：添加插件市场**

```
/plugin marketplace add mosjin/save-assets
```

**第二步：安装插件**

```
/plugin install save-assets
```

搞定。插件已在你的 Claude Code 会话中可用。

### 备用方式 B：一键脚本

```bash
git clone https://github.com/mosjin/save-assets
cd save-assets
python install.py
```

然后在 Claude Code 中运行 `/reload-plugins`。卸载：`python install.py --remove`。

### 备用方式 C：手动 JSON

在 `~/.claude/settings.json` 中添加：

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

然后 `/reload-plugins`。

---

## 使用

```
/save-assets        # 自动识别语言
/save-assets-zh     # 中文
/save-assets-en     # English
```

**自动触发**（无需输入命令）当你说：`保存资产` · `更新文档` · `更新记忆` · `save assets` · `update docs` · `update memory`

---

## 工作流（共 8 步）

| 步骤 | 操作 |
|------|------|
| -1 | 断言之前先检索——写「可能没做/还没建好」前先查文档和 issue 历史 |
| 0 | 内容检查——无新内容则立即退出 |
| 1 | 采集会话知识 |
| 2 | 更新 `docs/TECH_LOG.md` 经验教训 |
| 3 | 更新 `docs/CHANGELOG.md` 功能状态 |
| 3b | 更新 `README.md` 用户摘要（只改受影响章节） |
| 4 | 评论已确认修复的 GitHub Issue |
| 5 | 更新 `docs/IDEAS.md` 新想法 |
| 5b | 更新 `docs/LESSONS.md` 教训（踩坑/根因/规避） |
| 5c | 更新 `docs/VERIFIED_FACTS.md` 已验证能力状态（事实/日期/证据/失效条件） |
| 6 | 更新 Claude Code 自动记忆 (MEMORY.md)，含 6d 作废已被取代的进行时状态 |
| 7 | `git add docs/ README.md && git commit && git push` |

---

## 触发条件

**主动触发（无需用户明确要求）：**

| 信号 | 示例 |
|------|------|
| 用户确认功能可用 | "可以了"、"验证通过"、"it works" |
| 会话即将结束 / 上下文接近上限 | `/compact` 前 |
| 功能分支合并到 main | PR 合并后 |

**不触发：** 每次 `git commit`（太频繁）、模糊的"保存"/"记录"（意图不明）、测试失败时。

---

## 配置（选填）

所有配置项均**自动从 git 检测**，大多数情况下无需手动配置。

Skill 会自动识别：
- **GitHub 仓库** — 从 `git remote get-url origin` 解析
- **Remote host** — 从 remote URL 解析（`github.com` / `gitlab.com` / …）
- **当前分支** — 从 `git branch --show-current` 读取
- **文档目录** — 依次检测 `docs/`、`doc/`、项目根目录

> 🌐 非 GitHub 仓库（GitLab / Bitbucket / Gitea）会**自动跳过** Issue 评论步骤——`gh` 仅支持 GitHub。
> 🈳 default 版会**自动识别工作语言**（依据项目现有文档 / 对话语言），仅以单一语言写入，不强制双语。

如需覆盖，打开安装后的 SKILL.md，取消注释 CONFIG 块：

```markdown
<!-- 配置 — 选填，仅需覆盖自动检测值时填写
  GITHUB_REPO = owner/repo   （选填，自动从 git remote 检测）
  DOCS_DIR    = docs/        （选填，自动检测 ./docs/ 是否存在）
  BRANCH      = main         （选填，自动从 git branch 检测）
-->
```

> 📄 文档文件名（`TECH_LOG.md` / `CHANGELOG.md` / `IDEAS.md` / `LESSONS.md` / `VERIFIED_FACTS.md`）为约定俗成，如项目已有不同命名，可在 SKILL.md 中按需改名。

记忆路径由 Claude Code 自动检测，无需手动配置。

---

## 可选：Hooks

将 `hooks/settings-example.json` 中的内容复制到 `~/.claude/settings.json`：

- **SessionStart hook** — 每次会话注入 skill 提醒
- **Stop hook** — 会话结束时提醒保存

---

## 目录结构

```
save-assets/
├── install.py                              ← 备用一键安装脚本
├── .claude-plugin/
│   ├── plugin.json                         ← 插件元数据
│   └── marketplace.json                    ← GitHub 插件市场清单
├── .claude/skills/
│   ├── save-assets/SKILL.md        ← 双语默认版
│   ├── save-assets-zh/SKILL.md     ← 中文版
│   └── save-assets-en/SKILL.md     ← 英文版
├── hooks/settings-example.json             ← Hook 配置示例
├── README.md                               ← 中文文档（本文件）
└── README_EN.md                            ← English docs
```

---

## 前置条件

- [Claude Code](https://claude.ai/code) CLI
- `gh` CLI（用于 GitHub Issue 评论，可选）
- `git`
- 项目中有 `docs/` 目录（或在 SKILL.md 中调整路径）

---

## License

MIT

---

*从 [DiskCleaner](https://github.com/mosjin/DiskCleanerSimple) 实战中提炼而来。*
