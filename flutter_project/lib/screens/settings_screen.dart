/// Settings Screen - 配置屏幕
/// 功能：配置API Key、Base URL、总结偏好和并行模式
library settings_screen;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../theme/design_system.dart';
import '../../models/models.dart';
import '../../providers/app_state_provider.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({Key? key}) : super(key: key);

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late TextEditingController _apiKeyController;
  late TextEditingController _baseUrlController;
  late TextEditingController _userPromptController;

  @override
  void initState() {
    super.initState();
    final appState = context.read<AppStateProvider>();
    _apiKeyController = TextEditingController(text: appState.config.apiKey);
    _baseUrlController = TextEditingController(text: appState.config.baseUrl);
    _userPromptController = TextEditingController(text: appState.config.userPrompt);
  }

  @override
  void dispose() {
    _apiKeyController.dispose();
    _baseUrlController.dispose();
    _userPromptController.dispose();
    super.dispose();
  }

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
                SizedBox(
                  height: AppSpacing.lg,
                ),
                Text(
                  'Video Summarizer',
                  style: AppFonts.title.copyWith(
                    color: AppColors.textPrimary,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  '多模态智能总结',
                  style: AppFonts.subtitle.copyWith(
                    color: AppColors.textSecondary,
                  ),
                ),
                const SizedBox(height: AppSpacing.xl),

                // API Configuration Section
                Text(
                  'API 配置',
                  style: AppFonts.label.copyWith(
                    color: AppColors.textPrimary,
                  ),
                ),
                const SizedBox(height: AppSpacing.md),

                // API Key Input
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'OpenAI API Key',
                      style: AppFonts.caption.copyWith(
                        color: AppColors.textSecondary,
                      ),
                    ),
                    const SizedBox(height: 4),
                    TextField(
                      controller: _apiKeyController,
                      obscureText: true,
                      decoration: InputDecoration(
                        hintText: 'sk-...',
                        hintStyle: AppFonts.body.copyWith(
                          color: AppColors.textTertiary,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: AppSpacing.lg),

                // Base URL Input
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Base URL',
                      style: AppFonts.caption.copyWith(
                        color: AppColors.textSecondary,
                      ),
                    ),
                    const SizedBox(height: 4),
                    TextField(
                      controller: _baseUrlController,
                      decoration: InputDecoration(
                        hintText: 'https://api.openai.com/v1',
                        hintStyle: AppFonts.body.copyWith(
                          color: AppColors.textTertiary,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: AppSpacing.xl),

                // Summary Preference Section
                Text(
                  '总结偏好',
                  style: AppFonts.label.copyWith(
                    color: AppColors.textPrimary,
                  ),
                ),
                const SizedBox(height: AppSpacing.md),

                TextField(
                  controller: _userPromptController,
                  maxLines: 4,
                  decoration: InputDecoration(
                    hintText: '请输入总结重点（可选）',
                    hintStyle: AppFonts.body.copyWith(
                      color: AppColors.textTertiary,
                    ),
                  ),
                ),
                const SizedBox(height: AppSpacing.xl),

                // Concurrency Mode Section
                Text(
                  '并行模式',
                  style: AppFonts.label.copyWith(
                    color: AppColors.textPrimary,
                  ),
                ),
                const SizedBox(height: AppSpacing.md),

                // ThreadPool Option
                _ModeOption(
                  label: '✓ ThreadPool (默认)',
                  isSelected: appState.config.concurrencyMode == ConcurrencyMode.threadPool,
                  onTap: () async {
                    await appState.setConcurrencyMode(ConcurrencyMode.threadPool);
                  },
                ),
                const SizedBox(height: AppSpacing.md),

                // Send API Option
                _ModeOption(
                  label: '○ Send API',
                  isSelected: appState.config.concurrencyMode == ConcurrencyMode.sendAPI,
                  onTap: () async {
                    await appState.setConcurrencyMode(ConcurrencyMode.sendAPI);
                  },
                ),
                const SizedBox(height: AppSpacing.xl),

                // Save Button
                SizedBox(
                  width: double.infinity,
                  height: 44,
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primary,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(AppBorderRadius.medium),
                      ),
                    ),
                    onPressed: () async {
                      await appState.saveApiConfig(
                        apiKey: _apiKeyController.text,
                        baseUrl: _baseUrlController.text,
                      );
                      await appState.saveUserPrompt(_userPromptController.text);
                      
                      if (mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('配置已保存'),
                            duration: Duration(seconds: 2),
                          ),
                        );
                      }
                    },
                    child: Text(
                      '保存配置',
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
      ),
    );
  }
}

class _ModeOption extends StatelessWidget {
  final String label;
  final bool isSelected;
  final VoidCallback onTap;

  const _ModeOption({
    required this.label,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(AppSpacing.md),
        decoration: BoxDecoration(
          border: Border.all(
            color: isSelected ? AppColors.primary : AppColors.border,
            width: isSelected ? 2 : 1,
          ),
          borderRadius: BorderRadius.circular(AppBorderRadius.medium),
          color: isSelected ? AppColors.highlightBg : AppColors.white,
        ),
        child: Text(
          label,
          style: AppFonts.body.copyWith(
            color: isSelected ? AppColors.primary : AppColors.textTertiary,
          ),
        ),
      ),
    );
  }
}
