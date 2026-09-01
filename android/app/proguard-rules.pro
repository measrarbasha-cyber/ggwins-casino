# ProGuard rules for GG Wins
-keepattributes JavascriptInterface
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
-keep class site.ggwins.app.** { *; }
