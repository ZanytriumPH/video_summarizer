/// Summary Result Screen - 总结结果屏幕
/// 功能：展示完整的视频分析总结报告
library summary_result_screen;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../theme/design_system.dart';
import '../../providers/app_state_provider.dart';

class SummaryResultScreen extends StatefulWidget {
  const SummaryResultScreen({Key? key}) : super(key: key);

  @override
  State<SummaryResultScreen> createState() => _SummaryResultScreenState();
}

class _SummaryResultScreenState extends State<SummaryResultScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Consumer<AppStateProvider>(
        builder: (context, appState, _) {
          final summary = appState.summaryResult;
          
          if (summary == null) {
            return SafeArea(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      '📝 暂无总结结果',
                      style: AppFonts.title.copyWith(
                        color: AppColors.textSecondary,
                      ),
                    ),
                    const SizedBox(height: AppSpacing.md),
                    Text(
                      '请先处理视频',
                      style: AppFonts.subtitle.copyWith(
                        color: AppColors.textTertiary,
                      ),
                    ),
                  ],
                ),
              ),
            );
          }

          return SafeArea(
            child: Column(
              children: [
                Expanded(
                  child: SingleChildScrollView(
                    padding: const EdgeInsets.all(AppSpacing.screenPaddingHorizontal),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Header
                        SizedBox(height: AppSpacing.lg),
                        Text(
                          '总结结果',
                          style: AppFonts.title.copyWith(
                            color: AppColors.textPrimary,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          '完整的分析报告',
                          style: AppFonts.subtitle.copyWith(
                            color: AppColors.textSecondary,
                          ),
                        ),
                        const SizedBox(height: AppSpacing.xl),

                        // Title
                        Text(
                          summary.title,
                          style: AppFonts.title.copyWith(
                            color: AppColors.textPrimary,
                          ),
                        ),
                        const SizedBox(height: AppSpacing.lg),

                        // Key Points Section
                        _SectionCard(
                          icon: '🎯',
                          title: '核心要点',
                          items: summary.keyPoints,
                        ),
                        const SizedBox(height: AppSpacing.lg),

                        // Audio Summary Section
                        _SectionCard(
                          icon: '🎵',
                          title: '音频摘要',
                          items: [summary.audioSummary],
                        ),
                        const SizedBox(height: AppSpacing.lg),

                        // Visual Highlights Section
                        _SectionCard(
                          icon: '👁️',
                          title: '视觉亮点',
                          items: [summary.visualHighlights],
                        ),
                        const SizedBox(height: AppSpacing.lg),

                        // Full Content
                        Container(
                          padding: const EdgeInsets.all(AppSpacing.lg),
                          decoration: BoxDecoration(
                            color: AppColors.white,
                            borderRadius: BorderRadius.circular(AppBorderRadius.large),
                            border: Border.all(color: AppColors.border),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                '📄 完整内容',
                                style: AppFonts.label.copyWith(
                                  color: AppColors.textPrimary,
                                ),
                              ),
                              const SizedBox(height: AppSpacing.md),
                              Text(
                                summary.content,
                                style: AppFonts.body.copyWith(
                                  color: AppColors.textSecondary,
                                  height: 1.6,
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(height: AppSpacing.xl),

                        // Created at
                        Text(
                          '生成时间: ${summary.createdAt.toString().split('.')[0]}',
                          style: AppFonts.caption.copyWith(
                            color: AppColors.textTertiary,
                          ),
                        ),
                        const SizedBox(height: AppSpacing.xl),
                      ],
                    ),
                  ),
                ),

                // Action Buttons
                Padding(
                  padding: const EdgeInsets.all(AppSpacing.screenPaddingHorizontal),
                  child: Row(
                    children: [
                      Expanded(
                        child: ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppColors.primary,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(
                                AppBorderRadius.medium,
                              ),
                            ),
                            padding: const EdgeInsets.symmetric(
                              vertical: AppSpacing.md,
                            ),
                          ),
                          onPressed: () {
                            // Copy to clipboard
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text('已复制到剪贴板'),
                                duration: Duration(seconds: 2),
                              ),
                            );
                          },
                          child: Text(
                            '复制全文',
                            style: AppFonts.label.copyWith(
                              color: AppColors.white,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: AppSpacing.md),
                      Expanded(
                        child: OutlinedButton(
                          style: OutlinedButton.styleFrom(
                            side: const BorderSide(color: AppColors.primary),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(
                                AppBorderRadius.medium,
                              ),
                            ),
                            padding: const EdgeInsets.symmetric(
                              vertical: AppSpacing.md,
                            ),
                          ),
                          onPressed: () {
                            // Share
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text('分享功能开发中...'),
                                duration: Duration(seconds: 2),
                              ),
                            );
                          },
                          child: Text(
                            '分享报告',
                            style: AppFonts.label.copyWith(
                              color: AppColors.primary,
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: AppSpacing.md),
              ],
            ),
          );
        },
      ),
    );
  }
}

class _SectionCard extends StatelessWidget {
  final String icon;
  final String title;
  final List<String> items;

  const _SectionCard({
    required this.icon,
    required this.title,
    required this.items,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.lg),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(AppBorderRadius.large),
        border: Border.all(color: AppColors.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '$icon $title',
            style: AppFonts.label.copyWith(
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: AppSpacing.md),
          ...items.asMap().entries.map((entry) {
            int idx = entry.key;
            String item = entry.value;
            return Padding(
              padding: EdgeInsets.only(
                bottom: idx < items.length - 1 ? AppSpacing.md : 0,
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Padding(
                    padding: const EdgeInsets.only(
                      top: 4,
                      right: AppSpacing.md,
                    ),
                    child: Text(
                      '•',
                      style: AppFonts.body.copyWith(
                        color: AppColors.primary,
                      ),
                    ),
                  ),
                  Expanded(
                    child: Text(
                      item,
                      style: AppFonts.body.copyWith(
                        color: AppColors.textSecondary,
                        height: 1.5,
                      ),
                    ),
                  ),
                ],
              ),
            );
          }).toList(),
        ],
      ),
    );
  }
}
