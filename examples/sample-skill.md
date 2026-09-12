---
name: sample-skill
description: 展示 Skill 的基本结构和格式，供新 Skill 编写参考。
tags: [Skills, 项目结构规范]
---

# Sample Skill | 示例Skill

## 元信息

- **名称**: sample-skill
- **版本**: 1.0.0
- **作者**: XIM Super Library
- **创建日期**: 2026-07-04
- **更新日期**: 2026-07-04
- **分类**: tools
- **标签**: [Skills, 项目结构规范]
- **兼容AI**: trae, chatgpt, claude

## 简介

示例 Skill，展示 Skill 的基本结构和格式。Skill 是 XIM 超级图书馆的 AI 能力扩展模块，帮助 AI 在开发过程中获取相关信息。

## 使用方法

AI 可通过通用性 Skill 收集信息，在 XIM 图书馆获取帮助。

### 调用方式

```
查询: sample-skill [参数]
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | 是 | 查询内容 |
| version | string | 否 | 版本号 |

## 示例代码

```java
public class Example {
    public static void main(String[] args) {
        System.out.println("Hello, XIM Super Library!");
    }
}
```

## 相关资源

- [XIM超级图书馆](https://github.com/LOVE-U987/XIM-Super-Library)
- [通用性规则](../rules/general_rules.md)
- [命名规则](../rules/naming_rules.md)
- [摆放规则](../rules/placement_rules.md)
- [提交规则](../rules/commit_rules.md)

## 注意事项

- 本 Skill 仅作为示例，不包含实际功能
- 使用前请先阅读并理解相关规则文档
