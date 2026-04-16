/**
 * TimeTravelQAScreen.js - 时间旅行追问屏幕
 * 功能：按指定时间戳追问视频内容
 */

import React, { useState } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  SafeAreaView,
  Text,
  TextInput,
  TouchableOpacity,
  StatusBar,
  Slider,
} from 'react-native';
import {
  COLORS,
  FONTS,
  SPACING,
  BORDER_RADIUS,
} from '../App';

export default function TimeTravelQAScreen() {
  const [timestamp, setTimestamp] = useState('00:14:30');
  const [windowSize, setWindowSize] = useState(20);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;

    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setAnswer('根据视频在' + timestamp + '的内容，架构图展示了系统的三层设计架构，包括表现层、业务逻辑层和数据持久化层。每一层都有各自的职责分工。');
      setLoading(false);
    }, 2000);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar
        barStyle="light-content"
        backgroundColor="#000000"
        translucent={false}
      />

      {/* Status Bar */}
      <View style={styles.statusBar}>
        <Text style={styles.statusTime}>9:41</Text>
        <Text style={styles.statusIcon}>📶</Text>
      </View>

      <ScrollView
        style={styles.content}
        contentContainerStyle={styles.contentContainer}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={[FONTS.title, { color: COLORS.textPrimary }]}>
            时间旅行追问
          </Text>
          <Text style={[FONTS.subtitle, { color: COLORS.textSecondary, marginTop: SPACING.xs }]}>
            🕒 按时间戳追问
          </Text>
        </View>

        {/* Time Configuration Card */}
        <View style={styles.configCard}>
          <Text style={[FONTS.label, { color: COLORS.textPrimary, marginBottom: SPACING.md }]}>
            目标时间戳
          </Text>

          <TextInput
            style={styles.timestampInput}
            value={timestamp}
            onChangeText={setTimestamp}
            placeholder="MM:SS 或 HH:MM:SS"
            placeholderTextColor={COLORS.textTertiary}
          />

          <Text style={[
            FONTS.label,
            {
              color: COLORS.textPrimary,
              marginTop: SPACING.lg,
              marginBottom: SPACING.md
            }
          ]}>
            证据窗口 ({windowSize}秒)
          </Text>

          <Slider
            style={styles.slider}
            minimumValue={5}
            maximumValue={60}
            step={5}
            value={windowSize}
            onValueChange={setWindowSize}
            minimumTrackTintColor={COLORS.primary}
            maximumTrackTintColor={COLORS.border}
            thumbTintColor={COLORS.primary}
          />

          <Text style={[
            FONTS.caption,
            { color: COLORS.textSecondary, marginTop: SPACING.md }
          ]}>
            在{timestamp}前后各提取{Math.floor(windowSize / 2)}秒的内容作为分析证据
          </Text>
        </View>

        {/* Question Input Card */}
        <View style={styles.questionCard}>
          <Text style={[FONTS.label, { color: COLORS.textPrimary, marginBottom: SPACING.md }]}>
            追问问题
          </Text>

          <TextInput
            style={styles.questionInput}
            placeholder="请输入您的问题..."
            value={question}
            onChangeText={setQuestion}
            placeholderTextColor={COLORS.textTertiary}
            multiline
            numberOfLines={4}
            textAlignVertical="top"
          />
        </View>

        {/* Ask Button */}
        <TouchableOpacity
          style={[
            styles.askButton,
            loading && { opacity: 0.6 }
          ]}
          onPress={handleAsk}
          disabled={loading || !question.trim()}
        >
          <Text style={[FONTS.label, { color: COLORS.white }]}>
            {loading ? '🔍 分析中...' : '🔍 时间旅行追问'}
          </Text>
        </TouchableOpacity>

        {/* Answer Preview */}
        {answer && (
          <View style={styles.answerCard}>
            <Text style={[FONTS.label, { color: COLORS.warning, marginBottom: SPACING.md }]}>
              📌 追问结果
            </Text>
            <Text style={[FONTS.body, { color: COLORS.textPrimary, lineHeight: 20 }]}>
              {answer}
            </Text>
            <Text style={[
              FONTS.caption,
              { color: COLORS.textTertiary, marginTop: SPACING.md }
            ]}>
              📍 引用时间范围: {formatTime(Math.max(0, parseInt(timestamp.split(':')[0]) * 3600 + parseInt(timestamp.split(':')[1]) * 60 - windowSize/2))} 
              ~ {formatTime(Math.min(3600, parseInt(timestamp.split(':')[0]) * 3600 + parseInt(timestamp.split(':')[1]) * 60 + windowSize/2))}
            </Text>
          </View>
        )}

        {/* Tips */}
        {!answer && (
          <View style={styles.tipsCard}>
            <Text style={[FONTS.caption, { color: COLORS.textSecondary }]}>
              💡 提示: 输入时间戳并输入问题，系统会查找该时间点前后的相关内容来回答您的问题。
            </Text>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  statusBar: {
    height: 62,
    backgroundColor: '#000000',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: SPACING.lg,
  },
  statusTime: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.white,
  },
  statusIcon: {
    fontSize: 11,
    color: COLORS.white,
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    padding: SPACING.lg,
    paddingBottom: 100,
  },
  header: {
    marginBottom: SPACING.xxl,
  },
  configCard: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.large,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
  },
  timestampInput: {
    backgroundColor: COLORS.lightBg,
    borderRadius: BORDER_RADIUS.medium,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.primary,
  },
  slider: {
    height: 40,
  },
  questionCard: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.large,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
  },
  questionInput: {
    backgroundColor: COLORS.lightBg,
    borderRadius: BORDER_RADIUS.medium,
    borderWidth: 1,
    borderColor: COLORS.border,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.lg,
    fontSize: 12,
    color: COLORS.textPrimary,
    minHeight: 80,
  },
  askButton: {
    backgroundColor: COLORS.primary,
    borderRadius: BORDER_RADIUS.large,
    paddingVertical: SPACING.lg,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: SPACING.lg,
  },
  answerCard: {
    backgroundColor: COLORS.warningBg,
    borderRadius: BORDER_RADIUS.large,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
  },
  tipsCard: {
    backgroundColor: COLORS.highlightBg,
    borderRadius: BORDER_RADIUS.medium,
    padding: SPACING.lg,
    borderLeftWidth: 4,
    borderLeftColor: COLORS.primary,
  },
});
