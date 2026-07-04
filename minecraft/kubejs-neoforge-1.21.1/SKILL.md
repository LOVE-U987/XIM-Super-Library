---
name: kubejs-neoforge-1.21.1
description: "提供KubeJS NeoForge 1.21.1环境下的代码辅助，包含动态难度系统、自定义物品、配方、战利品表、玩家自定义倍数系统等功能。Invoke when user is writing KubeJS scripts for NeoForge 1.21.1 with EntityJS, Iron's Spells, LootJS addons."
---

# KubeJS NeoForge 1.21.1 开发技能

## 环境信息

- **平台**: NeoForge 1.21.1
- **KubeJS版本**: 1.7.2
- **额外插件**:
  - EntityJS - 实体相关功能
  - KubeJS Iron's Spells - 法术系统兼容
  - LootJS: KubeJS Addon - 战利品表修改

> ⚠️ **警告**: 如果在非该环境下使用，可能出现函数名错误问题

---

## 1. 动态难度系统 (difficulty_scaling.js)

### 配置系统

```javascript
// 运行时配置构建函数
function buildConfig() {
    return {
        DETECTION_RADIUS: 32,              // 检测半径
        BASE_HEALTH_MULTIPLIER: 1.0,       // 基础生命倍数
        BASE_ARMOR_MULTIPLIER: 1.0,        // 基础护甲倍数
        BASE_DAMAGE_MULTIPLIER: 1.0,       // 基础伤害倍数
        MAX_HEALTH_MULTIPLIER: 4.0,        // 最大生命倍数
        MAX_ARMOR_MULTIPLIER: 3.0,         // 最大护甲倍数
        MAX_DAMAGE_MULTIPLIER: 2.5,        // 最大伤害倍数
        HEALTH_PRECISION_FACTOR: 0.03,     // 生命-精度系数
        HEALTH_ARMOR_FACTOR: 0.02,         // 生命-护甲系数
        HEALTH_TOUGHNESS_FACTOR: 0.04,     // 生命-韧性系数
        HEALTH_SPELL_POWER_FACTOR: 0.05,   // 生命-法术强度系数
        ARMOR_ARMOR_FACTOR: 0.03,          // 护甲-护甲系数
        ARMOR_TOUGHNESS_FACTOR: 0.05,      // 护甲-韧性系数
        DAMAGE_SPELL_POWER_FACTOR: 0.04,   // 伤害-法术强度系数
        DAMAGE_PRECISION_FACTOR: 0.02,     // 伤害-精度系数
        PRECISION_BASE_PER_ITEM: 1.0,      // 每件装备基础精度
        PRECISION_SPECIAL_ENCHANT_MULTIPLIER: 2.0,  // 特殊附魔倍数
        PRECISION_GOOD_ENCHANT_MULTIPLIER: 1.5,     // 优质附魔倍数
        PRECISION_NORMAL_ENCHANT_MULTIPLIER: 0.5,   // 普通附魔倍数
        ARMOR_BASE_BONUS: 2.0,             // 护甲基础加成
        ARMOR_ENCHANT_BONUS: 0.5,          // 护甲附魔加成
        TOUGHNESS_DIAMOND_NETHERITE_BONUS: 2.0,  // 钻石/下界合金韧性加成
        TOUGHNESS_ENCHANT_BONUS: 0.25,     // 韧性附魔加成
        SPELL_POWER_BASE: 5.0,             // 法术强度基础值
        SPELL_POWER_ENCHANT_MULTIPLIER: 2.0,   // 法术强度附魔倍数
        SPELL_POWER_MANA_FACTOR: 0.01,     // 法术强度-法力系数
        VISUAL_EFFECT_THRESHOLD: 2.0,      // 视觉效果阈值
        UPDATE_FREQUENCY: 200              // 更新频率(ticks)
    };
}
```

### 工具函数

```javascript
// 安全日志输出
function safeLog(msg, force)

// 跳过非敌对实体检查
function shouldSkipEntity(e)

// 获取附近玩家
function getNearbyPlayers(level, pos, r)
```

### 玩家属性计算函数

```javascript
// 计算玩家装备精度
function calculatePlayerPrecision(p)

// 计算玩家护甲值
function calculatePlayerArmor(p)

// 计算玩家韧性
function calculatePlayerToughness(p)

// 计算玩家法术强度 (兼容Iron's Spells)
function calculatePlayerSpellPower(p)

// 计算玩家综合属性
function calculatePlayerStats(players)
```

### 怪物缩放函数

```javascript
// 计算生命倍数
function calculateHealthMultiplier(s)

// 计算护甲倍数
function calculateArmorMultiplier(s)

// 计算伤害倍数
function calculateDamageMultiplier(s)

// 获取强化类型
function getScalingType(s)

// 应用怪物缩放
function applyMonsterScaling(mob, stats)

// 基于玩家属性缩放怪物
function scaleMonsterBasedOnPlayerStats(mob)
```

### 事件监听

```javascript
// 实体生成时应用难度
EntityEvents.spawned(event => {
    const e = event.entity
    if (shouldSkipEntity(e)) return
    scaleMonsterBasedOnPlayerStats(e)
})

// 定时更新怪物属性
ServerEvents.tick(event => {
    const server = event.server
    if (server.tickCount % CONFIG.UPDATE_FREQUENCY !== 0) return
    // 更新逻辑...
})
```

### 命令注册

```javascript
ServerEvents.commandRegistry(function(event) {
    const Commands = event.commands
    const StringArgumentType = Java.loadClass('com.mojang.brigadier.arguments.StringArgumentType')
    const DoubleArgumentType = Java.loadClass('com.mojang.brigadier.arguments.DoubleArgumentType')
    const Component = Java.loadClass('net.minecraft.network.chat.Component')
    const ClickEvent = Java.loadClass('net.minecraft.network.chat.ClickEvent')
    const HoverEvent = Java.loadClass('net.minecraft.network.chat.HoverEvent')

    // /difficulty_config - 在线修改配置
    // /diffhelp - 帮助命令
    // /diffgui - GUI菜单
    // /debug_stats - 查看玩家属性
    // /difficulty_debug - 调试命令
})
```

---

## 2. 玩家自定义倍数系统

### 2.1 怪物血量倍数 (player_health_multiplier.js)

```javascript
// 配置
const PHM_CONFIG = {
    DEFAULT_MULTIPLIER: 1.0,
    MIN_MULTIPLIER: 0.1,
    MAX_MULTIPLIER: 100.0,
    PERMISSION_NODE: 'difficulty.player_health_multiplier',
    STORAGE_PATH: 'kubejs/player_health_multipliers.json'
};

// 核心函数
function phmHasPermission(player)
function phmLoadPlayerMultipliers()
function phmSavePlayerMultipliers()
function phmGetPlayerMultiplier(player)
function phmSetPlayerMultiplier(player, multiplier)
function phmApplyPlayerMultiplier(entity)
```

### 2.2 怪物攻击倍数 (player_damage_multiplier.js)

```javascript
// 配置
const PDM_CONFIG = {
    DEFAULT_MULTIPLIER: 1.0,
    MIN_MULTIPLIER: 0.1,
    MAX_MULTIPLIER: 100.0,
    PERMISSION_NODE: 'difficulty.player_damage_multiplier',
    STORAGE_PATH: 'kubejs/player_damage_multipliers.json'
};

// 核心函数
function pdmHasPermission(player)
function pdmLoadPlayerMultipliers()
function pdmSavePlayerMultipliers()
function pdmGetPlayerMultiplier(player)
function pdmSetPlayerMultiplier(player, multiplier)
function pdmApplyPlayerMultiplier(entity)
```

### 2.3 怪物护甲倍数 (player_armor_multiplier.js)

```javascript
// 配置
const PAM_CONFIG = {
    DEFAULT_MULTIPLIER: 1.0,
    MIN_MULTIPLIER: 0.1,
    MAX_MULTIPLIER: 100.0,
    PERMISSION_NODE: 'difficulty.player_armor_multiplier',
    STORAGE_PATH: 'kubejs/player_armor_multipliers.json'
};

// 核心函数
function pamHasPermission(player)
function pamLoadPlayerMultipliers()
function pamSavePlayerMultipliers()
function pamGetPlayerMultiplier(player)
function pamSetPlayerMultiplier(player, multiplier)
function pamApplyPlayerMultiplier(entity)
```

### 命令使用

```
/phm get              - 查看当前怪物血量倍率
/phm set <倍率>       - 设置怪物血量倍率
/pdm get              - 查看当前怪物攻击倍率
/pdm set <倍率>       - 设置怪物攻击倍率
/armorm get           - 查看当前怪物护甲倍率
/armorm set <倍率>    - 设置怪物护甲倍率
```

---

## 3. 自定义物品系统 (startup_scripts/add_custom_items.js)

### 物品配置格式

```javascript
const ITEMS_TO_ADD = [
    {
        id: "kubejs:item_id",           // 物品ID
        name: "物品名称",                // 显示名称
        type: "EPIC",                    // 稀有度: COMMON, UNCOMMON, RARE, EPIC, LEGENDARY
        maxStackSize: 64,                // 最大堆叠数量
        creativeTab: "minecraft:misc"    // 创造模式标签
    }
];
```

### 物品注册事件

```javascript
StartupEvents.registry("item", function(event) {
    for (var i = 0; i < ITEMS_TO_ADD.length; i++) {
        var itemConfig = ITEMS_TO_ADD[i];
        var itemBuilder = event.create(itemConfig.id)
            .displayName(itemConfig.name)
            .maxStackSize(itemConfig.maxStackSize)
            .rarity(itemConfig.type);  // COMMON, UNCOMMON, RARE, EPIC
    }
});
```

### 方块注册事件

```javascript
StartupEvents.registry("block", function(event) {
    // 方块注册逻辑
});
```

---

## 4. 自定义配方系统 (server_scripts/custom_recipes.js)

### 有序配方 (Shaped Recipe)

```javascript
ServerEvents.recipes(event => {
    event.shaped(
        Item.of('mod:output_item'),     // 输出物品
        [                               // 配方图案
            'A B',
            'CCC',
            '   '
        ],
        {                               // 材料映射
            A: 'mod:item_a',
            B: 'mod:item_b',
            C: 'mod:item_c'
        }
    );
});
```

### 无序配方 (Shapeless Recipe)

```javascript
ServerEvents.recipes(event => {
    event.shapeless(
        Item.of('mod:output_item', count),
        ['mod:item_a', 'mod:item_b', 'mod:item_c']
    );
});
```

### 配方修改

```javascript
ServerEvents.recipes(event => {
    // 移除配方
    event.remove({ id: 'mod:recipe_id' });
    
    // 替换配方
    event.replaceInput(
        { input: 'old:item' },
        'old:item',
        'new:item'
    );
});
```

---

## 5. 战利品表系统 (server_scripts/falling_object_configuration.js)

### 掉落配置系统

```javascript
const DropConfig = {
    // 稀有等级比例系数
    rarityFactors: {
        COMMON: 0.005,
        UNCOMMON: 0.0025,
        RARE: 0.001,
        EPIC: 0.0005,
        LEGENDARY: 0.00001
    },
    
    // 取整方式
    roundingMethod: 'floor',  // floor, round, ceil
    
    // 计算实际掉落权重
    calculateWeight: function(baseWeight, rarity) {
        const factor = this.rarityFactors[rarity] || this.rarityFactors.COMMON;
        const weight = baseWeight * factor;
        return Math.max(1, this.round(weight));
    },
    
    // 计算实际掉落数量范围
    calculateCountRange: function(minBase, maxDiff, factor) {
        const maxRaw = (minBase + maxDiff) * factor;
        const maxCount = Math.max(1, this.round(maxRaw));
        const minRaw = minBase * factor;
        const minCount = Math.max(1, this.round(minRaw));
        return [Math.min(minCount, maxCount), Math.max(minCount, maxCount)];
    },
    
    // 统一取整函数
    round: function(value) {
        switch (this.roundingMethod) {
            case 'ceil': return Math.ceil(value);
            case 'round': return Math.round(value);
            case 'floor': default: return Math.floor(value);
        }
    }
};
```

### 物品掉落配置

```javascript
const ItemDropConfigs = {
    "kubejs:item_id": {
        weight: {
            base: 1,
            rarity: "EPIC"
        },
        count: {
            minBase: 1,
            maxDiff: 2,
            factor: 1.0
        }
    }
};

// 获取物品掉落配置
function getItemDropConfig(itemId) {
    const config = ItemDropConfigs[itemId];
    if (!config) {
        return { weight: 1, count: [1, 1] };
    }
    
    const weight = DropConfig.calculateWeight(config.weight.base, config.weight.rarity);
    const countRange = DropConfig.calculateCountRange(
        config.count.minBase,
        config.count.maxDiff,
        config.count.factor
    );
    
    return { weight: weight, count: countRange };
}
```

### LootJS 战利品表修改

```javascript
LootJS.lootTables(event => {
    const itemConfig = getItemDropConfig("kubejs:item_id");
    
    event.getLootTable("minecraft:entities/zombie")
        .firstPool()
        .addEntry(LootEntry.of("kubejs:item_id")
            .withWeight(itemConfig.weight)
            .setCount(itemConfig.count));
});
```

---

## 6. 物品使用事件 (server_scripts/item_usage.js)

```javascript
ItemEvents.rightClicked(function(event) {
    var player = event.entity;
    var itemStack = event.item;
    
    if (itemStack && itemStack.id === 'kubejs:item_id') {
        // 消耗物品
        itemStack.count--;
        
        // 给予玩家经验
        player.giveExperiencePoints(exp);
        
        // 发送消息
        player.tell('消息内容');
        
        // 取消默认行为
        event.cancel();
    }
});
```

---

## 7. Apotheosis 兼容 (server_scripts/apotheosis_difficulty_scaling.js)

```javascript
// 计算玩家神化力量
function calculatePlayerApotheosisPower(player) {
    let apotheosisPower = 0;
    const equipmentSlots = ['head', 'chest', 'legs', 'feet', 'mainhand', 'offhand'];
    
    equipmentSlots.forEach(slot => {
        const item = player.getItemBySlot(slot);
        if (!item.isEmpty()) {
            const nbt = item.nbt;
            if (nbt) {
                // 检测Apotheosis特有的NBT数据
                // 处理逻辑...
            }
        }
    });
    
    return Math.max(0, apotheosisPower);
}

// 应用怪物缩放
function applyMonsterScaling(monster, playerStats) {
    if (!monster || monster.isRemoved() || !monster.isAlive()) {
        return;
    }
    // 缩放逻辑...
}
```

---

## 8. 常用事件参考

### 服务器事件

```javascript
// 服务器启动完成
ServerEvents.loaded(event => {
    // 初始化逻辑
});

// 服务器tick
ServerEvents.tick(event => {
    const server = event.server;
    // 每tick执行的逻辑
});

// 配方注册
ServerEvents.recipes(event => {
    // 添加/修改配方
});

// 命令注册
ServerEvents.commandRegistry(event => {
    const Commands = event.commands;
    // 注册自定义命令
});
```

### 实体事件

```javascript
// 实体生成
EntityEvents.spawned(event => {
    const entity = event.entity;
    // 处理逻辑
});

// 实体受到伤害
EntityEvents.hurt(event => {
    const entity = event.entity;
    const damage = event.damage;
    // 处理逻辑
});

// 实体死亡
EntityEvents.death(event => {
    const entity = event.entity;
    // 处理逻辑
});
```

### 物品事件

```javascript
// 物品右键点击
ItemEvents.rightClicked(event => {
    const player = event.entity;
    const item = event.item;
    // 处理逻辑
});

// 物品使用
ItemEvents.used(event => {
    // 处理逻辑
});
```

### 玩家事件

```javascript
// 玩家登录
PlayerEvents.loggedIn(event => {
    const player = event.player;
    // 处理逻辑
});

// 玩家登出
PlayerEvents.loggedOut(event => {
    const player = event.player;
    // 处理逻辑
});

// 玩家tick
PlayerEvents.tick(event => {
    const player = event.player;
    // 处理逻辑
});
```

---

## 9. 常用Java类加载

```javascript
// 参数类型
const StringArgumentType = Java.loadClass('com.mojang.brigadier.arguments.StringArgumentType');
const DoubleArgumentType = Java.loadClass('com.mojang.brigadier.arguments.DoubleArgumentType');
const IntegerArgumentType = Java.loadClass('com.mojang.brigadier.arguments.IntegerArgumentType');

// 聊天组件
const Component = Java.loadClass('net.minecraft.network.chat.Component');
const ClickEvent = Java.loadClass('net.minecraft.network.chat.ClickEvent');
const HoverEvent = Java.loadClass('net.minecraft.network.chat.HoverEvent');

// 其他常用类
const ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation');
```

---

## 10. 文件系统操作

```javascript
// 加载和保存JSON配置
function loadConfig() {
    try {
        const fs = require('fs');
        const path = require('path');
        const filePath = path.join(global.server.configDir, 'kubejs/config.json');
        
        if (fs.existsSync(filePath)) {
            const content = fs.readFileSync(filePath, 'utf8');
            return JSON.parse(content);
        }
    } catch (error) {
        console.log('加载配置失败: ' + error.message);
    }
    return {};
}

function saveConfig(data) {
    try {
        const fs = require('fs');
        const path = require('path');
        const filePath = path.join(global.server.configDir, 'kubejs/config.json');
        
        const dirPath = path.dirname(filePath);
        if (!fs.existsSync(dirPath)) {
            fs.mkdirSync(dirPath, { recursive: true });
        }
        
        fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
    } catch (error) {
        console.log('保存配置失败: ' + error.message);
    }
}
```

---

## 11. 实用代码片段

### 获取玩家装备

```javascript
const equipmentSlots = ['head', 'chest', 'legs', 'feet', 'mainhand', 'offhand'];
equipmentSlots.forEach(slot => {
    const item = player.getItemBySlot(slot);
    if (!item.isEmpty()) {
        // 处理装备
    }
});
```

### 修改实体属性

```javascript
// 获取属性
const healthAttr = entity.getAttribute('minecraft:generic.max_health');
const attackAttr = entity.getAttribute('minecraft:generic.attack_damage');
const armorAttr = entity.getAttribute('minecraft:generic.armor');

// 设置基础值
if (healthAttr) {
    healthAttr.setBaseValue(newValue);
}
```

### 持久化数据存储

```javascript
const data = entity.persistentData;

// 存储数据
data.putDouble('key', value);
data.putString('key', 'value');
data.putBoolean('key', true);
data.putInt('key', 123);

// 读取数据
const value = data.getDouble('key');
const str = data.getString('key');
const bool = data.getBoolean('key');
const int = data.getInt('key');

// 检查存在
if (data.contains('key')) {
    // 处理逻辑
}
```

### 粒子效果

```javascript
const pos = entity.position;
entity.level.runCommandSilent(
    `particle minecraft:enchanted_hit ${pos.x} ${pos.y + 1} ${pos.z} 0.3 0.3 0.3 0.1 5`
);
```

### 延迟执行

```javascript
entity.level.server.scheduleInTicks(ticks, function() {
    // 延迟执行的逻辑
});
```

---

## 12. 调试技巧

```javascript
// 调试开关
const DEBUG_FLAGS = {
    console: false,
    chat: false
};

// 安全日志
function safeLog(msg, force) {
    if (force || DEBUG_FLAGS.console) console.log(msg);
}

// 实体类型检查
function shouldSkipEntity(e) {
    if (!e || e.isPlayer() || !e.isAlive()) return true;
    const name = e.getType().toString();
    const skipTypes = ['villager', 'animal', 'iron_golem', 'bat', 'marker', 'item', 
        'arrow', 'projectile', 'area_effect_cloud', 'painting', 'boat', 'minecart'];
    return skipTypes.some(v => name.includes(v));
}
```