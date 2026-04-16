# 视频总结器移动端应用 - React Native 实现指南

## 📱 项目概述

这是一个为 iOS 和 Android 平台开发的视频总结器移动应用，采用 React Native 技术，包含完整的UI设计和多屏幕交互流程。

### 核心特性
- ✅ 5个完整的应用屏幕
- ✅ 底部导航栏（Pill风格）
- ✅ 实时进度显示
- ✅ 文件上传功能
- ✅ 时间旅行追问系统
- ✅ 完整的API集成点

## 🏗️ 项目结构

```
pencil/
├── App.js                          # 主应用入口 + 设计系统常量
├── package.json                    # 项目依赖配置
├── screens/
│   ├── SettingsScreen.js          # 配置屏幕 ⚙️
│   ├── VideoSelectionScreen.js    # 视频选择屏幕 🎬
│   ├── ProcessingProgressScreen.js# 处理进度屏幕 ⏳
│   ├── SummaryResultScreen.js     # 总结结果屏幕 📝
│   └── TimeTravelQAScreen.js      # 时间旅行追问屏幕 🔎
├── VideoSummarizerApp.md          # 设计文档（Pencil）
├── SETUP.md                       # 本文件
└── app.json                       # Expo配置（需自行创建）
```

## 🚀 快速开始

### 前置要求
- Node.js 16+ 和 npm
- Expo CLI (`npm install -g expo-cli`)
- iOS 开发工具（对 iOS）
- Android Studio（对 Android）

### 安装步骤

1. **克隆/创建项目**
   ```bash
   cd c:/Users/36076/Desktop/video_summarizer/pencil
   npm install
   ```

2. **安装依赖**
   ```bash
   npm install
   ```

3. **创建 `app.json` 文件**
   ```json
   {
     "expo": {
       "name": "Video Summarizer",
       "slug": "video-summarizer",
       "version": "1.0.0",
       "assetBundlePatterns": [
         "**/*"
       ],
       "ios": {
         "supportsTabletMode": true
       },
       "android": {
         "adaptiveIcon": {
           "foregroundImage": "./assets/adaptive-icon.png",
           "backgroundColor": "#FFFFFF"
         }
       },
       "plugins": [
         [
           "expo-document-picker",
           {
             "iCloudContainerEnvironment": "Production"
           }
         ]
       ]
     }
   }
   ```

4. **启动开发服务器**
   ```bash
   expo start
   ```

5. **在设备上运行**
   - **iOS**: 按 `i` 或使用 iOS Simulator
   - **Android**: 按 `a` 或使用 Android Emulator
   - **Web**: 按 `w`

## 📱 屏幕详情

### 1️⃣ Settings Screen (配置屏幕)
**路径**: `screens/SettingsScreen.js`

**功能**:
- OpenAI API Key 输入（密码字段）
- Base URL 配置
- 总结偏好文本区
- 并行模式选择（ThreadPool / Send API）

**主要组件**:
- `TextInput` - API 密钥和 URL 输入
- `TouchableOpacity` - 模式选择按钮
- 滚动内容区域

**集成建议**:
```javascript
// 连接到后端服务
import { VideoSummaryService } from '../services/workflow_service';

const handleProcessVideo = async () => {
  const service = new VideoSummaryService({
    apiKey,
    baseUrl,
    concurrencyMode: selectedMode,
  });
  // 处理视频...
};
```

---

### 2️⃣ Video Selection Screen (视频选择屏幕)
**路径**: `screens/VideoSelectionScreen.js`

**功能**:
- YouTube URL 输入
- 本地视频文件上传
- 拖拽上传区域
- 来源切换

**主要组件**:
- `TextInput` - URL 输入
- `DocumentPicker` - 文件选择
- `TouchableOpacity` - 来源切换和下一步按钮

**集成建议**:
```javascript
// 使用 DocumentPicker 选择视频
import * as DocumentPicker from 'react-native-document-picker';

const handleFileSelect = async () => {
  const result = await DocumentPicker.pick({
    type: [DocumentPicker.types.video],
    copyTo: 'cachesDirectory',
  });
  // 上传文件...
};
```

---

### 3️⃣ Processing Progress Screen (处理进度屏幕)
**路径**: `screens/ProcessingProgressScreen.js`

**功能**:
- 实时总体进度显示
- 音频分析进度
- 视觉分析进度
- 融合综合进度
- 处理日志消息

**主要组件**:
- 进度条组件（带 `Animated` API）
- 进度卡片（音频✓视觉✓融合）
- 状态消息列表

**集成建议**:
```javascript
// 接收实时进度更新
const updateProgress = (progressData) => {
  setProgress({
    overall: progressData.overall_percent,
    audio: progressData.audio_done / progressData.total_chunks * 100,
    vision: progressData.vision_done / progressData.total_chunks * 100,
    fusion: progressData.synthesis_done / progressData.total_chunks * 100,
  });
};

// 从 WebSocket 或 EventSource 订阅进度
useEffect(() => {
  const eventSource = new EventSource(`/api/progress/${threadId}`);
  eventSource.onmessage = (e) => {
    const data = JSON.parse(e.data);
    updateProgress(data);
  };
  return () => eventSource.close();
}, [threadId]);
```

---

### 4️⃣ Summary Result Screen (总结结果屏幕)
**路径**: `screens/SummaryResultScreen.js`

**功能**:
- 总结内容展示（可滚动）
- 复制全文功能
- 分享报告功能
- 元数据显示（时间、耗时等）

**主要组件**:
- `ScrollView` - 内容滚动区
- 总结卡片（核心要点、音频摘要、视觉亮点）
- `Share` API - 分享功能
- `Clipboard` - 复制功能

**集成建议**:
```javascript
// 从后端获取总结
useEffect(() => {
  const fetchSummary = async () => {
    const response = await fetch(`/api/summary/${threadId}`);
    const data = await response.json();
    setSummaryContent(data.content);
    setMetadata(data.metadata);
  };
  fetchSummary();
}, [threadId]);

// 实现复制功能
const handleCopyText = async () => {
  await Clipboard.setString(summaryContent);
  setCopied(true);
  setTimeout(() => setCopied(false), 2000);
};

// 实现分享功能
const handleShare = async () => {
  try {
    await Share.share({
      message: summaryContent,
      title: '视频分析报告',
    });
  } catch (error) {
    console.error('Share failed:', error);
  }
};
```

---

### 5️⃣ Time Travel Q&A Screen (时间旅行追问屏幕)
**路径**: `screens/TimeTravelQAScreen.js`

**功能**:
- 时间戳输入（MM:SS 格式）
- 证据窗口滑块调节（5-60秒）
- 追问问题输入
- 结果显示及时间范围引用

**主要组件**:
- `TextInput` - 时间戳输入
- `Slider` - 窗口大小调节
- 追问问题输入区
- 结果卡片（黄色背景）

**集成建议**:
```javascript
// 调用时间旅行追问 API
const handleAsk = async () => {
  setLoading(true);
  try {
    const response = await fetch('/api/time-travel-qa', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        thread_id: activeThreadId,
        timestamp,
        question,
        window_seconds: windowSize,
      }),
    });
    const data = await response.json();
    setAnswer(data.answer);
  } finally {
    setLoading(false);
  }
};
```

---

## 🎨 设计系统

所有屏幕共享统一的设计系统，定义在 `App.js` 中：

### 颜色系统
```javascript
COLORS = {
  primary: '#0066FF',           // 主色调（蓝色）
  background: '#F5F5F5',        // 背景色
  white: '#FFFFFF',             // 白色
  textPrimary: '#1A1A1A',       // 主文本
  textSecondary: '#666666',     // 次文本
  textTertiary: '#999999',      // 弱文本
  border: '#DDDDDD',            // 边框
  lightBg: '#F9F9F9',           // 轻背景
  highlightBg: '#F0F7FF',       // 强调背景
  warningBg: '#FFF8E1',         // 警告背景
}
```

### 字体系统
```javascript
FONTS = {
  title: { fontSize: 24, fontWeight: '700' },
  subtitle: { fontSize: 12, fontWeight: '400' },
  label: { fontSize: 13, fontWeight: '600' },
  body: { fontSize: 12, fontWeight: '400' },
  tabLabel: { fontSize: 10, fontWeight: '600' },
  caption: { fontSize: 11, fontWeight: '500' },
}
```

### 间距系统
```javascript
SPACING = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  xxl: 24,
}
```

### 圆角系统
```javascript
BORDER_RADIUS = {
  small: 4,
  medium: 8,
  large: 12,
  pill: 26,
  full: 36,
}
```

## 🔗 后端API集成

### 必需的 API 端点

```
1. POST /api/config
   - 保存 API Key 和 Base URL 配置

2. POST /api/process-video
   Body: {
     source_type: 'youtube' | 'local',
     video_url?: string,
     file_path?: string,
     user_prompt?: string,
     concurrency_mode: 'threadpool' | 'send_api'
   }
   Returns: { thread_id: string }

3. GET /api/progress/{thread_id}
   - WebSocket 或 EventSource 流式返回进度数据
   Returns: {
     overall_percent: number,
     audio_done: number,
     vision_done: number,
     synthesis_done: number,
     total_chunks: number
   }

4. GET /api/summary/{thread_id}
   Returns: {
     content: string,
     metadata: {
       generated_at: timestamp,
       processing_time: seconds,
       video_duration: string
     }
   }

5. POST /api/time-travel-qa
   Body: {
     thread_id: string,
     timestamp: string,
     question: string,
     window_seconds: number
   }
   Returns: { answer: string }
```

## 🚨 已知限制

1. **本地文件上传**: 需要用户授予文件访问权限
2. **进度更新**: 模拟数据需替换为真实的后端实现
3. **时间格式**: 暂时支持 MM:SS 格式，需要支持 HH:MM:SS
4. **离线支持**: 当前版本不支持离线使用
5. **国际化**: 暂仅支持中文/英文

## 🔒 安全建议

1. **API Key 存储**: 使用 `react-native-secure-storage` 加密存储
   ```bash
   npm install react-native-secure-storage
   ```

2. **HTTPS 通信**: 所有 API 调用应使用 HTTPS

3. **Token 刷新**: 实现 JWT Token 自动刷新机制

4. **权限管理**: 
   - iOS: 在 `ios/Podfile` 中配置权限
   - Android: 在 `AndroidManifest.xml` 中声明权限

## 📦 部署指南

### iOS 部署
```bash
# 生成 iOS 构建
eas build --platform ios

# 提交到 App Store
eas submit --platform ios
```

### Android 部署
```bash
# 生成 Android APK
eas build --platform android

# 上传到 Google Play
eas submit --platform android
```

## 🐛 故障排除

| 问题 | 解决方案 |
|------|--------|
| `Module not found` | 运行 `npm install` 并重启开发服务器 |
| 视频播放错误 | 检查视频格式支持（mp4、mov、avi、mkv） |
| 进度条不更新 | 检查后端 EventSource/WebSocket 连接 |
| 导航栏不显示 | 确保所有屏幕都在 TabNavigator 中注册 |
| 文件上传失败 | 检查文件权限和大小限制 |

## 📚 参考资源

- [React Native 文档](https://reactnative.dev/)
- [React Navigation 文档](https://reactnavigation.org/)
- [Expo 文档](https://docs.expo.dev/)
- [原设计文件](./VideoSummarizerApp.md)

## 👥 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**最后更新**: 2024-01-15
