# 📂 摆放规则

## 1. 目录结构

### 1.1 顶层目录
```
skill/
├── minecraft/              # Minecraft相关
│   ├── neoforge/           # NeoForge技能
│   ├── forge/              # Forge技能
│   └── fabric/             # Fabric技能
├── web/                    # Web开发相关
│   ├── frontend/           # 前端技能
│   └── backend/            # 后端技能
├── tools/                  # 工具相关
└── examples/               # 示例文件
```

### 1.2 环境分支结构
- 开发环境: 存放在对应环境分支(Forge/Fabric/NeoForge)
- Skill: 存放在skill分支
- 规则文档: 存放在skill分支的rules目录

## 2. Skill摆放

### 2.1 按技术栈分类
- Minecraft模组开发 → minecraft/
- Web开发 → web/
- 工具使用 → tools/

### 2.2 按版本分类
- 在技术栈目录下按版本号创建子目录
- 示例: minecraft/neoforge/1.21.1/

### 2.3 按功能分类
- API参考 → api/
- 教程指南 → guide/
- 配置文件 → config/
- 示例代码 → examples/

## 3. 文件组织

### 3.1 单一文件
- 小型Skill使用单一文件
- 文件名即为Skill名称

### 3.2 多文件
- 大型Skill使用目录结构
- 主文件命名为README.md
- 相关资源放在同一目录

## 4. 索引文件

### 4.1 目录索引
- 每个目录必须包含README.md
- README.md必须列出目录内容
- 提供内容摘要便于检索

### 4.2 全局索引
- 在skill分支根目录维护全局索引
- 索引包含所有Skill的清单
- 提供搜索和筛选功能
