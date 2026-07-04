---
name: "mc-config-ui"
description: "Minecraft 模组配置界面开发指南，包含 Modern UI（GPU 加速）和原生 Screen 两套方案。Invoke when developing config screens, settings UI, or any in-game GUI for Minecraft mods on NeoForge 1.21.1."
---

# Minecraft 模组配置界面开发指南

## 概述

本 SKILL 收录两套独立的配置界面方案：

| 方案 | 框架 | 渲染 | 适用场景 |
|:--|:--|:--|:--|
| **Modern UI** | `icyllis.modernui.*` | GPU 加速 (OpenGL 3.3+) | 华丽动画、毛玻璃、Material Design 风格 |
| **原生 Screen** | `net.minecraft.client.gui.screens.Screen` | CPU 软件渲染 | 轻量配置、与原版风格一致、低配兼容 |

---

## 方案一：Modern UI（GPU 加速）

### 依赖配置 (build.gradle)

```groovy
repositories {
    maven { url 'https://maven.izzel.io/releases' }
}

dependencies {
    implementation files('libs/ModernUI-NeoForge-1.21.1-3.12.0.2.jar')
    compileOnly files('libs/ModernUI-Core-3.12.0.jar')
    additionalRuntimeClasspath files('libs/ModernUI-Core-3.12.0.jar')
    compileOnly files('libs/ModernUI-Markflow-3.12.0.jar')
    additionalRuntimeClasspath files('libs/ModernUI-Markflow-3.12.0.jar')
}
```

> `implementation` 只管编译；`compileOnly` + `additionalRuntimeClasspath` 组合确保运行时也能找到 Core/Markflow 类。

### 入口：MuiModApi

```java
import icyllis.modernui.mc.MuiModApi;
import icyllis.modernui.mc.BlurHandler;

// 创建并打开 Modern UI 屏幕（带毛玻璃）
var screen = MuiModApi.get().createScreen(new MyFragment());
BlurHandler.INSTANCE.blur(screen);
Minecraft.getInstance().setScreen(screen);
```

**MuiModApi 方法一览：**

```java
// 获取单例
static MuiModApi get();

// 创建屏幕（返回 Screen & MuiScreen）
<T extends Screen & MuiScreen> T createScreen(Fragment fragment);
<T extends Screen & MuiScreen> T createScreen(Fragment, ScreenCallback);
<T extends Screen & MuiScreen> T createScreen(Fragment, ScreenCallback, Screen);
<T extends Screen & MuiScreen> T createScreen(Fragment, ScreenCallback, Screen, CharSequence);

// 直接打开（便捷方法）
static void openScreen(Fragment);
```

**BlurHandler 毛玻璃控制：**

```java
// 为屏幕开启毛玻璃
BlurHandler.INSTANCE.blur(screen);

// 全局模糊半径配置（由 Modern UI 配置控制）
BlurHandler.sBlurRadius;         // static volatile int
BlurHandler.sBlurEffect;         // static volatile boolean
```

### Fragment 生命周期

```java
public class MyFragment extends Fragment {
    // 创建视图（类似 Android Fragment）
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             DataSet savedInstanceState) {
        LinearLayout root = new LinearLayout(getContext());
        root.setOrientation(LinearLayout.VERTICAL);
        // ... 构建 UI
        return root;
    }

    // 视图创建完成后回调
    @Override
    public void onViewCreated(View view, DataSet savedInstanceState) { }

    // 初始化数据（类似 Android Bundle）
    @Override
    public void onCreate(DataSet savedInstanceState) { }
}
```

> **注意**：Modern UI 的 `onCreateView` 第三个参数是 `DataSet` 而非 `Bundle`。`LayoutInflater` 在 `icyllis.modernui.view` 包下。

### 核心视图体系

```
Fragment → onCreateView()
  └── View (ViewGroup)
       ├── LinearLayout (orientation: HORIZONTAL / VERTICAL)
       ├── TextView (text, textSize, textColor, gravity)
       ├── Button (extends TextView)
       ├── Switch (extends Button implements Checkable)
       ├── SeekBar (setMax, setProgress)
       └── View (占位/分割线)
```

**常用方法：**
```java
// View
view.setBackground(Drawable);           // 设置背景（GradientDrawable）
view.setAlpha(float);                   // 透明度
view.setTranslationX/Y/Z(float);        // 位移
view.setScaleX/Y(float);                // 缩放
view.setRotation/X/Y(float);            // 旋转
view.setPivotX/Y(float);                // 变换轴心
view.postDelayed(Runnable, long);       // 延迟执行
view.post(Runnable);

// TextView
textView.setText(CharSequence);
textView.setTextSize(float);            // sp 单位
textView.setTextColor(int);             // ARGB
textView.setGravity(int);               // Gravity.CENTER 等
textView.setPadding(l, t, r, b);

// ViewGroup / LinearLayout
layout.setOrientation(int);
layout.setGravity(int);
layout.addView(View);
layout.addView(View, LayoutParams);
layout.setPadding(l, t, r, b);
```

### GradientDrawable（形状背景）

```java
// 只支持无参构造器！
GradientDrawable bg = new GradientDrawable();               // 实心
GradientDrawable gradient = new GradientDrawable(            // 渐变色
    GradientDrawable.Orientation.TOP_BOTTOM, new int[]{...});

bg.setColor(int);                   // 填充色 ARGB
bg.setCornerRadius(float);          // 圆角半径
bg.setStroke(width, color);         // 边框

view.setBackground(bg);
```

**字段设置和颜色状态列表：**
```java
import icyllis.modernui.util.ColorStateList;

// 单个颜色的 ColorStateList
ColorStateList colorList = ColorStateList.valueOf(0xFF6C63FF);

// 设置 Switch 轨道/拇指颜色
switchBtn.setTrackTintList(colorList);
switchBtn.setThumbTintList(colorList);
```

### 动画系统

**核心 API：**
```java
View.ALPHA         // FloatProperty<View>
View.TRANSLATION_X // FloatProperty<View>
View.TRANSLATION_Y // FloatProperty<View>
View.SCALE_X       // FloatProperty<View>
View.SCALE_Y       // FloatProperty<View>
View.ROTATION      // FloatProperty<View>
```

**ObjectAnimator（属性动画）：**
```java
// 淡入
ObjectAnimator alphaAnim = ObjectAnimator.ofFloat(view, View.ALPHA, 0f, 1f);
alphaAnim.setDuration(400);
alphaAnim.setInterpolator(TimeInterpolator.DECELERATE);
alphaAnim.start();

// 平移
ObjectAnimator transAnim = ObjectAnimator.ofFloat(view, View.TRANSLATION_Y, 40f, 0f);
transAnim.setDuration(400);
transAnim.setInterpolator(new AnticipateOvershootInterpolator(1.2f));
transAnim.start();

// 缩放
ObjectAnimator scaleX = ObjectAnimator.ofFloat(view, View.SCALE_X, 1f, 0.92f);
scaleX.setDuration(80);
scaleX.start();
```

**ValueAnimator（值动画，用于颜色等）：**
```java
ValueAnimator colorAnim = ValueAnimator.ofArgb(0xFF6C63FF, 0xFF4CAF50, 0xFF6C63FF);
colorAnim.setDuration(600);
colorAnim.addUpdateListener(animator -> {
    int color = (int) animator.getAnimatedValue();
    GradientDrawable bg = new GradientDrawable();
    bg.setColor(color);
    bg.setCornerRadius(14f);
    button.setBackground(bg);
});
colorAnim.start();
```

**TimeInterpolator（插值器）：**
```java
// 内置常量
TimeInterpolator.LINEAR
TimeInterpolator.ACCELERATE
TimeInterpolator.DECELERATE
TimeInterpolator.ACCELERATE_DECELERATE
TimeInterpolator.OVERSHOOT
TimeInterpolator.ANTICIPATE_OVERSHOOT
TimeInterpolator.BOUNCE

// 工厂方法
TimeInterpolator.accelerate(float factor);
TimeInterpolator.decelerate(float factor);
TimeInterpolator.overshoot(float tension);

// 自定义插值器（需带张力参数用类构造）
AnticipateOvershootInterpolator(float tension);
AnticipateOvershootInterpolator(float tension, float extraTension);
```

### 控件事件

```java
// Switch 开关变化
switchBtn.setOnCheckedChangeListener((buttonView, isChecked) -> { });

// SeekBar 滑块变化
seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
    void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser);
    void onStartTrackingTouch(SeekBar seekBar);
    void onStopTrackingTouch(SeekBar seekBar);
});

// View 点击
view.setOnClickListener(v -> { });
```

### Modern UI 完整 Demo

参考项目中的：[ModConfigFragment.java](file:///c:/Users/97128/Documents/GitHub/Please%20use%20this%20one/src/main/java/com/pleaseusethisone/pleaseusethisone/client/gui/modern/ModConfigFragment.java)

---

## 方案二：原生 Screen（CPU 渲染）

### 基础架构

```java
public class MyConfigScreen extends Screen {
    private final Screen parent;
    private final List<AbstractWidget> configWidgets = new ArrayList<>();
    private int scrollOffset = 0;

    // 布局常量
    private static final int LIST_TOP    = 42;
    private static final int LIST_BOTTOM = 48;
    private static final int PADDING     = 24;
    private static final int ROW_HEIGHT  = 44;

    public MyConfigScreen(Screen parent) {
        super(Component.translatable("gui.mymod.config.title"));
        this.parent = parent;
        this.openTime = System.currentTimeMillis();  // 入场动画用
    }
}
```

### 注册为 NeoForge 配置界面

```java
// 在客户端构造方法中
container.registerExtensionPoint(IConfigScreenFactory.class,
    (IConfigScreenFactory) (modContainer, modListScreen) ->
            new MyConfigScreen(modListScreen));
```

`IConfigScreenFactory` 方法签名：`Screen createScreen(ModContainer container, Screen modListScreen)`

### 禁用模糊背景（关键技巧）

```java
@Override
protected void renderBlurredBackground(float partialTick) {
    // 空实现 —— 彻底禁用模糊背景，避免文字糊化
}
```

### 渲染流程（带裁剪区域）

```java
@Override
public void render(GuiGraphics gui, int mouseX, int mouseY, float partialTick) {
    // 1. 纯色背景（不要调 super.render()）
    gui.fill(0, 0, this.width, this.height, 0xFF1A1A2E);

    // 2. 列表区域背景
    gui.fill(PADDING, LIST_TOP, this.width - PADDING,
             this.height - LIST_BOTTOM, 0xCC1E1E3A);

    // 3. 标题（裁剪区域外）
    gui.drawCenteredString(this.font, this.title, this.width / 2, 14, 0xFFFFFF);

    // 4. 启用裁剪
    gui.enableScissor(PADDING, LIST_TOP, this.width - PADDING, this.height - LIST_BOTTOM);

    // 5. 渲染标签文字
    renderLabels(gui);

    // 6. 在裁剪区域内渲染控件
    for (AbstractWidget w : configWidgets) {
        if (w.visible) w.render(gui, mouseX, mouseY, partialTick);
    }

    // 7. 禁用裁剪
    gui.disableScissor();

    // 8. 渲染固定控件（保存按钮等）
    for (var r : this.renderables) {
        if (!configWidgets.contains(r)) r.render(gui, mouseX, mouseY, partialTick);
    }
}
```

### 控件工厂方法

```java
// 布尔开关按钮
private int addBooleanRow(int x, int y, String key, boolean value,
                          Consumer<Boolean> onChange) {
    int wx = this.width - PADDING - 110;
    CycleButton<Boolean> btn = CycleButton.booleanBuilder(
            Component.translatable("value.on"),
            Component.translatable("value.off")
    ).displayOnlyValue()
            .withInitialValue(value)
            .create(wx, y + 10, 110, 20, Component.empty(),
                    (b, val) -> onChange.accept(val));
    btn.setTooltip(Tooltip.create(Component.translatable(key + ".tooltip")));
    configWidgets.add(btn);
    this.addRenderableWidget(btn);
    return y + ROW_HEIGHT;
}

// 数值增减按钮
private int addIntensityRow(int x, int y, int value, Consumer<Integer> onChange) {
    int wx = this.width - PADDING - 110;
    int bs = 20;

    Button minus = Button.builder(Component.literal("-"),
            b -> onChange.accept(Math.max(0, value - 10)))
            .bounds(wx, y + 6, bs, bs).build();
    configWidgets.add(minus); this.addRenderableWidget(minus);

    Button display = Button.builder(Component.literal(String.valueOf(value)),
            b -> {}).bounds(wx + bs + 4, y + 6, 110 - bs * 2 - 8, bs).build();
    display.active = false;
    configWidgets.add(display); this.addRenderableWidget(display);

    Button plus = Button.builder(Component.literal("+"),
            b -> onChange.accept(Math.min(100, value + 10)))
            .bounds(wx + 110 - bs, y + 6, bs, bs).build();
    configWidgets.add(plus); this.addRenderableWidget(plus);

    return y + ROW_HEIGHT;
}
```

### 滚动系统

```java
@Override
public boolean mouseScrolled(double mx, double my, double sx, double sy) {
    int totalH = configWidgets.size() * ROW_HEIGHT;
    int visibleH = this.height - LIST_TOP - LIST_BOTTOM;
    int maxScroll = Math.max(0, totalH - visibleH);
    scrollOffset = (int) Math.max(0, Math.min(maxScroll, scrollOffset - sy * 12));
    updateWidgetPositions();
    return true;
}

private void updateWidgetPositions() {
    int y = LIST_TOP - scrollOffset;
    for (int i = 0; i < configWidgets.size(); i++) {
        AbstractWidget w = configWidgets.get(i);
        w.setY(y + 10);
        w.visible = y + ROW_HEIGHT > LIST_TOP && y < this.height - LIST_BOTTOM;
        // 强度行需特殊处理（索引跳过）
        y += ROW_HEIGHT;
    }
}
```

### 入场动画

```java
private long openTime;
private boolean animating = true;

private float getEntryProgress(int index) {
    if (!animating) return 1.0f;
    long elapsed = System.currentTimeMillis() - openTime;
    float delay = index * 60f;
    float duration = 350f;
    float raw = Math.max(0f, Math.min(1f, (elapsed - delay) / duration));
    float progress = easeOutCubic(raw);
    if (progress >= 1.0f && index >= 3) animating = false;
    return progress;
}

private float easeOutCubic(float t) {
    return 1.0f - (float) Math.pow(1.0f - t, 3);
}

private float easeOutQuart(float t) {
    return 1.0f - (float) Math.pow(1.0f - t, 4);
}
```

### 原生 Screen 完整 Demo

参考项目中的：[ModNativeConfigScreen.java](file:///c:/Users/97128/Documents/GitHub/Please%20use%20this%20one/src/main/java/com/pleaseusethisone/pleaseusethisone/client/gui/config/ModNativeConfigScreen.java)

---

## 语言文件规范

### 命名格式

```
gui.<modid>.config.title                    // 界面标题
gui.<modid>.config.<item_key>               // 配置项标签
gui.<modid>.config.<item_key>.tooltip       // 配置项悬停提示
gui.<modid>.config.save                     // 保存按钮
gui.<modid>.config.save.success             // 保存成功消息
gui.<modid>.config.value.on                 // 通用：开启
gui.<modid>.config.value.off                // 通用：关闭
```

### 代码中使用

```java
// 前缀常量
private static final String LANG_PREFIX = "gui.pleaseusethisone.config";

// 标题
Component.translatable(LANG_PREFIX + ".title")

// 配置项
Component.translatable(LANG_PREFIX + ".auto_mode")
Component.translatable(LANG_PREFIX + ".auto_mode.tooltip")

// 布尔值
Component.translatable(LANG_PREFIX + ".value.on")
Component.translatable(LANG_PREFIX + ".value.off")
```

### 示例 (zh_cn.json)

```json
{
  "gui.pleaseusethisone.config.title": "模组配置",
  "gui.pleaseusethisone.config.auto_mode": "自动模式",
  "gui.pleaseusethisone.config.auto_mode.tooltip": "开启后模组自动处理常规任务",
  "gui.pleaseusethisone.config.save": "保存配置",
  "gui.pleaseusethisone.config.save.success": "✅ 配置已保存！",
  "gui.pleaseusethisone.config.value.on": "开启",
  "gui.pleaseusethisone.config.value.off": "关闭"
}
```

---

## 方案对比 & 选型建议

| 对比维度 | Modern UI | 原生 Screen |
|:--|:--|:--|
| **渲染性能** | GPU 加速，动画丝滑 | CPU 渲染，复杂动画卡顿 |
| **视觉效果** | 毛玻璃、圆角、Material Design | 原版像素风格 |
| **布局开发** | LinearLayout 声明式布局 | 手动计算 x/y 坐标 |
| **动画开发** | ObjectAnimator/ValueAnimator，一行代码 | 手动计时 + 缓动函数，代码量大 |
| **学习成本** | 需学习 Modern UI API | 熟悉 Minecraft Screen 即可 |
| **依赖体积** | 额外 3 个 jar (约 4.5MB) | 零额外依赖 |
| **模组兼容性** | 与其他使用 Screen 的模组无冲突 | 标准方案 |
| **毛玻璃背景** | BlurHandler 一键开启 | 需手动禁用原版模糊，改纯色背景 |

**选型建议：**
- 需要华丽动画、毛玻璃、Material 风格 → **Modern UI**
- 轻量配置页、追求兼容性、与原版一致 → **原生 Screen**
- 两者可以共存，互不干扰（如本项目中按 B 开 Modern UI，Mod 列表配置按钮开原生 Screen）
