---
name: "attribute-modify"
description: "提供NeoForge 1.21.1环境下通过Attribute Modify模组修改物品属性的完整API参考。Invoke when user needs to modify item attributes, create data-driven attribute modifiers, or replace default item properties via datapack-style configuration."
---

# Attribute Modify 属性修改技能

## 功能描述

本技能提供在 **NeoForge 1.21.1** 环境下，通过 **Attribute Modify** 模组（或类似数据驱动属性修改方案）修改物品默认属性的完整开发规范。

主要功能包括：
- 修改物品的攻击力、攻击速度、护甲值等基础属性
- 添加自定义属性修饰符（Modifiers）
- 通过数据包（Datapack）方式实现物品属性的"替换"效果
- 兼容 Iron's Spellbooks、Cataclysm Spellbooks 等模组的自定义属性

## 环境信息

| 项目 | 版本/说明 |
|------|----------|
| 平台 | NeoForge 1.21.1 |
| KubeJS | 1.7.2 |
| 依赖模组 | Attribute Modify / NeoAttributeModify |
| 属性系统 | Minecraft Data Components (1.21+) |

> ⚠️ **重要提示**: 1.21.1 版本使用 Data Components 替代了旧的 NBT 系统，属性修改需使用新格式。

---

## 接口定义

### 1. 属性修饰符配置格式

```json
{
  "target": "模组ID:物品ID",
  "replace": true,
  "modifiers": [
    {
      "type": "属性类型",
      "amount": 数值,
      "operation": "操作类型",
      "slot": "装备槽位",
      "id": "唯一标识符"
    }
  ]
}
```

### 2. KubeJS 配方输出格式（带Data Components）

```javascript
ServerEvents.recipes(event => {
    event.custom({
        type: 'minecraft:crafting_shaped',
        pattern: [...],
        key: {...},
        result: {
            id: '模组ID:物品ID',
            components: {
                'minecraft:attribute_modifiers': {
                    modifiers: [...]
                },
                'minecraft:item_name': 'JSON字符串',
                'minecraft:lore': ['JSON字符串数组']
            }
        }
    });
});
```

---

## 参数说明

### 属性修饰符参数 (Modifier)

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `type` | string | ✅ | 属性类型ID | `"minecraft:generic.attack_damage"` |
| `amount` | number | ✅ | 属性数值 | `6.0`, `-2.0`, `0.5` |
| `operation` | string | ✅ | 操作类型 | `"add_value"`, `"add_multiplied_base"` |
| `slot` | string | ✅ | 装备槽位 | `"mainhand"`, `"head"`, `"chest"` |
| `id` | string | ✅ | 唯一标识符（UUID格式） | `"minecraft:07fdeded-3c69-37ca-bd0f-0fb94d557fbb"` |

### 操作类型 (Operation)

| 操作类型 | 说明 | 公式 |
|---------|------|------|
| `add_value` | 直接增加值 | 基础值 + amount |
| `add_multiplied_base` | 按基础值比例增加 | 基础值 × (1 + amount) |

### 常用属性类型

| 属性类型 | 说明 | 适用槽位 |
|---------|------|---------|
| `minecraft:generic.attack_damage` | 攻击伤害 | mainhand |
| `minecraft:generic.attack_speed` | 攻击速度 | mainhand |
| `minecraft:generic.armor` | 护甲值 | armor slots |
| `minecraft:generic.armor_toughness` | 护甲韧性 | armor slots |
| `minecraft:generic.max_health` | 最大生命值 | any |
| `minecraft:generic.movement_speed` | 移动速度 | any |
| `irons_spellbooks:ender_spell_power` | 末影法术强度 | mainhand |
| `irons_spellbooks:spell_power` | 法术强度 | mainhand |
| `irons_spellbooks:mana_regen` | 法力回复 | mainhand |
| `irons_spellbooks:cast_time_reduction` | 施法时间减少 | mainhand |
| `irons_spellbooks:ender_magic_resist` | 末影魔法抗性 | mainhand |
| `cataclysm_spellbooks:abyssal_spell_power` | 深渊法术强度 | mainhand |

### 装备槽位 (Slot)

| 槽位 | 说明 |
|------|------|
| `mainhand` | 主手 |
| `offhand` | 副手 |
| `head` | 头部 |
| `chest` | 胸部 |
| `legs` | 腿部 |
| `feet` | 脚部 |
| `any` | 任意槽位 |

---

## 返回值规范

### 数据包配置返回值

数据包配置本身无返回值，但会在游戏加载时自动应用。

### KubeJS 脚本返回值

```javascript
// 配方注册事件返回：无
ServerEvents.recipes(event => {
    // 返回 void
});

// 物品事件处理返回：boolean（是否取消事件）
ItemEvents.pickedUp(event => {
    // 返回 void 或 event.cancel()
});
```

---

## 错误处理机制

### 1. 配置格式错误

```json
{
  "error": "Invalid modifier format",
  "details": "Missing required field: 'type'",
  "solution": "确保所有必填字段已填写"
}
```

### 2. 属性类型不存在

```json
{
  "error": "Unknown attribute type",
  "details": "Attribute 'mod:unknown_attribute' not found",
  "solution": "检查属性类型ID是否正确，确认模组已加载"
}
```

### 3. 数值范围错误

```json
{
  "error": "Value out of range",
  "details": "Attack speed cannot be less than -4.0",
  "solution": "检查数值是否在合理范围内"
}
```

### KubeJS 错误处理示例

```javascript
ServerEvents.recipes(event => {
    try {
        event.custom({
            // 配方配置
        });
    } catch (error) {
        console.error('[AttributeModify] 配方注册失败: ' + error.message);
    }
});
```

---

## 使用示例

### 示例1：修改法杖攻击速度为-3

```json
{
  "target": "hazennstuff:umbranova_dormant",
  "replace": true,
  "modifiers": [
    {
      "type": "minecraft:generic.attack_speed",
      "amount": -3.0,
      "operation": "add_value",
      "slot": "mainhand",
      "id": "minecraft:976c51ac-2edc-3653-a3ad-af53e0a5d89a"
    }
  ]
}
```

### 示例2：完整法杖属性配置

```json
{
  "target": "hazennstuff:umbranova_dormant",
  "replace": true,
  "modifiers": [
    {
      "type": "minecraft:generic.attack_damage",
      "amount": 6.0,
      "operation": "add_value",
      "slot": "mainhand",
      "id": "minecraft:07fdeded-3c69-37ca-bd0f-0fb94d557fbb"
    },
    {
      "type": "minecraft:generic.attack_speed",
      "amount": -3.0,
      "operation": "add_value",
      "slot": "mainhand",
      "id": "minecraft:976c51ac-2edc-3653-a3ad-af53e0a5d89a"
    },
    {
      "type": "irons_spellbooks:ender_spell_power",
      "amount": 0.5,
      "operation": "add_multiplied_base",
      "slot": "mainhand",
      "id": "minecraft:cba1996b-df46-3485-b697-4f9fcc582caa"
    },
    {
      "type": "irons_spellbooks:spell_power",
      "amount": 0.3,
      "operation": "add_multiplied_base",
      "slot": "mainhand",
      "id": "minecraft:04025709-8c66-4f5e-a757-e27104ed4eb4"
    }
  ]
}
```

### 示例3：KubeJS 配方输出（带完整组件）

```javascript
ServerEvents.recipes(event => {
    event.custom({
        type: 'minecraft:crafting_shaped',
        pattern: [
            ' A ',
            ' B ',
            ' C '
        ],
        key: {
            A: { item: 'minecraft:ender_eye' },
            B: { item: 'minecraft:blaze_rod' },
            C: { item: 'minecraft:diamond' }
        },
        result: {
            id: 'hazennstuff:enderconic_scepter',
            components: {
                'minecraft:attribute_modifiers': {
                    modifiers: [
                        {
                            amount: 6.0,
                            id: "minecraft:07fdeded-3c69-37ca-bd0f-0fb94d557fbb",
                            operation: "add_value",
                            slot: "mainhand",
                            type: "minecraft:generic.attack_damage"
                        },
                        {
                            amount: -3.0,
                            id: "minecraft:976c51ac-2edc-3653-a3ad-af53e0a5d89a",
                            operation: "add_value",
                            slot: "mainhand",
                            type: "minecraft:generic.attack_speed"
                        }
                    ]
                },
                'minecraft:item_name': '{"extra":["",{"color":"dark_purple","text":"末影共鸣权杖"}],"italic":false,"text":""}',
                'minecraft:lore': [
                    '{"color":"white","extra":["",{"color":"dark_purple","text":"你清楚的知道..."},{"color":"light_purple","text":"这可不是它的极限..."}],"italic":false,"text":""}'
                ]
            }
        }
    });
});
```

### 示例4：动态属性修改（KubeJS事件）

```javascript
// 玩家拾取物品时自动修改属性
ItemEvents.pickedUp(event => {
    const item = event.item;
    
    if (item.id === 'hazennstuff:enderconic_scepter') {
        // 获取或创建属性修饰符组件
        const modifiers = item.getComponent('minecraft:attribute_modifiers');
        
        if (modifiers) {
            // 修改攻击速度
            modifiers.modifiers.forEach(modifier => {
                if (modifier.type === 'minecraft:generic.attack_speed') {
                    modifier.amount = -3.0;
                }
            });
            
            // 应用修改
            item.setComponent('minecraft:attribute_modifiers', modifiers);
        }
    }
});
```

---

## 开发注意事项

### 1. 版本兼容性

- **1.21.1** 使用 Data Components 系统，旧的 NBT 格式已废弃
- `ItemEvents.modification` **无法**修改 Data Components，请使用配方输出或事件监听
- 属性 UUID 必须使用字符串格式，不再使用整数数组

### 2. 属性叠加规则

- 多个 `add_value` 操作会**累加**
- `add_multiplied_base` 基于基础值计算，多个修饰符会**叠加计算**
- 使用 `replace: true` 可以完全替换原有属性，而不是叠加

### 3. 数值范围限制

| 属性 | 建议范围 | 说明 |
|------|---------|------|
| 攻击速度 | -4.0 ~ 0.0 | 低于-4会导致无法攻击 |
| 攻击伤害 | 0.0 ~ 100.0 | 过高会破坏平衡 |
| 法术强度倍数 | 0.0 ~ 2.0 | 1.0 = 100%加成 |

### 4. ID唯一性

- 每个属性修饰符的 `id` 字段必须**全局唯一**
- 建议使用 `minecraft:` 前缀 + UUID 格式
- 重复的 ID 会导致后加载的覆盖先加载的

### 5. 数据包加载顺序

- 数据包按加载顺序应用，后加载的会覆盖先加载的
- 使用 `replace: true` 可以强制完全替换
- 建议在数据包名称前加 `z_` 确保最后加载

### 6. 调试技巧

```javascript
// 输出物品当前属性到控制台
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

### 7. 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 属性不生效 | 数据包未加载 | 检查 `pack.mcmeta` 格式 |
| 属性叠加错误 | 未使用 `replace: true` | 添加 `replace: true` |
| 游戏崩溃 | 属性类型不存在 | 确认模组已加载 |
| 数值异常 | 超出有效范围 | 检查数值范围 |

---

## 相关技能

- [kubejs-neoforge-1.21.1](kubejs-neoforge-1.21.1/SKILL.md) - KubeJS 基础开发技能
- [irons-spells-neoforge-1-21-1](irons-spells-neoforge-1-21-1/SKILL.md) - Iron's Spells 法术开发
- [legendarymage-trail-system](legendarymage-trail-system/SKILL.md) - 拖尾特效系统

---

## 参考资源

- [Minecraft Wiki - Attribute](https://minecraft.wiki/w/Attribute)
- [NeoForge Documentation](https://docs.neoforged.net/)
- [KubeJS Documentation](https://kubejs.com/)
- [Iron's Spells 'n Spellbooks Wiki](https://github.com/iron431/irons-spells-n-spellbooks/wiki)
