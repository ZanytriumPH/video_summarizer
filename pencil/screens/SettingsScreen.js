/**
 * SettingsScreen.js - 配置屏幕
 * 功能：配置API Key、Base URL、总结偏好和并行模式
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
  Platform,
} from 'react-native';
import {
  COLORS,
  FONTS,
  SPACING,
  BORDER_RADIUS,
} from '../App';

export default function SettingsScreen() {
  const [apiKey, setApiKey] = useState('sk-...');
  const [baseUrl, setBaseUrl] = useState('https://api.openai.com/v1');
  const [userPrompt, setUserPrompt] = useState('');
  const [selectedMode, setSelectedMode] = useState('threadpool');

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
            Video Summarizer
          </Text>
          <Text style={[FONTS.subtitle, { color: COLORS.textSecondary, marginTop: SPACING.xs }]}>
            多模态智能总结
          </Text>
        </View>

        {/* API Configuration Section */}
        <View style={styles.section}>
          <Text style={[FONTS.label, { color: COLORS.textPrimary, marginBottom: SPACING.md }]}>
            API 配置
          </Text>

          {/* API Key Input */}
          <View style={styles.fieldGroup}>
            <Text style={[FONTS.caption, { color: COLORS.textSecondary, marginBottom: SPACING.xs }]}>
              OpenAI API Key
            </Text>
            <TextInput
              style={styles.input}
              placeholder="sk-..."
              value={apiKey}
              onChangeText={setApiKey}
              secureTextEntry={true}
              placeholderTextColor={COLORS.textTertiary}
            />
          </View>

          {/* Base URL Input */}
          <View style={styles.fieldGroup}>
            <Text style={[FONTS.caption, { color: COLORS.textSecondary, marginBottom: SPACING.xs }]}>
              Base URL
            </Text>
            <TextInput
              style={styles.input}
              placeholder="https://api.openai.com/v1"
              value={baseUrl}
              onChangeText={setBaseUrl}
              placeholderTextColor={COLORS.textTertiary}
            />
          </View>
        </View>

        {/* Summary Preference Section */}
        <View style={styles.section}>
          <Text style={[FONTS.label, { color: COLORS.textPrimary, marginBottom: SPACING.md }]}>
            总结偏好
          </Text>

          <TextInput
            style={[styles.textArea]}
            placeholder="请输入总结重点（可选）"
            value={userPrompt}
            onChangeText={setUserPrompt}
            multiline
            numberOfLines={4}
            placeholderTextColor={COLORS.textTertiary}
            textAlignVertical="top"
          />
        </View>

        {/* Concurrency Mode Section */}
        <View style={styles.section}>
          <Text style={[FONTS.label, { color: COLORS.textPrimary, marginBottom: SPACING.md }]}>
            并行模式
          </Text>

          {/* ThreadPool Option */}
          <TouchableOpacity
            style={[
              styles.modeOption,
              selectedMode === 'threadpool' && styles.modeOptionActive,
            ]}
            onPress={() => setSelectedMode('threadpool')}
          >
            <Text style={[
              FONTS.body,
              {
                color: selectedMode === 'threadpool' ? COLORS.primary : COLORS.textTertiary,
              }
            ]}>
              ✓ ThreadPool (默认)
            </Text>
          </TouchableOpacity>

          {/* Send API Option */}
          <TouchableOpacity
            style={[
              styles.modeOption,
              { marginTop: SPACING.md },
              selectedMode === 'send_api' && styles.modeOptionActive,
            ]}
            onPress={() => setSelectedMode('send_api')}
          >
            <Text style={[
              FONTS.body,
              {
                color: selectedMode === 'send_api' ? COLORS.primary : COLORS.textTertiary,
              }
            ]}>
              Send API (试点)
            </Text>
          </TouchableOpacity>
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
  section: {
    marginBottom: SPACING.xxl,
  },
  fieldGroup: {
    marginBottom: SPACING.lg,
  },
  input: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.medium,
    borderWidth: 1,
    borderColor: COLORS.border,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    fontSize: 12,
    color: COLORS.textPrimary,
  },
  textArea: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.medium,
    borderWidth: 1,
    borderColor: COLORS.border,
    padding: SPACING.lg,
    fontSize: 12,
    color: COLORS.textPrimary,
    minHeight: 80,
  },
  modeOption: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.medium,
    borderWidth: 1,
    borderColor: COLORS.border,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
  },
  modeOptionActive: {
    borderColor: COLORS.primary,
    borderWidth: 2,
  },
});
