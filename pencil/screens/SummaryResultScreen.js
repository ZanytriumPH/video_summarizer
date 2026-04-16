/**
 * SummaryResultScreen.js - 总结结果屏幕
 * 功能：展示完整的视频分析总结报告
 */

import React, { useState } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  SafeAreaView,
  Text,
  TouchableOpacity,
  StatusBar,
  Share,
  Clipboard,
} from 'react-native';
import {
  COLORS,
  FONTS,
  SPACING,
  BORDER_RADIUS,
} from '../App';

export default function SummaryResultScreen() {
  const [copied, setCopied] = useState(false);

  const summaryContent = `## 核心要点

• 视频主要分三个阶段进行讲解
• 第一阶段介绍了核心架构设计
• 第二阶段详细演示了操作流程
• 第三阶段总结了关键要点

## 音频摘要

演讲者强调了系统设计的三个重要原则：可扩展性、可维护性和高性能。通过实际案例演示，展示了如何在生产环境中应用这些原则。

## 视觉亮点

• 架构图展示了系统的模块化设计
• 表格数据突出了性能对比
• 代码示例演示了最佳实践`;

  const handleCopyText = async () => {
    try {
      await Clipboard.setString(summaryContent);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Copy failed:', err);
    }
  };

  const handleShare = async () => {
    try {
      await Share.share({
        message: summaryContent,
        title: '视频分析报告',
      });
    } catch (err) {
      console.error('Share failed:', err);
    }
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
            总结报告
          </Text>
          <Text style={[FONTS.subtitle, { color: COLORS.textSecondary, marginTop: SPACING.xs }]}>
            您的视频多模态分析已完成
          </Text>
        </View>

        {/* Summary Content Card */}
        <View style={styles.summaryCard}>
          <Text style={[FONTS.label, { color: COLORS.textPrimary, marginBottom: SPACING.md }]}>
            核心要点
          </Text>
          <Text style={[FONTS.body, { color: COLORS.textPrimary, lineHeight: 20 }]}>
            • 视频主要分三个阶段进行讲解{'\n'}
            • 第一阶段介绍了核心架构设计{'\n'}
            • 第二阶段详细演示了操作流程{'\n'}
            • 第三阶段总结了关键要点
          </Text>

          <Text style={[
            FONTS.label,
            {
              color: COLORS.textPrimary,
              marginTop: SPACING.lg,
              marginBottom: SPACING.md
            }
          ]}>
            音频摘要
          </Text>
          <Text style={[FONTS.body, { color: COLORS.textPrimary, lineHeight: 20 }]}>
            演讲者强调了系统设计的三个重要原则：可扩展性、可维护性和高性能。通过实际案例演示，展示了如何在生产环境中应用这些原则。
          </Text>

          <Text style={[
            FONTS.label,
            {
              color: COLORS.textPrimary,
              marginTop: SPACING.lg,
              marginBottom: SPACING.md
            }
          ]}>
            视觉亮点
          </Text>
          <Text style={[FONTS.body, { color: COLORS.textPrimary, lineHeight: 20 }]}>
            • 架构图展示了系统的模块化设计{'\n'}
            • 表格数据突出了性能对比{'\n'}
            • 代码示例演示了最佳实践
          </Text>
        </View>

        {/* Copy Button */}
        <TouchableOpacity
          style={styles.copyButton}
          onPress={handleCopyText}
        >
          <Text style={[FONTS.label, { color: COLORS.primary }]}>
            {copied ? '✓ 已复制' : '📋 复制全文'}
          </Text>
        </TouchableOpacity>

        {/* Share Button */}
        <TouchableOpacity
          style={styles.shareButton}
          onPress={handleShare}
        >
          <Text style={[FONTS.label, { color: COLORS.white }]}>
            🚀 分享报告
          </Text>
        </TouchableOpacity>

        {/* Metadata */}
        <View style={styles.metadata}>
          <Text style={[FONTS.caption, { color: COLORS.textTertiary }]}>
            📊 生成于: 2024-01-15 09:45
          </Text>
          <Text style={[FONTS.caption, { color: COLORS.textTertiary, marginTop: SPACING.xs }]}>
            ⏱️ 处理时间: 3 分 42 秒
          </Text>
          <Text style={[FONTS.caption, { color: COLORS.textTertiary, marginTop: SPACING.xs }]}>
            🎥 视频时长: 42 分 15 秒
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
  summaryCard: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.large,
    padding: SPACING.lg,
    marginBottom: SPACING.lg,
  },
  copyButton: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.medium,
    borderWidth: 1,
    borderColor: COLORS.border,
    paddingVertical: SPACING.md,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: SPACING.md,
  },
  shareButton: {
    backgroundColor: COLORS.primary,
    borderRadius: BORDER_RADIUS.medium,
    paddingVertical: SPACING.md,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: SPACING.lg,
  },
  metadata: {
    backgroundColor: COLORS.lightBg,
    borderRadius: BORDER_RADIUS.medium,
    padding: SPACING.md,
    marginTop: SPACING.md,
  },
});
