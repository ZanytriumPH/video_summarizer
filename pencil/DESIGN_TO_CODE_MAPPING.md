# 🎯 视频总结器移动端项目完整指南

## 项目成果物清单

本项目为您的视频总结器应用提供了完整的移动端（iOS/Android）解决方案：

### 📊 Pencil 设计文件
- **位置**: 在Pencil编辑器中打开此项目时可见
- **屏幕数量**: 5个独立屏幕，水平排列便于review
- **设计规格**: iPhone 12/13标准尺寸（428x926px）
- **特点**: 
  - 所有屏幕分开排列，便于同步审查
  - 详细的组件和交互说明
  - 完整的色彩、字体、间距系统

### 💻 React Native 代码文件

#### 核心文件
| 文件 | 说明 |
|------|------|
| `App.js` | 主应用入口 + 导航栏定义 + 设计系统常量 |
| `package.json` | 项目依赖配置 |
| `app.json` | Expo配置文件 |
| `SETUP.md` | 完整的安装和集成指南 |

#### 屏幕组件（Screen）
| 屏幕 | 文件 | 功能 |
|-----|------|------|
| ⚙️ Settings | `screens/SettingsScreen.js` | API配置、偏好设置、并行模式选择 |
| 🎬 Video Selection | `screens/VideoSelectionScreen.js` | YouTube URL输入、本地文件上传 |
| ⏳ Processing | `screens/ProcessingProgressScreen.js` | 实时处理进度展示（音频✓视觉✓融合） |
| 📝 Summary | `screens/SummaryResultScreen.js` | 总结报告展示、复制、分享 |
| 🔎 Time Travel Q&A | `screens/TimeTravelQAScreen.js` | 时间戳追问、证据窗口调节 |

## 🔄 Pencil 设计 ↔️ React Native 代码的对应关系

### 1️⃣ 设置配置屏幕 (Settings Screen)

**Pencil 设计中的元素**:
- 状态栏：黑色，显示时间和信号
- 标题："Video Summarizer" / "多模态智能总结"
- 输入字段 1: OpenAI API Key（密码输入）
- 输入字段 2: Base URL
- 输入区域 3: 总结偏好（文本区，80px高）
- 模式选择：ThreadPool (选中) 和 Send API (未选中)
- 底部导航栏：5个标签，第一个⚙️高亮

**React Native 实现**:
```javascript
// screens/SettingsScreen.js
- SafeAreaView 包装整个屏幕
- 状态栏组件：FlexRow，黑色背景，高度62px
- ScrollView：处理潜在的内容溢出
- TextInput：用于API Key、Base URL、用户提示
- TouchableOpacity：模式选择按钮
```

**样式映射**:
- 主标题 (24px, 700) → `FONTS.title`
- 副标题 (12px, 400) → `FONTS.subtitle`
- 输入框圆角 (8px) → `BORDER_RADIUS.medium`
- 卡片圆角 (12px) → `BORDER_RADIUS.large`
- 间距 (16px 内边距) → `SPACING.lg`

---

### 2️⃣ 视频选择屏幕 (Video Selection)

**Pencil 设计中的元素**:
- YouTube URL 选项（蓝色высокого highlight）
- 本地上传选项（白色，未选中）
- 拖拽上传区域：虚线边框，120x60px
- 下一步按钮：蓝色，全宽，48px高
- 状态栏与导航栏

**React Native 实现**:
```javascript
// screens/VideoSelectionScreen.js
- 两个 TouchableOpacity 作为切换选项
- TextInput 用于 YouTube URL
- DocumentPicker 用于文件选择
- 条件渲染：根据选中的来源类型显示相应输入
```

**关键功能**:
- `handleFileSelect()`: 使用 `react-native-document-picker` 选择视频
- `handleNext()`: 验证输入并导航到处理屏幕

---

### 3️⃣ 处理进度屏幕 (Processing Progress)

**Pencil 设计中的元素**:
- 主进度条：overall 35/100 (35%)
- 三个进度卡片：音频、视觉、融合，各自有:
  - 标签 (13px, 600)
  - 完成数值 (11px, 500, 蓝色)
  - 进度条 (6px高，灰色背景，蓝色填充)
- 状态消息：处理步骤列表

**React Native 实现**:
```javascript
// screens/ProcessingProgressScreen.js
- useState hook 管理进度状态
- useEffect hook 模拟进度更新（实际应连接WebSocket）
- ProgressBar 子组件：
  - 循环创建进度卡片
  - 动态计算进度条宽度百分比
```

**动画效果**:
- 进度条宽度动态计算：`width: ${Math.min(value, 100)}%`
- 每秒更新一次进度数据（模拟）

---

### 4️⃣ 总结结果屏幕 (Summary Result)

**Pencil 设计中的元素**:
- 标题 + 副标题
- 总结内容白色卡片（可滚动）：
  - ## 核心要点
  - ## 音频摘要
  - ## 视觉亮点
- 复制全文按钮：白色，边框
- 分享报告按钮：蓝色填充
- 元数据：生成时间、处理时间、视频时长

**React Native 实现**:
```javascript
// screens/SummaryResultScreen.js
- ScrollView 支持长内容滚动
- 静态总结内容文本
- Clipboard API：复制文本到剪贴板
- Share API：调用系统分享
- 状态管理：tracking 复制状态
```

**交互**:
- 复制按钮点击 → 设置 copied 状态 → 2秒后恢复
- 分享按钮 → 调用原生分享菜单

---

### 5️⃣ 时间旅行追问屏幕 (Time Travel Q&A)

**Pencil 设计中的元素**:
- 目标时间戳输入：灰色背景，蓝色文本 (14px, 600)
- 证据窗口标签 + 值显示
- 滑块：范围 5-60秒，当前值 20秒
- 追问问题输入框：80px高，白色背景，1px边框
- 提交按钮：蓝色，48px高
- 结果卡片：黄色背景 (#FFF8E1)，包含答案和时间范围

**React Native 实现**:
```javascript
// screens/TimeTravelQAScreen.js
- TextInput：时间戳输入 (MM:SS 格式)
- Slider 组件：处理证据窗口大小
- TextInput：多行问题输入
- 条件渲染：answer 内容显示黄色卡片
```

**核心逻辑**:
```javascript
const handleAsk = async () => {
  // 调用后端 /api/time-travel-qa 端点
  // 传递：thread_id, timestamp, question, window_seconds
  // 接收：answer 字符串
  // 显示结果及时间范围
};
```

---

## 🎨 视觉一致性检查表

在实现时，请确保以下视觉元素完全匹配Pencil设计：

### 颜色匹配
- [ ] 主色调蓝色 (#0066FF) 用于主CTA和活跃状态
- [ ] 背景灰色 (#F5F5F5) 用于屏幕背景
- [ ] 文本黑色 (#1A1A1A) 用于主标题
- [ ] 文本灰色 (#666666) 用于副文本
- [ ] 边框灰色 (#DDDDDD) 用于输入框和卡片边框
- [ ] 黄色警告背景 (#FFF8E1) 用于结果预览

### 字体大小匹配
- [ ] 页面标题：24px, fontWeight 700
- [ ] 副标题：12px, fontWeight 400
- [ ] 标签（如"API 配置"）：13px, fontWeight 600
- [ ] 正文：12px, fontWeight 400
- [ ] 底部导航标签：10px, fontWeight 600（大写）

### 间距匹配
- [ ] 屏幕内边距：16px（左右）
- [ ] 内容块间距：16-20px
- [ ] 卡片内间距：12-16px
- [ ] 状态栏高度：62px
- [ ] 底部导航栏高度：62px

### 圆角匹配
- [ ] 卡片：12px
- [ ] 输入框：8px
- [ ] 导航栏胶囊：36px
- [ ] 导航项：26px

---

## 📱 底部导航栏详解

### Pencil 设计规格
```
容器：
  - 背景：白色 (#FFFFFF)
  - 边框：1px, #EEEEEE
  - 圆角：36px（完全胶囊形）
  - 内边距：4px

标签项（5个）：
  1. ⚙️ SETTINGS
  2. 🎬 SELECT
  3. ⏳ PROGRESS
  4. 📝 SUMMARY
  5. 🔎 TRAVEL

活跃状态：
  - 背景：蓝色 (#0066FF)
  - 文本颜色：白色 (#FFFFFF)
  - 圆角：26px

非活跃状态：
  - 背景：透明
  - 文本颜色：灰色 (#999999)
```

### React Native 实现
```javascript
// App.js 中的 CustomTabBar 组件
<View style={styles.tabBarPill}>
  {state.routes.map((route, index) => (
    <TouchableOpacity
      key={route.key}
      onPress={() => navigation.navigate(route.name)}
      style={[
        styles.tabItem,
        isFocused && styles.tabItemActive,
      ]}
    >
      <Text>{tabIcons[index]}</Text>
      <Text>{tabLabels[index]}</Text>
    </TouchableOpacity>
  ))}
</View>
```

---

## 🚀 从设计到代码的工作流

### 第1步：理解Pencil设计
1. 在Pencil中打开设计文件
2. 分别查看5个屏幕（从左到右排列）
3. 注意每个屏幕的布局、间距、颜色

### 第2步：对应React Native代码
1. 在 `App.js` 中找到设计系统常量（COLORS, FONTS, SPACING）
2. 打开对应的屏幕组件文件
3. 审查组件和容器的结构

### 第3步：验证视觉一致性
1. 运行应用：`expo start`
2. 在iOS模拟器或Android模拟器中查看
3. 与Pencil设计进行像素级对比
4. 调整样式直至完全一致

### 第4步：集成后端API
1. 将模拟数据替换为真实API调用
2. 实现状态管理（Redux/Context API）
3. 添加错误处理和重试逻辑
4. 测试各个场景

---

## 📋 检查表：在开发时使用

- [ ] 所有屏幕都在 TabNavigator 中注册
- [ ] 底部导航栏在所有屏幕上显示
- [ ] 状态栏在所有屏幕上显示（高度62px）
- [ ] 所有文本使用 FONTS 常量
- [ ] 所有颜色使用 COLORS 常量
- [ ] 所有间距使用 SPACING 常量
- [ ] 进度屏幕实时更新动画流畅
- [ ] 文件上传功能正常工作
- [ ] 分享功能调用系统菜单
- [ ] 时间戳格式验证正确
- [ ] 没有报错或警告信息

---

## 💡 常见问题解答

**Q: 如何在Pencil和React Native之间保持同步？**
A: 设计系统常量（COLORS、FONTS、SPACING）充当bridge。更新Pencil时，同时更新 App.js 中的常量。

**Q: Pencil设计中的某个元素在React Native中怎样实现？**
A: 见本文档中的"对应关系"部分。通常Pencil中的矩形 → View，文本 → Text，可交互元素 → TouchableOpacity。

**Q: 如何处理不同屏幕尺寸？**
A: React Native 会自动缩放。使用 `Dimensions` API 获取屏幕尺寸，使用百分比或flex布局适配。

**Q: 底部导航栏在某些屏幕上消失了？**
A: 检查屏幕是否在 TabNavigator 中正确注册。内容是否有 `paddingBottom` 避免被导航栏覆盖。

---

## 📞 技术支持

如有问题，请参考：
- [React Native 官方文档](https://reactnative.dev/docs/getting-started)
- [React Navigation 文档](https://reactnavigation.org/docs/getting-started/)
- [Expo 文档](https://docs.expo.dev/)
- 本项目的 `SETUP.md` 文件

---

**项目创建日期**: 2024-01-15  
**最后更新**: 2024-01-15  
**版本**: 1.0.0
