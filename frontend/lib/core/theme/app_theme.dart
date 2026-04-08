import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData light() {
    const colorScheme = ColorScheme(
      brightness: Brightness.light,
      primary: Color(0xFF1E4F8A),
      onPrimary: Colors.white,
      secondary: Color(0xFF117A65),
      onSecondary: Colors.white,
      error: Color(0xFFB42318),
      onError: Colors.white,
      surface: Color(0xFFF6F8FC),
      onSurface: Color(0xFF13243E),
    );

    final base = ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
    );

    return base.copyWith(
      scaffoldBackgroundColor: const Color(0xFFEAF0F8),
      visualDensity: VisualDensity.standard,
      textTheme: base.textTheme.copyWith(
        displaySmall: const TextStyle(
          fontSize: 36,
          fontWeight: FontWeight.w700,
          color: Color(0xFF0F223D),
          letterSpacing: -0.9,
        ),
        headlineMedium: const TextStyle(
          fontSize: 30,
          fontWeight: FontWeight.w700,
          color: Color(0xFF10233F),
          letterSpacing: -0.6,
        ),
        titleLarge: const TextStyle(
          fontSize: 21,
          fontWeight: FontWeight.w700,
          color: Color(0xFF12284B),
        ),
        titleMedium: const TextStyle(
          fontSize: 15,
          fontWeight: FontWeight.w600,
          color: Color(0xFF1D3557),
        ),
        bodyLarge: const TextStyle(
          fontSize: 15.5,
          height: 1.5,
          color: Color(0xFF2F425B),
        ),
        bodyMedium: const TextStyle(
          fontSize: 14,
          height: 1.5,
          color: Color(0xFF52657F),
        ),
        labelLarge: const TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.w600,
        ),
      ),
      cardTheme: const CardThemeData(
        color: Colors.white,
        elevation: 0,
        margin: EdgeInsets.zero,
        shadowColor: Color(0x160A2342),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.all(Radius.circular(26)),
          side: BorderSide(color: Color(0xFFE2E9F3)),
        ),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        foregroundColor: Color(0xFF13294B),
        elevation: 0,
      ),
      dividerColor: const Color(0xFFE3EAF5),
      snackBarTheme: const SnackBarThemeData(
        behavior: SnackBarBehavior.floating,
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.white,
        contentPadding: const EdgeInsets.symmetric(
          horizontal: 16,
          vertical: 16,
        ),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(18),
          borderSide: const BorderSide(color: Color(0xFFD7E2F0)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(18),
          borderSide: const BorderSide(color: Color(0xFFD7E2F0)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(18),
          borderSide: const BorderSide(
            color: Color(0xFF1F4B99),
            width: 1.4,
          ),
        ),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: const Color(0xFF1E4F8A),
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(18),
          ),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: const Color(0xFF1E4F8A),
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
          side: const BorderSide(color: Color(0xFFD4DFEE)),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(18),
          ),
        ),
      ),
      chipTheme: base.chipTheme.copyWith(
        backgroundColor: const Color(0xFFF1F5FB),
        selectedColor: const Color(0xFFDCE8FF),
        side: const BorderSide(color: Color(0xFFE0E8F4)),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(14),
        ),
        labelStyle: const TextStyle(
          color: Color(0xFF294066),
          fontWeight: FontWeight.w600,
        ),
      ),
      navigationRailTheme: const NavigationRailThemeData(
        backgroundColor: Colors.transparent,
        indicatorColor: Color(0x1FFFFFFF),
        unselectedIconTheme: IconThemeData(
          color: Color(0xFF9EB1CF),
          size: 22,
        ),
        selectedIconTheme: IconThemeData(
          color: Colors.white,
          size: 22,
        ),
        unselectedLabelTextStyle: TextStyle(
          color: Color(0xFFD4DEEE),
          fontSize: 14,
        ),
        selectedLabelTextStyle: TextStyle(
          color: Colors.white,
          fontSize: 14,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }
}
