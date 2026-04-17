/// 主应用入口
/// Flutter 视频总结器应用
/// 支持 iOS 和 Android 平台

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'theme/design_system.dart';
import 'providers/app_state_provider.dart';
import 'screens/settings_screen.dart';
import 'screens/video_selection_screen.dart';
import 'screens/processing_progress_screen.dart';
import 'screens/summary_result_screen.dart';
import 'screens/time_travel_qa_screen.dart';

/// 应用程序入口函数
/// Flutter 应用从这里开始执行
void main() {
  // runApp() 是 Flutter 应用的起点，它会将给定的 widget 连接到屏幕上
  runApp(const MyApp());
}

/// 应用根 Widget
/// 负责配置全局状态管理和主题
/// 
/// 使用 StatelessWidget 因为此组件本身不需要维护状态
class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // ChangeNotifierProvider: Provider 包提供的状态管理组件
    // 它会在整个应用树中提供 AppStateProvider 实例
    return ChangeNotifierProvider(
      // create: 当 Provider 首次被需要时，创建 AppStateProvider 实例
      create: (_) => AppStateProvider(),
      // child: MaterialApp 是 Flutter 应用的核心组件，提供 Material Design 风格
      child: MaterialApp(
        title: 'Video Summarizer', // 应用标题（用于任务切换器等）
        theme: AppTheme.light, // 应用主题（从 design_system.dart 导入）
        home: const MainApp(), // 应用的主页面
        debugShowCheckedModeBanner: false, // 隐藏右上角的 DEBUG 标签
      ),
    );
  }
}

/// 主应用框架 Widget
/// 管理底部导航栏和屏幕切换
/// 
/// 使用 StatefulWidget 因为需要维护当前选中的导航索引状态
class MainApp extends StatefulWidget {
  const MainApp({Key? key}) : super(key: key);

  @override
  State<MainApp> createState() => _MainAppState();
}

/// MainApp 的状态类
/// 管理当前选中的导航项索引
class _MainAppState extends State<MainApp> {
  // 当前选中的导航项索引（0-4）
  int _currentIndex = 0;

  // 导航项列表：定义5个屏幕及其对应的图标和标签
  final List<_NavItem> _navItems = [
    _NavItem(
      label: 'SETTINGS', // 设置
      icon: '⚙️',
      screen: const SettingsScreen(), // 配置屏幕
    ),
    _NavItem(
      label: 'VIDEO', // 视频选择
      icon: '🎬',
      screen: const VideoSelectionScreen(), // 视频选择屏幕
    ),
    _NavItem(
      label: 'PROGRESS', // 处理进度
      icon: '⏳',
      screen: const ProcessingProgressScreen(), // 进度显示屏幕
    ),
    _NavItem(
      label: 'SUMMARY', // 总结结果
      icon: '📝',
      screen: const SummaryResultScreen(), // 结果展示屏幕
    ),
    _NavItem(
      label: 'Q&A', // 时间旅行问答
      icon: '🔎',
      screen: const TimeTravelQAScreen(), // 问答屏幕
    ),
  ];

  @override
  Widget build(BuildContext context) {
    // Scaffold 是 Material Design 的基本布局结构
    return Scaffold(
      backgroundColor: AppColors.background, // 背景色（从设计系统获取）
      // body: 显示当前选中的屏幕
      body: _navItems[_currentIndex].screen,
      // bottomNavigationBar: 自定义底部导航栏
      bottomNavigationBar: _BottomNavBar(
        items: _navItems, // 传递导航项列表
        currentIndex: _currentIndex, // 当前选中项的索引
        // onTap: 点击导航项时的回调函数
        onTap: (index) {
          // setState 通知 Flutter 状态已改变，需要重新构建 UI
          setState(() {
            _currentIndex = index; // 更新选中的索引
          });
        },
      ),
    );
  }
}

/// 导航项数据类
/// 封装每个导航项的标签、图标和对应的屏幕 Widget
/// 
/// 使用私有类（以下划线开头）表示仅在内部使用
class _NavItem {
  final String label; // 导航标签文本
  final String icon; // 导航图标（emoji）
  final Widget screen; // 对应的屏幕 Widget

  _NavItem({
    required this.label, // required 表示此参数必须提供
    required this.icon,
    required this.screen,
  });
}

/// 自定义底部导航栏组件
/// 实现圆角胶囊样式的导航栏
/// 
/// 使用 StatelessWidget 因为所有数据都通过构造函数传入
class _BottomNavBar extends StatelessWidget {
  final List<_NavItem> items; // 导航项列表
  final int currentIndex; // 当前选中的索引
  final Function(int) onTap; // 点击回调函数

  const _BottomNavBar({
    required this.items,
    required this.currentIndex,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    // 外层 Container：白色背景和顶部边框
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.lg, // 水平内边距
        vertical: AppSpacing.md, // 垂直内边距
      ),
      decoration: BoxDecoration(
        color: AppColors.white, // 白色背景
        border: Border(
          top: BorderSide(
            color: AppColors.border, // 顶部边框颜色
            width: 1, // 边框宽度
          ),
        ),
      ),
      // 内层 Container：圆角胶囊样式
      child: Container(
        padding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.md,
          vertical: AppSpacing.xs,
        ),
        decoration: BoxDecoration(
          color: AppColors.background, // 背景色
          borderRadius: BorderRadius.circular(AppBorderRadius.navContainer), // 圆角半径
          border: Border.all(
            color: AppColors.border, // 边框颜色
            width: 1,
          ),
        ),
        // Row: 横向排列导航项
        child: Row(
          // List.generate: 根据导航项数量生成对应数量的 Widget
          children: List.generate(
            items.length,
            (index) => Expanded( // Expanded: 让每个导航项平均分配空间
              child: GestureDetector(
                behavior: HitTestBehavior.opaque, // 确保整个区域都可点击
                onTap: () => onTap(index), // 点击时调用回调
                child: _NavItem_Widget(
                  icon: items[index].icon, // 传递图标
                  label: items[index].label, // 传递标签
                  isSelected: currentIndex == index, // 判断是否选中
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

/// 单个导航项 Widget
/// 显示图标和标签，并根据选中状态改变样式
/// 
/// 使用 AnimatedContainer 实现选中状态的平滑过渡动画
class _NavItem_Widget extends StatelessWidget {
  final String icon; // 图标
  final String label; // 标签文本
  final bool isSelected; // 是否处于选中状态

  const _NavItem_Widget({
    required this.icon,
    required this.label,
    required this.isSelected,
  });

  @override
  Widget build(BuildContext context) {
    // AnimatedContainer: 当属性改变时自动播放过渡动画
    return AnimatedContainer(
      duration: const Duration(milliseconds: 180), // 动画持续时间 180ms
      curve: Curves.easeOut, // 动画曲线（减速效果）
      width: double.infinity, // 占满父容器宽度
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.xs,
        vertical: AppSpacing.sm,
      ),
      decoration: BoxDecoration(
        // 选中时显示主色背景，未选中时透明
        color: isSelected ? AppColors.primary : Colors.transparent,
        borderRadius: BorderRadius.circular(AppBorderRadius.navItem), // 圆角
      ),
      // Column: 纵向排列图标和文字
      child: Column(
        mainAxisSize: MainAxisSize.min, // 最小化垂直空间
        crossAxisAlignment: CrossAxisAlignment.center, // 水平居中
        children: [
          // 图标文本（emoji）
          Text(
            icon,
            style: const TextStyle(fontSize: 16),
          ),
          const SizedBox(height: 2), // 间距
          // 标签文本
          Text(
            label,
            maxLines: 1, // 最多显示一行
            overflow: TextOverflow.ellipsis, // 超出部分显示省略号
            softWrap: false, // 不换行
            textAlign: TextAlign.center, // 文本居中
            // 选中时白色文字，未选中时使用辅助色
            style: AppFonts.tabLabel.copyWith(
              color: isSelected ? AppColors.white : AppColors.textTertiary,
            ),
          ),
        ],
      ),
    );
  }
}
