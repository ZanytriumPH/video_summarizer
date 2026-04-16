# Flutter开发环境设置指南

## 系统要求

- Windows 10/11 或 macOS 或 Linux
- 至少4GB RAM（8GB推荐）
- 150MB可用磁盘空间

## Windows 开发环境设置

### 1. 安装Flutter SDK

1. 从[Flutter官网](https://flutter.dev/docs/get-started/install/windows)下载最新版本
2. 解压到本地目录（推荐：`C:\flutter`）
3. 添加Flutter bin目录到PATH环境变量：
   - 打开"环境变量"设置
   - 在系统变量中找到PATH
   - 添加 `C:\flutter\bin`
4. 打开PowerShell或CMD，验证安装：
   ```bash
   flutter --version
   ```

### 2. 安装Android Studio

1. 从[Android Studio官网](https://developer.android.com/studio)下载
2. 运行安装程序
3. 在IDE中安装Android SDK：
   - Tools → SDK Manager
   - SDK Platforms: 选择至少一个API级别（推荐API 30+）
   - SDK Tools: 确保已安装"Android SDK Platform-Tools"和"Android SDK Tools"

### 3. 同意Android许可证

```bash
flutter doctor --android-licenses
```

### 4. 安装VS Code（可选）

1. 从[VS Code官网](https://code.visualstudio.com)下载
2. 安装Flutter和Dart插件

### 5. 验证环境

```bash
flutter doctor
```

确保所有必需项都是✓状态。

## macOS 开发环境设置

### 1. 安装Flutter SDK

```bash
git clone https://github.com/flutter/flutter.git -b stable
export PATH="$PATH:`pwd`/flutter/bin"
```

### 2. 安装Xcode

```bash
xcode-select --install
```

### 3. 验证环境

```bash
flutter doctor
```

## 项目配置

### 1. 克隆或进入项目目录

```bash
cd flutter_project
```

### 2. 获取依赖

```bash
flutter pub get
```

### 3. 生成必要的代码

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

### 4. 检查应用配置

**android/app/build.gradle**
```gradle
android {
    compileSdkVersion 34  // 使用最新的SDK版本
    
    defaultConfig {
        minSdkVersion 21   // 最低支持API 21
        targetSdkVersion 34 // 目标SDK版本
    }
}
```

**ios/Podfile**
```ruby
platform :ios, '12.0'  # 最低支持iOS 12
```

## 运行应用

### 使用模拟器

**Android：**
```bash
# 启动Android模拟器
emulator -avd Pixel_3a  # 替换为你的AVD名称

# 或直接运行
flutter run -d android
```

**iOS：**
```bash
# 打开iOS模拟器
open -a Simulator

# 运行应用
flutter run -d ios
```

### 使用真机设备

**Android：**
1. 连接设备到电脑
2. 启用USB调试
3. 运行：`flutter run -d <device-id>`

**iOS：**
1. 连接设备到Mac
2. 信任开发者
3. 运行：`flutter run -d <device-id>`

## 常见问题解决

### 问题：`flutter: command not found`

**解决方案：**
1. 确保PATH环境变量正确设置
2. 重启终端或命令行
3. 运行 `echo $PATH` 检查Flutter路径是否包含

### 问题：`Android SDK is missing`

**解决方案：**
1. 运行 `flutter doctor --android-licenses`
2. 在Android Studio中手动配置SDK路径：
   - File → Settings → Appearance & Behavior → System Settings → Android SDK
   - 设置正确的SDK路径

### 问题：`Unable to locate a Java Runtime`

**解决方案：**
1. 安装JDK 11或更高版本
2. 设置JAVA_HOME环境变量
3. 验证：`java -version`

### 问题：iOS构建失败

**解决方案：**
```bash
cd ios
pod deintegrate
cd ..
flutter clean
flutter pub get
cd ios
pod install
cd ..
flutter run
```

### 问题：依赖冲突

**解决方案：**
```bash
flutter pub cache clean
flutter pub get
```

## 开发工作流

### 日常开发

1. **启动开发服务器**
   ```bash
   flutter run
   ```

2. **热重新加载**
   - 按 `r` 进行热重新加载（保留应用状态）
   - 按 `R` 进行完整重启
   - 按 `q` 退出

3. **调试**
   ```bash
   flutter run -v  # 详细模式
   ```

### 代码格式化

```bash
flutter format lib/
```

### 静态分析

```bash
flutter analyze
```

### 运行测试

```bash
flutter test
```

## 构建APK

### 调试APK

```bash
flutter build apk --debug
```

### 发布APK

```bash
# 生成单个APK
flutter build apk --release

# 分离架构的APK（更小）
flutter build apk --split-per-abi --release
```

APK文件将生成到：`build/app/outputs/apk/`

## 构建iOS应用

### 开发版本

```bash
flutter build ios --debug
```

### 发布版本

```bash
flutter build ios --release
```

使用Xcode打开生成的应用：
```bash
open ios/Runner.xcworkspace
```

## 配置选项

### 启用桌面支持（可选）

```bash
flutter config --enable-windows-desktop
flutter config --enable-macos-desktop
```

### 配置Flutter Channel

```bash
# 查看当前channel
flutter channel

# 切换到stable
flutter channel stable
flutter upgrade
```

## IDE配置

### VS Code

1. 安装扩展：
   - Flutter
   - Dart
   - Awesome Flutter Snippets

2. 创建 `.vscode/launch.json`：
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flutter",
            "type": "dart",
            "request": "launch",
            "program": "lib/main.dart"
        }
    ]
}
```

### Android Studio

1. 安装插件：
   - Flutter
   - Dart

2. 创建运行配置：
   - Run → Edit Configurations
   - 新增Flutter运行配置

## 性能测试

```bash
# 运行性能分析
flutter run --profile

# 生成性能报告
flutter run --trace-startup
```

## 资源

- [Flutter官方文档](https://flutter.dev/docs)
- [Dart官方文档](https://dart.dev/guides)
- [Flutter社区](https://flutter.dev/community)
- [StackOverflow - flutter标签](https://stackoverflow.com/questions/tagged/flutter)

## 下一步

1. 阅读 [README.md](README.md) 了解项目结构
2. 查看 [lib/main.dart](lib/main.dart) 了解应用入口
3. 查看 [lib/theme/design_system.dart](lib/theme/design_system.dart) 了解设计系统
4. 开始开发！

## 获取帮助

遇到问题？尝试以下步骤：

1. 运行 `flutter clean` 清理构建
2. 运行 `flutter pub get` 重新获取依赖
3. 运行 `flutter doctor` 检查环境
4. 查看[Flutter FAQ](https://flutter.dev/docs/resources/faq)
5. 在GitHub提交Issue
