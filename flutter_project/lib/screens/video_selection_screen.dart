/// Video Selection Screen - 视频选择屏幕
/// 功能：选择本地视频并开始总结
library video_selection_screen;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:file_picker/file_picker.dart';
import '../../theme/design_system.dart';
import '../../models/models.dart';
import '../../providers/app_state_provider.dart';

class VideoSelectionScreen extends StatefulWidget {
  const VideoSelectionScreen({super.key});

  @override
  State<VideoSelectionScreen> createState() => _VideoSelectionScreenState();
}

class _VideoSelectionScreenState extends State<VideoSelectionScreen> {
  String? _selectedFileName;
  String? _selectedFilePath;

  Future<void> _pickFile() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.video,
      );

      if (result != null) {
        setState(() {
          _selectedFileName = result.files.single.name;
          _selectedFilePath = result.files.single.path;
        });
      }
    } on Exception catch (e) {
      debugPrint('Error picking file: $e');
    }
  }

  bool _isValid() {
    return _selectedFileName != null;
  }

  void _handleNext() {
    if (!_isValid()) return;

    final appState = context.read<AppStateProvider>();

    appState.setSelectedVideo(
      VideoSource(
        fileName: _selectedFileName!,
        filePath: _selectedFilePath,
      ),
    );

    // 开始进度模拟
    appState.simulateProgress();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.screenPaddingHorizontal),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header
              SizedBox(height: AppSpacing.lg),
              Text(
                '选择本地视频',
                style: AppFonts.title.copyWith(
                  color: AppColors.textPrimary,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                '上传本地视频进行总结',
                style: AppFonts.subtitle.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),
              const SizedBox(height: AppSpacing.xl),

              // Local Upload Option
              _SourceOption(
                icon: '📤',
                title: '本地上传',
                subtitle: '点击选择文件',
                child: Column(
                  children: [
                    const SizedBox(height: AppSpacing.lg),
                    GestureDetector(
                      onTap: _pickFile,
                      child: Container(
                        padding: const EdgeInsets.symmetric(
                          vertical: AppSpacing.lg,
                        ),
                        decoration: BoxDecoration(
                          border: Border.all(
                            color: AppColors.border,
                          ),
                          borderRadius: BorderRadius.circular(
                            AppBorderRadius.medium,
                          ),
                        ),
                        child: Center(
                          child: Text(
                            '+ 点击选择视频',
                            style: AppFonts.body.copyWith(
                              color: AppColors.textTertiary,
                            ),
                          ),
                        ),
                      ),
                    ),
                    if (_selectedFileName != null)
                      Padding(
                        padding: const EdgeInsets.only(top: AppSpacing.md),
                        child: Text(
                          '✓ 已选择: $_selectedFileName',
                          style: AppFonts.caption.copyWith(
                            color: AppColors.primary,
                          ),
                        ),
                      ),
                  ],
                ),
              ),
              const SizedBox(height: AppSpacing.xl),

              // Next Button
              SizedBox(
                width: double.infinity,
                height: 44,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    disabledBackgroundColor: AppColors.primary.withValues(
                      alpha: 0.5,
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(AppBorderRadius.medium),
                    ),
                  ),
                  onPressed: _isValid() ? _handleNext : null,
                  child: Text(
                    '下一步',
                    style: AppFonts.label.copyWith(
                      color: AppColors.white,
                    ),
                  ),
                ),
              ),
              const SizedBox(height: AppSpacing.xl),
            ],
          ),
        ),
      ),
    );
  }
}

class _SourceOption extends StatelessWidget {
  final String icon;
  final String title;
  final String subtitle;
  final Widget child;

  const _SourceOption({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.lg),
      decoration: BoxDecoration(
        border: Border.all(
          color: AppColors.primary,
          width: 2,
        ),
        borderRadius: BorderRadius.circular(AppBorderRadius.medium),
        color: AppColors.highlightBg,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(
                icon,
                style: const TextStyle(fontSize: 20),
              ),
              const SizedBox(width: AppSpacing.md),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: AppFonts.label.copyWith(
                        color: AppColors.primary,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      subtitle,
                      style: AppFonts.subtitle.copyWith(
                        color: AppColors.textSecondary,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          child,
        ],
      ),
    );
  }
}
