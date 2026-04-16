# Flutter 快速参考

## Dart 基础语法

### 变量声明
```dart
var name = 'John';           // 类型推断
String name = 'John';         // 显式声明
final finalName = 'John';     // 不可重赋值
const constantName = 'John';  // 编译时常量
```

### 函数
```dart
String greet(String name) => 'Hello, $name';  // 箭头函数
String greet(String name) { return 'Hello, $name'; }  // 传统

// 可选参数
void printName(String name, [String? nickname]) {}

// 命名参数
void printInfo({required String name, String? age}) {}
```

### 类和继承
```dart
class Animal {
  String name;
  
  Animal(this.name);
  
  void speak() { print('$name makes a sound'); }
}

class Dog extends Animal {
  Dog(String name) : super(name);
  
  @override
  void speak() { print('$name barks'); }
}
```

### 对象和映射
```dart
// 对象
var person = Person(name: 'John', age: 30);

// Map
var map = {'name': 'John', 'age': 30};
var value = map['name'];
```

### 异步编程
```dart
// Future
Future<String> fetchData() async {
  return 'data';
}

// 调用
var data = await fetchData();

// 或使用then
fetchData().then((data) { print(data); });
```

## Flutter Widget 基础

### 常用Widgets
```dart
// 布局
Container()          // 盒子模型
Column()            // 纵向布局
Row()               // 横向布局
Stack()             // 层叠布局
Expanded()          // 占用剩余空间
Padding()           // 内边距
Align()             // 对齐

// 文本和输入
Text()              // 文本
TextField()         // 文本输入
RichText()          // 富文本

// 按钮
ElevatedButton()    // 凸起按钮
OutlinedButton()    // 边框按钮
TextButton()        // 文本按钮

// 滚动
SingleChildScrollView()  // 单子元素滚动
ListView()          // 列表视图
GridView()          // 网格视图
CustomScrollView()  // 自定义滚动

// 对话框
showDialog()        // 显示对话框
ScaffoldMessenger.of(context).showSnackBar()  // 显示提示
```

### 常用属性
```dart
Container(
  width: 100,
  height: 100,
  color: Colors.blue,
  margin: EdgeInsets.all(16),
  padding: EdgeInsets.symmetric(horizontal: 16),
  decoration: BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(8),
    border: Border.all(color: Colors.grey),
    boxShadow: [BoxShadow(color: Colors.black12)],
  ),
  child: Text('Content'),
)
```

## 状态管理（Provider）

### 定义Provider
```dart
class AppState extends ChangeNotifier {
  String _name = '';
  
  String get name => _name;
  
  void setName(String name) {
    _name = name;
    notifyListeners();  // 通知监听者
  }
}
```

### 使用Provider
```dart
// 在MaterialApp中注册
ChangeNotifierProvider(
  create: (_) => AppState(),
  child: MyApp(),
)

// 读取值（单次）
final appState = context.read<AppState>();

// 监听并构建UI
Consumer<AppState>(
  builder: (context, appState, _) {
    return Text(appState.name);
  },
)

// 选择特定属性
Consumer<AppState>(
  selector: (_, provider) => provider.name,
  builder: (_, name, __) => Text(name),
)
```

## 常用命令

### 项目管理
```bash
flutter create my_app              # 创建项目
flutter pub get                    # 获取依赖
flutter pub upgrade                # 升级依赖
flutter clean                      # 清理构建
```

### 开发
```bash
flutter run                        # 运行应用
flutter run -v                    # 详细模式
flutter run --profile             # 性能模式
flutter run -d <device>           # 指定设备
```

### 热重载快捷键
```
r          - 热重载
R          - 完整重启
h          - 显示帮助
w          - 打印widget树
q          - 退出
```

### 分析和测试
```bash
flutter analyze                    # 静态分析
flutter test                       # 运行测试
flutter test --coverage            # 代码覆盖率
flutter doctor                     # 检查环境
```

### 构建
```bash
flutter build apk                  # Android APK
flutter build apk --split-per-abi  # 分离架构APK
flutter build ios                  # iOS应用
flutter build web                  # Web应用
```

### 调试
```bash
flutter attach                     # 附加到运行的应用
flutter logs                       # 查看日志
flutter devtools                   # 打开开发者工具
```

## 布局技巧

### 响应式布局
```dart
// 获取屏幕尺寸
final screenWidth = MediaQuery.of(context).size.width;
final screenHeight = MediaQuery.of(context).size.height;

// 响应式padding
final padding = screenWidth > 600 ? 32.0 : 16.0;

// 条件构建
screenWidth > 600 
  ? _buildWideLayout()
  : _buildNarrowLayout()
```

### 水平分布
```dart
Row(
  mainAxisAlignment: MainAxisAlignment.spaceEvenly,  // 平均分布
  // 或 MainAxisAlignment.spaceBetween (两端对齐)
  // 或 MainAxisAlignment.center (居中)
  children: [...],
)
```

### 垂直分布
```dart
Column(
  mainAxisAlignment: MainAxisAlignment.end,      // 底部
  crossAxisAlignment: CrossAxisAlignment.center,  // 水平居中
  children: [...],
)
```

### 弹性布局
```dart
Row(
  children: [
    Expanded(child: Widget1()),     // 占用剩余空间
    Flexible(child: Widget2()),     // 灵活大小
    SizedBox(width: 100),           // 固定大小
  ],
)
```

## 样式和主题

### 文本样式
```dart
Text(
  'Hello',
  style: TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.bold,
    color: Colors.blue,
    fontStyle: FontStyle.italic,
  ),
)
```

### 装饰
```dart
decoration: BoxDecoration(
  color: Colors.blue,
  borderRadius: BorderRadius.circular(12),
  border: Border.all(color: Colors.grey),
  boxShadow: [
    BoxShadow(
      color: Colors.black12,
      blurRadius: 4,
      offset: Offset(0, 2),
    ),
  ],
)
```

## 事件处理

### 点击事件
```dart
GestureDetector(
  onTap: () { print('Tapped'); },
  child: Text('Tap me'),
)

// 或
ElevatedButton(
  onPressed: () { print('Pressed'); },
  child: Text('Press me'),
)
```

### 表单输入
```dart
TextField(
  controller: _controller,
  onChanged: (value) { print(value); },
  onSubmitted: (value) { print('Submitted: $value'); },
  decoration: InputDecoration(
    hintText: 'Enter text',
    labelText: 'Name',
    border: OutlineInputBorder(),
  ),
)
```

## 导航

### 页面跳转
```dart
// Push（可返回）
Navigator.push(
  context,
  MaterialPageRoute(builder: (_) => NextPage()),
);

// Pop（返回）
Navigator.pop(context);

// 带返回值
final result = await Navigator.push(
  context,
  MaterialPageRoute(builder: (_) => NextPage()),
);

// Replace（不可返回）
Navigator.pushReplacementNamed(context, '/home');
```

## 调试

### 打印日志
```dart
print('Simple log');
debugPrint('Debug message');  // 适合长消息
```

### 条件断点
```dart
void myFunction() {
  debugger();  // 添加断点
  // 代码...
}
```

### 性能检查
```dart
final sw = Stopwatch()..start();
// 代码...
print('Time: ${sw.elapsedMilliseconds}ms');
```

## 本地存储

### SharedPreferences
```dart
// 保存
final prefs = await SharedPreferences.getInstance();
await prefs.setString('key', 'value');
await prefs.setInt('count', 10);

// 读取
final value = prefs.getString('key');
final count = prefs.getInt('count') ?? 0;

// 删除
await prefs.remove('key');
```

## HTTP 请求

### 使用 http 包
```dart
import 'package:http/http.dart' as http;

// GET
final response = await http.get(Uri.parse('https://api.example.com'));
if (response.statusCode == 200) {
  final data = jsonDecode(response.body);
}

// POST
final response = await http.post(
  Uri.parse('https://api.example.com'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({'key': 'value'}),
);
```

## 常见错误及解决

### 错误：'BuildContext' is not defined
**原因**: 没有导入flutter/material.dart  
**解决**: `import 'package:flutter/material.dart';`

### 错误：setState() 在StatelessWidget中调用
**原因**: 在无状态widget中修改状态  
**解决**: 使用StatefulWidget或使用Provider

### 错误：RenderFlex children overflow
**原因**: 列/行内容超出屏幕  
**解决**: 使用Expanded或SingleChildScrollView

### 错误：setState() called after dispose()
**原因**: 在widget销毁后修改状态  
**解决**: 检查mounted或取消订阅

## 有用的资源

- [Flutter官方文档](https://flutter.dev/docs)
- [Dart官方文档](https://dart.dev)
- [Flutter Cookbook](https://flutter.dev/docs/cookbook)
- [Pub.dev 包管理](https://pub.dev)

---

## 项目特定快速参考

### 本项目的核心文件

| 文件 | 用途 |
|------|------|
| lib/main.dart | 应用入口和导航 |
| lib/theme/design_system.dart | 颜色、字体、间距定义 |
| lib/providers/app_state_provider.dart | 全局状态管理 |
| lib/screens/*.dart | 各个屏幕实现 |

### 快速修改

**修改颜色方案**:
编辑 `lib/theme/design_system.dart` 中的 `AppColors` 类

**添加新屏幕**:
1. 在 `lib/screens/` 创建新文件
2. 在 `main.dart` 的 `_NavItem` 列表中注册

**修改导航栏**:
编辑 `main.dart` 中的 `_BottomNavBar` 组件
