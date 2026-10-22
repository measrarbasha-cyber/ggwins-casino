package site.ggwins.app;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.media.AudioAttributes;
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

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

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
    private ScheduledExecutorService backgroundPoller;
    private int lastKnownPendingDeposits = -1;

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
            startAdminDepositNotificationPoller();
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
            channel.setVibrationPattern(new long[]{0, 250, 100, 250}); // WhatsApp double-vibe
            channel.setLockscreenVisibility(NotificationCompat.VISIBILITY_PUBLIC);

            AudioAttributes audioAttributes = new AudioAttributes.Builder()
                    .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                    .setUsage(AudioAttributes.USAGE_NOTIFICATION_COMMUNICATION_INSTANT)
                    .build();
            channel.setSound(RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION), audioAttributes);

            NotificationManager notificationManager = getSystemService(NotificationManager.class);
            if (notificationManager != null) {
                notificationManager.createNotificationChannel(channel);
            }
        }
    }

    private void showWhatsAppSystemNotification(String title, String message, String type) {
        Uri defaultSoundUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);

        Intent intent = new Intent(this, MainActivity.class);
        intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);
        intent.putExtra("OPEN_TARGET", HOST_URL);
        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            flags |= PendingIntent.FLAG_IMMUTABLE;
        }
        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, intent, flags);

        NotificationCompat.Builder builder = new NotificationCompat.Builder(this, CHANNEL_ID)
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle(title)
                .setContentText(message)
                .setStyle(new NotificationCompat.BigTextStyle().bigText(message))
                .setPriority(NotificationCompat.PRIORITY_MAX)
                .setDefaults(NotificationCompat.DEFAULT_ALL)
                .setSound(defaultSoundUri)
                .setVibrate(new long[]{0, 250, 100, 250})
                .setAutoCancel(true)
                .setContentIntent(pendingIntent)
                .setCategory(NotificationCompat.CATEGORY_MESSAGE);

        NotificationManagerCompat notificationManager = NotificationManagerCompat.from(this);
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) == PackageManager.PERMISSION_GRANTED || Build.VERSION.SDK_INT < Build.VERSION_CODES.TIRAMISU) {
            try {
                notificationManager.notify((int) System.currentTimeMillis(), builder.build());
            } catch (Exception ignored) {}
        }
    }

    private void startAdminDepositNotificationPoller() {
        if (!BuildConfig.IS_ADMIN_APP) return;
        if (backgroundPoller != null && !backgroundPoller.isShutdown()) return;

        backgroundPoller = Executors.newSingleThreadScheduledExecutor();
        backgroundPoller.scheduleWithFixedDelay(() -> {
            try {
                URL url = new URL("https://ggwins.site/api/all-deposits");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(5000);
                conn.setRequestProperty("User-Agent", "GGWinsAdminApp/1.1 (BackgroundPoller)");

                if (conn.getResponseCode() == 200) {
                    BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                    StringBuilder sb = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        sb.append(line);
                    }
                    reader.close();

                    JSONObject json = new JSONObject(sb.toString());
                    JSONArray deposits = json.optJSONArray("deposits");
                    if (deposits != null) {
                        int pendingCount = 0;
                        JSONObject newestDeposit = null;
                        for (int i = 0; i < deposits.length(); i++) {
                            JSONObject d = deposits.getJSONObject(i);
                            if ("Pending".equalsIgnoreCase(d.optString("status"))) {
                                pendingCount++;
                                if (newestDeposit == null) {
                                    newestDeposit = d;
                                }
                            }
                        }

                        // If new deposit arrived or first run with pending deposits
                        if (lastKnownPendingDeposits != -1 && pendingCount > lastKnownPendingDeposits && newestDeposit != null) {
                            double amount = newestDeposit.optDouble("amount", 0.0);
                            String user = newestDeposit.optString("username", "Player");
                            String utr = newestDeposit.optString("utr", "N/A");
                            String title = String.format("💰 New Deposit: ₹%,.2f", amount);
                            String subtitle = String.format("From @%s • UTR: %s • Tap to approve", user, utr);

                            runOnUiThread(() -> showWhatsAppSystemNotification(title, subtitle, "deposit"));
                        }
                        lastKnownPendingDeposits = pendingCount;
                    }
                }
            } catch (Exception ignored) {}
        }, 2, 4, TimeUnit.SECONDS);
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        if (intent != null && intent.hasExtra("OPEN_TARGET")) {
            String target = intent.getStringExtra("OPEN_TARGET");
            if (webView != null && target != null) {
                webView.loadUrl(target);
            }
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

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (backgroundPoller != null && !backgroundPoller.isShutdown()) {
            backgroundPoller.shutdownNow();
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
