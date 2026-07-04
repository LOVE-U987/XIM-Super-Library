---
name: tacz-recipe-1.20.1
description: 该Skill的环境是1.20.1 Forge，kubejs版本为1.6.5，需tacz的任意版本，如需要调用该方法，请查看有关的环境，否则可能报错  Converts JSON recipe data to KubeJS TaCZ recipe code. Invoke when user provides a JSON file with recipe data and asks to convert it to KubeJS format.
---

# TaCZ Recipe Converter

This skill converts simplified JSON recipe format into proper KubeJS TaCZ recipe code.

## Input Format

User provides a JSON file with the following structure:

```json
{
    "输出物品": "modid:item_name",
    "输出数量": 1,
    "输入物品": [
        {
            "tag": "forge:ingots/copper",
            "count": 5
        },
        {
            "item": "modid:item_name",
            "count": 1
        }
    ],
    "配方类型": "tacz:gun_smith_table_crafting"
}
```

### Field Mapping

| JSON Field | Meaning | KubeJS Field |
|------------|---------|--------------|
| `输出物品` | Result item ID | `result.item.item` |
| `输出数量` | Result count | `result.item.count` |
| `输入物品` | Materials array | `materials` |
| `配方类型` | Recipe type | `type` |

### Material Format

Each material in `输入物品` can have:
- `"tag": "forge:xxx"` - Use Forge ore dictionary tag
- `"item": "modid:xxx"` - Use specific item ID
- `"count": number` - Quantity required

## Output Format

Generate KubeJS code following this structure:

```javascript
// 配方名称（从输出物品推断）
event.custom({
  type: "tacz:gun_smith_table_crafting",
  materials: [
    { item: { tag: "forge:ingots/copper" }, count: 5 },    // 材料注释
    { item: { item: "modid:item_name" }, count: 1 }       // 材料注释
  ],
  result: {
    type: "custom",
    group: "tacz:ammo",
    item: {
      item: "modid:result_item",
      count: 1
    }
  }
});
```

## Processing Steps

1. **Read the JSON file** provided by user
2. **Extract all fields** from the JSON
3. **Convert materials**:
   - If `tag` field exists → use `{ item: { tag: "..." }, count: X }`
   - If `item` field exists → use `{ item: { item: "..." }, count: X }`
4. **Generate comments** for each material (use Chinese names if identifiable)
5. **Build the KubeJS code** with proper indentation and formatting
6. **Append to recipes.js** or provide as insertable code block

## Code Style Guidelines

- Use 2-space indentation
- Add Chinese comments for each material
- Add empty line before each recipe
- End each recipe with `});`
- Use `//` separator comments for recipe categories if applicable

## Example Conversion

**Input JSON:**
```json
{
    "输出物品": "superbwarfare:medium_anti_air_missile",
    "输出数量": 1,
    "输入物品": [
        {"tag": "forge:ingots/copper", "count": 5},
        {"item": "superbwarfare:missile_engine", "count": 1},
        {"item": "superbwarfare:seeker", "count": 1},
        {"item": "superbwarfare:high_energy_explosives", "count": 1}
    ],
    "配方类型": "tacz:gun_smith_table_crafting"
}
```

**Output KubeJS:**
```javascript
// 中型对空导弹
event.custom({
  type: "tacz:gun_smith_table_crafting",
  materials: [
    { item: { tag: "forge:ingots/copper" }, count: 5 },              // 铜锭
    { item: { item: "superbwarfare:missile_engine" }, count: 1 },   // 导弹发动机
    { item: { item: "superbwarfare:seeker" }, count: 1 },           // 导引头
    { item: { item: "superbwarfare:high_energy_explosives" }, count: 1 } // 高能量炸药
  ],
  result: {
    type: "custom",
    group: "tacz:ammo",
    item: {
      item: "superbwarfare:medium_anti_air_missile",
      count: 1
    }
  }
});
```

## Common Material Names (for comments)

| Item ID Pattern | Chinese Name |
|-----------------|--------------|
| `*_ingot` | XX锭 |
| `*_nugget` | XX粒 |
| `*_plate` | XX板 |
| `gunpowder` | 火药 |
| `redstone` | 红石 |
| `iron_bars` | 铁栏杆 |
| `planks` | 木板 |
| `primer` | 底火 |
| `motor` | 马达 |
| `seeker` | 导引头 |
| `missile_engine` | 导弹发动机 |
| `high_energy_explosives` | 高能量炸药 |
| `fusee` | 引信 |