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

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => AppStateProvider(),
      child: MaterialApp(
        title: 'Video Summarizer',
        theme: AppTheme.light,
        home: const MainApp(),
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}

class MainApp extends StatefulWidget {
  const MainApp({Key? key}) : super(key: key);

  @override
  State<MainApp> createState() => _MainAppState();
}

class _MainAppState extends State<MainApp> {
  int _currentIndex = 0;

  final List<_NavItem> _navItems = [
    _NavItem(
      label: 'SETTINGS',
      icon: '⚙️',
      screen: const SettingsScreen(),
    ),
    _NavItem(
      label: 'VIDEO',
      icon: '🎬',
      screen: const VideoSelectionScreen(),
    ),
    _NavItem(
      label: 'PROGRESS',
      icon: '⏳',
      screen: const ProcessingProgressScreen(),
    ),
    _NavItem(
      label: 'SUMMARY',
      icon: '📝',
      screen: const SummaryResultScreen(),
    ),
    _NavItem(
      label: 'Q&A',
      icon: '🔎',
      screen: const TimeTravelQAScreen(),
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: _navItems[_currentIndex].screen,
      bottomNavigationBar: _BottomNavBar(
        items: _navItems,
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
      ),
    );
  }
}

class _NavItem {
  final String label;
  final String icon;
  final Widget screen;

  _NavItem({
    required this.label,
    required this.icon,
    required this.screen,
  });
}

class _BottomNavBar extends StatelessWidget {
  final List<_NavItem> items;
  final int currentIndex;
  final Function(int) onTap;

  const _BottomNavBar({
    required this.items,
    required this.currentIndex,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.lg,
        vertical: AppSpacing.md,
      ),
      decoration: BoxDecoration(
        color: AppColors.white,
        border: Border(
          top: BorderSide(
            color: AppColors.border,
            width: 1,
          ),
        ),
      ),
      child: Container(
        padding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.md,
          vertical: AppSpacing.xs,
        ),
        decoration: BoxDecoration(
          color: AppColors.background,
          borderRadius: BorderRadius.circular(AppBorderRadius.navContainer),
          border: Border.all(
            color: AppColors.border,
            width: 1,
          ),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: List.generate(
            items.length,
            (index) => GestureDetector(
              onTap: () => onTap(index),
              child: _NavItem_Widget(
                icon: items[index].icon,
                label: items[index].label,
                isSelected: currentIndex == index,
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _NavItem_Widget extends StatelessWidget {
  final String icon;
  final String label;
  final bool isSelected;

  const _NavItem_Widget({
    required this.icon,
    required this.label,
    required this.isSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.lg,
        vertical: AppSpacing.sm,
      ),
      decoration: BoxDecoration(
        color: isSelected ? AppColors.primary : Colors.transparent,
        borderRadius: BorderRadius.circular(AppBorderRadius.navItem),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            icon,
            style: const TextStyle(fontSize: 16),
          ),
          const SizedBox(height: 2),
          Text(
            label,
            style: AppFonts.tabLabel.copyWith(
              color: isSelected ? AppColors.white : AppColors.textTertiary,
            ),
          ),
        ],
      ),
    );
  }
}
