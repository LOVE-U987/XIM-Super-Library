---
name: "neoforge-item-modify-workflow"
description: "提供NeoForge 1.21.1环境下修改物品属性的完整工作流参考，包括NeoAttributeModify数据包配置和KubeJS事件监听方案。Invoke when user needs to modify item attributes, item_name, lore, or rarity in NeoForge 1.21.1 environment."
---

# NeoForge 1.21.1 物品属性修改工作流

## 概述

本技能记录在 **NeoForge 1.21.1** 环境下，通过 **NeoAttributeModify** 模组和 **KubeJS** 修改物品属性的完整工作流。

## 环境信息

| 项目 | 版本/说明 |
|------|----------|
| 平台 | NeoForge 1.21.1 |
| KubeJS | 1.7.2 |
| 依赖模组 | NeoAttributeModify |
| 属性系统 | Minecraft Data Components (1.21+) |

---

## 核心架构

### 双轨制方案

由于技术限制，需要**两个系统协同工作**：

| 功能 | 负责系统 | 说明 |
|------|---------|------|
| 属性修改（攻击力、攻击速度、法术强度等） | NeoAttributeModify 数据包 | 自动应用到所有方式获得的物品 |
| 显示属性（item_name、lore、rarity） | KubeJS 事件监听 | 在特定事件触发时修改 |

---

## 第一部分：NeoAttributeModify 数据包配置

### 文件路径

```
kubejs/data/<namespace>/item_attributes/<item_id>.json
```

### 配置格式

```json
{
  "<模组ID>:<物品ID>": {
    "equipment_slots": {
      "<槽位>": [
        {
          "attribute": "<属性类型>",
          "action": "<操作类型>",
          "amount": <数值>,
          "operation": "<计算方式>",
          "modifier_id": "<唯一ID>"
        }
      ]
    }
  }
}
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `attribute` | string | ✅ | 属性类型ID | `"minecraft:generic.attack_damage"` |
| `action` | string | ✅ | 操作类型 | `"add"`（叠加）或 `"modify"`（替换） |
| `amount` | number | ✅ | 属性数值 | `3.0`, `-3.0`, `0.5` |
| `operation` | string | ✅ | 计算方式 | `"add_value"`, `"add_multiplied_base"` |
| `modifier_id` | string | ✅ | 唯一标识符 | `"minecraft:07fdeded-3c69-37ca-bd0f-0fb94d557fbb"` |

### 常用属性类型

| 属性类型 | 说明 | 适用槽位 |
|---------|------|---------|
| `minecraft:generic.attack_damage` | 攻击伤害 | mainhand |
| `minecraft:generic.attack_speed` | 攻击速度 | mainhand |
| `irons_spellbooks:ender_spell_power` | 末影法术强度 | mainhand |
| `irons_spellbooks:spell_power` | 法术强度 | mainhand |
| `irons_spellbooks:mana_regen` | 法力回复 | mainhand |
| `irons_spellbooks:cast_time_reduction` | 施法时间减少 | mainhand |
| `irons_spellbooks:ender_magic_resist` | 末影魔法抗性 | mainhand |
| `cataclysm_spellbooks:abyssal_spell_power` | 深渊法术强度 | mainhand |

### 完整示例

```json
{
  "hazennstuff:umbranova_dormant": {
    "equipment_slots": {
      "mainhand": [
        {
          "attribute": "minecraft:generic.attack_damage",
          "action": "modify",
          "amount": 3.0,
          "operation": "add_value",
          "modifier_id": "minecraft:07fdeded-3c69-37ca-bd0f-0fb94d557fbb"
        },
        {
          "attribute": "minecraft:generic.attack_speed",
          "action": "modify",
          "amount": -3.0,
          "operation": "add_value",
          "modifier_id": "minecraft:976c51ac-2edc-3653-a3ad-af53e0a5d89a"
        },
        {
          "attribute": "irons_spellbooks:ender_spell_power",
          "action": "add",
          "amount": 0.5,
          "operation": "add_multiplied_base",
          "modifier_id": "minecraft:cba1996b-df46-3485-b697-4f9fcc582caa"
        }
      ]
    }
  }
}
```

---

## 第二部分：KubeJS 显示属性修改

### 限制说明

**重要**：以下方法在 KubeJS 1.21.1 中**不可用**或**有问题**：

| 方法 | 问题 |
|------|------|
| `player.getItemBySlot('mainhand')` | 返回字符串而非 ItemStack |
| `player.mainHandItem` | 返回字符串而非 ItemStack |
| `item.setRarity()` | 方法不存在 |

### 可用方案

使用 **ItemEvents** 获取真正的 ItemStack 对象：

```javascript
// 可用的物品事件
ItemEvents.pickedUp(event => {
    const item = event.item; // 这是真正的 ItemStack 对象
    // 可以调用 getComponent、setName、setLore 等方法
});

ItemEvents.rightClicked(event => {
    const item = event.item; // 这是真正的 ItemStack 对象
    // 可以调用 getComponent、setName、setLore 等方法
});
```

### 完整JS示例

```javascript
// 超新星法杖属性调整脚本

/**
 * 修改超新星法杖的显示属性
 * @param {ItemStack} item - 物品堆栈
 */
function modifyUmbranovaDisplay(item) {
    // 检查物品是否已经被修改过（避免重复修改）
    const customData = item.getComponent('minecraft:custom_data');
    if (customData && customData.this_is_a_magic_staff && customData.this_is_a_magic_staff.is_transformed) {
        return; // 已经修改过，跳过
    }
    
    // 设置自定义名称（超新星 - 深紫色）
    item.setName(Text.of('超新星').darkPurple());
    
    // 设置Lore（终末之上，燃起希望新星）
    item.setLore([Text.of('终末之上，燃起希望新星').darkPurple()]);
    
    // 设置 custom_data 标记
    if (!customData) {
        item.setComponent('minecraft:custom_data', {
            this_is_a_magic_staff: {
                is_transformed: true
            }
        });
    }
    
    console.info('[KubeJS] 已修改超新星法杖的显示属性');
}

// 玩家拾取物品时修改显示属性
ItemEvents.pickedUp(event => {
    const item = event.item;
    if (item.id === 'hazennstuff:umbranova_dormant') {
        modifyUmbranovaDisplay(item);
    }
});

// 玩家右键点击物品时修改显示属性
ItemEvents.rightClicked(event => {
    const item = event.item;
    if (item.id === 'hazennstuff:umbranova_dormant') {
        const customData = item.getComponent('minecraft:custom_data');
        if (!customData || !customData.this_is_a_magic_staff || !customData.this_is_a_magic_staff.is_transformed) {
            modifyUmbranovaDisplay(item);
        }
    }
});
```

---

## 第三部分：数据包配置

### pack.mcmeta

```json
{
  "pack": {
    "pack_format": 57,
    "supported_formats": {
      "min_inclusive": 57,
      "max_inclusive": 61
    },
    "description": "物品属性调整数据包"
  }
}
```

### 目录结构

```
kubejs/data/<namespace>/
├── pack.mcmeta
└── item_attributes/
    └── <item_id>.json
```

---

## 常见问题与解决方案

### 问题1：属性不生效

**原因**：
- 数据包未正确加载
- 属性类型ID错误
- 模组版本不兼容

**解决方案**：
1. 检查 `pack.mcmeta` 格式
2. 确认属性类型ID正确
3. 使用 `/reload` 重载数据包
4. 查看控制台日志

### 问题2：属性叠加错误

**原因**：使用了 `"action": "add"` 而不是 `"modify"`

**解决方案**：
- 使用 `"action": "modify"` 替换原有属性
- 使用 `"action": "add"` 在原有属性基础上叠加

### 问题3：无法修改 item_name 和 lore

**原因**：尝试使用 `player.getItemBySlot()` 获取物品，但返回的是字符串

**解决方案**：
- 使用 `ItemEvents.pickedUp` 或 `ItemEvents.rightClicked` 获取 ItemStack 对象
- 或者使用配方输出设置 item_name 和 lore

### 问题4：Iron's Spellbooks 属性报错

**原因**：属性类型不存在或模组未加载

**解决方案**：
1. 确认 Iron's Spellbooks 模组已安装
2. 检查属性类型ID拼写
3. 先测试基础属性（如 `minecraft:generic.attack_damage`）

---

## 最佳实践

### 1. 分阶段测试

1. **第一阶段**：测试基础属性（攻击伤害、攻击速度）
2. **第二阶段**：添加模组属性（法术强度等）
3. **第三阶段**：添加显示属性（item_name、lore）

### 2. 使用标记避免重复修改

```javascript
// 使用 custom_data 标记已修改的物品
item.setComponent('minecraft:custom_data', {
    modified: true
});

// 检查标记
const customData = item.getComponent('minecraft:custom_data');
if (customData && customData.modified) {
    return; // 已修改，跳过
}
```

### 3. 保持ID唯一性

每个属性修饰符的 `modifier_id` 必须全局唯一：

```json
"modifier_id": "minecraft:07fdeded-3c69-37ca-bd0f-0fb94d557fbb"
```

建议使用 `minecraft:` 前缀 + UUID 格式。

---

## 调试技巧

### 查看物品当前属性

```javascript
function logItemAttributes(item) {
    console.log('物品ID: ' + item.id);
    const modifiers = item.getComponent('minecraft:attribute_modifiers');
    if (modifiers) {
        modifiers.modifiers.forEach(mod => {
            console.log(`  - ${mod.type}: ${mod.amount} (${mod.operation})`);
        });
    }
}
```

### 测试属性修改

```javascript
// 临时增加100点伤害测试
{
  "attribute": "minecraft:generic.attack_damage",
  "action": "add",
  "amount": 100.0,
  "operation": "add_value",
  "modifier_id": "minecraft:test_modifier"
}
```

如果攻击伤害增加了100点，说明数据包生效。

---

## 参考资源

- [NeoAttributeModify CurseForge](https://www.curseforge.com/minecraft/mc-mods/attribute-modify)
- [KubeJS Documentation](https://kubejs.com/)
- [Minecraft Wiki - Attribute](https://minecraft.wiki/w/Attribute)
- [Iron's Spells 'n Spellbooks Wiki](https://github.com/iron431/irons-spells-n-spellbooks/wiki)

---

## 相关技能

- [attribute-modify](../attribute-modify/SKILL.md) - 属性修改详细API
- [kubejs-neoforge-1.21.1](../kubejs-neoforge-1.21.1/SKILL.md) - KubeJS 基础开发
- [irons-spells-neoforge-1-21-1](../irons-spells-neoforge-1-21-1/SKILL.md) - Iron's Spells 法术开发
