# Video Summarizer - Flutter 版本

这是从React Native迁移而来的视频总结器应用的Flutter实现版本。采用现代Flutter架构，支持iOS和Android平台。

## 项目概述

Video Summarizer是一个多模态智能视频总结应用，支持：
- 🎵 **音频分析**: 提取和分析视频中的音频内容
- 👁️ **视觉分析**: 识别关键视觉元素和场景
- 🔗 **融合综合**: 结合音频和视觉信息生成综合总结
- 🔎 **时间旅行问答**: 按时间戳追问视频特定内容

## 功能屏幕

### 1. ⚙️ Settings 配置屏幕
- 配置OpenAI API Key
- 设置Base URL
- 输入总结偏好
- 选择并行处理模式（ThreadPool/Send API）

### 2. 🎬 Video Selection 视频选择屏幕
- YouTube URL输入
- 本地视频文件上传
- 拖拽上传支持

### 3. ⏳ Processing Progress 处理进度屏幕
- 实时显示整体进度
- 音频分析进度
- 视觉分析进度
- 融合综合进度
- 各模块独立进度条

### 4. 📝 Summary Result 总结结果屏幕
- 展示完整分析报告
- 核心要点提取
- 音频摘要
- 视觉亮点
- 复制全文和分享功能

### 5. 🔎 Time Travel Q&A 时间旅行追问屏幕
- 时间戳精确定位
- 证据窗口配置（5-60秒）
- 按时间戳追问问题
- 问答历史记录

## 架构

```
lib/
├── main.dart                      # 主应用入口
├── theme/
│   └── design_system.dart        # 设计系统（颜色、字体、间距）
├── models/
│   └── models.dart               # 数据模型
├── providers/
│   └── app_state_provider.dart   # 应用状态管理
└── screens/
    ├── settings_screen.dart           # 配置屏幕
    ├── video_selection_screen.dart    # 视频选择屏幕
    ├── processing_progress_screen.dart # 进度屏幕
    ├── summary_result_screen.dart     # 结果屏幕
    └── time_travel_qa_screen.dart     # 时间旅行屏幕
```

## 设计系统

### 颜色系统
- **主色**: #0066FF（蓝色）
- **背景**: #F5F5F5（浅灰色）
- **文本主色**: #1A1A1A（深灰）
- **文本辅色**: #666666（中灰）
- **边框**: #DDDDDD（浅灰）
- **警告**: #FFF8E1（浅黄）

### 字体
- **标题**: 24px, 700
- **标签**: 13px, 600
- **正文**: 12px, 400
- **导航标签**: 10px, 600

### 圆角
- **大圆角**: 12px（卡片）
- **中圆角**: 8px（输入框）
- **导航圆角**: 36px/26px

## 快速开始

### 环境要求
- Flutter SDK >= 3.0.0
- Dart >= 3.0.0
- Android SDK (API 21+)
- Xcode (iOS开发)

### 安装步骤

1. **安装依赖**
```bash
flutter pub get
```

2. **运行应用**
```bash
# 运行到模拟器/真机
flutter run

# 特定平台运行
flutter run -d android
flutter run -d ios
```

3. **构建APK**
```bash
flutter build apk --split-per-abi
```

4. **构建iOS应用**
```bash
flutter build ios
```

## 项目结构

### 核心文件说明

**lib/main.dart**
- 应用入口点
- 5个屏幕的底部导航管理
- 全局Provider配置

**lib/theme/design_system.dart**
- 颜色常量定义
- 字体样式定义
- 间距系统
- 圆角常量
- 全局主题配置

**lib/providers/app_state_provider.dart**
- 使用Provider进行状态管理
- 配置保存到SharedPreferences
- 进度更新模拟
- 结果存储和历史记录

**lib/screens/**
- 各屏幕实现
- 响应式布局
- 用户交互处理

## 主要依赖

- **provider**: 6.4.0 - 状态管理
- **shared_preferences**: 2.2.0 - 本地数据持久化
- **file_picker**: 8.0.0 - 文件选择
- **http**: 1.2.0 - HTTP请求
- **percent_indicator**: 4.1.1 - 进度显示

## 开发指南

### 添加新屏幕
1. 在`lib/screens/`创建新文件
2. 继承`StatefulWidget`或`StatelessWidget`
3. 在`main.dart`的`_NavItem`列表中注册
4. 使用设计系统常量保持UI一致性

### 修改主题颜色
1. 编辑`lib/theme/design_system.dart`中的`AppColors`
2. 更新对应的Material主题配置
3. 所有屏幕会自动应用新颜色

### 保存用户配置
```dart
final appState = context.read<AppStateProvider>();
await appState.saveApiConfig(
  apiKey: 'sk-...',
  baseUrl: 'https://api.openai.com/v1',
);
```

## 状态管理流程

1. **初始化**: AppStateProvider在main.dart中使用ChangeNotifierProvider注册
2. **读取**: `context.read<AppStateProvider>()`获取单次值
3. **监听**: `Consumer<AppStateProvider>`实时监听状态变化
4. **更新**: 调用provider的方法更新状态，自动通知所有listeners

## 响应式设计

应用基于标准iPhone尺寸优化（428x926），但支持各种屏幕尺寸：
- 使用`MediaQuery`获取屏幕尺寸
- 使用flex布局自适应宽度
- 使用`SingleChildScrollView`处理内容溢出

## 测试

```bash
# 运行所有测试
flutter test

# 特定测试文件
flutter test test/screens/settings_screen_test.dart

# 代码覆盖率
flutter test --coverage
```

## 常见问题

**Q: 如何连接到真实后端API？**
A: 在`lib/providers/app_state_provider.dart`中的各个方法中实现HTTP请求，替换当前的模拟数据。

**Q: 如何添加权限？**
A: 编辑`android/app/src/main/AndroidManifest.xml`和`ios/Runner/Info.plist`

**Q: 如何调整UI样式？**
A: 所有样式都在`lib/theme/design_system.dart`中定义，修改后自动应用到全部UI。

## 构建和发布

### Android
1. 配置签名密钥
2. 运行 `flutter build apk --release`
3. 上传到Google Play

### iOS
1. 配置证书和预配文件
2. 运行 `flutter build ios --release`
3. 使用Xcode或TestFlight发布

## 性能优化

- 使用`const`构造函数减少重建
- 使用`Provider`的`select`方法精确订阅
- 异步操作使用`Future`或`Stream`
- 列表使用`ListView.builder`实现虚拟化

## 许可证

MIT License

## 支持

如有问题或建议，请提交Issue或联系开发团队。
