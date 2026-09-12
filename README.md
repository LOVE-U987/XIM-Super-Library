# XIM Super Library | XIM超级图书馆 - Skill分支

## 简介

XIM超级图书馆的 AI 能力扩展模块库。Skill 是帮助 AI 在开发过程中获取相关帮助信息的模块，AI 可通过通用性 Skill 在图书馆中检索资源。

## 目录结构

```
skill/
├── minecraft/      # Minecraft模组开发
├── web/            # Web开发
├── tools/          # 工具使用
├── rules/          # 规则文档
├── examples/       # 示例Skill
└── README.md       # 本文件
```

## 标签体系

标签是知识库资源定位的核心依据，完整定义见 [提交规则](rules/commit_rules.md)。主标签：

我的世界开发 · 网页开发 · UI与动画 · 项目结构规范 · 重构审查规范 · 逻辑规范 · 代码质量规范 · 个人规则 · 项目规则 · 特定模组开发 · 图形化UI布局 · Skills

## Skill 分类

### Minecraft 模组开发

| Skill | 说明 | 标签 |
|-------|------|------|
| [neoforge-item-modify-workflow](minecraft/neoforge-item-modify-workflow/SKILL.md) | NeoForge物品属性修改工作流 | 我的世界开发、特定模组开发 |
| [attribute-modify](minecraft/attribute-modify/SKILL.md) | 属性修改API参考 | 我的世界开发、特定模组开发 |
| [legendary-mage-trail-system](minecraft/legendary-mage-trail-system/SKILL.md) | 拖尾特效系统 | 我的世界开发、特定模组开发、图形化UI布局 |
| [irons-spells-neoforge-1.21.1](minecraft/irons-spells-neoforge-1.21.1/SKILL.md) | Iron's Spells法术开发 | 我的世界开发、特定模组开发 |
| [tacz-recipe-1.20.1](minecraft/tacz-recipe-1.20.1/SKILL.md) | TaCZ配方转换 | 我的世界开发、特定模组开发 |
| [neoforge-1.21.1-config-screen](minecraft/neoforge-1.21.1-config-screen/SKILL.md) | 配置界面渲染开发 | 我的世界开发、图形化UI布局 |
| [kubejs-neoforge-1.21.1](minecraft/kubejs-neoforge-1.21.1/SKILL.md) | KubeJS NeoForge开发 | 我的世界开发 |
| [kubejs-forge-1.20.1](minecraft/kubejs-forge-1.20.1/SKILL.md) | KubeJS Forge开发 | 我的世界开发 |
| [pasterdream-dimension-api](minecraft/pasterdream-dimension-api/SKILL.md) | 维度注册API | 我的世界开发、特定模组开发 |
| [neoforge-1.21.1-config-ui](minecraft/neoforge-1.21.1-config-ui/SKILL.md) | 配置界面双方案指南 | 我的世界开发、UI与动画、图形化UI布局 |
| [modern-ui](minecraft/modern-ui/SKILL.md) | Modern UI框架 | 我的世界开发、UI与动画、图形化UI布局 |
| [api-split-multi-module](minecraft/api-split-multi-module/SKILL.md) | 多模块架构 | 我的世界开发、项目结构规范 |

### Web 开发

| Skill | 说明 | 标签 |
|-------|------|------|
| [frontend-design](web/frontend-design/SKILL.md) | 前端界面设计 | 网页开发、UI与动画 |
| [frontend-skill](web/frontend-skill/SKILL.md) | 前端开发技能 | 网页开发、UI与动画 |
| [shadcn](web/shadcn/SKILL.md) | shadcn组件库 | 网页开发、UI与动画 |
| [gsap](web/gsap/SKILL.md) | GSAP动画库 | 网页开发、UI与动画 |
| [animejs](web/animejs/SKILL.md) | Anime.js动画 | 网页开发、UI与动画 |
| [interaction-design](web/interaction-design/SKILL.md) | 交互设计 | 网页开发、UI与动画 |
| [theme-factory](web/theme-factory/SKILL.md) | 主题工厂 | 网页开发、UI与动画 |
| [web-design-guidelines](web/web-design-guidelines/SKILL.md) | Web设计指南 | 网页开发、UI与动画 |

### 工具使用

| Skill | 说明 | 标签 |
|-------|------|------|
| [redis-development](tools/redis-development/SKILL.md) | Redis开发 | Skills |
| [agent-browser](tools/agent-browser/SKILL.md) | 浏览器自动化 | Skills |
| [webapp-testing](tools/webapp-testing/SKILL.md) | Web应用测试 | Skills、网页开发 |
| [screenshot](tools/screenshot/SKILL.md) | 截图工具 | Skills |
| [writing-plans](tools/writing-plans/SKILL.md) | 写作计划 | Skills、项目结构规范 |
| [brainstorming](tools/brainstorming/SKILL.md) | 头脑风暴 | Skills |
| [code-reviewer](tools/code-reviewer/SKILL.md) | 代码审查 | Skills、重构审查规范 |
| [gh-cli](tools/gh-cli/SKILL.md) | GitHub CLI | Skills |
| [git-commit](tools/git-commit/SKILL.md) | Git提交 | Skills、项目规则 |
| [algorithmic-art](tools/algorithmic-art/SKILL.md) | 算法艺术 | 网页开发、UI与动画 |

## 规则文档

| 文件 | 说明 | 标签 |
|------|------|------|
| [通用性规则](rules/general_rules.md) | Skill编写质量标准 | Skills、代码质量规范 |
| [命名规则](rules/naming_rules.md) | 资源命名规范 | Skills、项目结构规范 |
| [摆放规则](rules/placement_rules.md) | 目录组织规范 | Skills、项目结构规范 |
| [提交规则](rules/commit_rules.md) | 提交规范与标签体系 | Skills、项目规则、代码质量规范 |
| [通用性Skill](rules/universal_skill.md) | AI资源检索入口 | Skills |

## 通用性 Skill

**xim-universal-skill** 是 XIM超级图书馆的核心入口，指导 AI 理解用户需求并自动检索图书馆资源。功能：分析需求、追问缺失信息、匹配资源、返回下载链接或部署方案。工作流程：

```
用户提出需求 → AI分析需求 → 获取缺失信息 → 查找XIM图书馆 → 返回结果
```

## 贡献指南

- Skill 满足通用性规则、命名规则与摆放规则
- frontmatter 包含 1-3 个主标签
- 新增或变更资源后同步本 README 与分类 README
- 提交信息遵循 [提交规则](rules/commit_rules.md)

## 统计信息

- 总 Skill 数：31 个（Minecraft 12、Web 8、Tools 10、通用 1）
- 规则文档：5 篇
- 更新时间：2026-09-12
