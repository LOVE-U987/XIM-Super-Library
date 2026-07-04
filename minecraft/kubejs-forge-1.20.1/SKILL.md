---
name: kubejs-forge-1.20.1
description: 提供KubeJS Forge 1.20.1环境下的代码辅助，包含玩家属性修改、事件处理、命令注册、配方修改等功能。Invoke when user is writing KubeJS scripts for Forge 1.20.1 with KubeJS 1.6.5.
---

# KubeJS Forge 1.20.1 开发技能

## 环境信息

- **平台**: Forge 1.20.1
- **KubeJS版本**: 1.6.5
- **无额外插件**

> ⚠️ **警告**: 如果在非该环境下使用，可能出现函数名错误问题

---

## 1. 玩家属性修改

### 修改玩家最大血量

```javascript
// 获取玩家属性
const maxHealthAttr = player.getAttribute('minecraft:generic.max_health');

// 设置基础值
if (maxHealthAttr) {
    maxHealthAttr.setBaseValue(40); // 40 = 20颗心
    player.setHealth(40); // 恢复满血
}
```

### 常用属性ID

| 属性ID | 说明 |
|--------|------|
| `minecraft:generic.max_health` | 最大生命值 |
| `minecraft:generic.attack_damage` | 攻击伤害 |
| `minecraft:generic.armor` | 护甲值 |
| `minecraft:generic.armor_toughness` | 护甲韧性 |
| `minecraft:generic.movement_speed` | 移动速度 |
| `minecraft:generic.knockback_resistance` | 击退抗性 |

---

## 2. 事件处理

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

// 玩家重生
PlayerEvents.respawned(event => {
    const player = event.player;
    // 处理逻辑
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
    // 注册自定义命令
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
```

---

## 3. 命令注册

### 加载必要的Java类

```javascript
// 参数类型
const FloatArgumentType = Java.loadClass('com.mojang.brigadier.arguments.FloatArgumentType');
const IntegerArgumentType = Java.loadClass('com.mojang.brigadier.arguments.IntegerArgumentType');
const StringArgumentType = Java.loadClass('com.mojang.brigadier.arguments.StringArgumentType');
const BoolArgumentType = Java.loadClass('com.mojang.brigadier.arguments.BoolArgumentType');

// 实体参数
const EntityArgument = Java.loadClass('net.minecraft.commands.arguments.EntityArgument');

// 聊天组件
const Component = Java.loadClass('net.minecraft.network.chat.Component');
```

### 简单命令示例

```javascript
ServerEvents.commandRegistry(event => {
    const Commands = event.commands;
    
    event.register(
        Commands.literal('mycommand')
            .requires(ctx => ctx.hasPermission(0)) // 权限等级 0=所有人, 2=管理员
            .executes(ctx => {
                const player = ctx.source.player;
                ctx.source.sendSuccess(Component.literal('命令执行成功！'), true);
                return 1;
            })
    );
});
```

### 带参数的命令

```javascript
ServerEvents.commandRegistry(event => {
    const Commands = event.commands;
    
    event.register(
        Commands.literal('sethealth')
            .requires(ctx => ctx.hasPermission(2))
            .then(Commands.argument('player', EntityArgument.player())
                .then(Commands.argument('health', FloatArgumentType.floatArg(1, 1000))
                    .executes(ctx => {
                        const targetPlayer = EntityArgument.getPlayer(ctx, 'player');
                        const health = FloatArgumentType.getFloat(ctx, 'health');
                        
                        // 执行逻辑
                        
                        ctx.source.sendSuccess(Component.literal(`设置成功`), true);
                        return 1;
                    })
                )
            )
    );
});
```

---

## 4. 配方修改

### 有序配方

```javascript
ServerEvents.recipes(event => {
    event.shaped(
        Item.of('minecraft:diamond', 1),
        [
            'AAA',
            'ABA',
            'AAA'
        ],
        {
            A: 'minecraft:gold_ingot',
            B: 'minecraft:emerald'
        }
    );
});
```

### 无序配方

```javascript
ServerEvents.recipes(event => {
    event.shapeless(
        Item.of('minecraft:diamond', 1),
        ['minecraft:coal', 'minecraft:coal', 'minecraft:coal']
    );
});
```

### 移除配方

```javascript
ServerEvents.recipes(event => {
    // 按ID移除
    event.remove({ id: 'minecraft:stick' });
    
    // 按输出物品移除
    event.remove({ output: 'minecraft:diamond' });
    
    // 按输入物品移除
    event.remove({ input: 'minecraft:oak_log' });
});
```

---

## 5. 数据持久化

### 玩家数据存储

```javascript
// 存储数据
const data = player.persistentData;
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

// 删除数据
data.remove('key');
```

---

## 6. 实用代码片段

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

### 延迟执行

```javascript
// 延迟指定tick执行
server.scheduleInTicks(ticks, () => {
    // 延迟执行的逻辑
});
```

### 粒子效果

```javascript
const pos = player.position;
player.level.runCommandSilent(
    `particle minecraft:enchanted_hit ${pos.x} ${pos.y + 1} ${pos.z} 0.3 0.3 0.3 0.1 5`
);
```

### 发送消息给玩家

```javascript
// 发送普通消息
player.tell('普通消息');

// 发送带颜色的消息（使用Component）
player.tell(Component.literal('§a绿色消息§r'));
```

### 给予物品

```javascript
// 给予物品
player.give(Item.of('minecraft:diamond', 5));

// 给予经验
player.giveExperiencePoints(100);
```

---

## 7. 文件系统操作

```javascript
// 加载和保存JSON配置
function loadConfig() {
    try {
        const fs = require('fs');
        const path = require('path');
        const filePath = path.join('kubejs/config/myconfig.json');
        
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
        const filePath = path.join('kubejs/config/myconfig.json');
        
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

## 8. 调试技巧

```javascript
// 调试日志
console.log('调试信息: ' + value);

// 带条件的调试
const DEBUG = true;
function debugLog(msg) {
    if (DEBUG) console.log('[Debug] ' + msg);
}

// 实体类型检查
function shouldSkipEntity(entity) {
    if (!entity || entity.isPlayer() || !entity.isAlive()) return true;
    const name = entity.getType().toString();
    const skipTypes = ['villager', 'animal', 'iron_golem', 'bat', 'marker', 'item'];
    return skipTypes.some(v => name.includes(v));
}
```

---

## 9. 完整示例：玩家血量修改脚本

```javascript
// 配置项
const CONFIG = {
    INITIAL_MAX_HEALTH: 40,
    ONLY_FIRST_JOIN: true,
    DATA_KEY: 'kubejs_health_initialized'
};

// 设置玩家血量
function setPlayerHealth(player) {
    if (!player || !player.isAlive()) return;
    
    const maxHealthAttr = player.getAttribute('minecraft:generic.max_health');
    if (!maxHealthAttr) return;
    
    if (CONFIG.ONLY_FIRST_JOIN) {
        const persistentData = player.persistentData;
        if (persistentData.contains(CONFIG.DATA_KEY)) return;
        persistentData.putBoolean(CONFIG.DATA_KEY, true);
    }
    
    maxHealthAttr.setBaseValue(CONFIG.INITIAL_MAX_HEALTH);
    player.setHealth(CONFIG.INITIAL_MAX_HEALTH);
}

// 玩家登录事件
PlayerEvents.loggedIn(event => {
    const player = event.player;
    if (!player) return;
    
    event.server.scheduleInTicks(1, () => {
        setPlayerHealth(player);
    });
});

// 玩家重生事件
PlayerEvents.respawned(event => {
    const player = event.player;
    if (!player) return;
    
    event.server.scheduleInTicks(1, () => {
        if (player.getHealth() < player.getMaxHealth()) {
            player.setHealth(player.getMaxHealth());
        }
    });
});

console.log('[PlayerHealth] 玩家血量修改脚本已加载');
```

---

## 10. 常用Java类参考

| 类名 | 用途 |
|------|------|
| `com.mojang.brigadier.arguments.FloatArgumentType` | 浮点数参数 |
| `com.mojang.brigadier.arguments.IntegerArgumentType` | 整数参数 |
| `com.mojang.brigadier.arguments.StringArgumentType` | 字符串参数 |
| `com.mojang.brigadier.arguments.BoolArgumentType` | 布尔参数 |
| `net.minecraft.commands.arguments.EntityArgument` | 实体参数 |
| `net.minecraft.network.chat.Component` | 聊天组件 |
| `net.minecraft.resources.ResourceLocation` | 资源位置 |