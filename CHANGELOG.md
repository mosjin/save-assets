# Changelog

本项目所有重要变更记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

## [Unreleased]

### 🐛 Fixed — 通用性修复（[#1](https://github.com/mosjin/save-project-assets/issues/1)）

- **Step 4 不再假设 host = GitHub**：Step 0b 现解析 remote host 并存为 `GIT_HOST`；当 host 非 `github.com`（GitLab / Bitbucket / Gitea）时静默跳过 Issue 评论步骤。此前仅"无 remote"才跳过，非 GitHub 仓库会执行 `gh issue comment` 报错。（3 变体均修复，zh 变体以 Step 4 内联 guard 实现）
- **default 变体不再强制双语**：新增 **Language / 语言** 指令——自动识别工作语言（依据项目现有文档 / 对话语言），仅以单一语言写入。修复 README 宣称"自动识别语言"与默认模板硬编码双语 header 的矛盾。

### 📝 Docs

- README.md / README_EN.md：auto-detect 段补充 **Remote host** 检测与非 GitHub 跳过、default 语言自适应说明。

### 审计结论

`save-project-assets` 通用性审计（见 #1）：无项目专属硬编码（通过 ✅）；本次修复 2 项真正的"不通用"阻断点。剩余改进项（Step 7 自动 push 可选化、zh 变体 auto-detect 同步、固定文档名可覆盖）在 #1 中跟踪。
