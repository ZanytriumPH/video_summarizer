# React Native 到 Flutter 迁移指南

## 概述

本文档概述了从React Native版本迁移到Flutter版本的关键变更、架构差异和功能映射。

## 项目结构对比

### React Native
```
pencil/
├── App.js                          # 主入口
├── screens/
│   ├── SettingsScreen.js
│   ├── VideoSelectionScreen.js
│   ├── ProcessingProgressScreen.js
│   ├── SummaryResultScreen.js
│   └── TimeTravelQAScreen.js
├── android/
├── app.json
└── package.json
```

### Flutter
```
flutter_project/
├── lib/
│   ├── main.dart                   # 主入口
│   ├── theme/
│   │   └── design_system.dart      # 设计系统
│   ├── models/
│   │   └── models.dart             # 数据模型
│   ├── providers/
│   │   └── app_state_provider.dart # 状态管理
│   └── screens/
│       ├── settings_screen.dart
│       ├── video_selection_screen.dart
│       ├── processing_progress_screen.dart
│       ├── summary_result_screen.dart
│       └── time_travel_qa_screen.dart
├── android/
├── ios/
├── pubspec.yaml                    # 依赖管理
└── analysis_options.yaml           # Lint配置
```

## 核心技术栈变更

| 功能 | React Native | Flutter |
|------|-------------|---------|
| 语言 | JavaScript | Dart |
| UI框架 | React Native | Flutter |
| 导航 | @react-navigation | go_router / Navigator |
| 状态管理 | useState | Provider |
| 本地存储 | AsyncStorage | shared_preferences |
| HTTP请求 | axios / fetch | http / dio |
| 文件选择 | react-native-document-picker | file_picker |
| 进度显示 | react-native-progress | percent_indicator |

## 功能映射

### 1. 设计系统

**React Native (App.js)**
```javascript
export const COLORS = { /* 颜色定义 */ };
export const FONTS = { /* 字体定义 */ };
export const SPACING = { /* 间距定义 */ };
```

**Flutter (lib/theme/design_system.dart)**
```dart
class AppColors { /* 颜色常量 */ }
class AppFonts { /* 文本样式 */ }
class AppSpacing { /* 间距常量 */ }
class AppTheme { /* 全局主题 */ }
```

### 2. 状态管理

**React Native (useState)**
```javascript
const [apiKey, setApiKey] = useState('sk-...');
// 更新: setApiKey(newValue);
```

**Flutter (Provider)**
```dart
final appState = context.read<AppStateProvider>();
appState.saveApiConfig(apiKey: newValue);
// 监听: Consumer<AppStateProvider>
```

### 3. 屏幕导航

**React Native (Bottom Tab Navigator)**
```javascript
<TabNavigator>
  <Tab.Screen name="Settings" component={SettingsScreen} />
  <Tab.Screen name="Video" component={VideoSelectionScreen} />
  // ...
</TabNavigator>
```

**Flutter (Custom Bottom Navigation)**
```dart
Scaffold(
  body: _navItems[_currentIndex].screen,
  bottomNavigationBar: _BottomNavBar(...)
)
```

### 4. TextInput -> TextField

**React Native**
```javascript
<TextInput
  style={styles.input}
  placeholder="..."
  value={apiKey}
  onChangeText={setApiKey}
/>
```

**Flutter**
```dart
TextField(
  controller: _apiKeyController,
  decoration: InputDecoration(
    hintText: '...',
  ),
)
```

### 5. ScrollView 保持不变

**React Native**
```javascript
<ScrollView>
  {/* 内容 */}
</ScrollView>
```

**Flutter**
```dart
SingleChildScrollView(
  child: Column(
    children: [ /* 内容 */ ]
  ),
)
```

### 6. 文件选择

**React Native**
```javascript
const res = await DocumentPicker.pick({
  type: [DocumentPicker.types.video],
});
```

**Flutter**
```dart
FilePickerResult? result = await FilePicker.platform.pickFiles(
  type: FileType.video,
);
```

### 7. 进度条

**React Native**
```javascript
<View style={styles.progressBarContainer}>
  <View style={[styles.progressBarFill, { width: `${value}%` }]} />
</View>
```

**Flutter**
```dart
LinearProgressIndicator(
  value: progress / 100,
)
```

## 关键架构差异

### 1. 热重载 vs 热更新

- **React Native**: 通常需要重启应用
- **Flutter**: 按 `r` 进行热重载，保持应用状态

### 2. 性能

- **Flutter**: 编译为原生代码，性能通常更好
- **React Native**: 运行在JavaScript bridge上

### 3. UI组件

- **Flutter**: 所有UI都是组件（Widgets）
- **React Native**: 使用原生UI组件

### 4. 样式系统

- **React Native**: StyleSheet + inline styles
- **Flutter**: 主要使用参数化构造函数

## 迁移检查清单

- [x] 创建Flutter项目结构
- [x] 实现设计系统（颜色、字体、间距）
- [x] 创建数据模型
- [x] 实现状态管理Provider
- [x] 迁移所有5个屏幕
- [x] 实现底部导航栏
- [x] 配置Android和iOS
- [ ] 集成真实API端点
- [ ] 添加错误处理
- [ ] 实现本地数据持久化
- [ ] 添加单元测试
- [ ] 性能测试和优化
- [ ] 应用市场发布准备

## 常见迁移问题

### 问题1：RN中的组件库在Flutter中不可用

**解决**: 寻找等效的Flutter包或自定义实现

### 问题2：异步操作处理方式不同

**RN (async/await)**
```javascript
const data = await fetchData();
```

**Flutter (Future)**
```dart
var data = await fetchData();
// 或使用FutureBuilder
FutureBuilder<Data>(
  future: fetchData(),
  builder: (context, snapshot) { ... }
)
```

### 问题3：屏幕尺寸和响应式设计

**Flutter**
```dart
// 获取屏幕尺寸
final screenWidth = MediaQuery.of(context).size.width;

// 响应式布局
Expanded(child: ...)  // 占用剩余空间
Flexible(child: ...)  // 灵活大小
```

## 性能优化建议

### 1. 使用const构造函数
```dart
const Text('Hello')  // 不会重建
```

### 2. 使用Provider的select方法
```dart
Consumer<AppStateProvider>(
  selector: (_, provider) => provider.progress,
  builder: (_, progress, __) { ... }
)
```

### 3. 使用ListView.builder虚拟化列表
```dart
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ...
)
```

### 4. 使用RepaintBoundary减少重绘
```dart
RepaintBoundary(
  child: MyExpensiveWidget(),
)
```

## 调试

### Flutter调试工具

```bash
# 详细日志
flutter run -v

# 性能分析
flutter run --profile

# 运行测试
flutter test
```

### 使用DevTools

```bash
flutter pub global activate devtools
devtools
```

然后访问提供的URL。

## 测试策略

### 单元测试
```dart
test('AppStateProvider saves API config', () async {
  final provider = AppStateProvider();
  await provider.saveApiConfig(
    apiKey: 'test-key',
    baseUrl: 'test-url',
  );
  expect(provider.config.apiKey, 'test-key');
});
```

### 集成测试
```dart
testWidgets('Settings screen displays', (WidgetTester tester) async {
  await tester.pumpWidget(const MyApp());
  expect(find.text('Video Summarizer'), findsOneWidget);
});
```

## 下一步

1. **运行应用**: `flutter run`
2. **连接API**: 在`lib/providers/app_state_provider.dart`中实现真实API调用
3. **添加测试**: 创建`test/`目录中的测试文件
4. **性能优化**: 使用Flutter DevTools分析性能
5. **发布**: 按照`SETUP.md`中的发布步骤操作

## 资源

- [Flutter官方文档](https://flutter.dev/docs)
- [Flutter最佳实践](https://flutter.dev/docs/testing/best-practices)
- [Provider文档](https://pub.dev/packages/provider)
- [Dart语言指南](https://dart.dev/guides)

## 支持

如有迁移相关问题，请参考：
1. `README.md` - 项目概述
2. `SETUP.md` - 开发环境设置
3. Flutter官方文档
4. Stack Overflow - flutter标签
