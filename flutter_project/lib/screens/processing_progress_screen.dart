/// Processing Progress Screen - 处理进度屏幕
/// 功能：实时显示视频多模态分析的进度
library processing_progress_screen;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../theme/design_system.dart';
import '../../providers/app_state_provider.dart';

class ProcessingProgressScreen extends StatefulWidget {
  const ProcessingProgressScreen({Key? key}) : super(key: key);

  @override
  State<ProcessingProgressScreen> createState() => _ProcessingProgressScreenState();
}

class _ProcessingProgressScreenState extends State<ProcessingProgressScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Consumer<AppStateProvider>(
        builder: (context, appState, _) => SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(AppSpacing.screenPaddingHorizontal),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header
                SizedBox(height: AppSpacing.lg),
                Text(
                  '处理中...',
                  style: AppFonts.title.copyWith(
                    color: AppColors.textPrimary,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  '正在分析视频内容',
                  style: AppFonts.subtitle.copyWith(
                    color: AppColors.textSecondary,
                  ),
                ),
                const SizedBox(height: AppSpacing.xl),

                // Overall Progress Card
                _ProgressCard(
                  title: '整体进度',
                  icon: '📊',
                  progress: appState.progress.overall,
                  subtitle: '${appState.progress.overall.toStringAsFixed(0)}% 已完成',
                ),
                const SizedBox(height: AppSpacing.lg),

                // Audio Analysis
                _ProgressCard(
                  title: '🎵 音频分析',
                  icon: '',
                  progress: appState.progress.audio,
                  subtitle: '${appState.progress.audio.toStringAsFixed(0)}/100 已完成',
                ),
                const SizedBox(height: AppSpacing.lg),

                // Vision Analysis
                _ProgressCard(
                  title: '👁️ 视觉分析',
                  icon: '',
                  progress: appState.progress.vision,
                  subtitle: '${appState.progress.vision.toStringAsFixed(0)}/100 已完成',
                ),
                const SizedBox(height: AppSpacing.lg),

                // Fusion Analysis
                _ProgressCard(
                  title: '🔗 融合综合',
                  icon: '',
                  progress: appState.progress.fusion,
                  subtitle: '${appState.progress.fusion.toStringAsFixed(0)}/100 已完成',
                ),
                const SizedBox(height: AppSpacing.xl),

                // Status Info
                Container(
                  padding: const EdgeInsets.all(AppSpacing.md),
                  decoration: BoxDecoration(
                    color: AppColors.highlightBg,
                    borderRadius: BorderRadius.circular(AppBorderRadius.medium),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '处理信息',
                        style: AppFonts.label.copyWith(
                          color: AppColors.textPrimary,
                        ),
                      ),
                      const SizedBox(height: AppSpacing.md),
                      Text(
                        '总分块数: ${appState.progress.totalChunks}',
                        style: AppFonts.body.copyWith(
                          color: AppColors.textSecondary,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        '状态: ${appState.isProcessing ? '处理中' : '已完成'}',
                        style: AppFonts.body.copyWith(
                          color: appState.isProcessing 
                              ? AppColors.warning 
                              : AppColors.primary,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: AppSpacing.xl),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _ProgressCard extends StatelessWidget {
  final String title;
  final String icon;
  final double progress;
  final String subtitle;

  const _ProgressCard({
    required this.title,
    required this.icon,
    required this.progress,
    required this.subtitle,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.lg),
      decoration: BoxDecoration(
        color: AppColors.white,
        borderRadius: BorderRadius.circular(AppBorderRadius.large),
        border: Border.all(
          color: AppColors.border,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              if (icon.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.only(right: AppSpacing.md),
                  child: Text(
                    icon,
                    style: const TextStyle(fontSize: 18),
                  ),
                ),
              Expanded(
                child: Text(
                  title,
                  style: AppFonts.label.copyWith(
                    color: AppColors.textPrimary,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.md),
          Text(
            subtitle,
            style: AppFonts.caption.copyWith(
              color: AppColors.primary,
            ),
          ),
          const SizedBox(height: AppSpacing.md),
          // Progress bar
          ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: LinearProgressIndicator(
              value: progress / 100,
              minHeight: 6,
              backgroundColor: AppColors.border,
              valueColor: AlwaysStoppedAnimation<Color>(
                AppColors.primary.withOpacity(0.8),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
