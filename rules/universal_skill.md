---
name: xim-universal-skill
description: XIM超级图书馆核心入口，指导AI助手分析用户开发需求、检索图书馆资源并提供下载链接或部署方案。
tags: [Skills]
---

# XIM超级图书馆 - 通用性 Skill

## 简介

本 Skill 是 XIM 超级图书馆的核心入口，指导 AI 助手理解用户需求并自动检索图书馆中的开发环境和 Skill 资源。

功能：
1. 理解用户需求（环境需求、Skill 需求）
2. 主动询问缺失信息
3. 到 XIM 图书馆检索匹配资源
4. 返回下载链接或部署方案

## 工作流程

```
用户提出需求 → 分析需求 → 获取缺失信息 → 查找资源 → 返回结果
```

## 需求分析

### 1. 识别需求类型

| 需求类型 | 关键词 | 示例 |
|---------|-------|------|
| 环境部署 | 环境、配置、安装、搭建 | "我要配置一个1.20.1 Forge环境" |
| Skill获取 | 技能、api、开发指南、参考 | "我需要NeoForge物品修改的API" |
| 混合需求 | 既需要环境又需要Skill | "我要开发1.21.1 NeoForge模组" |

### 2. 提取关键信息

- 环境部署：框架（Forge/Fabric/NeoForge）、Minecraft版本、部署路径（可选）
- Skill获取：技术栈（minecraft/web/tools）、具体主题、版本要求（如有）

### 3. 信息缺失时的询问策略

按顺序追问：
1. 框架："您需要哪种框架？(Forge / Fabric / NeoForge)"
2. 版本："您需要哪个版本？(如：1.21.1)"
3. 主题："您具体需要哪方面的帮助？"

## 资源定位

### 1. 环境资源（按 GitHub 分支）

| 框架 | 分支名 | 文件格式 |
|------|--------|---------|
| Forge | `Forge` | Forge-{version}-{build}.7z |
| Fabric | `Fabric` | Fabric-{version}-{loader}.7z |
| NeoForge | `NeoForge` | NeoForge-{version}-{build}.7z |

URL 格式：`https://raw.githubusercontent.com/LOVE-U987/XIM-Super-Library/{branch}/{filename}`

### 2. Skill 资源（skill 分支）

按类别组织：`minecraft/`（模组开发）、`web/`（Web开发）、`tools/`（工具使用）。

文件结构：
```
skill/{category}/{skill-name}/
├── SKILL.md              # 主Skill文档
├── references/           # 参考文档（如有）
└── README.md             # 说明文档（如有）
```

URL 格式：`https://raw.githubusercontent.com/LOVE-U987/XIM-Super-Library/skill/{category}/{skill-name}/SKILL.md`

### 3. 资源检索方法

- GitHub API：`GET https://api.github.com/repos/LOVE-U987/XIM-Super-Library/git/trees/{branch}?recursive=1`
- 分支文件列表：浏览 `https://github.com/LOVE-U987/XIM-Super-Library/tree/{branch}`
- 关键词匹配：根据需求关键词匹配文件名，如"1.20.1 Forge" → `Forge-1.20.1*.7z`

### 4. 按标签定位

各 Skill 的 frontmatter 包含主标签与二级标签，完整标签体系见 [提交规则](commit_rules.md)。AI 可按标签（如"我的世界开发""特定模组开发"）快速筛选匹配资源。

## 结果返回

### 环境部署结果

```
✅ 找到您需要的开发环境！
- 框架：{框架名称}
- 版本：{版本号}
- 文件大小：{大小}

⬇️ 下载链接：
{下载URL}

安装说明：
1. 下载压缩包
2. 解压到开发目录
3. 使用IDE打开

💡 提示：您可能还需要以下Skill：
- {相关Skill名称1} - {描述}
```

### Skill 获取结果

```
✅ 找到您需要的Skill！
- 名称：{Skill名称}
- 类别：{类别}

内容摘要：{Skill简介}
详细文档：{Skill文件URL}

💡 配合以下Skill使用效果更好：
- {相关Skill名称} - {描述}
```

### 未找到资源

```
❌ 未找到您需要的资源

可能的原因：
- 版本号输入有误
- 框架名称不正确
- 该资源尚未添加到图书馆

建议：检查输入，或提交Issue：
https://github.com/LOVE-U987/XIM-Super-Library/issues/new
```

## AI 行为准则

1. **主动询问**：信息不足时主动追问，直到获得足够信息
2. **智能匹配**：结合用户上下文推荐资源（如开发 1.21.1 NeoForge 模组时推荐环境包 + neoforge-item-modify-workflow + attribute-modify）
3. **推荐相关资源**：找到目标资源后主动推荐配套 Skill
4. **使用中文回复**：保持友好、专业的语气

## 下载加速策略

国内用户直接访问 `raw.githubusercontent.com` 下载环境包会遇到下载极慢、易断连的问题，按以下三级方案加速：

### 方案一：ghproxy 镜像（中国境内首选）

```
原始:  https://raw.githubusercontent.com/{repo}/{branch}/{file}
加速:  https://ghproxy.com/https://raw.githubusercontent.com/{repo}/{branch}/{file}
```

检测到用户在中国境内时优先使用 ghproxy；不可用则降级到原始 URL。

### 方案二：git clone 深度克隆（最稳定）

```bash
git clone --depth 1 --single-branch -b Forge https://github.com/LOVE-U987/XIM-Super-Library.git forge-env
# 配合ghproxy（中国境内极速）
git clone --depth 1 --single-branch -b Forge https://ghproxy.com/https://github.com/LOVE-U987/XIM-Super-Library.git forge-env
```

优势：git 协议传输快、`--depth 1` 体积最小、支持断点续传。

### 方案三：aria2 多线程下载（极致速度）

```bash
aria2c -x 16 -s 16 -k 1M https://ghproxy.com/https://raw.githubusercontent.com/LOVE-U987/XIM-Super-Library/Forge/Forge-1.20.1-47.4.10.7z
```

未安装时可引导用户安装：`winget install aria2`

### 方案选择优先级

```
中国境内  →  ghproxy + git clone（推荐）→ ghproxy + aria2 → ghproxy + Python下载
中国境外  →  git clone（推荐）→ aria2 → raw GitHub
```

## 注意事项

1. **版本匹配**：确保环境版本与 Skill 版本匹配
2. **网络问题**：ghproxy 不可用时降级到原始 GitHub URL
3. **资源更新**：图书馆资源定期更新，建议定期检查新版本
4. **反馈建议**：找不到资源时提交 Issue

## 相关资源

- [XIM超级图书馆GitHub](https://github.com/LOVE-U987/XIM-Super-Library)
- [通用性规则](general_rules.md)
- [命名规则](naming_rules.md)
- [摆放规则](placement_rules.md)
- [提交规则](commit_rules.md)
