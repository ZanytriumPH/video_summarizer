/**
 * ProcessingProgressScreen.js - 处理进度屏幕
 * 功能：实时显示视频多模态分析的进度
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  SafeAreaView,
  Text,
  StatusBar,
  Animated,
  Easing,
} from 'react-native';
import {
  COLORS,
  FONTS,
  SPACING,
  BORDER_RADIUS,
} from '../App';

export default function ProcessingProgressScreen() {
  const [progress, setProgress] = useState({
    overall: 35,
    audio: 25,
    vision: 40,
    fusion: 45,
    totalChunks: 100,
  });

  // Simulate progress updates
  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(prev => ({
        ...prev,
        overall: Math.min(prev.overall + Math.random() * 5, 99),
        audio: Math.min(prev.audio + Math.random() * 4, 100),
        vision: Math.min(prev.vision + Math.random() * 4, 100),
        fusion: Math.min(prev.fusion + Math.random() * 4, 100),
      }));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const ProgressBar = ({ label, value, icon }) => (
    <View style={styles.progressCard}>
      <Text style={[FONTS.label, { color: COLORS.textPrimary, marginBottom: SPACING.xs }]}>
        {icon} {label}
      </Text>
      <Text style={[FONTS.caption, { color: COLORS.primary, marginBottom: SPACING.xs }]}>
        {Math.round(value)}/100 已完成
      </Text>
      <View style={styles.progressBarContainer}>
        <View
          style={[
            styles.progressBarFill,
            { width: `${Math.min(value, 100)}%` }
          ]}
        />
      </View>
    </View>
  );

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
            处理中...
          </Text>
          <Text style={[FONTS.subtitle, { color: COLORS.textSecondary, marginTop: SPACING.xs }]}>
            正在分析视频内容
          </Text>
        </View>

        {/* Overall Progress Card */}
        <View style={styles.mainProgressCard}>
          <Text style={[FONTS.label, { color: COLORS.textPrimary, marginBottom: SPACING.md }]}>
            整体进度
          </Text>

          <Text style={[FONTS.caption, { color: COLORS.textSecondary, marginBottom: SPACING.xs }]}>
            总体: {Math.round(progress.overall)}/100 ({Math.round(progress.overall)}%)
          </Text>

          <View style={styles.mainProgressBarContainer}>
            <View
              style={[
                styles.mainProgressBarFill,
                { width: `${Math.min(progress.overall, 100)}%` }
              ]}
            />
          </View>

          {/* Individual Progress Cards */}
          <View style={styles.progressCardsContainer}>
            <ProgressBar
              label="音频分析"
              value={progress.audio}
              icon="🎵"
            />
            <ProgressBar
              label="视觉分析"
              value={progress.vision}
              icon="👁️"
            />
            <ProgressBar
              label="融合综合"
              value={progress.fusion}
              icon="🔗"
            />
          </View>
        </View>

        {/* Status Messages */}
        <View style={styles.statusMessages}>
          <Text style={[FONTS.caption, { color: COLORS.textSecondary, marginBottom: SPACING.md }]}>
            📌 处理步骤:
          </Text>
          <Text style={[FONTS.body, { color: COLORS.textPrimary, marginBottom: SPACING.sm }]}>
            • 正在提取音频轨道...
          </Text>
          <Text style={[FONTS.body, { color: COLORS.textPrimary, marginBottom: SPACING.sm }]}>
            • 正在转录语音内容...
          </Text>
          <Text style={[FONTS.body, { color: COLORS.textPrimary, marginBottom: SPACING.sm }]}>
            • 正在分析视觉帧...
          </Text>
          <Text style={[FONTS.body, { color: COLORS.textPrimary }]}>
            • 正在融合多模态信息...
          </Text>
        </View>
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
  mainProgressCard: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.large,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
  },
  mainProgressBarContainer: {
    height: 8,
    backgroundColor: '#EEEEEE',
    borderRadius: BORDER_RADIUS.small,
    overflow: 'hidden',
    marginBottom: SPACING.lg,
  },
  mainProgressBarFill: {
    height: '100%',
    backgroundColor: COLORS.primary,
  },
  progressCardsContainer: {
    gap: SPACING.md,
  },
  progressCard: {
    backgroundColor: COLORS.lightBg,
    borderRadius: BORDER_RADIUS.medium,
    padding: SPACING.md,
  },
  progressBarContainer: {
    height: 6,
    backgroundColor: '#EEEEEE',
    borderRadius: BORDER_RADIUS.small,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: COLORS.primary,
  },
  statusMessages: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.large,
    padding: SPACING.lg,
  },
});
