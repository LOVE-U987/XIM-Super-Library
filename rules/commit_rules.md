---
name: commit-rules
tags: [Skills, 项目规则, 代码质量规范]
---

# 提交规则

本文件定义 XIM 超级图书馆知识库的提交规范、标签体系与资源变更要求，保证版本控制与知识管理一致。

## 1. 提交信息格式

采用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<type>[optional scope]: <description>
```

| Type | 用途 |
|------|------|
| `feat` | 新增功能或资源 |
| `fix` | 修复错误 |
| `docs` | 仅文档变更 |
| `style` | 格式调整（不影响逻辑） |
| `refactor` | 重构（不新增功能/不修 bug） |
| `perf` | 性能优化 |
| `test` | 新增或更新测试 |
| `build` | 构建系统或依赖变更 |
| `ci` | CI 配置变更 |
| `chore` | 维护性工作 |
| `revert` | 回滚提交 |

要求：
- 描述使用祈使句、现在时，不超过 72 字符
- 一次提交只包含一个逻辑变更
- 关联 Issue：`Closes #123`、`Refs #456`
- 破坏性变更在 type 后加 `!` 或使用 `BREAKING CHANGE` footer

示例：

```
feat(skill): 新增 neoforge-1.21.1-config-ui 技能
fix(rule): 修正命名规则中版本号格式示例
docs(readme): 同步资源列表与标签
refactor(deploy): 统一 Skill 名称映射
```

## 2. 标签体系

标签是知识库资源定位的核心依据，每个资源必须包含 1-3 个主标签，可附加二级标签。

### 2.1 主标签

| 主标签 | 适用对象 |
|--------|---------|
| 我的世界开发 | Minecraft 模组开发相关技能 |
| 网页开发 | Web 前端/后端开发相关技能 |
| UI与动画 | 界面设计、动画、交互相关技能 |
| 项目结构规范 | 目录结构、多模块架构、命名规则 |
| 重构审查规范 | 代码审查、重构规范 |
| 逻辑规范 | 业务逻辑、算法设计规范 |
| 代码质量规范 | 代码质量、通用性规则 |
| 个人规则 | 个人专属开发规范 |
| 项目规则 | 项目级提交、摆放、维护规范 |
| 特定模组开发 | 针对特定模组（如 Iron's Spells、TaCZ）的开发技能 |
| 图形化UI布局 | 游戏内 GUI、配置界面、渲染布局 |
| Skills | 通用工具类技能（浏览器、测试、截图等） |

### 2.2 二级标签

用于细粒度定位，包括但不限于：

`neoforge`、`forge`、`fabric`、`kubejs`、`1.21.1`、`1.20.1`、`物品属性`、`法术开发`、`配置界面`、`渲染`、`维度注册`、`多模块`、`配方转换`、`前端`、`动画`、`交互设计`、`主题`、`设计规范`、`redis`、`浏览器自动化`、`测试`、`截图`、`计划`、`头脑风暴`、`代码审查`、`github`、`git`、`算法艺术`、`api`、`数据驱动`

### 2.3 资源标签映射

| 资源 | 主标签 |
|------|--------|
| neoforge-item-modify-workflow | 我的世界开发、特定模组开发 |
| attribute-modify | 我的世界开发、特定模组开发 |
| legendary-mage-trail-system | 我的世界开发、特定模组开发、图形化UI布局 |
| irons-spells-neoforge-1.21.1 | 我的世界开发、特定模组开发 |
| tacz-recipe-1.20.1 | 我的世界开发、特定模组开发 |
| neoforge-1.21.1-config-screen | 我的世界开发、图形化UI布局 |
| kubejs-neoforge-1.21.1 | 我的世界开发 |
| kubejs-forge-1.20.1 | 我的世界开发 |
| pasterdream-dimension-api | 我的世界开发、特定模组开发 |
| neoforge-1.21.1-config-ui | 我的世界开发、UI与动画、图形化UI布局 |
| modern-ui | 我的世界开发、UI与动画、图形化UI布局 |
| api-split-multi-module | 我的世界开发、项目结构规范 |
| frontend-design | 网页开发、UI与动画 |
| frontend-skill | 网页开发、UI与动画 |
| shadcn | 网页开发、UI与动画 |
| gsap | 网页开发、UI与动画 |
| animejs | 网页开发、UI与动画 |
| interaction-design | 网页开发、UI与动画 |
| theme-factory | 网页开发、UI与动画 |
| web-design-guidelines | 网页开发、UI与动画 |
| redis-development | Skills |
| agent-browser | Skills |
| webapp-testing | Skills、网页开发 |
| screenshot | Skills |
| writing-plans | Skills、项目结构规范 |
| brainstorming | Skills |
| code-reviewer | Skills、重构审查规范 |
| gh-cli | Skills |
| git-commit | Skills、项目规则 |
| algorithmic-art | 网页开发、UI与动画 |
| general_rules | Skills、代码质量规范 |
| naming_rules | Skills、项目结构规范 |
| placement_rules | Skills、项目结构规范 |
| universal_skill | Skills |
| commit_rules | Skills、项目规则、代码质量规范 |
| sample-skill | Skills |

## 3. 资源变更要求

新增、重命名或修改知识库资源时，必须同时满足：

### 3.1 命名
- 目录与 frontmatter `name` 保持一致
- 格式：`技术栈-版本号-功能描述`，小写字母、数字与连字符
- 版本号使用点分隔：`neoforge-1.21.1-config-ui`

### 3.2 标签
- frontmatter 必须包含 `tags` 字段，从主标签中选择 1-3 个，可按需附加二级标签

### 3.3 同步
- 更新根 `README.md` 及对应分类 `README.md` 的索引
- 如资源名变更，同步更新 `deploy.py`、`deploy_fast.py` 中的名称列表
- 更新其他资源中的交叉链接与 `universal_skill.md` 引用

## 4. Emoji 使用规范

遵循「必要才使用」原则：
- 禁止：标题、装饰性列表、问候语中的冗余 emoji
- 保留：语义标记 `⚠️`（警告）、`✅`/`❌`（正确/错误对照）、AI 输出模板中的状态符号

## 5. 提交前检查清单

- [ ] 提交信息符合 Conventional Commits 格式
- [ ] 资源命名符合规范，目录与 frontmatter name 一致
- [ ] frontmatter 包含 1-3 个主标签
- [ ] README 索引与标签已同步
- [ ] 无冗余 emoji
- [ ] 无重复内容，信息已精简
