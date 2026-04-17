/// 应用状态模型
library models;

/// 并行模式
enum ConcurrencyMode { threadPool, sendAPI }

/// 视频源
class VideoSource {
  final String fileName;
  final String? filePath;

  const VideoSource({required this.fileName, this.filePath});
}

/// 处理进度
class ProcessingProgress {
  final double overall;
  final double audio;
  final double vision;
  final double fusion;
  final int totalChunks;

  ProcessingProgress({
    this.overall = 0,
    this.audio = 0,
    this.vision = 0,
    this.fusion = 0,
    this.totalChunks = 100,
  });

  ProcessingProgress copyWith({
    double? overall,
    double? audio,
    double? vision,
    double? fusion,
    int? totalChunks,
  }) {
    return ProcessingProgress(
      overall: overall ?? this.overall,
      audio: audio ?? this.audio,
      vision: vision ?? this.vision,
      fusion: fusion ?? this.fusion,
      totalChunks: totalChunks ?? this.totalChunks,
    );
  }
}

/// 总结结果
class SummaryResult {
  final String title;
  final String content;
  final List<String> keyPoints;
  final String audioSummary;
  final String visualHighlights;
  final DateTime createdAt;

  SummaryResult({
    required this.title,
    required this.content,
    required this.keyPoints,
    required this.audioSummary,
    required this.visualHighlights,
    required this.createdAt,
  });
}

/// 时间旅行问答结果
class TimeTravelResult {
  final String timestamp;
  final String evidence;
  final String question;
  final String answer;

  TimeTravelResult({
    required this.timestamp,
    required this.evidence,
    required this.question,
    required this.answer,
  });
}

/// 应用配置
class AppConfig {
  String apiKey;
  String baseUrl;
  String userPrompt;
  ConcurrencyMode concurrencyMode;

  AppConfig({
    this.apiKey = 'sk-...',
    this.baseUrl = 'https://api.openai.com/v1',
    this.userPrompt = '',
    this.concurrencyMode = ConcurrencyMode.threadPool,
  });
}
