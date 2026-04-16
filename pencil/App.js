/**
 * App.js - 主应用入口
 * React Native 视频总结器应用
 * 支持 iOS 和 Android 平台
 */

import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  SafeAreaView,
  StatusBar,
  Platform,
  TouchableOpacity,
  Text,
  Dimensions,
} from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

// Import screens
import SettingsScreen from './screens/SettingsScreen';
import VideoSelectionScreen from './screens/VideoSelectionScreen';
import ProcessingProgressScreen from './screens/ProcessingProgressScreen';
import SummaryResultScreen from './screens/SummaryResultScreen';
import TimeTravelQAScreen from './screens/TimeTravelQAScreen';

// Design System Constants
export const COLORS = {
  primary: '#0066FF',
  background: '#F5F5F5',
  white: '#FFFFFF',
  textPrimary: '#1A1A1A',
  textSecondary: '#666666',
  textTertiary: '#999999',
  border: '#DDDDDD',
  lightBg: '#F9F9F9',
  highlightBg: '#F0F7FF',
  warningBg: '#FFF8E1',
  warning: '#F57C00',
};

export const FONTS = {
  title: { fontSize: 24, fontWeight: '700' },
  subtitle: { fontSize: 12, fontWeight: '400' },
  label: { fontSize: 13, fontWeight: '600' },
  body: { fontSize: 12, fontWeight: '400' },
  tabLabel: { fontSize: 10, fontWeight: '600' },
  caption: { fontSize: 11, fontWeight: '500' },
};

export const SPACING = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  xxl: 24,
};

export const BORDER_RADIUS = {
  small: 4,
  medium: 8,
  large: 12,
  pill: 26,
  full: 36,
};

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

/**
 * 自定义底部导航栏
 */
function CustomTabBar({ state, descriptors, navigation }) {
  return (
    <SafeAreaView
      edges={['bottom']}
      style={styles.tabBarContainer}
    >
      <View style={styles.tabBarPill}>
        {state.routes.map((route, index) => {
          const { options } = descriptors[route.key];
          const isFocused = state.index === index;
          
          const tabIcons = ['⚙️', '🎬', '⏳', '📝', '🔎'];
          const tabLabels = ['SETTINGS', 'SELECT', 'PROGRESS', 'SUMMARY', 'TRAVEL'];

          return (
            <TouchableOpacity
              key={route.key}
              onPress={() => navigation.navigate(route.name)}
              style={[
                styles.tabItem,
                isFocused && styles.tabItemActive,
              ]}
            >
              <Text style={[
                styles.tabIcon,
                { color: isFocused ? COLORS.white : COLORS.textTertiary }
              ]}>
                {tabIcons[index]}
              </Text>
              <Text style={[
                styles.tabLabel,
                { color: isFocused ? COLORS.white : COLORS.textTertiary }
              ]}>
                {tabLabels[index]}
              </Text>
            </TouchableOpacity>
          );
        })}
      </View>
    </SafeAreaView>
  );
}

/**
 * 主导航栈
 */
function MainNavigator() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: COLORS.primary,
        tabBarInactiveTintColor: COLORS.textTertiary,
      }}
      tabBar={(props) => <CustomTabBar {...props} />}
    >
      <Tab.Screen
        name="Settings"
        component={SettingsScreen}
        options={{ title: 'Settings' }}
      />
      <Tab.Screen
        name="VideoSelection"
        component={VideoSelectionScreen}
        options={{ title: 'Video Selection' }}
      />
      <Tab.Screen
        name="Processing"
        component={ProcessingProgressScreen}
        options={{ title: 'Processing' }}
      />
      <Tab.Screen
        name="Summary"
        component={SummaryResultScreen}
        options={{ title: 'Summary' }}
      />
      <Tab.Screen
        name="TimeTravel"
        component={TimeTravelQAScreen}
        options={{ title: 'Time Travel' }}
      />
    </Tab.Navigator>
  );
}

/**
 * 主应用组件
 */
export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Main" component={MainNavigator} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  tabBarContainer: {
    backgroundColor: COLORS.background,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
  },
  tabBarPill: {
    flexDirection: 'row',
    backgroundColor: COLORS.white,
    borderRadius: BORDER_RADIUS.full,
    borderWidth: 1,
    borderColor: '#EEEEEE',
    overflow: 'hidden',
    padding: SPACING.xs,
    gap: SPACING.xs,
  },
  tabItem: {
    flex: 1,
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: BORDER_RADIUS.pill,
    paddingVertical: SPACING.md,
    gap: SPACING.xs,
  },
  tabItemActive: {
    backgroundColor: COLORS.primary,
  },
  tabIcon: {
    fontSize: 18,
  },
  tabLabel: {
    ...FONTS.tabLabel,
    letterSpacing: 0.5,
  },
});
