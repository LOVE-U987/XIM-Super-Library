---
name: animejs
description: 提供 Anime.js v4 动画库的代码辅助，包含动画创建、时间轴、缓动函数、拖拽、滚动监听等功能。Invoke when user is writing animation code with Anime.js or needs help with web animations.
---

# Anime.js v4 Skill

## 概述

Anime.js 是一个快速、多功能且轻量级的 JavaScript 动画库，具有简单而强大的 API。它支持 CSS 属性、SVG、DOM 属性和 JavaScript 对象的动画。

- **版本**: v4.3.6
- **官网**: https://animejs.com
- **文档**: https://animejs.com/documentation

## 核心功能模块

### 1. 基础动画 (animate)

```javascript
import { animate, stagger } from 'animejs';

// 基础动画
animate('.square', {
  x: 320,
  rotate: { from: -180 },
  duration: 1250,
  delay: stagger(65, { from: 'center' }),
  ease: 'inOutQuint',
  loop: true,
  alternate: true
});
```

**AnimationParams 参数说明：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `targets` | string \| Element \| Array | 动画目标元素 |
| `duration` | number \| Function | 动画持续时间（毫秒） |
| `delay` | number \| Function | 动画延迟时间 |
| `ease` | string \| Function \| Spring | 缓动函数 |
| `loop` | boolean \| number | 循环次数 |
| `alternate` | boolean | 是否交替播放 |
| `autoplay` | boolean \| ScrollObserver | 是否自动播放 |
| `onBegin` | Callback | 动画开始回调 |
| `onUpdate` | Callback | 动画更新回调 |
| `onComplete` | Callback | 动画完成回调 |

### 2. 时间轴 (Timeline)

```javascript
import { createTimeline, stagger } from 'animejs';

const tl = createTimeline({
  defaults: { duration: 1000 },
  autoplay: true
});

tl.add('.box', { x: 100 }, 0)
  .add('.box', { y: 100 }, '+=500')
  .add('.box', { rotate: 180 }, '<')
  .call(() => console.log('完成'), '+=100');
```

**时间轴位置参数：**
- `number` - 绝对位置（毫秒）
- `'+=number'` - 在上一个动画结束后延迟
- `'-=number'` - 在上一个动画结束前开始
- `'*=number'` - 基于总时长的比例位置
- `'<'` - 与上一个动画结束位置对齐
- `'<<'` - 与上一个动画开始位置对齐
- `'label'` - 标签位置

### 3. 缓动函数 (Easings)

```javascript
import { eases, spring, cubicBezier, steps, linear, irregular } from 'animejs';

// 预设缓动
animate('.el', { x: 100, ease: 'inOutQuint' });
animate('.el', { x: 100, ease: eases.outQuint });

// 弹簧缓动
animate('.el', { x: 100, ease: spring({ mass: 1, stiffness: 100, damping: 10 }) });

// 贝塞尔曲线
animate('.el', { x: 100, ease: cubicBezier(0.25, 0.1, 0.25, 1) });

// 阶梯函数
animate('.el', { x: 100, ease: steps(5) });
```

**预设缓动列表：**
- `linear`, `none`
- `in`, `out`, `inOut`
- `inQuad`, `outQuad`, `inOutQuad`
- `inCubic`, `outCubic`, `inOutCubic`
- `inQuart`, `outQuart`, `inOutQuart`
- `inQuint`, `outQuint`, `inOutQuint`
- `inSine`, `outSine`, `inOutSine`
- `inCirc`, `outCirc`, `inOutCirc`
- `inExpo`, `outExpo`, `inOutExpo`
- `inBounce`, `outBounce`, `inOutBounce`
- `inBack`, `outBack`, `inOutBack`
- `inElastic`, `outElastic`, `inOutElastic`

### 4. 交错动画 (Stagger)

```javascript
import { stagger } from 'animejs';

animate('.box', {
  x: 100,
  delay: stagger(100), // 每个元素延迟 100ms
  duration: stagger(500, { from: 'center' }), // 从中心开始
});

// Stagger 参数
stagger(value, {
  start: 0,        // 起始延迟
  from: 'first',   // 'first' | 'center' | 'last' | 'random' | number
  reversed: false, // 是否反向
  grid: [5, 5],    // 网格布局 [列, 行]
  axis: 'x',       // 'x' | 'y'
  ease: 'linear',  // 缓动函数
});
```

### 5. 可动画对象 (Animatable)

```javascript
import { createAnimatable } from 'animejs';

const box = createAnimatable('.box', {
  x: { duration: 500, ease: 'outQuint' },
  y: { duration: 500, ease: 'outQuint' },
  rotate: { duration: 1000 },
});

// 使用
box.x(100);           // 动画到 x: 100
box.y(200, 1000);     // 动画到 y: 200，持续 1000ms
box.rotate(180, 500, 'inOutQuad'); // 带缓动函数

// 获取当前值
console.log(box.x()); // 获取当前 x 值
```

### 6. 拖拽 (Draggable)

```javascript
import { createDraggable } from 'animejs';

// 基础拖拽
const draggable = createDraggable('.box');

// 高级配置
const draggable = createDraggable('.box', {
  container: '.container',  // 限制容器
  x: true,                  // 启用 X 轴
  y: true,                  // 启用 Y 轴
  snap: 50,                 // 吸附步长
  containerPadding: 10,     // 容器内边距
  containerFriction: 0.8,   // 容器摩擦力
  dragSpeed: 1,             // 拖拽速度
  scrollSpeed: 1.5,         // 滚动速度
  releaseEase: 'outQuint',  // 释放缓动
  releaseMass: 1,           // 释放质量
  releaseStiffness: 80,     // 释放刚度
  releaseDamping: 20,       // 释放阻尼
  cursor: {
    onHover: 'grab',
    onGrab: 'grabbing'
  },
  onGrab: (self) => console.log('抓取'),
  onDrag: (self) => console.log('拖拽中'),
  onRelease: (self) => console.log('释放'),
  onSettle: (self) => console.log('稳定'),
  onSnap: (self) => console.log('吸附'),
});

// 方法
draggable.setX(100);           // 设置 X 位置
draggable.setY(100);           // 设置 Y 位置
draggable.enable();            // 启用
draggable.disable();           // 禁用
draggable.reset();             // 重置
draggable.revert();            // 还原
draggable.scrollInView();      // 滚动到视图内
```

### 7. 滚动监听 (Scroll Observer)

```javascript
import { onScroll } from 'animejs';

// 基础滚动监听
onScroll({
  target: '.section',
  enter: 'top 80%',
  leave: 'bottom 20%',
  onEnter: (self) => console.log('进入视图'),
  onLeave: (self) => console.log('离开视图'),
});

// 同步动画到滚动
const animation = animate('.box', { x: 500, autoplay: false });

onScroll({
  sync: animation,
  target: '.section',
  enter: 'top bottom',
  leave: 'bottom top',
});
```

### 8. SVG 动画

```javascript
import { createMotionPath, createDrawable, morphTo } from 'animejs';

// 运动路径
const path = createMotionPath('#motion-path');
animate('.follower', {
  motionPath: path,
  duration: 2000,
});

// 描边动画
const drawable = createDrawable('#svg-path');
animate(drawable, {
  draw: ['0%', '100%'],
  duration: 2000,
});

// 形状变形
morphTo('#path1', '#path2', {
  duration: 1000,
  ease: 'inOutQuad'
});
```

### 9. 文本动画

```javascript
import { splitText } from 'animejs';

// 分割文本
const text = splitText('.text', {
  chars: true,   // 按字符分割
  words: true,   // 按单词分割
  lines: true,   // 按行分割
});

// 动画字符
animate(text.chars, {
  y: [-20, 0],
  opacity: [0, 1],
  delay: stagger(30),
});
```

### 10. 工具函数 (Utils)

```javascript
import {
  random, randomPick, shuffle,           // 随机
  lerp, clamp, mapRange, snap,           // 数学
  degToRad, radToDeg, round,             // 转换
  get, set, cleanInlineStyles,           // DOM
  stagger,                               // 交错
  keepTime, sync,                        // 时间
} from 'animejs';

// 随机
random(0, 100);           // 0-100 随机数
randomPick([1, 2, 3]);    // 随机选择
shuffle([1, 2, 3]);       // 随机打乱

// 数学
lerp(0, 100, 0.5);        // 线性插值
clamp(150, 0, 100);       // 限制范围
mapRange(50, 0, 100, 0, 1); // 映射范围
snap(23, 10);             // 吸附到 10 的倍数

// DOM
get('.el', 'width');      // 获取属性
set('.el', { x: 100 });   // 设置属性
```

### 11. 作用域 (Scope)

```javascript
import { createScope } from 'animejs';

const scope = createScope({
  root: '.container',
  defaults: { duration: 1000 },
  mediaQueries: {
    mobile: '(max-width: 768px)',
    desktop: '(min-width: 769px)',
  }
});

scope.add(self => {
  // 在作用域内创建动画
  const animation = self.animate('.box', { x: 100 });
  
  // 响应式
  if (self.matches('mobile')) {
    animation.stretch(500);
  }
  
  // 清理函数
  return () => {
    animation.revert();
  };
});
```

### 12. WAAPI 支持

```javascript
import { waapi } from 'animejs';

// 使用 Web Animations API
const animation = waapi('.box', {
  x: 100,
  duration: 1000,
  ease: 'ease-out',
});
```

## 动画控制方法

所有动画实例（Timer、JSAnimation、Timeline）都有以下方法：

| 方法 | 说明 |
|------|------|
| `play()` | 播放动画 |
| `pause()` | 暂停动画 |
| `resume()` | 恢复动画 |
| `restart()` | 重新开始 |
| `reverse()` | 反向播放 |
| `seek(time)` | 跳转到指定时间 |
| `cancel()` | 取消动画 |
| `revert()` | 还原并取消 |
| `complete()` | 立即完成 |
| `stretch(duration)` | 拉伸/压缩时长 |
| `refresh()` | 刷新函数值 |

**属性：**

| 属性 | 说明 |
|------|------|
| `currentTime` | 当前时间 |
| `progress` | 进度 (0-1) |
| `iterationCurrentTime` | 当前迭代时间 |
| `iterationProgress` | 当前迭代进度 |
| `currentIteration` | 当前迭代次数 |
| `speed` | 播放速度 |
| `reversed` | 是否反向 |
| `paused` | 是否暂停 |
| `completed` | 是否完成 |
| `cancelled` | 是否取消 |

## 回调函数

```javascript
animate('.el', {
  duration: 1000,
  onBegin: (self) => {},      // 动画开始
  onBeforeUpdate: (self) => {}, // 更新前
  onUpdate: (self) => {},      // 更新时
  onLoop: (self) => {},        // 循环时
  onPause: (self) => {},       // 暂停时
  onComplete: (self) => {},    // 完成时
  onRender: (self) => {},      // 渲染时（仅动画）
});
```

## Promise 支持

```javascript
const animation = animate('.box', { x: 100 });

// 使用 Promise
await animation.then();
console.log('动画完成');

// 或者
animation.then(() => {
  console.log('动画完成');
});
```

## 最佳实践

1. **性能优化**
   - 使用 `transform` 和 `opacity` 属性获得最佳性能
   - 大量元素动画时考虑使用 `composition: 'none'`
   - 使用 `will-change` CSS 属性

2. **可访问性**
   - 尊重 `prefers-reduced-motion` 媒体查询
   - 提供动画关闭选项

3. **内存管理**
   - 动画完成后调用 `revert()` 清理
   - 使用 `createScope` 管理多个动画

4. **响应式**
   - 使用 `createScope` 和 `mediaQueries`
   - 监听窗口大小变化并调用 `refresh()`

## 完整示例

```javascript
import { 
  animate, 
  createTimeline, 
  stagger, 
  createDraggable,
  onScroll,
  splitText 
} from 'animejs';

// 1. 页面加载动画
const intro = createTimeline()
  .add('.logo', { scale: [0, 1], opacity: [0, 1] }, 0)
  .add('.nav-item', { y: [-20, 0], opacity: [0, 1] }, stagger(100))
  .add('.hero-text', { y: [50, 0], opacity: [0, 1] }, '-=500');

// 2. 滚动触发动画
const sections = document.querySelectorAll('.section');
sections.forEach(section => {
  onScroll({
    target: section,
    enter: 'top 80%',
    onEnter: () => animate(section.querySelectorAll('.card'), {
      y: [50, 0],
      opacity: [0, 1],
      delay: stagger(100),
    }),
  });
});

// 3. 可拖拽卡片
const cards = document.querySelectorAll('.card');
cards.forEach(card => {
  createDraggable(card, {
    container: '.container',
    snap: 10,
    onRelease: (self) => {
      if (self.velocity > 0.5) {
        // 快速滑动时的惯性效果
      }
    },
  });
});

// 4. 文本动画
const headline = splitText('.headline', { chars: true });
animate(headline.chars, {
  y: [50, 0],
  rotateX: [90, 0],
  opacity: [0, 1],
  delay: stagger(30),
});
```