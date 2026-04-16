/// 应用设计系统常量
/// 包含颜色、字体、间距等设计系统定义
library design_system;

import 'package:flutter/material.dart';

/// 颜色系统
class AppColors {
  // 主色
  static const Color primary = Color(0xFF0066FF);
  
  // 背景色
  static const Color background = Color(0xFFF5F5F5);
  static const Color lightBg = Color(0xFFF9F9F9);
  static const Color white = Color(0xFFFFFFFF);
  
  // 文本颜色
  static const Color textPrimary = Color(0xFF1A1A1A);
  static const Color textSecondary = Color(0xFF666666);
  static const Color textTertiary = Color(0xFF999999);
  
  // 边框和强调
  static const Color border = Color(0xFFDDDDDD);
  static const Color highlightBg = Color(0xFFF0F7FF);
  static const Color warningBg = Color(0xFFFFF8E1);
  static const Color warning = Color(0xFFF57C00);
}

/// 字体系统
class AppFonts {
  static const String fontFamily = 'Roboto';
  
  // 标题：24px, fontWeight: 700
  static const TextStyle title = TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.w700,
    fontFamily: fontFamily,
  );
  
  // 副标题：12px, fontWeight: 400
  static const TextStyle subtitle = TextStyle(
    fontSize: 12,
    fontWeight: FontWeight.w400,
    fontFamily: fontFamily,
  );
  
  // 标签：13px, fontWeight: 600
  static const TextStyle label = TextStyle(
    fontSize: 13,
    fontWeight: FontWeight.w600,
    fontFamily: fontFamily,
  );
  
  // 正文：12px, fontWeight: 400
  static const TextStyle body = TextStyle(
    fontSize: 12,
    fontWeight: FontWeight.w400,
    fontFamily: fontFamily,
  );
  
  // 底部导航标签：10px, fontWeight: 600
  static const TextStyle tabLabel = TextStyle(
    fontSize: 10,
    fontWeight: FontWeight.w600,
    fontFamily: fontFamily,
  );
  
  // 小标题：11px, fontWeight: 500
  static const TextStyle caption = TextStyle(
    fontSize: 11,
    fontWeight: FontWeight.w500,
    fontFamily: fontFamily,
  );
}

/// 间距系统
class AppSpacing {
  static const double xs = 4.0;
  static const double sm = 8.0;
  static const double md = 12.0;
  static const double lg = 16.0;
  static const double xl = 20.0;
  static const double xxl = 24.0;
  
  // 屏幕padding
  static const double screenPaddingHorizontal = 16.0;
  static const double screenPaddingVertical = 20.0;
  
  // 状态栏/导航栏高度
  static const double statusBarHeight = 62.0;
  static const double navBarHeight = 62.0;
}

/// 圆角系统
class AppBorderRadius {
  static const double large = 12.0;     // 卡片、主容器
  static const double medium = 8.0;     // 输入框、副容器
  static const double navContainer = 36.0;  // 导航栏外壳
  static const double navItem = 26.0;   // 导航项
}

/// 主题配置
class AppTheme {
  static ThemeData get light {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.light(
        primary: AppColors.primary,
        background: AppColors.background,
      ),
      scaffoldBackgroundColor: AppColors.background,
      appBarTheme: const AppBarTheme(
        backgroundColor: AppColors.white,
        elevation: 0,
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AppColors.white,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppBorderRadius.medium),
          borderSide: const BorderSide(color: AppColors.border),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppBorderRadius.medium),
          borderSide: const BorderSide(color: AppColors.border),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppBorderRadius.medium),
          borderSide: const BorderSide(color: AppColors.primary),
        ),
        contentPadding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.md,
          vertical: AppSpacing.md,
        ),
      ),
    );
  }
}
