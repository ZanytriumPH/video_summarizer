// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter_test/flutter_test.dart';

import 'package:video_summarizer/main.dart';

void main() {
  testWidgets('bottom navigation renders five tabs and switches screens', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(const MyApp());
    await tester.pumpAndSettle();

    expect(find.text('SETTINGS'), findsOneWidget);
    expect(find.text('VIDEO'), findsOneWidget);
    expect(find.text('PROGRESS'), findsOneWidget);
    expect(find.text('SUMMARY'), findsOneWidget);
    expect(find.text('Q&A'), findsOneWidget);
    expect(find.text('Video Summarizer'), findsOneWidget);

    await tester.tap(find.text('VIDEO'));
    await tester.pumpAndSettle();
    expect(find.text('选择视频源'), findsOneWidget);

    await tester.tap(find.text('PROGRESS'));
    await tester.pumpAndSettle();
    expect(find.text('处理中...'), findsOneWidget);

    await tester.tap(find.text('SUMMARY'));
    await tester.pumpAndSettle();
    expect(find.text('请先处理视频'), findsOneWidget);

    await tester.tap(find.text('Q&A'));
    await tester.pumpAndSettle();
    expect(find.text('时间旅行问答'), findsOneWidget);
  });
}
