/// Time Travel Q&A Screen - 时间旅行追问屏幕
/// 功能：按指定时间戳追问视频内容
library time_travel_qa_screen;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../theme/design_system.dart';
import '../../models/models.dart';
import '../../providers/app_state_provider.dart';

class TimeTravelQAScreen extends StatefulWidget {
  const TimeTravelQAScreen({Key? key}) : super(key: key);

  @override
  State<TimeTravelQAScreen> createState() => _TimeTravelQAScreenState();
}

class _TimeTravelQAScreenState extends State<TimeTravelQAScreen> {
  late TextEditingController _timestampController;
  late TextEditingController _questionController;
  double _evidenceWindow = 15.0; // 5-60 seconds

  @override
  void initState() {
    super.initState();
    _timestampController = TextEditingController();
    _questionController = TextEditingController();
  }

  @override
  void dispose() {
    _timestampController.dispose();
    _questionController.dispose();
    super.dispose();
  }

  bool _isValid() {
    return _timestampController.text.isNotEmpty && 
           _questionController.text.isNotEmpty;
  }

  void _handleAsk() {
    if (!_isValid()) return;

    final appState = context.read<AppStateProvider>();
    final result = TimeTravelResult(
      timestamp: _timestampController.text,
      evidence: '${_evidenceWindow.toStringAsFixed(0)} seconds',
      question: _questionController.text,
      answer: '这是根据时间戳 ${_timestampController.text} 的视频内容生成的回答...',
    );

    appState.addTimeTravelResult(result);
    _questionController.clear();

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('问题已添加'),
        duration: Duration(seconds: 2),
      ),
    );
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
                SizedBox(height: AppSpacing.lg),
                Text(
                  '时间旅行问答',
                  style: AppFonts.title.copyWith(
                    color: AppColors.textPrimary,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  '按时间戳追问视频内容',
                  style: AppFonts.subtitle.copyWith(
                    color: AppColors.textSecondary,
                  ),
                ),
                const SizedBox(height: AppSpacing.xl),

                // Timestamp Input
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '时间戳 (MM:SS)',
                      style: AppFonts.label.copyWith(
                        color: AppColors.textPrimary,
                      ),
                    ),
                    const SizedBox(height: AppSpacing.md),
                    TextField(
                      controller: _timestampController,
                      decoration: InputDecoration(
                        hintText: '例如: 1:30',
                        hintStyle: AppFonts.body.copyWith(
                          color: AppColors.textTertiary,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: AppSpacing.xl),

                // Evidence Window Slider
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          '证据窗口',
                          style: AppFonts.label.copyWith(
                            color: AppColors.textPrimary,
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: AppSpacing.md,
                            vertical: AppSpacing.xs,
                          ),
                          decoration: BoxDecoration(
                            color: AppColors.highlightBg,
                            borderRadius: BorderRadius.circular(
                              AppBorderRadius.medium,
                            ),
                          ),
                          child: Text(
                            '${_evidenceWindow.toStringAsFixed(0)} 秒',
                            style: AppFonts.caption.copyWith(
                              color: AppColors.primary,
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: AppSpacing.md),
                    Slider(
                      value: _evidenceWindow,
                      min: 5,
                      max: 60,
                      divisions: 11,
                      activeColor: AppColors.primary,
                      inactiveColor: AppColors.border,
                      onChanged: (value) {
                        setState(() {
                          _evidenceWindow = value;
                        });
                      },
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          '5秒',
                          style: AppFonts.caption.copyWith(
                            color: AppColors.textTertiary,
                          ),
                        ),
                        Text(
                          '60秒',
                          style: AppFonts.caption.copyWith(
                            color: AppColors.textTertiary,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: AppSpacing.xl),

                // Question Input
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '追问问题',
                      style: AppFonts.label.copyWith(
                        color: AppColors.textPrimary,
                      ),
                    ),
                    const SizedBox(height: AppSpacing.md),
                    TextField(
                      controller: _questionController,
                      maxLines: 4,
                      decoration: InputDecoration(
                        hintText: '请输入您的问题...',
                        hintStyle: AppFonts.body.copyWith(
                          color: AppColors.textTertiary,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: AppSpacing.xl),

                // Ask Button
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
                    onPressed: _isValid() ? _handleAsk : null,
                    child: Text(
                      '追问问题',
                      style: AppFonts.label.copyWith(
                        color: AppColors.white,
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: AppSpacing.xl),

                // Results Section
                if (appState.timeTravelResults.isNotEmpty)
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '问答历史',
                        style: AppFonts.label.copyWith(
                          color: AppColors.textPrimary,
                        ),
                      ),
                      const SizedBox(height: AppSpacing.md),
                      ...appState.timeTravelResults.asMap().entries.map((entry) {
                        int idx = entry.key;
                        TimeTravelResult result = entry.value;
                        return Padding(
                          padding: EdgeInsets.only(
                            bottom: idx < appState.timeTravelResults.length - 1
                                ? AppSpacing.lg
                                : 0,
                          ),
                          child: _ResultCard(result: result),
                        );
                      }).toList(),
                      const SizedBox(height: AppSpacing.xl),
                    ],
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _ResultCard extends StatelessWidget {
  final TimeTravelResult result;

  const _ResultCard({required this.result});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.lg),
      decoration: BoxDecoration(
        color: AppColors.warningBg,
        borderRadius: BorderRadius.circular(AppBorderRadius.large),
        border: Border.all(color: AppColors.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: AppSpacing.md,
                  vertical: AppSpacing.xs,
                ),
                decoration: BoxDecoration(
                  color: AppColors.white,
                  borderRadius: BorderRadius.circular(AppBorderRadius.medium),
                  border: Border.all(color: AppColors.border),
                ),
                child: Text(
                  result.timestamp,
                  style: AppFonts.caption.copyWith(
                    color: AppColors.primary,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(width: AppSpacing.md),
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: AppSpacing.md,
                  vertical: AppSpacing.xs,
                ),
                decoration: BoxDecoration(
                  color: AppColors.white,
                  borderRadius: BorderRadius.circular(AppBorderRadius.medium),
                  border: Border.all(color: AppColors.border),
                ),
                child: Text(
                  result.evidence,
                  style: AppFonts.caption.copyWith(
                    color: AppColors.textSecondary,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.md),
          Text(
            '问题:',
            style: AppFonts.label.copyWith(
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            result.question,
            style: AppFonts.body.copyWith(
              color: AppColors.textSecondary,
              height: 1.5,
            ),
          ),
          const SizedBox(height: AppSpacing.md),
          Text(
            '答案:',
            style: AppFonts.label.copyWith(
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            result.answer,
            style: AppFonts.body.copyWith(
              color: AppColors.textSecondary,
              height: 1.5,
            ),
          ),
        ],
      ),
    );
  }
}
