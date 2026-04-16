/**
 * VideoSelectionScreen.js - 视频选择屏幕
 * 功能：选择视频源（YouTube URL或本地上传）
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
} from 'react-native';
import DocumentPicker from 'react-native-document-picker';
import {
  COLORS,
  FONTS,
  SPACING,
  BORDER_RADIUS,
} from '../App';

export default function VideoSelectionScreen() {
  const [sourceType, setSourceType] = useState('youtube');
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileSelect = async () => {
    try {
      const res = await DocumentPicker.pick({
        type: [DocumentPicker.types.video],
      });
      setSelectedFile(res);
    } catch (err) {
      if (DocumentPicker.isCancel(err)) {
        // User cancelled
      } else {
        throw err;
      }
    }
  };

  const handleNext = () => {
    if (sourceType === 'youtube' && youtubeUrl) {
      // Navigate to processing
      console.log('Processing YouTube:', youtubeUrl);
    } else if (sourceType === 'local' && selectedFile) {
      // Navigate to processing
      console.log('Processing file:', selectedFile);
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
            选择视频源
          </Text>
          <Text style={[FONTS.subtitle, { color: COLORS.textSecondary, marginTop: SPACING.xs }]}>
            上传本地或输入URL
          </Text>
        </View>

        {/* YouTube Option */}
        <TouchableOpacity
          style={[
            styles.sourceOption,
            sourceType === 'youtube' && styles.sourceOptionActive,
          ]}
          onPress={() => setSourceType('youtube')}
        >
          <Text style={[FONTS.label, { color: COLORS.primary }]}>
            🌐 YouTube URL
          </Text>
          <Text style={[FONTS.subtitle, { color: COLORS.textSecondary, marginTop: SPACING.xs }]}>
            输入视频链接
          </Text>

          {sourceType === 'youtube' && (
            <TextInput
              style={[styles.input, { marginTop: SPACING.lg }]}
              placeholder="https://youtube.com/watch?v=..."
              value={youtubeUrl}
              onChangeText={setYoutubeUrl}
              placeholderTextColor={COLORS.textTertiary}
            />
          )}
        </TouchableOpacity>

        {/* Local Upload Option */}
        <TouchableOpacity
          style={[
            styles.sourceOption,
            { marginTop: SPACING.lg },
            sourceType === 'local' && styles.sourceOptionActive,
          ]}
          onPress={() => setSourceType('local')}
        >
          <Text style={[FONTS.label, { color: COLORS.textPrimary }]}>
            📤 本地上传
          </Text>
          <Text style={[FONTS.subtitle, { color: COLORS.textSecondary, marginTop: SPACING.xs }]}>
            点击选择文件
          </Text>

          {sourceType === 'local' && (
            <>
              <TouchableOpacity
                style={styles.uploadArea}
                onPress={handleFileSelect}
              >
                <Text style={[FONTS.body, { color: COLORS.textTertiary }]}>
                  + 点击或拖拽视频
                </Text>
              </TouchableOpacity>

              {selectedFile && (
                <Text style={[FONTS.caption, { color: COLORS.primary, marginTop: SPACING.md }]}>
                  ✓ 已选择: {selectedFile.name}
                </Text>
              )}
            </>
          )}
        </TouchableOpacity>

        {/* Next Button */}
        <TouchableOpacity
          style={[styles.nextButton, !((sourceType === 'youtube' && youtubeUrl) || (sourceType === 'local' && selectedFile)) && { opacity: 0.5 }]}
          onPress={handleNext}
          disabled={!((sourceType === 'youtube' && youtubeUrl) || (sourceType === 'local' && selectedFile))}
        >
          <Text style={[FONTS.label, { color: COLORS.white }]}>
            下一步
          </Text>
        </TouchableOpacity>
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
  sourceOption: {
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.large,
    borderWidth: 1,
    borderColor: COLORS.border,
    padding: SPACING.lg,
  },
  sourceOptionActive: {
    backgroundColor: COLORS.highlightBg,
    borderColor: COLORS.primary,
    borderWidth: 2,
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
  uploadArea: {
    borderWidth: 2,
    borderColor: COLORS.border,
    borderStyle: 'dashed',
    borderRadius: BORDER_RADIUS.medium,
    padding: SPACING.lg,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 60,
    backgroundColor: '#FAFAFA',
    marginTop: SPACING.md,
  },
  nextButton: {
    backgroundColor: COLORS.primary,
    borderRadius: BORDER_RADIUS.large,
    paddingVertical: SPACING.lg,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: SPACING.xxl,
    marginBottom: SPACING.lg,
  },
});
