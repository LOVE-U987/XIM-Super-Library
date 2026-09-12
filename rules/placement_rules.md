---
name: placement-rules
tags: [Skills, 项目结构规范]
---

# 摆放规则

## 1. 目录结构

```
skill/
├── minecraft/      # Minecraft模组开发
├── web/            # Web开发
├── tools/          # 工具使用
├── rules/          # 规则文档
└── examples/       # 示例文件
```

## 2. Skill 摆放

### 2.1 按类别分类
- Minecraft 模组开发 → `minecraft/`
- Web 开发 → `web/`
- 工具使用 → `tools/`

### 2.2 按版本分类
- 在技术栈目录下按版本号组织
- 版本号用于命名而非建目录层级，如 `kubejs-neoforge-1.21.1/`

### 2.3 按功能分类
- API 参考 → 名称含 `api`
- 教程指南 → 名称含 `guide`
- 配置文件 → 名称含 `config`

## 3. 文件组织

### 3.1 单一文件
- 小型 Skill 使用单一文件
- 文件名即为 Skill 名称

### 3.2 多文件
- 大型 Skill 使用目录结构
- 主文件统一命名为 `SKILL.md`
- 相关资源放在 `references/` 等子目录

## 4. 索引文件

### 4.1 目录索引
- 每个分类目录维护 `README.md`
- 列出目录内容并提供标签，便于检索

### 4.2 全局索引
- 根目录 `README.md` 维护全量索引
- 索引包含所有 Skill 的清单、说明和标签
