/// 应用全局状态管理
library providers;

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/models.dart';

/// 应用状态提供者
class AppStateProvider extends ChangeNotifier {
  AppConfig _config = AppConfig();
  VideoSource? _selectedVideo;
  ProcessingProgress _progress = ProcessingProgress();
  SummaryResult? _summaryResult;
  List<TimeTravelResult> _timeTravelResults = [];
  
  bool _isProcessing = false;
  String? _errorMessage;

  // Getters
  AppConfig get config => _config;
  VideoSource? get selectedVideo => _selectedVideo;
  ProcessingProgress get progress => _progress;
  SummaryResult? get summaryResult => _summaryResult;
  List<TimeTravelResult> get timeTravelResults => _timeTravelResults;
  bool get isProcessing => _isProcessing;
  String? get errorMessage => _errorMessage;

  // 构造函数
  AppStateProvider() {
    _loadConfig();
  }

  /// 加载保存的配置
  Future<void> _loadConfig() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      _config.apiKey = prefs.getString('apiKey') ?? 'sk-...';
      _config.baseUrl = prefs.getString('baseUrl') ?? 'https://api.openai.com/v1';
      _config.userPrompt = prefs.getString('userPrompt') ?? '';
      final modeIndex = prefs.getInt('concurrencyMode') ?? 0;
      _config.concurrencyMode = ConcurrencyMode.values[modeIndex];
      notifyListeners();
    } catch (e) {
      print('Error loading config: $e');
    }
  }

  /// 保存API配置
  Future<void> saveApiConfig({
    required String apiKey,
    required String baseUrl,
  }) async {
    _config.apiKey = apiKey;
    _config.baseUrl = baseUrl;
    
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('apiKey', apiKey);
      await prefs.setString('baseUrl', baseUrl);
    } catch (e) {
      _errorMessage = 'Failed to save config: $e';
    }
    notifyListeners();
  }

  /// 保存用户提示词
  Future<void> saveUserPrompt(String prompt) async {
    _config.userPrompt = prompt;
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('userPrompt', prompt);
    } catch (e) {
      _errorMessage = 'Failed to save user prompt: $e';
    }
    notifyListeners();
  }

  /// 设置并行模式
  Future<void> setConcurrencyMode(ConcurrencyMode mode) async {
    _config.concurrencyMode = mode;
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setInt('concurrencyMode', mode.index);
    } catch (e) {
      _errorMessage = 'Failed to save concurrency mode: $e';
    }
    notifyListeners();
  }

  /// 设置选中的视频
  void setSelectedVideo(VideoSource video) {
    _selectedVideo = video;
    notifyListeners();
  }

  /// 更新进度
  void updateProgress(ProcessingProgress progress) {
    _progress = progress;
    notifyListeners();
  }

  /// 模拟进度更新（用于演示）
  void simulateProgress() {
    _isProcessing = true;
    _errorMessage = null;
    
    Future.doWhile(() async {
      await Future.delayed(Duration(milliseconds: 500));
      
      if (_progress.overall >= 100) {
        _isProcessing = false;
        _summaryResult = SummaryResult(
          title: '视频总结',
          content: '这是视频内容的完整总结...',
          keyPoints: ['关键点1', '关键点2', '关键点3'],
          audioSummary: '音频部分的总结内容',
          visualHighlights: '视觉亮点总结',
          createdAt: DateTime.now(),
        );
        notifyListeners();
        return false;
      }

      _progress = _progress.copyWith(
        overall: (_progress.overall + 5).clamp(0, 100),
        audio: (_progress.audio + 4).clamp(0, 100),
        vision: (_progress.vision + 4).clamp(0, 100),
        fusion: (_progress.fusion + 4).clamp(0, 100),
      );
      notifyListeners();
      return true;
    });
  }

  /// 添加时间旅行结果
  void addTimeTravelResult(TimeTravelResult result) {
    _timeTravelResults.add(result);
    notifyListeners();
  }

  /// 清除状态
  void clearState() {
    _selectedVideo = null;
    _progress = ProcessingProgress();
    _summaryResult = null;
    _timeTravelResults = [];
    _isProcessing = false;
    _errorMessage = null;
    notifyListeners();
  }
}
