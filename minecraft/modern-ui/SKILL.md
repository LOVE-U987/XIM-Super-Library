---
name: modern-ui
description: 提供 Modern UI (ModernUI-MC) 在 NeoForge 1.21.1 环境下开发 GPU 加速、高视觉效果 UI 的完整 API 参考和代码指南。Invoke when developing Minecraft mod UI using Modern UI framework on NeoForge 1.21.1, including Fragment-based screens, animations, Material Design components, and advanced visual effects.
---

# Modern UI - NeoForge 1.21.1 现代化 UI 开发指南

## 📋 概述

**Modern UI (ModernUI-MC)** 是由 BloCamLimb 开发的跨平台桌面 UI 框架，已深度集成到 Minecraft 渲染管道中。

### ✨ 核心优势

| 特性 | 说明 |
|------|------|
| **GPU 加速渲染** | 基于 OpenGL 3.3+ / Vulkan 1.1，摆脱 GuiGraphics 的 2D 位图限制 |
| **Android 风格 API** | Fragment/View/ViewGroup 体系，像写 Android App 一样写 MC UI |
| **高级视觉效果** | 原生支持阴影、圆角、渐变、毛玻璃、贝塞尔曲线 |
| **动画系统** | ValueAnimator/ObjectAnimator，60fps 硬件加速动画 |
| **Material Design** | 内置 Material 组件库（Button, Switch, Slider, TabLayout 等） |
| **富文本** | Markflow 扩展支持 Markdown 渲染 |

### 🏗️ 架构层级

```
Minecraft Screen
  └── ModernUIRoot (由 ModernUIApi 创建)
        └── Fragment (UI 页面单元)
              ├── ViewGroup (布局容器)
              │     ├── LinearLayout
              │     ├── FrameLayout
              │     ├── ScrollView
              │     ├── RecyclerView
              │     └── ConstraintLayout
              └── View (具体控件)
                    ├── TextView / Button / EditText
                    ├── ImageView / SeekBar / Switch
                    ├── ProgressBar / CheckBox
                    └── 自定义 View (onDraw 绘制)
```

---

## 🔧 环境配置

### 1. build.gradle 依赖

```groovy
repositories {
    // Maven Central —— Modern UI 的传递依赖（如 commonmark）托管在此
    mavenCentral()

    // IzzelAliz Maven —— 存放 Modern UI 框架核心依赖
    maven {
        name 'IzzelAliz Maven'
        url 'https://maven.izzel.io/releases/'
    }
}

dependencies {
    // ========== Modern UI —— GPU 加速的现代化 UI 框架 ==========
    // ⚠️ 由于 ModDevGradle 对第三方 Maven 仓库的模块化类加载支持有限，
    // 推荐从 IzzelAliz Maven 下载 jar 后放入 libs/ 目录使用本地文件引用

    // Modern UI for Minecraft NeoForge 集成（模组 jar）
    implementation files('libs/ModernUI-NeoForge-1.21.1-3.12.0.2.jar')
    // Core + Markflow：compileOnly（编译需要）+ additionalRuntimeClasspath（NeoForge 模块系统运行时需要）
    compileOnly files('libs/ModernUI-Core-3.12.0.jar')
    additionalRuntimeClasspath files('libs/ModernUI-Core-3.12.0.jar')
    compileOnly files('libs/ModernUI-Markflow-3.12.0.jar')
    additionalRuntimeClasspath files('libs/ModernUI-Markflow-3.12.0.jar')

    // 如需从 Maven 自动解析（⚠️ 注意：ModDevGradle 中可能因仓库优先级问题解析失败）：
    // implementation("icyllis.modernui:ModernUI-NeoForge:${minecraft_version}-${modernui_version}") { ... }
    // implementation("icyllis.modernui:ModernUI-Core:${modernui_core_version}") { ... }
    // implementation("icyllis.modernui:ModernUI-Markflow:${modernui_core_version}") { ... }
}

### 2. 下载 Modern UI jar

从 IzzelAliz Maven 手动下载以下 jar 放入项目的 `libs/` 目录：

| 文件 | 下载链接 | 大小 |
|------|---------|------|
| ModernUI-NeoForge | https://maven.izzel.io/releases/icyllis/modernui/ModernUI-NeoForge/1.21.1-3.12.0.2/ModernUI-NeoForge-1.21.1-3.12.0.2.jar | ~829 KB |
| ModernUI-Core | https://maven.izzel.io/releases/icyllis/modernui/ModernUI-Core/3.12.0/ModernUI-Core-3.12.0.jar | ~3.6 MB |
| ModernUI-Markflow | https://maven.izzel.io/releases/icyllis/modernui/ModernUI-Markflow/3.12.0/ModernUI-Markflow-3.12.0.jar | ~38 KB |

```powershell
# PowerShell 一键下载命令（在项目根目录运行）
$base = "https://maven.izzel.io/releases/icyllis/modernui"
$files = @(
    "ModernUI-NeoForge/1.21.1-3.12.0.2/ModernUI-NeoForge-1.21.1-3.12.0.2.jar",
    "ModernUI-Core/3.12.0/ModernUI-Core-3.12.0.jar",
    "ModernUI-Markflow/3.12.0/ModernUI-Markflow-3.12.0.jar"
)
foreach ($f in $files) {
    $url = "$base/$f"
    $name = $f.Split('/')[-1]
    Invoke-WebRequest -Uri $url -OutFile "libs/$name"
}
```

### 3. gradle.properties

```properties
# Modern UI 框架版本（详见 https://github.com/BloCamLimb/ModernUI-MC）
modernui_version=3.12.0.2
# Modern UI Core/Markflow 库版本（与 NeoForge 集成版的后缀不同）
modernui_core_version=3.12.0
```

### 3. neoforge.mods.toml（模组依赖声明）

```toml
# Modern UI —— GPU 加速的现代化桌面 UI 框架
[[dependencies.${mod_id}]]
    modId="modernui"
    type="required"
    versionRange="[3.12,)"
    ordering="AFTER"
    side="CLIENT"
```

---

## 🧩 核心概念

### 1. ModernUIApi —— 入口 API

```java
/**
 * Modern UI 的核心 API 入口，提供创建 Fragment UI 的工厂方法。
 * 通过 ModernUIApi.get() 获取单例实例。
 */
public interface ModernUIApi {

    /**
     * 获取 ModernUIApi 单例实例。
     *
     * @return ModernUIApi 实例
     */
    static ModernUIApi get();

    /**
     * 创建一个 Fragment 屏幕。
     * 这是 Modern UI 最常用的入口：传入 Fragment 实例，自动包装为 Screen。
     *
     * @param fragment 要展示的 Fragment 实例
     * @return 包装好的 Screen，可直接通过 Minecraft.setScreen() 打开
     */
    Screen createScreen(@NotNull Fragment fragment);

    /**
     * 创建一个 Fragment 屏幕，带背景模糊效果。
     *
     * @param fragment 要展示的 Fragment 实例
     * @param blurRadius 模糊半径（像素）
     * @return 包装好的 Screen，带背景模糊
     */
    Screen createScreen(@NotNull Fragment fragment, int blurRadius);
}
```

**典型用法**：
```java
// 通过 ModernUIApi 打开一个 Fragment 屏幕
Minecraft.getInstance().setScreen(
    ModernUIApi.get().createScreen(new MyConfigFragment())
);

// 带背景模糊（模糊半径 25px）
Minecraft.getInstance().setScreen(
    ModernUIApi.get().createScreen(new MyConfigFragment(), 25)
);
```

### 2. Fragment —— UI 页面单元

```java
/**
 * Fragment 是 Modern UI 中 UI 页面的基本单元。
 * 类似于 Android 的 Fragment，有自己的生命周期。
 * 一个 Fragment 拥有一个根 View（由 onCreateView 返回）。
 */
public abstract class Fragment {

    /**
     * 创建 Fragment 的根视图。
     * 在此方法中 inflate 布局、初始化控件、设置事件监听。
     *
     * @param inflater  用于创建 View 的 LayoutInflater
     * @param container 父容器（可为 null）
     * @param savedInstanceState 保存的状态（可为 null）
     * @return Fragment 的根 View
     */
    @Nullable
    public abstract View onCreateView(@NotNull LayoutInflater inflater,
                                       @Nullable ViewGroup container,
                                       @Nullable Bundle savedInstanceState);

    /**
     * 当 View 被创建后调用。
     * 可在此进行 View 创建后的初始化操作。
     *
     * @param view              创建的根 View
     * @param savedInstanceState 保存的状态
     */
    public void onViewCreated(@NotNull View view, @Nullable Bundle savedInstanceState);

    /**
     * 获取 Fragment 的根 View。
     *
     * @return 根 View
     */
    @Nullable
    public View getView();

    /**
     * 获取 Fragment 的 Activity（即 Minecraft 窗口上下文）。
     *
     * @return FragmentActivity
     */
    @Nullable
    public FragmentActivity getActivity();

    /**
     * 获取 Fragment 的 Context。
     *
     * @return Context 上下文
     */
    @Nullable
    public Context getContext();

    /**
     * 关闭当前 Fragment（返回到上一个 Fragment 或关闭屏幕）。
     */
    public void dismiss();
}
```

### 3. View —— 所有 UI 组件的基类

```java
/**
 * View 是所有 UI 组件的基类。
 * 负责测量、布局、绘制和事件处理。
 */
public class View {

    public View(Context context);

    // ========== 布局参数 ==========

    /** 设置 View 的宽度（像素或 MATCH_PARENT / WRAP_CONTENT） */
    public void setLayoutParams(@NonNull ViewGroup.LayoutParams params);

    /** 设置外边距（像素） */
    public void setMargin(int left, int top, int right, int bottom);

    /** 设置内边距（像素） */
    public void setPadding(int left, int top, int right, int bottom);

    /** 设置最小宽度 / 高度 */
    public void setMinimumWidth(int minWidth);
    public void setMinimumHeight(int minHeight);

    // ========== 视觉属性 ==========

    /** 设置背景颜色（ARGB 颜色值） */
    public void setBackgroundColor(@ColorInt int color);

    /** 设置背景 Drawable（支持 GradientDrawable、RippleDrawable 等） */
    public void setBackground(Drawable background);

    /** 设置背景 Drawable 并保留内边距 */
    public void setBackgroundDrawable(Drawable background);

    /** 设置透明度（0.0f ~ 1.0f） */
    public void setAlpha(float alpha);

    /** 设置旋转角度（度） */
    public void setRotation(float degrees);

    /** 设置缩放 */
    public void setScaleX(float scaleX);
    public void setScaleY(float scaleY);

    /** 设置平移 */
    public void setTranslationX(float translationX);
    public void setTranslationY(float translationY);

    /** 设置剪裁圆（圆形头像效果） */
    public void setClipCircle(float radius);

    /** 设置剪裁圆角矩形 */
    public void setClipCorner(float radius);

    /** 设置 Z 轴高度（影响阴影投射） */
    public void setZ(float z);

    /** 设置阴影（通过 elevation 自动产生投影） */
    public void setElevation(float elevation);

    // ========== 交互 ==========

    /** 设置点击监听器 */
    public void setOnClickListener(@Nullable OnClickListener l);

    /** 设置长按监听器 */
    public void setOnLongClickListener(@Nullable OnLongClickListener l);

    /** 设置触摸监听器 */
    public void setOnTouchListener(@Nullable OnTouchListener l);

    /** 设置是否可点击 */
    public void setClickable(boolean clickable);

    /** 设置是否启用 */
    public void setEnabled(boolean enabled);

    /** 设置是否可见 */
    public void setVisibility(@Visibility int visibility);
    // 可见性常量: View.VISIBLE, View.INVISIBLE, View.GONE

    // ========== 动画 ==========

    /** 启动属性动画 */
    public void animate();

    /** 清除动画 */
    public void clearAnimation();

    // ========== 状态 ==========

    /** 请求重新布局 */
    public void requestLayout();

    /** 请求重新绘制 */
    public void invalidate();

    /** 获取 View 的上下文 */
    public Context getContext();

    /** 获取 View 的父容器 */
    public ViewParent getParent();

    /** 查找子 View（按 ID） */
    @Nullable
    public <T extends View> T findViewById(@IdRes int id);
}
```

### 4. ViewGroup —— 容器基类

```java
/**
 * ViewGroup 是可以包含子 View 的容器基类。
 * 所有布局（LinearLayout、FrameLayout 等）都继承自它。
 */
public abstract class ViewGroup extends View {

    /**
     * 添加子 View。
     *
     * @param child 子 View
     */
    public void addView(@NonNull View child);

    /**
     * 添加子 View 并指定布局参数。
     *
     * @param child  子 View
     * @param params 布局参数
     */
    public void addView(@NonNull View child, @NonNull ViewGroup.LayoutParams params);

    /**
     * 添加子 View 并指定宽高。
     *
     * @param child  子 View
     * @param width  宽度（像素或 MATCH_PARENT / WRAP_CONTENT）
     * @param height 高度（像素或 MATCH_PARENT / WRAP_CONTENT）
     */
    public void addView(@NonNull View child, int width, int height);

    /**
     * 移除所有子 View。
     */
    public void removeAllViews();

    /**
     * 移除指定子 View。
     *
     * @param view 要移除的子 View
     */
    public void removeView(@NonNull View view);

    /**
     * 获取子 View 数量。
     *
     * @return 子 View 数量
     */
    public int getChildCount();

    /**
     * 获取指定位置的子 View。
     *
     * @param index 索引
     * @return 子 View
     */
    public View getChildAt(int index);
}
```

### 5. LayoutParams —— 布局参数常量

```java
// ViewGroup.LayoutParams 常用常量
ViewGroup.LayoutParams.MATCH_PARENT  // = -1，匹配父容器大小
ViewGroup.LayoutParams.WRAP_CONTENT  // = -2，包裹内容大小

// 创建布局参数的典型方式
new ViewGroup.LayoutParams(width, height)
new LinearLayout.LayoutParams(width, height)
new FrameLayout.LayoutParams(width, height)

// LinearLayout 特有 —— weight 权重
new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1.0f)
// 参数: width, height, weight
// weight=1.0 表示占用剩余空间的 1 份

// FrameLayout 特有 —— gravity 对齐
FrameLayout.LayoutParams lp = new FrameLayout.LayoutParams(WRAP_CONTENT, WRAP_CONTENT);
lp.gravity = Gravity.CENTER;  // 或 Gravity.CENTER_HORIZONTAL | Gravity.BOTTOM 等
```

---

## 📐 布局系统 (Layouts)

### 1. LinearLayout —— 线性布局

```java
/**
 * LinearLayout 按水平或垂直方向排列子 View。
 * 最常用的布局容器，支持 weight 权重分配。
 */
public class LinearLayout extends ViewGroup {

    /** 创建 LinearLayout */
    public LinearLayout(Context context);

    /** 设置方向 */
    public void setOrientation(@Orientation int orientation);
    // LinearLayout.HORIZONTAL (0) —— 水平排列
    // LinearLayout.VERTICAL (1) —— 垂直排列

    /** 设置子 View 间距（像素） */
    public void setDividerDrawable(Drawable divider);
    public void setShowDividers(int showDividers);
    public void setDividerPadding(int padding);

    /** 设置 Gravity（子 View 对齐方式） */
    public void setGravity(int gravity);

    /** 设置子 View 权重总和（默认 1.0） */
    public void setWeightSum(float weightSum);
}
```

### 2. FrameLayout —— 帧布局

```java
/**
 * FrameLayout 是所有子 View 叠加显示（类似 CardLayout）。
 * 通常用于单个子 View 或层叠效果。
 */
public class FrameLayout extends ViewGroup {

    public FrameLayout(Context context);

    /** 设置前景 Drawable */
    public void setForeground(Drawable foreground);

    /** 设置前景 Gravity */
    public void setForegroundGravity(int foregroundGravity);

    /** 设置是否测量所有子 View（默认 true） */
    public void setMeasureAllChildren(boolean measureAll);
}
```

**FrameLayout 典型用法**：
```java
FrameLayout root = new FrameLayout(context);
root.setLayoutParams(new ViewGroup.LayoutParams(MATCH_PARENT, MATCH_PARENT));

// 子 View 可以通过 LayoutParams 的 gravity 定位在 FrameLayout 的任意位置
TextView title = new TextView(context);
title.setText("Hello Modern UI");
FrameLayout.LayoutParams lp = new FrameLayout.LayoutParams(WRAP_CONTENT, WRAP_CONTENT);
lp.gravity = Gravity.CENTER; // 居中
root.addView(title, lp);
```

### 3. ScrollView —— 滚动容器

```java
/**
 * ScrollView 是垂直方向可滚动的容器。
 * 只能有一个直接子 View（通常包裹一个 LinearLayout）。
 */
public class ScrollView extends FrameLayout {

    public ScrollView(Context context);

    /** 是否启用平滑滚动 */
    public void setSmoothScrollingEnabled(boolean enabled);

    /** 是否启用过度滚动效果 */
    public void setOverScrollMode(int mode);

    /** 滚动到指定位置 */
    public void scrollTo(int x, int y);

    /** 平滑滚动到指定位置 */
    public void smoothScrollTo(int x, int y);

    /** 获取当前滚动 Y 位置 */
    public int getScrollY();
}
```

### 4. HorizontalScrollView —— 水平滚动容器

```java
/**
 * HorizontalScrollView 是水平方向可滚动的容器。
 * 用法与 ScrollView 相同，只是方向为水平。
 */
public class HorizontalScrollView extends FrameLayout {
    public HorizontalScrollView(Context context);
    // 方法与 ScrollView 类似
}
```

### 5. RecyclerView —— 高性能列表

```java
/**
 * RecyclerView 是高效的列表/网格视图，支持大数据集。
 * 需要配合 Adapter 和 LayoutManager 使用。
 */
public class RecyclerView extends ViewGroup {

    public RecyclerView(Context context);

    /** 设置布局管理器（决定列表排列方式） */
    public void setLayoutManager(@Nullable LayoutManager layout);
    // LinearLayoutManager —— 线性列表
    // GridLayoutManager —— 网格列表

    /** 设置适配器（数据源） */
    public void setAdapter(@Nullable Adapter adapter);

    /** 添加列表项装饰（分割线、间距等） */
    public void addItemDecoration(@NonNull ItemDecoration decor);

    /** 设置列表项动画 */
    public void setItemAnimator(@Nullable ItemAnimator animator);

    /** 刷新适配器数据 */
    public void notifyDataSetChanged();
}
```

### 6. ConstraintLayout —— 约束布局

```java
/**
 * ConstraintLayout 通过约束关系定位子 View。
 * 适合复杂布局，减少嵌套层级。
 * 注意：Modern UI 的 ConstraintLayout 是简化的实现，与 Android 版不完全相同。
 */
public class ConstraintLayout extends ViewGroup {

    public ConstraintLayout(Context context);

    // 子 View 通过 ConstraintLayout.LayoutParams 设置约束
    // 支持: left/right/top/bottom/center/start/end 约束
}
```

### 布局选择指南

| 布局 | 适用场景 | 嵌套建议 |
|------|---------|---------|
| **LinearLayout** | 简单顺序排列（表单、设置项列表） | 首选，性能最好 |
| **FrameLayout** | 单子 View、层叠效果、Fragment 容器 | 轻量 |
| **ScrollView** | 内容超过一屏时 | 内部包一个 LinearLayout |
| **RecyclerView** | 大量数据列表（> 20 项） | 高性能，必须用 |
| **ConstraintLayout** | 复杂相对定位布局 | 减少嵌套，但性能略低 |

---

## 🎨 控件库 (Widgets)

### 1. TextView —— 文本显示

```java
/**
 * TextView 用于显示文本内容。
 * 支持富文本、自动换行、字体大小/颜色等。
 */
public class TextView extends View {

    public TextView(Context context);

    /** 设置文本内容 */
    public void setText(CharSequence text);

    /** 获取文本内容 */
    public CharSequence getText();

    /** 设置文本大小（sp 单位） */
    public void setTextSize(float size);

    /** 设置文本颜色 */
    public void setTextColor(@ColorInt int color);

    /** 设置字体样式 */
    public void setTypeface(@Nullable Typeface typeface);
    // Typeface.DEFAULT —— 默认
    // Typeface.BOLD —— 粗体
    // Typeface.ITALIC —— 斜体
    // Typeface.MONOSPACE —— 等宽字体

    /** 设置 Gravity（文本对齐方式） */
    public void setGravity(int gravity);
    // Gravity.START / Gravity.END / Gravity.CENTER / Gravity.CENTER_HORIZONTAL

    /** 设置行间距（倍数，默认 1.0） */
    public void setLineSpacing(float add, float mult);

    /** 设置最大行数（超出显示...） */
    public void setMaxLines(int maxLines);

    /** 设置 Ellipsize（文本过长时的省略方式） */
    public void setEllipsize(TextUtils.TruncateAt where);
    // TextUtils.TruncateAt.END —— 末尾省略

    /** 启用/禁用自动换行 */
    public void setSingleLine(boolean singleLine);

    /** 设置阴影 */
    public void setShadowLayer(float radius, float dx, float dy, int color);

    /** 设置链接颜色（可点击链接） */
    public void setLinkTextColor(@ColorInt int color);
}
```

### 2. EditText —— 文本输入

```java
/**
 * EditText 是支持用户输入的文本控件。
 * 可设置输入类型、最大长度、提示文本等。
 */
public class EditText extends TextView {

    public EditText(Context context);

    /** 设置提示文本（输入框为空时显示） */
    public void setHint(CharSequence hint);

    /** 设置输入类型（数字、文本、密码等） */
    public void setInputType(int type);
    // InputType.TYPE_CLASS_TEXT —— 文本
    // InputType.TYPE_CLASS_NUMBER —— 数字
    // InputType.TYPE_TEXT_VARIATION_PASSWORD —— 密码

    /** 设置最大输入长度 */
    public void setFilters(InputFilter[] filters);
    // 示例: new InputFilter.LengthFilter(20) —— 最大 20 字符

    /** 设置文本变化监听 */
    public void addTextChangedListener(TextWatcher watcher);

    /** 设置光标位置 */
    public void setSelection(int index);

    /** 选择全部文本 */
    public void selectAll();
}
```

### 3. Button (MaterialButton) —— 按钮

```java
/**
 * MaterialButton 是 Material Design 风格的按钮。
 * 支持 filled / outlined / text 三种样式。
 */
public class MaterialButton extends Button {

    public MaterialButton(Context context);

    /** 设置按钮文字 */
    public void setText(CharSequence text);

    /** 设置按钮样式 */
    public void setBackgroundTintList(ColorStateList tint);
    public void setStrokeColor(ColorStateList strokeColor);
    public void setStrokeWidth(int width);
    public void setCornerRadius(int radius);

    /** 设置图标 */
    public void setIcon(Drawable icon);
    public void setIconGravity(int iconGravity);

    /** 设置按钮是否可点击（禁用/启用） */
    public void setEnabled(boolean enabled);

    /** 设置按钮高度 */
    public void setMinimumHeight(int minHeight);
}

/**
 * 传统 Button（如果你不想用 Material 风格的话）。
 * 但建议用 MaterialButton 获得更好视觉效果。
 */
public class Button extends TextView {
    public Button(Context context);
}
```

### 4. ImageView —— 图片显示

```java
/**
 * ImageView 用于显示图片/图标。
 * 支持 Bitmap、Drawable 资源，以及缩放模式。
 */
public class ImageView extends View {

    public ImageView(Context context);

    /** 设置图片资源 */
    public void setImageDrawable(@Nullable Drawable drawable);

    /** 设置 Bitmap 图片 */
    public void setImageBitmap(@Nullable Bitmap bitmap);

    /** 设置缩放模式 */
    public void setScaleType(@NotNull ScaleType scaleType);
    // ScaleType.FIT_CENTER —— 居中适应（默认）
    // ScaleType.CENTER_CROP —— 居中裁剪
    // ScaleType.CENTER_INSIDE —— 居中内含
    // ScaleType.FIT_XY —— 拉伸填满
}
```

### 5. Switch —— 开关

```java
/**
 * Switch 是打开/关闭的二状态开关控件。
 * 用于配置项中的开关设置。
 */
public class Switch extends CompoundButton {

    public Switch(Context context);

    /** 设置开关状态 */
    public void setChecked(boolean checked);

    /** 获取开关状态 */
    public boolean isChecked();

    /** 切换开关状态 */
    public void toggle();

    /** 设置状态变化监听 */
    public void setOnCheckedChangeListener(@Nullable OnCheckedChangeListener listener);
}
```

### 6. SeekBar —— 滑块

```java
/**
 * SeekBar 是拖动滑块，用于选择范围内的值。
 * 常用于音量、亮度等数值设置。
 */
public class SeekBar extends ProgressBar {

    public SeekBar(Context context);

    /** 设置最大值 */
    public void setMax(int max);

    /** 获取当前进度 */
    public int getProgress();

    /** 设置当前进度 */
    public void setProgress(int progress);

    /** 设置进度变化监听 */
    public void setOnSeekBarChangeListener(@Nullable OnSeekBarChangeListener listener);
}
```

### 7. ProgressBar —— 进度条

```java
/**
 * ProgressBar 用于显示加载进度。
 * 支持确定性（确定进度）和不确定性（循环动画）两种模式。
 */
public class ProgressBar extends View {

    public ProgressBar(Context context);

    /** 设置是否不确定性模式（循环转圈） */
    public void setIndeterminate(boolean indeterminate);

    /** 设置最大值 */
    public void setMax(int max);

    /** 设置当前进度 */
    public void setProgress(int progress);

    /** 获取当前进度 */
    public int getProgress();

    /** 设置进度颜色 */
    public void setProgressTintList(ColorStateList tint);

    /** 设置进度条样式（水平/圆形） */
    public void setProgressDrawable(Drawable d);
}
```

### 8. CheckBox —— 复选框

```java
/**
 * CheckBox 是多选/单选复选框。
 * 也可配合 RadioButton 实现单选组。
 */
public class CheckBox extends CompoundButton {

    public CheckBox(Context context);

    public void setChecked(boolean checked);
    public boolean isChecked();
    public void toggle();
    public void setOnCheckedChangeListener(@Nullable OnCheckedChangeListener listener);
}
```

### 9. TabLayout —— 标签页

```java
/**
 * TabLayout 是 Material Design 的标签导航组件。
 * 常配合 ViewPager 使用实现页面滑动切换。
 */
public class TabLayout extends HorizontalScrollView {

    public TabLayout(Context context);

    /** 添加标签 */
    public Tab newTab();
    public void addTab(@NonNull Tab tab, boolean setSelected);

    /** 设置标签选中监听 */
    public void addOnTabSelectedListener(@Nullable OnTabSelectedListener listener);

    /** 关联 ViewPager */
    public void setupWithViewPager(@Nullable ViewPager viewPager);

    /** 设置标签文字颜色 */
    public void setTabTextColors(ColorStateList colors);

    /** 设置选中指示器颜色 */
    public void setSelectedTabIndicatorColor(@ColorInt int color);

    /** 设置标签内边距 */
    public void setTabPaddingStart(int padding);
    public void setTabPaddingEnd(int padding);
}
```

### 10. ViewPager —— 页面滑动

```java
/**
 * ViewPager 支持左右滑动切换页面。
 * 需要配合 PagerAdapter 使用。
 */
public class ViewPager extends ViewGroup {

    public ViewPager(Context context);

    /** 设置适配器 */
    public void setAdapter(@Nullable PagerAdapter adapter);

    /** 设置当前页面 */
    public void setCurrentItem(int item);
    public void setCurrentItem(int item, boolean smoothScroll);

    /** 获取当前页面 */
    public int getCurrentItem();

    /** 设置页面变化监听 */
    public void addOnPageChangeListener(@Nullable OnPageChangeListener listener);

    /** 设置页面间距 */
    public void setPageMargin(int marginPixels);
}
```

---

## 🎯 高级视觉效果

### 1. Canvas —— 自定义绘制

```java
/**
 * Canvas 是 Modern UI 的 2D 绘制 API（GPU 加速版本）。
 * 用于在自定义 View 的 onDraw 方法中绘制图形。
 */
public class Canvas {

    /** 绘制颜色（填充整个画布） */
    public void drawColor(@ColorInt int color);

    /** 绘制矩形 */
    public void drawRect(float left, float top, float right, float bottom, @NonNull Paint paint);

    /** 绘制圆角矩形 */
    public void drawRoundRect(@NonNull RectF rect, float rx, float ry, @NonNull Paint paint);

    /** 绘制圆 */
    public void drawCircle(float cx, float cy, float radius, @NonNull Paint paint);

    /** 绘制文字 */
    public void drawText(@NonNull String text, float x, float y, @NonNull Paint paint);

    /** 绘制线段 */
    public void drawLine(float startX, float startY, float stopX, float stopY, @NonNull Paint paint);

    /** 绘制路径（任意形状） */
    public void drawPath(@NonNull Path path, @NonNull Paint paint);

    /** 绘制图片 */
    public void drawBitmap(@NonNull Bitmap bitmap, float left, float top, @Nullable Paint paint);

    /** 绘制 Drawable */
    public void drawDrawable(@NonNull Drawable drawable);

    /** 保存画布状态 */
    public int save();

    /** 恢复画布状态 */
    public void restore();

    /** 平移画布 */
    public void translate(float dx, float dy);

    /** 旋转画布 */
    public void rotate(float degrees, float px, float py);

    /** 缩放画布 */
    public void scale(float sx, float sy, float px, float py);

    /** 裁剪为矩形区域 */
    public boolean clipRect(float left, float top, float right, float bottom);

    /** 裁剪为圆角矩形区域 */
    public boolean clipRoundRect(@NonNull RectF rect, float rx, float ry);
}
```

### 2. Paint —— 绘制画笔

```java
/**
 * Paint 定义了绘制时的样式（颜色、粗细、填充方式等）。
 * 每个需要绘制的图形都需要一个 Paint 对象。
 */
public class Paint {

    public Paint();

    /** 设置颜色 */
    public void setColor(@ColorInt int color);

    /** 设置抗锯齿（默认为 true） */
    public void setAntiAlias(boolean aa);

    /** 设置样式 */
    public void setStyle(@NonNull Style style);
    // Style.FILL —— 填充
    // Style.STROKE —— 描边
    // Style.FILL_AND_STROKE —— 填充 + 描边

    /** 设置描边宽度（仅在 STROKE 模式下有效） */
    public void setStrokeWidth(float width);

    /** 设置描边线帽 */
    public void setStrokeCap(Cap cap);
    // Cap.ROUND —— 圆头
    // Cap.SQUARE —— 方头
    // Cap.BUTT —— 平头

    /** 设置描边连接方式 */
    public void setStrokeJoin(Join join);
    // Join.MITER, Join.ROUND, Join.BEVEL

    /** 设置文字大小 */
    public void setTextSize(float textSize);

    /** 设置字体 */
    public void setTypeface(@Nullable Typeface typeface);

    /** 设置 Shader（渐变、位图等） */
    public void setShader(@Nullable Shader shader);

    /** 设置遮罩滤镜（用于 BlurMaskFilter 等） */
    public void setMaskFilter(@Nullable MaskFilter maskfilter);

    /** 设置阴影 */
    public void setShadowLayer(float radius, float dx, float dy, @ColorInt int shadowColor);
    // 注意: radius 为阴影模糊半径，dx/dy 为阴影偏移
}
```

### 3. Shader —— 着色器（渐变效果）

```java
/**
 * Shader 是着色器基类，用于实现渐变等效果。
 * 使用 setShader() 将 Shader 应用到 Paint 上。
 */
public abstract class Shader {

    /** 声明平铺模式 */
    public enum TileMode {
        CLAMP,   // 边缘拉伸（默认）
        REPEAT,  // 重复平铺
        MIRROR   // 镜像平铺
    }
}

/**
 * 线性渐变。使颜色沿直线方向渐变。
 */
public class LinearGradient extends Shader {

    /**
     * 创建线性渐变。
     *
     * @param x0      起点 X
     * @param y0      起点 Y
     * @param x1      终点 X
     * @param y1      终点 Y
     * @param colors  颜色数组
     * @param positions 每个颜色的位置比例（可为 null，自动均匀分布）
     * @param tile    平铺模式
     */
    public LinearGradient(float x0, float y0, float x1, float y1,
                          @NonNull @ColorInt int[] colors,
                          @Nullable float[] positions,
                          @NonNull TileMode tile);

    /** 两色渐变的简化版 */
    public LinearGradient(float x0, float y0, float x1, float y1,
                          @ColorInt int color0, @ColorInt int color1,
                          @NonNull TileMode tile);
}

/**
 * 径向渐变。从中心点向外辐射渐变。
 */
public class RadialGradient extends Shader {

    /**
     * 创建径向渐变。
     *
     * @param centerX  中心 X
     * @param centerY  中心 Y
     * @param radius   半径
     * @param colors   颜色数组
     * @param positions 位置比例（可为 null）
     * @param tile     平铺模式
     */
    public RadialGradient(float centerX, float centerY, float radius,
                          @NonNull @ColorInt int[] colors,
                          @Nullable float[] positions,
                          @NonNull TileMode tile);

    public RadialGradient(float centerX, float centerY, float radius,
                          @ColorInt int centerColor, @ColorInt int edgeColor,
                          @NonNull TileMode tile);
}
```

### 4. GradientDrawable —— 可绘制形状

```java
/**
 * GradientDrawable 是最常用的 Drawable 实现。
 * 支持定义形状、颜色、渐变、圆角、描边和阴影。
 * 相当于 CSS 中的 background 属性。
 */
public class GradientDrawable extends Drawable {

    /** 形状常量 */
    public static final int RECTANGLE = 0;   // 矩形（默认）
    public static final int OVAL = 1;        // 椭圆
    public static final int LINE = 2;        // 线
    public static final int RING = 3;        // 环

    public GradientDrawable();

    /**
     * 创建指定形状的 GradientDrawable。
     *
     * @param shape 形状常量
     */
    public GradientDrawable(@Shape int shape);

    /** 设置形状 */
    public void setShape(@Shape int shape);

    /** 设置填充颜色 */
    public void setColor(@ColorInt int argb);

    /** 设置颜色状态列表（支持不同状态不同颜色） */
    public void setColor(@Nullable ColorStateList colorStateList);

    /** 设置渐变颜色 */
    public void setColors(@Nullable @ColorInt int[] colors);

    /** 设置渐变方向 */
    public void setGradientType(int type);
    // GradientDrawable.LINEAR_GRADIENT —— 线性渐变
    // GradientDrawable.RADIAL_GRADIENT —— 径向渐变
    // GradientDrawable.SWEEP_GRADIENT —— 扫描渐变

    /** 设置线性渐变方向 */
    public void setOrientation(@Nullable Orientation orientation);
    // Orientation.LEFT_RIGHT, TOP_BOTTOM, TL_BR, BL_TR 等

    /** 设置圆角（所有角统一） */
    public void setCornerRadius(float radius);

    /** 设置各角不同圆角 */
    public void setCornerRadii(@Nullable float[] radii);
    // radii = [topLeft, topRight, bottomRight, bottomLeft] 各角的 X/Y 半径

    /** 设置描边 */
    public void setStroke(int width, @ColorInt int color);
    public void setStroke(int width, @ColorInt int color, float dashWidth, float dashGap);

    /** 设置尺寸 */
    public void setSize(int width, int height);

    /** 设置内边距 */
    public void setPadding(int left, int top, int right, int bottom);

    /** 设置阴影 */
    public void setShadowLayer(float radius, float dx, float dy, @ColorInt int shadowColor);
}
```

### 5. 毛玻璃效果（背景模糊）

```java
/**
 * 在 Modern UI 中实现毛玻璃/背景模糊效果有两种方式：
 *
 * 方式 1：创建 Screen 时指定 blurRadius
 */
// 在打开 Fragment 屏幕时直接指定背景模糊半径
Minecraft.getInstance().setScreen(
    ModernUIApi.get().createScreen(new MyFragment(), 25) // 25px 模糊半径
);

/**
 * 方式 2：使用 View 的 setBackground() 配合模糊 Drawable
 * 注意：Modern UI 本身在 Fragment 背景上提供模糊，不需要额外 API。
 * 对于弹窗/浮层，使用 Fragment 自身的 dismiss() 管理即可。
 */
```

---

## 🎬 动画系统

### 1. ValueAnimator —— 值动画

```java
/**
 * ValueAnimator 通过对某个值进行插值来驱动动画。
 * 最灵活的动画方式，可以 animated 任何数值。
 */
public class ValueAnimator extends Animator {

    /**
     * 创建一个值动画。
     *
     * @param values 动画的目标值序列
     * @return ValueAnimator
     */
    public static ValueAnimator ofFloat(float... values);

    public static ValueAnimator ofInt(int... values);

    public static ValueAnimator ofArgb(int... values);

    /** 设置动画时长（毫秒，默认 300ms） */
    public ValueAnimator setDuration(long duration);

    /** 设置插值器 */
    public void setInterpolator(@Nullable TimeInterpolator value);
    // AccelerateDecelerateInterpolator —— 缓入缓出（默认）
    // LinearInterpolator —— 线性
    // AccelerateInterpolator —— 加速
    // DecelerateInterpolator —— 减速
    // OvershootInterpolator —— 过冲
    // BounceInterpolator —— 弹跳
    // AnticipateOvershootInterpolator —— 预冲 + 过冲

    /** 设置重复模式 */
    public void setRepeatMode(int value);
    // ValueAnimator.RESTART —— 重新开始
    // ValueAnimator.REVERSE —— 反向播放

    /** 设置重复次数（-1 为无限循环） */
    public void setRepeatCount(int value);

    /** 添加值更新监听器 */
    public void addUpdateListener(@NonNull AnimatorUpdateListener listener);

    /** 启动动画 */
    public void start();

    /** 取消动画 */
    public void cancel();

    /** 结束动画 */
    public void end();

    /** 获取当前动画值 */
    public float getAnimatedFraction();
    public Object getAnimatedValue();
}

/** ValueAnimator 使用示例 —— 淡入淡出动画 */
ValueAnimator animator = ValueAnimator.ofFloat(0f, 1f);
animator.setDuration(300);
animator.addUpdateListener(animation -> {
    float value = (float) animation.getAnimatedValue();
    myView.setAlpha(value);
});
animator.start();

/** ValueAnimator 使用示例 —— ARGB 颜色过渡动画 */
ValueAnimator colorAnim = ValueAnimator.ofArgb(0xFF1A1B2F, 0xFF6C63FF);
colorAnim.setDuration(500);
colorAnim.addUpdateListener(animation -> {
    int color = (int) animation.getAnimatedValue();
    myView.setBackgroundColor(color);
});
colorAnim.start();
```

### 2. ObjectAnimator —— 对象属性动画

```java
/**
 * ObjectAnimator 直接对对象的属性进行动画。
 * 比 ValueAnimator 更简洁，自动调用 setter 方法。
 */
public class ObjectAnimator extends ValueAnimator {

    /**
     * 创建对象属性动画。
     *
     * @param target     动画目标对象
     * @param property   属性名（对应 setXxx 方法）
     * @param values     目标值
     * @return ObjectAnimator
     */
    public static ObjectAnimator ofFloat(Object target, String property, float... values);

    public static ObjectAnimator ofInt(Object target, String property, int... values);

    public static ObjectAnimator ofArgb(Object target, String property, int... values);
}

/** ObjectAnimator 使用示例 —— 平移动画 */
ObjectAnimator animator = ObjectAnimator.ofFloat(myView, "translationY", 0f, -100f);
animator.setDuration(300);
animator.setInterpolator(new OvershootInterpolator());
animator.start();

/** ObjectAnimator 使用示例 —— 透明度 + 旋转组合 */
ObjectAnimator alphaAnim = ObjectAnimator.ofFloat(myView, "alpha", 0f, 1f);
alphaAnim.setDuration(300);

ObjectAnimator rotateAnim = ObjectAnimator.ofFloat(myView, "rotation", 0f, 360f);
rotateAnim.setDuration(500);

alphaAnim.start();
rotateAnim.start();
```

### 3. AnimatorSet —— 动画集合

```java
/**
 * AnimatorSet 用于组合多个动画。
 * 可以顺序播放、同时播放或按延迟播放。
 */
public class AnimatorSet extends Animator {

    public AnimatorSet();

    /** 同时播放多个动画 */
    public void playTogether(Animator... items);

    /** 依次播放多个动画 */
    public void playSequentially(Animator... items);

    /** 设置某个动画在另一个动画之后播放 */
    public AnimatorSet.Builder play(Animator anim);

    /** 设置动画时长 */
    public AnimatorSet setDuration(long duration);

    /** 设置插值器（所有子动画共用） */
    public void setInterpolator(@Nullable TimeInterpolator interpolator);

    /** 启动 */
    public void start();

    /** 取消 */
    public void cancel();
}

/** AnimatorSet 使用示例 —— 顺序播放 */
AnimatorSet set = new AnimatorSet();
set.playSequentially(
    ObjectAnimator.ofFloat(view, "alpha", 0f, 1f).setDuration(200),
    ObjectAnimator.ofFloat(view, "translationY", 0f, -50f).setDuration(300),
    ObjectAnimator.ofFloat(view, "translationY", -50f, 0f).setDuration(200)
);
set.start();
```

### 4. ViewPropertyAnimator —— View 便捷动画

```java
/**
 * View 自带的便捷动画 API。
 * 通过 view.animate() 获取，链式调用。
 * 自动启动，无需手动 start()。
 */
// ViewPropertyAnimator 使用示例
view.animate()
    .alpha(0.5f)          // 透明度
    .translationY(-100f)  // Y 轴平移
    .rotation(45f)        // 旋转
    .scaleX(1.2f)         // X 轴缩放
    .scaleY(1.2f)         // Y 轴缩放
    .setDuration(300)
    .setInterpolator(new OvershootInterpolator())
    .withStartAction(() -> { /* 动画开始时 */ })
    .withEndAction(() -> { /* 动画结束时 */ });
```

### 5. 常用插值器速查

| 插值器 | 效果 | 适用场景 |
|--------|------|---------|
| `AccelerateDecelerateInterpolator` | 缓入缓出 | 通用（默认） |
| `LinearInterpolator` | 匀速 | 进度条、循环动画 |
| `AccelerateInterpolator` | 加速 | 退出动画 |
| `DecelerateInterpolator` | 减速 | 进入动画 |
| `OvershootInterpolator` | 过冲后回弹 | 弹窗、按钮 |
| `BounceInterpolator` | 弹跳 | 趣味动画 |
| `AnticipateOvershootInterpolator` | 预退后过冲 | 强调动画 |

---

## 🏆 Material Design 组件

Modern UI 内置了 Material Design 3 风格的组件库，直接可用。

### 常用 Material 组件

| 组件类 | 用途 | 特殊方法 |
|--------|------|---------|
| `MaterialButton` | Material 风格按钮 | `setBackgroundTintList()`, `setStrokeColor()`, `setCornerRadius()`, `setIcon()` |
| `MaterialTextView` | Material 风格文本 | 同上 TextView |
| `MaterialSwitch` | Material 风格开关 | 同上 Switch |
| `MaterialSlider` | Material 风格滑块 | `setValue()`, `setValueFrom()`, `setValueTo()` |
| `MaterialCardView` | 卡片容器 | `setCardBackgroundColor()`, `setRadius()`, `setCardElevation()` |
| `MaterialProgressBar` | Material 风格进度条 | 同上 ProgressBar |
| `TabLayout` | 标签导航 | `addTab()`, `setupWithViewPager()` |
| `MaterialToolbar` | 顶栏/标题栏 | `setTitle()`, `setSubtitle()` |

### MaterialCardView —— 卡片视图

```java
/**
 * MaterialCardView 是 Material Design 的卡片组件。
 * 自带圆角、阴影和点击涟漪效果。
 */
public class MaterialCardView extends FrameLayout {

    public MaterialCardView(Context context);

    /** 设置卡片背景颜色 */
    public void setCardBackgroundColor(@ColorInt int color);
    public void setCardBackgroundColor(@Nullable ColorStateList color);

    /** 设置圆角半径 */
    public void setRadius(float radius);

    /** 设置阴影高度（Elevation） */
    public void setCardElevation(float elevation);

    /** 设置最大阴影高度 */
    public void setMaxCardElevation(float maxElevation);

    /** 设置描边 */
    public void setStrokeColor(@ColorInt int color);
    public void setStrokeWidth(int width);

    /** 设置是否可点击（是否有涟漪效果） */
    public void setClickable(boolean clickable);

    /** 设置前景（涟漪效果） */
    public void setForeground(Drawable foreground);
}
```

---

## 🖐️ 事件处理

### 1. 点击事件

```java
// 方式 1：Lambda 表达式（推荐）
button.setOnClickListener(v -> {
    System.out.println("Button clicked!");
});

// 方式 2：匿名内部类
button.setOnClickListener(new View.OnClickListener() {
    @Override
    public void onClick(View v) {
        // 处理点击
    }
});

// 方式 3：接口实现
public class MyFragment extends Fragment implements View.OnClickListener {
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        LinearLayout root = new LinearLayout(getContext());
        Button btn = new Button(getContext());
        btn.setOnClickListener(this);
        root.addView(btn);
        return root;
    }

    @Override
    public void onClick(View v) {
        // 处理点击
    }
}
```

### 2. 触摸事件

```java
view.setOnTouchListener((v, event) -> {
    switch (event.getAction()) {
        case MotionEvent.ACTION_DOWN:
            // 手指按下
            return true;
        case MotionEvent.ACTION_MOVE:
            // 手指移动
            float x = event.getX();
            float y = event.getY();
            return true;
        case MotionEvent.ACTION_UP:
            // 手指抬起
            return true;
        case MotionEvent.ACTION_CANCEL:
            // 触摸取消
            return true;
    }
    return false;
});
```

### 3. 长按事件

```java
view.setOnLongClickListener(v -> {
    System.out.println("Long pressed!");
    return true; // 返回 true 表示消费事件
});
```

### 4. 自定义 View 绘制示例

```java
/**
 * 自定义 View 示例 —— 绘制一个带渐变和阴影的圆角矩形。
 */
public class CustomGradientView extends View {

    private final Paint mPaint;
    private final Paint mShadowPaint;

    /**
     * 创建自定义 View。
     *
     * @param context 上下文
     */
    public CustomGradientView(Context context) {
        super(context);
        mPaint = new Paint();
        mPaint.setAntiAlias(true);
        mPaint.setStyle(Paint.Style.FILL);

        mShadowPaint = new Paint();
        mShadowPaint.setAntiAlias(true);
        mShadowPaint.setShadowLayer(15f, 0f, 5f, 0x66000000);
    }

    @Override
    protected void onDraw(@NonNull Canvas canvas) {
        super.onDraw(canvas);

        // 创建线性渐变
        LinearGradient gradient = new LinearGradient(
            0, 0, getWidth(), getHeight(),
            new int[]{0xFF6C63FF, 0xFF3F51B5},
            null,
            Shader.TileMode.CLAMP
        );
        mPaint.setShader(gradient);

        // 绘制带阴影和渐变的圆角矩形
        canvas.drawRoundRect(
            20, 20, getWidth() - 20, getHeight() - 20,
            16, 16, mShadowPaint
        );
        canvas.drawRoundRect(
            20, 20, getWidth() - 20, getHeight() - 20,
            16, 16, mPaint
        );
    }
}
```

### 5. EditText 输入监听

```java
EditText editText = new EditText(getContext());
editText.addTextChangedListener(new TextWatcher() {
    @Override
    public void beforeTextChanged(CharSequence s, int start, int count, int after) {
        // 文本变化前
    }

    @Override
    public void onTextChanged(CharSequence s, int start, int before, int count) {
        // 文本变化中
    }

    @Override
    public void afterTextChanged(Editable s) {
        // 文本变化后
        System.out.println("Current text: " + s.toString());
    }
});
```

### 6. Switch 状态监听

```java
Switch switchBtn = new Switch(getContext());
switchBtn.setText("启用功能");
switchBtn.setOnCheckedChangeListener((buttonView, isChecked) -> {
    if (isChecked) {
        System.out.println("Switch ON");
    } else {
        System.out.println("Switch OFF");
    }
});
```

### 7. SeekBar 进度监听

```java
SeekBar seekBar = new SeekBar(getContext());
seekBar.setMax(100);
seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
    @Override
    public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
        // 进度变化
    }

    @Override
    public void onStartTrackingTouch(SeekBar seekBar) {
        // 开始拖动
    }

    @Override
    public void onStopTrackingTouch(SeekBar seekBar) {
        // 停止拖动
    }
});
```

---

## 💡 完整示例

### 示例 1：简单的配置界面 Fragment

```java
package com.pleaseusethisone.pleaseusethisone.client.modernui;

import icyllis.modernui.animation.ObjectAnimator;
import icyllis.modernui.animation.OvershootInterpolator;
import icyllis.modernui.fragment.Fragment;
import icyllis.modernui.graphics.drawable.GradientDrawable;
import icyllis.modernui.view.Gravity;
import icyllis.modernui.view.View;
import icyllis.modernui.view.ViewGroup;
import icyllis.modernui.widget.*;
import icyllis.modernui.core.Context;
import icyllis.modernui.util.ColorStateList;

/**
 * Modern UI 示例 —— 模组配置界面 Fragment。
 * 展示如何使用 Fragment、布局和 Material 组件构建一个完整的配置页。
 */
public class ModConfigFragment extends Fragment {

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // 1. 创建根布局 —— 垂直方向
        LinearLayout root = new LinearLayout(getContext());
        root.setOrientation(LinearLayout.VERTICAL);
        root.setLayoutParams(new ViewGroup.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.MATCH_PARENT
        ));

        // 设置根布局背景（圆角深色卡片背景）
        GradientDrawable bg = new GradientDrawable(GradientDrawable.RECTANGLE);
        bg.setColor(0xFF1E1E2E);
        bg.setCornerRadius(16f);
        root.setBackground(bg);
        root.setPadding(24, 24, 24, 24);

        // 2. 标题
        TextView title = new TextView(getContext());
        title.setText("⚙ 模组配置");
        title.setTextSize(24);
        title.setTextColor(0xFFFFFFFF);
        title.setGravity(Gravity.CENTER);
        title.setPadding(0, 0, 0, 24);
        root.addView(title, new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.WRAP_CONTENT
        ));

        // 3. 添加设置项列表
        root.addView(createSettingItem(getContext(), "启用自动功能", "开启后模组将自动执行任务", true));
        root.addView(createDivider(getContext()));
        root.addView(createSettingItem(getContext(), "调试模式", "显示调试信息和日志", false));
        root.addView(createDivider(getContext()));
        root.addView(createSliderItem(getContext(), "效果强度", 50));
        root.addView(createDivider(getContext()));
        root.addView(createButtonItem(getContext(), "保存配置"));

        // 4. 入口动画
        title.setAlpha(0f);
        title.setTranslationY(-30f);
        title.animate()
            .alpha(1f)
            .translationY(0f)
            .setDuration(400)
            .setInterpolator(new OvershootInterpolator())
            .start();

        return root;
    }

    /**
     * 创建开关设置项。
     *
     * @param context  上下文
     * @param title    设置项标题
     * @param desc     设置项描述
     * @param checked  默认开关状态
     * @return 设置项的 LinearLayout
     */
    private View createSettingItem(Context context, String title, String desc, boolean checked) {
        LinearLayout item = new LinearLayout(context);
        item.setOrientation(LinearLayout.HORIZONTAL);
        item.setPadding(8, 16, 8, 16);

        // 左侧文字区域
        LinearLayout textArea = new LinearLayout(context);
        textArea.setOrientation(LinearLayout.VERTICAL);
        textArea.setLayoutParams(new LinearLayout.LayoutParams(
            0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f
        ));

        TextView tvTitle = new TextView(context);
        tvTitle.setText(title);
        tvTitle.setTextSize(16);
        tvTitle.setTextColor(0xFFFFFFFF);
        textArea.addView(tvTitle);

        TextView tvDesc = new TextView(context);
        tvDesc.setText(desc);
        tvDesc.setTextSize(12);
        tvDesc.setTextColor(0xFF888888);
        textArea.addView(tvDesc);

        item.addView(textArea);

        // 右侧开关
        Switch switchBtn = new Switch(context);
        switchBtn.setChecked(checked);
        item.addView(switchBtn);

        // 开关点击动画
        switchBtn.setOnCheckedChangeListener((buttonView, isChecked) -> {
            float target = isChecked ? 1f : 0f;
            ObjectAnimator anim = ObjectAnimator.ofFloat(buttonView, "alpha", target);
            anim.setDuration(150);
            anim.start();
        });

        return item;
    }

    /**
     * 创建分割线。
     *
     * @param context 上下文
     * @return 分割线 View
     */
    private View createDivider(Context context) {
        View divider = new View(context);
        divider.setBackgroundColor(0xFF333355);
        divider.setLayoutParams(new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, 1
        ));
        return divider;
    }

    /**
     * 创建滑块设置项。
     *
     * @param context 上下文
     * @param title   设置项标题
     * @param value   默认值
     * @return 滑块设置项的 LinearLayout
     */
    private View createSliderItem(Context context, String title, int value) {
        LinearLayout item = new LinearLayout(context);
        item.setOrientation(LinearLayout.VERTICAL);
        item.setPadding(8, 16, 8, 16);

        TextView tvTitle = new TextView(context);
        tvTitle.setText(title);
        tvTitle.setTextSize(16);
        tvTitle.setTextColor(0xFFFFFFFF);
        item.addView(tvTitle);

        SeekBar seekBar = new SeekBar(context);
        seekBar.setMax(100);
        seekBar.setProgress(value);
        item.addView(seekBar);

        return item;
    }

    /**
     * 创建按钮项。
     *
     * @param context 上下文
     * @param text    按钮文字
     * @return 按钮 View
     */
    private View createButtonItem(Context context, String text) {
        MaterialButton button = new MaterialButton(context);
        button.setText(text);
        button.setLayoutParams(new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            48
        ));
        ((LinearLayout.LayoutParams) button.getLayoutParams()).setMargins(0, 16, 0, 0);

        // Material 风格
        button.setBackgroundTintList(ColorStateList.valueOf(0xFF6C63FF));
        button.setCornerRadius(12);

        button.setOnClickListener(v -> {
            // 点击反馈动画
            v.animate()
                .scaleX(0.95f)
                .scaleY(0.95f)
                .setDuration(100)
                .withEndAction(() -> v.animate()
                    .scaleX(1f)
                    .scaleY(1f)
                    .setDuration(100)
                    .start()
                );
            System.out.println("配置已保存！");
        });

        return button;
    }
}
```

### 示例 2：使用 ModernUIApi 打开 Fragment

```java
// 在任意 Client 事件中打开 Modern UI 屏幕
// 例如按键绑定回调、命令执行等

// 方式 1：无背景模糊
Minecraft.getInstance().setScreen(
    ModernUIApi.get().createScreen(new ModConfigFragment())
);

// 方式 2：带背景模糊（推荐，视觉效果更好）
Minecraft.getInstance().setScreen(
    ModernUIApi.get().createScreen(new ModConfigFragment(), 25)
);
```

### 示例 3：带 TabLayout + ViewPager 的多页配置

```java
package com.pleaseusethisone.pleaseusethisone.client.modernui;

import icyllis.modernui.fragment.Fragment;
import icyllis.modernui.fragment.FragmentManager;
import icyllis.modernui.fragment.FragmentPagerAdapter;
import icyllis.modernui.view.LayoutInflater;
import icyllis.modernui.view.View;
import icyllis.modernui.view.ViewGroup;
import icyllis.modernui.widget.*;
import icyllis.modernui.core.Bundle;
import icyllis.modernui.graphics.drawable.GradientDrawable;

/**
 * 带 TabLayout + ViewPager 的多页面配置界面 Fragment。
 * 适合需要分类展示配置项的场景。
 */
public class TabConfigFragment extends Fragment {

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        LinearLayout root = new LinearLayout(getContext());
        root.setOrientation(LinearLayout.VERTICAL);
        root.setLayoutParams(new ViewGroup.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.MATCH_PARENT
        ));

        GradientDrawable bg = new GradientDrawable(GradientDrawable.RECTANGLE);
        bg.setColor(0xFF1E1E2E);
        root.setBackground(bg);

        // TabLayout
        TabLayout tabLayout = new TabLayout(getContext());
        tabLayout.setLayoutParams(new ViewGroup.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.WRAP_CONTENT
        ));
        tabLayout.addTab(tabLayout.newTab().setText("基础"));
        tabLayout.addTab(tabLayout.newTab().setText("高级"));
        tabLayout.addTab(tabLayout.newTab().setText("关于"));
        root.addView(tabLayout);

        // ViewPager
        ViewPager viewPager = new ViewPager(getContext());
        viewPager.setLayoutParams(new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            0, 1f
        ));
        viewPager.setAdapter(new ConfigPagerAdapter(getChildFragmentManager()));
        root.addView(viewPager);

        // 关联 TabLayout 和 ViewPager
        tabLayout.setupWithViewPager(viewPager);

        return root;
    }

    /**
     * ViewPager 适配器 —— 管理各页的 Fragment。
     */
    private static class ConfigPagerAdapter extends FragmentPagerAdapter {

        public ConfigPagerAdapter(FragmentManager fm) {
            super(fm);
        }

        @Override
        public Fragment getItem(int position) {
            switch (position) {
                case 0: return new BasicConfigFragment();
                case 1: return new AdvancedConfigFragment();
                case 2: return new AboutFragment();
                default: return new BasicConfigFragment();
            }
        }

        @Override
        public int getCount() {
            return 3;
        }

        @Override
        public CharSequence getPageTitle(int position) {
            switch (position) {
                case 0: return "基础";
                case 1: return "高级";
                case 2: return "关于";
                default: return "";
            }
        }
    }
}
```

### 示例 4：在 Client 事件中通过按键打开 Modern UI 屏幕

```java
// 在 PleaseusethisoneClient.java 中
// 通过 NeoForge 事件系统注册按键绑定并打开 Modern UI 屏幕

@SubscribeEvent
public static void onClientTick(ClientTickEvent.Post event) {
    if (KEY_OPEN_MODERN_UI.consumeClick()) {
        Minecraft.getInstance().setScreen(
            ModernUIApi.get().createScreen(new ModConfigFragment(), 25)
        );
    }
}
```

---

## ⚡ 常见模式和最佳实践

### 1. Fragment 与 Screen 的选择

```
使用 Fragment（推荐）:
  - 享受生命周期管理
  - 自动处理返回栈
  - 更容易维护和测试
  - 通过 ModernUIApi.createScreen(fragment) 打开

直接继承 Screen（不推荐）:
  - 需要手动管理渲染循环
  - 没有生命周期回调
  - 仅在需要完全控制渲染管道时使用
```

### 2. 性能优化

```java
// ✅ 好的做法
// 1. 重用 Paint 对象（不要在 onDraw 中 new）
private final Paint mPaint = new Paint();

// 2. 使用 ViewPropertyAnimator 而非 ValueAnimator
view.animate().alpha(0.5f).setDuration(200).start();

// 3. 使用 RecyclerView 替代 ScrollView 当列表项超过 20 个
// 4. 使用 ConstraintLayout 减少布局层级

// ❌ 不好的做法
// 1. 在 onDraw 中创建对象
protected void onDraw(Canvas canvas) {
    Paint p = new Paint();  // ❌ 每次绘制都创建对象
    // ...
}

// 2. 过度嵌套布局
LinearLayout outer -> LinearLayout mid -> LinearLayout inner  // ❌ 嵌套过深
// 改为: ConstraintLayout 或 更扁平的层级
```

### 3. 颜色常量速查

```java
// Modern UI 中颜色格式为 ARGB 32 位整数
// 0xAARRGGBB
public static final int WHITE       = 0xFFFFFFFF;
public static final int BLACK       = 0xFF000000;
public static final int TRANSPARENT = 0x00000000;

// 深色主题配色（推荐用于 MC 模组 UI）
public static final int DARK_BG       = 0xFF1E1E2E;  // 深色背景
public static final int DARK_SURFACE  = 0xFF2A2A3E;  // 卡片表面
public static final int DARK_PRIMARY  = 0xFF6C63FF;  // 主色调
public static final int DARK_ACCENT   = 0xFF3F51B5;  // 强调色
public static final int TEXT_PRIMARY  = 0xFFFFFFFF;   // 主文字
public static final int TEXT_SECONDARY = 0xFF888888;  // 次要文字
public static final int DIVIDER_COLOR = 0xFF333355;   // 分割线
```

### 4. Fragment 生命周期回调

```java
public class MyFragment extends Fragment {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Fragment 创建时调用（适合初始化数据）
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // 创建 View 层级（必须实现）
        return rootView;
    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        // View 创建完成后调用（适合设置监听器、启动动画等）
    }

    @Override
    public void onResume() {
        super.onResume();
        // Fragment 可见时调用
    }

    @Override
    public void onPause() {
        super.onPause();
        // Fragment 不可见时调用（例如被另一个 Fragment 覆盖）
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        // View 层级被销毁时调用
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        // Fragment 被销毁时调用
    }
}
```

### 5. 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `ClassNotFoundException: icyllis.modernui...` | ModernUI 依赖未正确添加 | 检查 build.gradle 的 dependencies 配置 |
| 屏幕打开后全黑 | Fragment 的 onCreateView 返回了 null | 确保 onCreateView 返回有效的 View |
| 背景模糊不生效 | 未调用带 blurRadius 的 createScreen | 使用 `createScreen(fragment, 25)` |
| 动画不流畅 | 在 onDraw 中频繁创建对象 | 将 Paint 等对象声明为成员变量复用 |
| 按钮点击没反应 | 未设置 setOnClickListener | 检查是否正确设置了点击监听器 |
| 控件位置不对 | 未正确设置 LayoutParams | 检查宽高参数和 gravity/margins |

---

## 📚 参考资源

- **GitHub**: https://github.com/BloCamLimb/ModernUI-MC
- **Javadoc**: https://blocamlimb.github.io/ModernUI-MC/
- **Maven**: https://maven.izzel.io/releases/ （IzzelAliz Maven）
- **当前版本**: 3.12.0.2 (MC 1.21.1)
