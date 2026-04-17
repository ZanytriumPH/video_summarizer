# 🚀 立即开始

## 在5分钟内运行应用

### 前提条件
- Flutter SDK 3.0+ 已安装
- 一个模拟器或真机设备

### 步骤

#### 1️⃣ 获取依赖（30秒）
```bash
flutter pub get
```

#### 2️⃣ 运行应用（2分钟）
```bash
# 连接设备或启动模拟器，然后：
flutter run
```

#### 3️⃣ 看到应用启动！（2分钟）
- 应用会在你的设备上启动
- 可以看到5个标签的底部导航栏
- 尝试切换不同的屏幕

---

## 🎮 探索应用

### 测试流程

1. **⚙️ Settings** 
   - 输入API Key和Base URL
   - 修改并行模式
   - 点击"保存配置"

2. **🎬 Video Selection**
   - 选择本地视频文件
   - 点击"下一步"

3. **⏳ Progress**
   - 查看实时进度更新
   - 看进度条动画

4. **📝 Summary**
   - 查看总结结果（处理完成后）
   - 点击"复制全文"

5. **🔎 Q&A**
   - 输入时间戳
   - 调整滑块
   - 提交问题

---

## 📚 文档指南

| 文档 | 内容 | 阅读时间 |
|------|------|---------|
| [README.md](README.md) | 项目概述和功能 | 10分钟 |
| [SETUP.md](SETUP.md) | 开发环境配置 | 15分钟 |
| [USER_GUIDE.md](USER_GUIDE.md) | 应用功能说明 | 10分钟 |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Dart/Flutter速查 | 按需查看 |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 项目完成总结 | 5分钟 |

---

## 🔥 常用开发命令

### 热开发
```bash
flutter run          # 运行应用
r                    # 热重载（保持状态）
R                    # 完全重启
q                    # 退出
```

### 代码质量
```bash
flutter analyze      # 检查代码问题
flutter format lib/  # 格式化代码
flutter test         # 运行测试
```

### 调试
```bash
flutter run -v       # 详细模式（显示所有日志）
flutter run --profile # 性能分析模式
```

### 清理和构建
```bash
flutter clean        # 清理构建文件
flutter pub get      # 重新获取依赖
```

---

## 📁 项目结构一览

```
lib/
├── main.dart                          # 应用入口 ← 从这里开始
├── theme/design_system.dart           # UI系统设计
├── models/models.dart                 # 数据模型
├── providers/app_state_provider.dart  # 状态管理
└── screens/
    ├── settings_screen.dart           # ⚙️ 设置
    ├── video_selection_screen.dart    # 🎬 视频选择
    ├── processing_progress_screen.dart # ⏳ 进度
    ├── summary_result_screen.dart     # 📝 结果
    └── time_travel_qa_screen.dart     # 🔎 Q&A
```

---

## 🎨 修改应用样式

### 改变主色为红色

编辑 `lib/theme/design_system.dart`:

```dart
class AppColors {
  static const Color primary = Color(0xFFFF0000);  // 改为红色
  // 其他颜色...
}
```

重新加载应用：按 `r`

### 改变字体大小

编辑 `lib/theme/design_system.dart`:

```dart
static const TextStyle title = TextStyle(
  fontSize: 28,  // 从24改为28
  fontWeight: FontWeight.w700,
);
```

重新加载应用：按 `r`

---

## 🔗 集成你的API

### 修改API端点

编辑 `lib/providers/app_state_provider.dart`，在以下方法中添加真实的HTTP调用：

1. `simulateProgress()` - 实现真实的进度更新
2. `addTimeTravelResult()` - 实现真实的API查询

示例：
```dart
Future<void> realApiCall() async {
  final response = await http.post(
    Uri.parse(_config.baseUrl),
    headers: {'Authorization': 'Bearer ${_config.apiKey}'},
    body: jsonEncode({'video': _selectedVideo?.url}),
  );
  
  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    // 处理响应
  }
}
```

---

## 🧪 运行测试

创建 `test/unit_test.dart`:

```dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('AppConfig initialization', () {
    final config = AppConfig();
    expect(config.apiKey, 'sk-...');
  });
}
```

运行测试：
```bash
flutter test
```

---

## 📦 构建和发布

### 构建Android APK

```bash
flutter build apk --release
```

APK会保存到：`build/app/outputs/apk/release/`

### 构建iOS应用

```bash
flutter build ios --release
```

然后在Xcode中打开：`ios/Runner.xcworkspace`

---

## 🆘 快速故障排除

### 问题：`flutter: command not found`
```bash
# 检查Flutter安装
flutter --version

# 添加Flutter到PATH
export PATH="$PATH:`pwd`/flutter/bin"
```

### 问题：依赖无法安装
```bash
flutter clean
flutter pub cache clean
flutter pub get
```

### 问题：应用无法启动
```bash
flutter run -v  # 查看详细日志
```

---

## 📞 需要帮助？

### 查看文档
- 应用功能 → [USER_GUIDE.md](USER_GUIDE.md)
- 代码语法 → [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- 开发环境 → [SETUP.md](SETUP.md)
- 技术细节 → [README.md](README.md)

### 常见资源
- [Flutter官方](https://flutter.dev)
- [Dart官方](https://dart.dev)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/flutter)

---

## ✨ 下一步建议

1. ✅ 运行应用，熟悉UI
2. ✅ 阅读[USER_GUIDE.md](USER_GUIDE.md)了解功能
3. ✅ 修改[design_system.dart](lib/theme/design_system.dart)定制样式
4. ✅ 在[app_state_provider.dart](lib/providers/app_state_provider.dart)集成真实API
5. ✅ 添加测试到`test/`目录
6. ✅ 构建APK/IPA准备发布

---

## 🎉 准备好了吗？

```bash
flutter run
```

开始开发！ 🚀

---

**需要详细信息？** 查看 [FILE_INVENTORY.md](FILE_INVENTORY.md) 了解所有文件的完整清单。

**想要深入？** 参考 [QUICK_REFERENCE.md](QUICK_REFERENCE.md) 获得Dart/Flutter语法速查。
