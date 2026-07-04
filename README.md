# 🚩 XIM Super Library | XIM超级图书馆 - Skill分支

## 🎉 欢迎来到XIM超级图书馆Skill分支 🎉

### 🧠 什么是Skill

Skill是XIM超级图书馆的AI能力扩展模块，用于帮助AI在开发过程中获取相关的帮助信息。

### 📚 如何使用

AI可以通过通用性skill来收集相应的信息，在XIM图书馆里获取帮助。

### 📂 目录结构

```
skill/
├── minecraft/                # Minecraft模组开发
│   ├── neoforge/             # NeoForge相关Skill
│   ├── forge/                # Forge相关Skill
│   └── fabric/               # Fabric相关Skill
├── web/                      # Web开发
│   ├── frontend/             # 前端开发Skill
│   └── backend/              # 后端开发Skill
├── tools/                    # 工具使用
│   ├── devops/               # DevOps工具
│   └── utilities/            # 实用工具
├── rules/                    # 规则文档
│   ├── general_rules.md      # 通用性规则
│   ├── naming_rules.md       # 命名规则
│   └── placement_rules.md    # 摆放规则
├── examples/                 # 示例Skill
│   └── sample-skill.md       # 示例Skill文件
└── README.md                 # 本文件
```

### 📦 Skill分类

#### 🏗️ Minecraft模组开发
| Skill | 说明 |
|-------|------|
| [neoforge-item-modify-workflow](minecraft/neoforge-item-modify-workflow/SKILL.md) | NeoForge物品属性修改工作流 |
| [attribute-modify](minecraft/attribute-modify/SKILL.md) | 属性修改API参考 |
| [legendarymage-trail-system](minecraft/legendarymage-trail-system/SKILL.md) | 拖尾特效系统 |
| [irons-spells-neoforge-1-21-1](minecraft/irons-spells-neoforge-1-21-1/SKILL.md) | Iron's Spells法术开发 |
| [tacz-recipe](minecraft/tacz-recipe/SKILL.md) | TaCZ配方转换 |
| [neoforge-1.21.1-config-screen](minecraft/neoforge-1.21.1-config-screen/SKILL.md) | 配置界面开发 |
| [kubejs-neoforge-1.21.1](minecraft/kubejs-neoforge-1.21.1/SKILL.md) | KubeJS NeoForge开发 |
| [kubejs-forge-1.20.1](minecraft/kubejs-forge-1.20.1/SKILL.md) | KubeJS Forge开发 |
| [pasterdream-dimension-api](minecraft/pasterdream-dimension-api/SKILL.md) | 维度注册API |
| [mc-config-ui](minecraft/mc-config-ui/SKILL.md) | 配置界面开发指南 |
| [modern-ui](minecraft/modern-ui/SKILL.md) | Modern UI框架 |
| [api-split-multi-module](minecraft/api-split-multi-module/SKILL.md) | 多模块架构 |

#### 🌐 Web开发
| Skill | 说明 |
|-------|------|
| [frontend-design](web/frontend-design/SKILL.md) | 前端界面设计 |
| [frontend-skill](web/frontend-skill/SKILL.md) | 前端开发技能 |
| [shadcn](web/shadcn/SKILL.md) | shadcn组件库 |
| [gsap](web/gsap/SKILL.md) | GSAP动画库 |
| [animejs](web/animejs/SKILL.md) | Anime.js动画 |
| [interaction-design](web/interaction-design/SKILL.md) | 交互设计 |
| [theme-factory](web/theme-factory/SKILL.md) | 主题工厂 |
| [web-design-guidelines](web/web-design-guidelines/SKILL.md) | Web设计指南 |

#### 🛠️ 工具使用
| Skill | 说明 |
|-------|------|
| [redis-development](tools/redis-development/SKILL.md) | Redis开发 |
| [agent-browser](tools/agent-browser/SKILL.md) | 浏览器自动化 |
| [webapp-testing](tools/webapp-testing/SKILL.md) | Web应用测试 |
| [screenshot](tools/screenshot/SKILL.md) | 截图工具 |
| [writing-plans](tools/writing-plans/SKILL.md) | 写作计划 |
| [brainstorming](tools/brainstorming/SKILL.md) | 头脑风暴 |
| [code-reviewer](tools/code-reviewer/SKILL.md) | 代码审查 |
| [gh-cli](tools/gh-cli/SKILL.md) | GitHub CLI |
| [git-commit](tools/git-commit/SKILL.md) | Git提交 |
| [algorithmic-art](tools/algorithmic-art/SKILL.md) | 算法艺术 |

### 🧠 通用性Skill

**xim-universal-skill** 是XIM超级图书馆的核心入口，用于指导AI助手理解用户需求并自动到图书馆获取资源。

**功能**:
- 🤖 理解用户的开发需求（环境需求、Skill需求）
- ❓ 主动询问用户以获取足够的信息
- 🔍 到XIM图书馆查找匹配的资源
- 📤 为用户提供下载链接或部署方案

**工作流程**:
```
用户提出需求 → AI分析需求 → 获取缺失信息 → 查找XIM图书馆 → 返回结果
```

**示例对话**:
```
用户: 我要配置一个1.20.1 Forge环境
AI:   ✅ 找到您需要的开发环境！
      
      📦 Forge 1.20.1
      ⬇️ 下载链接: https://xxx
      
      💡 推荐配合以下Skill使用：
      - kubejs-forge-1.20.1 - KubeJS开发
```

**文档**: [universal_skill.md](rules/universal_skill.md)

### 🎯 贡献指南

- 确保您的skill满足通用性规则
- 满足命名规则与摆放规则
- 提交PR前请确保测试通过

---

**🚀 开始贡献您的Skill，让AI更加强大！**

### 📊 统计信息

- **总Skill数**: 31个（含通用性Skill）
- **Minecraft类别**: 12个
- **Web类别**: 8个
- **Tools类别**: 10个
- **通用性Skill**: 1个
- **更新时间**: 2026-07-05
