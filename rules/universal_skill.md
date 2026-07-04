# 🧠 XIM超级图书馆 - 通用性Skill

## 📋 元信息

- **名称**: xim-universal-skill
- **版本**: 1.0.0
- **作者**: XIM Super Library
- **创建日期**: 2026-07-05
- **更新日期**: 2026-07-05
- **分类**: tools
- **标签**: universal, xim, library, ai-assistant
- **兼容AI**: trae, chatgpt, claude

## 📝 简介

本Skill是XIM超级图书馆的核心入口，用于指导AI助手理解用户需求并自动到XIM超级图书馆获取所需的开发环境和Skill资源。

当AI读取本Skill后，它将能够：
1. 理解用户的开发需求（环境需求、Skill需求）
2. 主动询问用户以获取足够的信息
3. 到XIM超级图书馆查找匹配的资源
4. 为用户提供下载链接或部署方案

## 🎯 工作流程

```
用户提出需求 → AI分析需求 → 获取缺失信息 → 查找XIM图书馆 → 返回结果
    ↓              ↓              ↓              ↓              ↓
"我要配置环境"  识别关键词   询问版本/框架   搜索分支/文件    提供下载链接
"我需要技能"    提取关键信息  询问技术栈      搜索Skill目录    提供Skill文档
```

## 🔍 需求分析

### 4.1 识别需求类型

AI需要识别用户的需求属于以下哪种类型：

| 需求类型 | 关键词 | 示例 |
|---------|-------|------|
| **环境部署** | 环境、配置、安装、搭建、开发环境 | "我要配置一个1.20.1 Forge环境" |
| **Skill获取** | 技能、api、开发指南、帮助、参考 | "我需要NeoForge物品修改的API" |
| **混合需求** | 既需要环境又需要Skill | "我要开发1.21.1 NeoForge模组，需要环境和技能" |

### 4.2 提取关键信息

根据需求类型，AI需要提取以下关键信息：

**环境部署需求**:
- 框架类型（Forge / Fabric / NeoForge）
- Minecraft版本（1.20.1 / 1.21.1 等）
- 部署目标路径（可选）

**Skill获取需求**:
- 技术栈（Minecraft / Web / Tools）
- 具体主题（物品修改、法术开发、前端设计等）
- 版本要求（如有）

### 4.3 信息缺失时的询问策略

当关键信息缺失时，AI应按照以下顺序询问：

**环境部署**:
1. "您需要哪种框架？(Forge / Fabric / NeoForge)"
2. "您需要哪个版本？(如：1.21.1)"

**Skill获取**:
1. "您需要哪个技术栈的Skill？(Minecraft / Web / Tools)"
2. "您具体需要哪方面的帮助？(如：物品修改、法术开发)"

**示例对话**:
```
用户: 我要配置一个环境
AI:   好的！您需要哪种框架？(Forge / Fabric / NeoForge)
用户: Forge
AI:   您需要哪个版本？(如：1.20.1)
用户: 1.20.1
AI:   正在为您查找1.20.1 Forge环境...找到了！下载链接：xxx
```

## 📚 XIM图书馆资源定位

### 5.1 环境资源定位

环境资源位于不同的GitHub分支：

| 框架 | 分支名 | 文件格式 |
|------|--------|---------|
| Forge | `Forge` | Forge-{version}-{build}.7z |
| Fabric | `Fabric` | Fabric-{version}-{loader}.7z |
| NeoForge | `NeoForge` | NeoForge-{version}-{build}.7z |

**资源URL格式**:
```
https://raw.githubusercontent.com/LOVE-U987/XIM-Super-Library/{branch}/{filename}
```

**示例**:
```
Forge 1.20.1:
https://raw.githubusercontent.com/LOVE-U987/XIM-Super-Library/Forge/Forge-1.20.1-47.4.10.7z

NeoForge 1.21.1:
https://raw.githubusercontent.com/LOVE-U987/XIM-Super-Library/NeoForge/NeoForge-1.21.1-21.1.219-beta.7z
```

### 5.2 Skill资源定位

Skill资源位于 `skill` 分支，按类别组织：

| 类别 | 目录 | 说明 |
|------|------|------|
| Minecraft | `minecraft/` | Minecraft模组开发相关Skill |
| Web | `web/` | Web开发相关Skill |
| Tools | `tools/` | 工具使用相关Skill |

**Skill文件结构**:
```
skill/{category}/{skill-name}/
├── SKILL.md              # 主Skill文档
├── references/           # 参考文档（如有）
├── examples/             # 示例代码（如有）
└── README.md             # 说明文档（如有）
```

**资源URL格式**:
```
https://raw.githubusercontent.com/LOVE-U987/XIM-Super-Library/skill/{category}/{skill-name}/SKILL.md
```

**示例**:
```
物品修改工作流:
https://raw.githubusercontent.com/LOVE-U987/XIM-Super-Library/skill/minecraft/neoforge-item-modify-workflow/SKILL.md

前端设计指南:
https://raw.githubusercontent.com/LOVE-U987/XIM-Super-Library/skill/web/frontend-design/SKILL.md
```

### 5.3 资源搜索方法

AI可以通过以下方式搜索资源：

**方法1：GitHub API搜索**
```
GET https://api.github.com/repos/LOVE-U987/XIM-Super-Library/git/trees/{branch}?recursive=1
```

**方法2：分支文件列表**
- 访问: https://github.com/LOVE-U987/XIM-Super-Library/tree/{branch}
- 浏览文件列表找到目标文件

**方法3：关键词匹配**
- 根据用户需求的关键词匹配文件名
- 示例：用户说"1.20.1 Forge" → 匹配 "Forge-1.20.1*.7z"

## 📤 结果返回

### 6.1 环境部署结果

返回格式：
```
✅ 找到您需要的开发环境！

📦 环境信息：
- 框架：{框架名称}
- 版本：{版本号}
- 文件大小：{大小}

⬇️ 下载链接：
{下载URL}

📝 安装说明：
1. 点击下载链接下载压缩包
2. 解压到您的开发目录
3. 使用IDE打开即可开始开发

💡 提示：您可能还需要以下Skill：
- {相关Skill名称1} - {描述}
- {相关Skill名称2} - {描述}
```

### 6.2 Skill获取结果

返回格式：
```
✅ 找到您需要的Skill！

📚 Skill信息：
- 名称：{Skill名称}
- 类别：{类别}
- 版本：{版本}

📖 Skill内容摘要：
{Skill简介}

🔗 详细文档：
{Skill文件URL}

📋 包含内容：
- {内容项1}
- {内容项2}

💡 提示：配合以下Skill使用效果更好：
- {相关Skill名称} - {描述}
```

### 6.3 未找到资源

当未找到匹配资源时，返回：
```
❌ 未找到您需要的资源

📝 可能的原因：
- 版本号输入有误
- 框架名称不正确
- 该资源尚未添加到图书馆

💡 建议：
- 检查版本号和框架名称是否正确
- 尝试其他版本
- 提交Issue请求添加资源：
  https://github.com/LOVE-U987/XIM-Super-Library/issues/new
```

## 🧠 AI行为准则

### 7.1 主动询问

当用户提供的信息不足时，AI必须主动询问，直到获取足够的信息。

**正确示例**:
```
用户: 我要配置环境
AI:   好的！您需要哪种框架？(Forge / Fabric / NeoForge)
```

**错误示例**:
```
用户: 我要配置环境
AI:   请提供框架类型和版本号
```

### 7.2 智能匹配

AI应根据用户的上下文智能匹配资源：

**示例**:
```
用户: 我正在开发1.21.1 NeoForge模组，需要修改物品属性
AI:   已理解！您正在开发1.21.1 NeoForge模组，需要修改物品属性。
      正在为您查找相关资源...
      
      ✅ 推荐资源：
      1. NeoForge 1.21.1环境包 - 开发基础
      2. neoforge-item-modify-workflow - 物品属性修改工作流
      3. attribute-modify - 属性修改API参考
```

### 7.3 推荐相关资源

当找到用户需要的资源后，AI应主动推荐相关的资源：

**示例**:
```
用户: 我需要1.21.1 NeoForge环境
AI:   ✅ 找到NeoForge 1.21.1环境包！
      
      💡 推荐配合以下Skill使用：
      - neoforge-item-modify-workflow - 物品属性修改
      - kubejs-neoforge-1.21.1 - KubeJS开发
      - mc-config-ui - 配置界面开发
```

### 7.4 使用中文回复

所有回复必须使用中文，保持友好、专业的语气。

## 📊 统计信息

- **总环境数量**: 26个（Forge: 4, Fabric: 11, NeoForge: 11）
- **总Skill数量**: 30个（Minecraft: 12, Web: 8, Tools: 10）
- **更新时间**: 2026-07-05
- **GitHub仓库**: https://github.com/LOVE-U987/XIM-Super-Library

## ⚠️ 注意事项

1. **版本匹配**: 确保环境版本与Skill版本匹配
2. **网络问题**: 如果下载失败，请检查网络连接
3. **资源更新**: 图书馆资源会定期更新，建议定期检查新版本
4. **反馈建议**: 如果找不到需要的资源，请提交Issue反馈

## 📚 相关资源

- [XIM超级图书馆GitHub](https://github.com/LOVE-U987/XIM-Super-Library)
- [通用性规则](general_rules.md)
- [命名规则](naming_rules.md)
- [摆放规则](placement_rules.md)
