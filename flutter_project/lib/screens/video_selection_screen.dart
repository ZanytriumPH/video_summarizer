/// Video Selection Screen - 视频选择屏幕
/// 功能：选择视频源（YouTube URL或本地上传）
library video_selection_screen;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:file_picker/file_picker.dart';
import '../../theme/design_system.dart';
import '../../models/models.dart';
import '../../providers/app_state_provider.dart';

class VideoSelectionScreen extends StatefulWidget {
  const VideoSelectionScreen({Key? key}) : super(key: key);

  @override
  State<VideoSelectionScreen> createState() => _VideoSelectionScreenState();
}

class _VideoSelectionScreenState extends State<VideoSelectionScreen> {
  late TextEditingController _urlController;
  VideoSourceType _sourceType = VideoSourceType.youtube;
  String? _selectedFileName;

  @override
  void initState() {
    super.initState();
    _urlController = TextEditingController();
  }

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  Future<void> _pickFile() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.video,
      );

      if (result != null) {
        setState(() {
          _selectedFileName = result.files.single.name;
        });
      }
    } catch (e) {
      print('Error picking file: $e');
    }
  }

  bool _isValid() {
    if (_sourceType == VideoSourceType.youtube) {
      return _urlController.text.isNotEmpty;
    } else {
      return _selectedFileName != null;
    }
  }

  void _handleNext() {
    if (!_isValid()) return;

    final appState = context.read<AppStateProvider>();
    
    if (_sourceType == VideoSourceType.youtube) {
      appState.setSelectedVideo(
        VideoSource(
          type: VideoSourceType.youtube,
          url: _urlController.text,
        ),
      );
    } else {
      appState.setSelectedVideo(
        VideoSource(
          type: VideoSourceType.local,
          url: _selectedFileName ?? '',
          fileName: _selectedFileName,
        ),
      );
    }

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
                '选择视频源',
                style: AppFonts.title.copyWith(
                  color: AppColors.textPrimary,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                '上传本地或输入URL',
                style: AppFonts.subtitle.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),
              const SizedBox(height: AppSpacing.xl),

              // YouTube Option
              _SourceOption(
                icon: '🌐',
                title: 'YouTube URL',
                subtitle: '输入视频链接',
                isSelected: _sourceType == VideoSourceType.youtube,
                onTap: () {
                  setState(() {
                    _sourceType = VideoSourceType.youtube;
                  });
                },
                child: _sourceType == VideoSourceType.youtube
                    ? Column(
                        children: [
                          const SizedBox(height: AppSpacing.lg),
                          TextField(
                            controller: _urlController,
                            decoration: InputDecoration(
                              hintText: 'https://youtube.com/watch?v=...',
                              hintStyle: AppFonts.body.copyWith(
                                color: AppColors.textTertiary,
                              ),
                            ),
                          ),
                        ],
                      )
                    : null,
              ),
              const SizedBox(height: AppSpacing.lg),

              // Local Upload Option
              _SourceOption(
                icon: '📤',
                title: '本地上传',
                subtitle: '点击选择文件',
                isSelected: _sourceType == VideoSourceType.local,
                onTap: () {
                  setState(() {
                    _sourceType = VideoSourceType.local;
                  });
                },
                child: _sourceType == VideoSourceType.local
                    ? Column(
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
                                  style: BorderStyle.solid,
                                ),
                                borderRadius: BorderRadius.circular(
                                  AppBorderRadius.medium,
                                ),
                              ),
                              child: Center(
                                child: Text(
                                  '+ 点击或拖拽视频',
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
                      )
                    : null,
              ),
              const SizedBox(height: AppSpacing.xl),

              // Next Button
              SizedBox(
                width: double.infinity,
                height: 44,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    disabledBackgroundColor: AppColors.primary.withOpacity(0.5),
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
  final bool isSelected;
  final VoidCallback onTap;
  final Widget? child;

  const _SourceOption({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.isSelected,
    required this.onTap,
    this.child,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(AppSpacing.lg),
        decoration: BoxDecoration(
          border: Border.all(
            color: isSelected ? AppColors.primary : AppColors.border,
            width: isSelected ? 2 : 1,
          ),
          borderRadius: BorderRadius.circular(AppBorderRadius.medium),
          color: isSelected ? AppColors.highlightBg : AppColors.white,
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
            if (child != null) child!,
          ],
        ),
      ),
    );
  }
}
