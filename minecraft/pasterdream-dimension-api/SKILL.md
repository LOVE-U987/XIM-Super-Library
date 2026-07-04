---
name: "pasterdream-dimension-api"
description: "PasterDream 模组维度注册专用 API，提供 Facade+Builder 模式一键注册自定义维度。在需要创建新维度、配置维度类型/生物群系/背景音乐或生成维度 JSON 时调用。"
---

# PasterDream 维度注册 API

## 快速开始

```java
// 1. 在 PDDimensions.java 中使用 DimensionAPI 注册维度
DimensionResult result = DimensionAPI.createDimension("my_dimension")
    .natural(false)
    .hasSkylight(false)
    .bedWorks(false)
    .build();

// 2. 在 ClientSetup.java 中注册维度特效
event.register(id, new DimensionSpecialEffects(...));
```

## ⚠️ Minecraft 1.21 维度 JSON 格式要求（反复踩坑警告）

**这是本项目最常出问题的点！每次创建新维度前务必核对以下规则。**

### 1. 维度 JSON 必须包含的字段

Minecraft 1.21 要求 `data/<modid>/dimension/<name>.json` 必须包含以下字段：

| 字段 | 说明 | ⚠️ 常见错误 |
|------|------|------------|
| `type` | 维度类型引用，如 `pasterdream:my_dimension` | ❌ 缺失导致 "No key type" |
| `generator.type` | 必须是 `minecraft:noise` | ❌ 使用 `flat` 导致解析失败 |
| `generator.biome_source` | 生物群系来源配置 | ❌ 缺失导致加载失败 |
| `generator.settings` | 噪声生成器设置 | ❌ 缺失导致 "No key generator" |
| `generator.settings.noise_router` | **1.21 必须字段** | ❌ ❌ **缺失直接崩溃，报 "No key noise_router"** |
| `generator.settings.surface_rule` | **1.21 必须字段** | ❌ ❌ **缺失直接崩溃，报 "No key surface_rule"** |

### 2. 虚空维度模板（推荐使用）

对于不需要地形生成的虚空世界（如 BOSS 竞技场），使用以下模板：

```json
{
  "type": "pasterdream:my_arena_world",
  "generator": {
    "type": "minecraft:noise",
    "biome_source": {
      "type": "minecraft:fixed",
      "biome": "pasterdream:my_arena_biome"
    },
    "settings": {
      "name": "pasterdream:my_arena_world",
      "sea_level": 0,
      "legacy_random_source": true,
      "disable_mob_generation": true,
      "aquifers_enabled": false,
      "ore_veins_enabled": false,
      "default_block": {
        "Name": "minecraft:air"
      },
      "default_fluid": {
        "Name": "minecraft:air"
      },
      "spawn_target": [],
      "noise": {
        "min_y": 0,
        "height": 128,
        "size_horizontal": 2,
        "size_vertical": 1
      },
      "noise_router": {
        "barrier": 0.0,
        "fluid_level_floodedness": 0.0,
        "fluid_level_spread": 0.0,
        "lava": 0.0,
        "temperature": 0.0,
        "vegetation": 0.0,
        "continents": 0.0,
        "erosion": 0.0,
        "depth": 0.0,
        "ridges": 0.0,
        "initial_density_without_jaggedness": 0.0,
        "final_density": -1000000.0,
        "vein_toggle": 0.0,
        "vein_ridged": 0.0,
        "vein_gap": 0.0
      },
      "surface_rule": {
        "type": "minecraft:sequence",
        "sequence": []
      }
    }
  }
}
```

> ⚠️ **特别注意**：`noise_router` 中**不能使用 `minecraft:empty`**，必须使用：
> - 数字 `0.0`（用于简单标量）
> - 数字 `-1000000.0`（用于虚空世界的 final_density）
> - 不能直接引用未定义的资源位置
> - **不能**使用 `{"type": "minecraft:constant", "value": ...}` 对象格式，因为 constant 只能使用简写数字格式

### 3. 维度类型 JSON 要求

`data/<modid>/dimension_type/<name>.json` 必须包含以下字段：

```json
{
  "height": 128,
  "height_minus_one": 127,
  "logical_height": 128,
  "bed_works": false,
  "has_skylight": false,
  "has_ceiling": false,
  "coordinate_scale": 1.0,
  "ambient_light": 0.0,
  "ultra_warm": false,
  "natural": false,
  "piglin_safe": true,
  "respawn_anchor_works": false,
  "bed_enabled": false,
  "force_ruin_temp": false,
  "min_y": 0,
  "monster_spawn_light_level": {
    "type": "minecraft:constant",
    "value": 0
  },
  "monster_spawn_block_light_level": {
    "type": "minecraft:constant",
    "value": 0
  }
}
```

### 4. 常见错误与解决方案

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `No key noise_router` | 维度 JSON 缺失 `noise_router` 字段 | 添加完整的 `noise_router` 配置 |
| `No key surface_rule` | 维度 JSON 缺失 `surface_rule` 字段 | 添加 `surface_rule: {type: sequence, sequence: []}` |
| `Failed to parse either. Not a number: {"type":"minecraft:empty"...}` | 使用了无效的 `minecraft:empty` | 使用数字 `0.0` 代替 |
| `Failed to parse either. Not a number: {"type":"minecraft:constant"...}` | `minecraft:constant` 使用了对象格式 | 使用简写数字 `-1000000.0` 代替 |
| `Failed to parse dimension` | JSON 格式错误或缺少必需字段 | 检查 JSON 语法，确保所有字段完整 |
| `No key type` | `type` 字段引用了不存在的维度类型 | 确认维度类型 JSON 已正确创建 |

### 5. 正确放置文件

| 文件类型 | 正确路径 | ❌ 错误路径 |
|---------|---------|------------|
| 维度 JSON | `data/<modid>/dimension/<name>.json` | `assets/<modid>/dimension/` |
| 维度类型 JSON | `data/<modid>/dimension_type/<name>.json` | `assets/<modid>/dimension_type/` |
| 生物群系 JSON | `data/<modid>/worldgen/biome/<name>.json` | `assets/<modid>/biome/` |
| 结构模板 NBT | `data/<modid>/structures/<name>.nbt` | `assets/<modid>/structures/` |

### 6. 代码中使用 DimensionAPI

```java
// PasterDream/src/main/java/.../PDDimensions.java
public static final DimensionResult AARONCOS_ARENA_WORLD;

static {
    AARONCOS_ARENA_WORLD = DimensionAPI.createDimension("aaroncos_arena_world")
            .natural(false)
            .hasSkylight(false)
            .bedWorks(false)
            .hasRaids(false)
            .piglinSafe(true)
            .ambientLight(0.0f)
            .minY(0)
            .height(128)
            .logicalHeight(128)
            .coordinateScale(1.0)
            .monsterSpawnLightLevel(0, 0)
            .hasCeiling(false)
            .ultraWarm(false)
            .respawnAnchorWorks(false)
            .forceRuinTemp(false)
            .generateJson(false)  // 虚空维度需要手动编写 JSON
            .build();
}
```

## 维度特效注册（ClientSetup）

```java
// PasterDream/src/main/java/.../client/ClientSetup.java
@SubscribeEvent
public static void registerDimensionEffects(RegisterDimensionSpecialEffectsEvent event) {
    // 深灰色迷雾虚空世界
    event.register(
        ResourceLocation.fromNamespaceAndPath("pasterdream", "aaroncos_arena_world"),
        new DimensionSpecialEffects.Builder()
            .fogColor(0.2f, 0.2f, 0.2f)
            .skyColor(0x000000)
            .skyType(SkyType.NONE)
            .hasAmbientLighting(true)
            .ambientLightMultiplier(1.0f)
            .redstoneTintMethod(Ambient DarknessMethods.DEFAULT)
            .build()
    );
}
```

## 维度进入事件处理

```java
// PasterDream/src/main/java/.../registry/PDArenaEvents.java
public class PDArenaEvents {
    public static void onPlayerChangedDimension(PlayerEvent.PlayerChangedDimensionEvent event) {
        if (!event.getTo().equals(PDDimensions.MY_DIMENSION.levelKey())) {
            return;
        }
        // 处理玩家进入维度的逻辑
        // 如：放置结构、清除实体、赋予效果等
    }
}

// 在 PasterDreamMod.java 中注册事件
NeoForge.EVENT_BUS.addListener(PDArenaEvents::onPlayerChangedDimension);
```

## 调试技巧

1. **检查日志**：游戏崩溃时查看 `run/logs/latest.log`，搜索 `Registry loading errors`
2. **验证 JSON**：使用在线 JSON 验证器检查语法
3. **对比参考**：参考项目中已工作的维度 JSON（`dyedream_world.json`）
4. **逐步添加**：先使用最小配置，确认能加载后再逐步添加功能

## 参考文件

- 虚空维度示例：`data/pasterdream/dimension/aaroncos_arena_world.json`
- 复杂维度示例：`data/pasterdream/dimension/dyedream_world.json`
- 维度类型示例：`data/pasterdream/dimension_type/aaroncos_arena_world.json`
