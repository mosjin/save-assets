# Changelog

本项目所有重要变更记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [2.1.0] — 2026-08-13

### 🚀 Feature — 检索侧、状态作废、已验证能力台账

一次真实的失败复盘：某次会话把「某能力已验证可用」准确地存进了 CHANGELOG，但几天后仍然断言「那个能力可能还没做好」——问题不在存，在**存了却没查**；而且记忆里一句过期的「正在做 X」比正确的记录更容易被读到、被相信。这次改动把 skill 从「只讲怎么存」扩展到「也讲什么时候该查、旧记录什么时候该退休」：

- **新增 Step -1：断言之前先检索** —— 之前 Step 0 到 Step 7 全是「怎么存」，没有一步讲「什么时候该去查已存的东西」。现在写任何「可能没做 / 还没建好 / 不可用 / 最可能的解释是…」这类关于项目状态的否定或猜测之前，必须先 `grep` 文档目录、查 issue 历史；查不到才能说「不清楚」。核心教训：进行时的记忆没有日期，不能推出「现在还没做」。
- **新增第八类资产「已验证能力状态」+ Step 5c：更新 VERIFIED_FACTS.md** —— 区分「架构/偏好/约束」这类基本不过期的持久事实，和「某功能已验证可用」「某权限已授予」这类**会过期**的能力状态。新模板五个必填字段：事实、验证日期、证据、谁验的、失效条件。并加规则：台账里的事实只能被新证据推翻，不能被推理推翻。
- **Step 6 新增 6d：作废已被取代的状态** —— 原 Step 1/6a 只讲「只写新内容，不重复」，没有一条讲「进行时状态变成完成时之后，要回去把旧记录改掉」。CHANGELOG 是流水账（append-only 正确），但记忆文件 / 交接便条是状态不是历史，需要单独的作废规则。
- **Step 5b（LESSONS）新增「判断失误」子模板** —— 原模板偏技术坑，装不下「推理链哪一步歪了」。新增三问：错判了什么、依据是什么、依据本身错在哪、下次该先查什么。
- **Step 0 的内容检查门槛补一问** —— 「之前记录过的事实，状态变了吗」，覆盖「能力从未验证变已验证」「阻塞解除」这类原先会被漏检的信号。

同步更新全部 6 个 SKILL.md 变体（bilingual / EN / ZH × `.claude/skills/` + `skills/`）：Step -1、Step 5c、Step 6d 三处新锚点；Step 1 采集表、Asset Locations 表新增 VERIFIED_FACTS 行；Step 7 `git add` 新增 `docs/VERIFIED_FACTS.md`；Checklist 新增对应条目。README / README_EN 同步功能列表与步骤总览。

## [2.0.0] — 2026-07-12

### ⚠️ Breaking — 重命名 skill / plugin

- **`save-project-assets` → `save-assets`**：斜杠命令由 `/save-project-assets` 缩短为 `/save-assets`（三变体同步：`save-assets` · `save-assets-en` · `save-assets-zh`）。命令更短好记。
- 目录重命名（`git mv` 保留历史）：`skills/` 与 `.claude/skills/` 下各 3 个 skill 目录。
- plugin 名与 marketplace 名同步改为 `save-assets`；`repository` 字段指向新仓库名。
- README / README_EN / install.py / hooks/settings-example.json 中的引用级联更新。
- **升级须知**：已安装用户需按新名 `save-assets` 重新触发；GitHub 仓库已改名，旧 URL 由 GitHub 自动重定向，经 git 安装的用户不受影响。因 plugin 名变更属破坏性，按 semver 升为主版本号 **2.0.0**。

## [1.4.0] — 2026-07-03

### 🚀 Feature

- **新增 LESSONS.md 教训类别** — 与 IDEAS 平级的一等资产。语义分工：`TECH_LOG.md` 为流水日志（工程经验、根因），`LESSONS.md` 为教训要点（踩过的坑 / 根因 / 下次规避，三段式模板）。
- 新增独立步骤 **Step 5b：更新 LESSONS.md**（三语：bilingual `## Step 5b` · EN `## Step 5b` · ZH `## 第五步之二`）。
- 同步更新全部 6 个 SKILL.md 变体（bilingual / EN / ZH × `.claude/skills/` + `skills/`）：Step 1 采集表新增 Lessons 行、Asset Locations 表新增 LESSONS 行、Step 7 `git add` 新增 `docs/LESSONS.md`、Checklist 新增 LESSONS 条目。
- README 同步：功能列表、步骤表、文件名约定注记均加入 LESSONS。

## [1.3.0] — 2026-07-01

### 🚀 Feature

- **Step 3b：新增更新 README.md 步骤** — 保存工作流在写完 CHANGELOG 后，自动检查并更新 README 中受影响章节（功能列表、变更记录、已知问题、安装说明），只改有变化的部分。
- 同步更新全部 6 个 SKILL.md 变体（bilingual / EN / ZH × `.claude/skills/` + `skills/`）。
- Step 1 采集表新增 `README summary` 行；Step 7 `git add` 新增 `README.md`；Checklist 增加 README 条目。

---

## [1.2.0] — 2026-06-17

### 🐛 Fixed — 通用性修复 续（[#1](https://github.com/mosjin/save-project-assets/issues/1)）

- **Step 7 不再无条件 `git push`**：受保护 / 需 review 分支上 commit 后停止，交由用户 push 或开 PR（3 变体）。
- **zh 变体补齐 auto-detect**：新增「第零步b 自动检测项目上下文」（含 `GIT_HOST` 与非 GitHub 跳过逻辑），移除 #1 引入的冗余内联 guard；资产表不再要求手填仓库；Step 4 占位符统一为已解析的 `{GITHUB_REPO}`（3 变体）。

### 📝 Docs

- README / README_EN：说明文档文件名为约定俗成、可在 SKILL.md 改名。

## [1.1.0] — 2026-06-17

### 🐛 Fixed — 通用性修复（[#1](https://github.com/mosjin/save-project-assets/issues/1)）

- **Step 4 不再假设 host = GitHub**：Step 0b 现解析 remote host 并存为 `GIT_HOST`；当 host 非 `github.com`（GitLab / Bitbucket / Gitea）时静默跳过 Issue 评论步骤。此前仅"无 remote"才跳过，非 GitHub 仓库会执行 `gh issue comment` 报错。（3 变体均修复，zh 变体以 Step 4 内联 guard 实现）
- **default 变体不再强制双语**：新增 **Language / 语言** 指令——自动识别工作语言（依据项目现有文档 / 对话语言），仅以单一语言写入。修复 README 宣称"自动识别语言"与默认模板硬编码双语 header 的矛盾。

### 📝 Docs

- README.md / README_EN.md：auto-detect 段补充 **Remote host** 检测与非 GitHub 跳过、default 语言自适应说明。

### 审计结论

`save-project-assets` 通用性审计（见 #1）：无项目专属硬编码（通过 ✅）；本次修复 2 项真正的"不通用"阻断点。剩余改进项（Step 7 自动 push 可选化、zh 变体 auto-detect 同步、固定文档名可覆盖）在 #1 中跟踪。
