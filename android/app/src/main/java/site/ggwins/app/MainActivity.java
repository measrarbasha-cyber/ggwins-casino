package site.ggwins.app;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;
import androidx.core.content.ContextCompat;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

public class MainActivity extends AppCompatActivity {

    private static final String DEFAULT_URL = BuildConfig.START_URL;
    private static final String HOST_URL = "https://ggwins.site/host/index.html";
    private static final String CASINO_URL = "https://ggwins.site";
    private static final String CHANNEL_ID = "ggwins_admin_whatsapp_channel";
    private static final int FILE_CHOOSER_REQUEST_CODE = 1001;
    private static final int NOTIFICATION_PERMISSION_CODE = 1002;

    private WebView webView;
    private ProgressBar progressBar;
    private SwipeRefreshLayout swipeRefreshLayout;
    private LinearLayout adminDock;
    private ValueCallback<Uri[]> filePathCallback;
    private long lastBackgroundTime = 0;

    public class AndroidNotificationBridge {
        @JavascriptInterface
        public void notifyAdmin(String title, String message, String type) {
            runOnUiThread(() -> showWhatsAppSystemNotification(title, message, type));
        }

        @JavascriptInterface
        public boolean isAndroidApp() {
            return true;
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Dark status bar
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = getWindow();
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);
            window.setStatusBarColor(0xFF07090E);
        }

        setContentView(R.layout.activity_main);

        webView = findViewById(R.id.webView);
        progressBar = findViewById(R.id.progressBar);
        swipeRefreshLayout = findViewById(R.id.swipeRefresh);
        adminDock = findViewById(R.id.adminDock);

        swipeRefreshLayout.setColorSchemeColors(0xFFFFD700, 0xFF00E676);
        swipeRefreshLayout.setProgressBackgroundColorSchemeColor(0xFF0F1527);
        swipeRefreshLayout.setOnRefreshListener(() -> webView.reload());

        // Setup notification channel
        createNotificationChannel();

        // Request notification permissions on Android 13+
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.POST_NOTIFICATIONS}, NOTIFICATION_PERMISSION_CODE);
            }
        }

        // Setup Admin controls if this is the Admin App flavor
        if (BuildConfig.IS_ADMIN_APP) {
            adminDock.setVisibility(View.VISIBLE);
            setupAdminDock();
        } else {
            adminDock.setVisibility(View.GONE);
        }

        configureWebView();

        if (savedInstanceState != null) {
            webView.restoreState(savedInstanceState);
        } else {
            webView.loadUrl(DEFAULT_URL);
        }
    }

    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            CharSequence name = "GG Wins Admin WhatsApp Alerts";
            String description = "High-priority instant notifications for deposits, withdrawals, and VIP requests";
            int importance = NotificationManager.IMPORTANCE_HIGH;
            NotificationChannel channel = new NotificationChannel(CHANNEL_ID, name, importance);
            channel.setDescription(description);
            channel.enableLights(true);
            channel.setLightColor(0xFF00E676);
            channel.enableVibration(true);
            channel.setVibrationPattern(new long[]{0, 200, 100, 200}); // WhatsApp double-vibe

            NotificationManager notificationManager = getSystemService(NotificationManager.class);
            if (notificationManager != null) {
                notificationManager.createNotificationChannel(channel);
            }
        }
    }

    private void showWhatsAppSystemNotification(String title, String message, String type) {
        Uri defaultSoundUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);

        NotificationCompat.Builder builder = new NotificationCompat.Builder(this, CHANNEL_ID)
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle(title)
                .setContentText(message)
                .setStyle(new NotificationCompat.BigTextStyle().bigText(message))
                .setPriority(NotificationCompat.PRIORITY_MAX)
                .setSound(defaultSoundUri)
                .setVibrate(new long[]{0, 200, 100, 200})
                .setAutoCancel(true)
                .setCategory(NotificationCompat.CATEGORY_MESSAGE);

        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(this);
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) == PackageManager.PERMISSION_GRANTED || Build.VERSION.SDK_INT < Build.VERSION_CODES.TIRAMISU) {
            try {
                notificationManager.notify((int) System.currentTimeMillis(), builder.build());
            } catch (Exception ignored) {}
        }
    }

    private void setupAdminDock() {
        Button btnTerminal = findViewById(R.id.btnNavTerminal);
        Button btnCasino = findViewById(R.id.btnNavCasino);
        Button btnLock = findViewById(R.id.btnNavLock);
        Button btnReload = findViewById(R.id.btnNavReload);

        btnTerminal.setOnClickListener(v -> {
            webView.loadUrl(HOST_URL);
            Toast.makeText(this, "👑 Switching to Host Terminal", Toast.LENGTH_SHORT).show();
        });

        btnCasino.setOnClickListener(v -> {
            webView.loadUrl(CASINO_URL);
            Toast.makeText(this, "🎰 Switching to Casino Lobby", Toast.LENGTH_SHORT).show();
        });

        btnLock.setOnClickListener(v -> {
            lockTerminal();
        });

        btnReload.setOnClickListener(v -> {
            webView.reload();
            Toast.makeText(this, "🔄 Syncing Terminal", Toast.LENGTH_SHORT).show();
        });
    }

    private void lockTerminal() {
        if (webView != null) {
            webView.evaluateJavascript(
                "if(typeof logoutAdmin==='function'){ logoutAdmin(); } " +
                "else if(typeof lockAdminUI==='function'){ lockAdminUI(); } " +
                "else { window.location.href='https://ggwins.site/host/index.html'; }",
                null
            );
            Toast.makeText(this, "🔒 Admin Terminal Locked", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        lastBackgroundTime = System.currentTimeMillis();
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (BuildConfig.IS_ADMIN_APP && lastBackgroundTime > 0) {
            long elapsed = System.currentTimeMillis() - lastBackgroundTime;
            // Auto-lock security policy: lock terminal if app was backgrounded for > 45 seconds
            if (elapsed > 45000) {
                lockTerminal();
            }
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    private void configureWebView() {
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        s.setSupportZoom(false);
        s.setBuiltInZoomControls(false);
        s.setDisplayZoomControls(false);
        s.setLoadWithOverviewMode(true);
        s.setUseWideViewPort(true);
        s.setMediaPlaybackRequiresUserGesture(false);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            s.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        }

        // Custom User Agent identification
        String defaultUA = s.getUserAgentString();
        String appTag = BuildConfig.IS_ADMIN_APP ? " GGWinsAdminApp/1.1 (Android)" : " GGWinsApp/1.1 (Android)";
        s.setUserAgentString(defaultUA + appTag);

        // Bind native notification bridge for real-time WhatsApp-style alerts
        webView.addJavascriptInterface(new AndroidNotificationBridge(), "AndroidBridge");

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return handleCustomUri(request.getUrl().toString());
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return handleCustomUri(url);
            }

            private boolean handleCustomUri(String url) {
                if (url == null) return false;

                // Handle UPI payment links
                if (url.startsWith("upi://") || url.startsWith("whatsapp://") || 
                    url.startsWith("intent://") || url.startsWith("phonepe://") || 
                    url.startsWith("paytmmp://") || url.startsWith("gpay://")) {
                    try {
                        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                        startActivity(intent);
                        return true;
                    } catch (Exception e) {
                        Toast.makeText(MainActivity.this, "No external app found for this request.", Toast.LENGTH_SHORT).show();
                        return true;
                    }
                }

                // If within ggwins.site, keep inside WebView
                if (url.contains("ggwins.site")) {
                    return false;
                }

                // External links open in browser
                try {
                    Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                    startActivity(browserIntent);
                    return true;
                } catch (Exception e) {
                    return false;
                }
            }

            @Override
            public void onPageStarted(WebView view, String url, Bitmap favicon) {
                progressBar.setVisibility(View.VISIBLE);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                progressBar.setVisibility(View.GONE);
                swipeRefreshLayout.setRefreshing(false);
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                progressBar.setProgress(newProgress);
                if (newProgress == 100) {
                    progressBar.setVisibility(View.GONE);
                } else {
                    progressBar.setVisibility(View.VISIBLE);
                }
            }

            // File Chooser for UTR screenshot proof uploads
            @Override
            public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, FileChooserParams fileChooserParams) {
                if (MainActivity.this.filePathCallback != null) {
                    MainActivity.this.filePathCallback.onReceiveValue(null);
                }
                MainActivity.this.filePathCallback = filePathCallback;

                Intent intent = fileChooserParams.createIntent();
                try {
                    startActivityForResult(intent, FILE_CHOOSER_REQUEST_CODE);
                } catch (Exception e) {
                    MainActivity.this.filePathCallback = null;
                    return false;
                }
                return true;
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == FILE_CHOOSER_REQUEST_CODE) {
            if (filePathCallback == null) return;
            Uri[] results = null;
            if (resultCode == Activity.RESULT_OK && data != null) {
                String dataString = data.getDataString();
                if (dataString != null) {
                    results = new Uri[]{Uri.parse(dataString)};
                } else if (data.getClipData() != null) {
                    int numSelected = data.getClipData().getItemCount();
                    results = new Uri[numSelected];
                    for (int i = 0; i < numSelected; i++) {
                        results[i] = data.getClipData().getItemAt(i).getUri();
                    }
                }
            }
            filePathCallback.onReceiveValue(results);
            filePathCallback = null;
        }
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
