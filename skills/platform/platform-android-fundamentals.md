# Android Fundamentals - Platform Core Components

---
description: Master Android platform core components - Activities, Fragments, Lifecycle, Services, Intent system, and component communication
capabilities:
  - Activity lifecycle management and stack management
  - Fragment lifecycle and transactions
  - Service creation and lifecycle (foreground, background, bound)
  - Intent system (explicit, implicit, intent filters)
  - BroadcastReceiver and local broadcasts
  - ContentProvider and data access patterns
  - Lifecycle-aware components with modern AndroidX
  - State management across configuration changes
  - Process death recovery and state persistence
  - Permission handling and runtime permissions
---

## 1. ACTIVITIES - Foundation of Android UI

### What is an Activity?

An Activity represents a single screen with a user interface. It's the fundamental building block of Android app UI. Activities manage the UI window and lifecycle events.

```kotlin
class MainActivity : AppCompatActivity() {
    // Activity is the single window in the foreground
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Initialize UI components, setup observers
    }
}
```

### Activity Lifecycle - Complete Flow

The Activity lifecycle has 7 key callback methods:

```
┌─────────────────────────────────────────────┐
│         USER LAUNCHES APP                   │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   onCreate()         │ (required) - Called once when Activity is created
        │   - Inflate layouts  │           - Cannot show dialogs
        │   - Initialize vars  │           - Use savedInstanceState to restore state
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   onStart()          │ (required) - Activity becoming visible
        │   - Register         │           - UI is in background but visible
        │     observers        │           - Activity about to interact with user
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   onResume()         │ (required) - Activity in foreground
        │   - Start animations │           - User can interact with Activity
        │   - Acquire camera   │           - Most frequently overridden
        │   - Acquire resources│
        └──────────┬───────────┘
                   │
        ┌──────────┴──────────┐
        │   ACTIVITY RUNNING  │
        │   (Interacting)     │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────────┐
        │  USER PRESSES BACK/     │
        │  ANOTHER ACTIVITY OPENS │
        └──────────┬──────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │   onPause()          │ - Activity partially visible
        │   - Pause animations │ - Another Activity is in foreground (translucent/small)
        │   - Release camera   │ - Activity still visible
        │   - Stop broadcasts  │ - Very brief duration
        │   - Release sensors  │ - onResume() follows or onStop()
        └──────────┬───────────┘
                   │
         ┌─────────┴──────────────┐
         │   (pause briefly)      │
         │   (can resume)         │
         └─────────┬──────────────┘
                   │
         ┌─────────▼────────────────────┐
         │ NO (return to activity) │ YES (activity not visible) │
         └─────────┬──────────────┘
                   │
           ┌───────▼──────────┐
           │   onResume()     │        (back button or new activity)
           │   - Restart UI   │
           └──────────────────┘
                                        │
                                ┌───────▼──────────┐
                                │   onStop()       │ - Activity not visible
                                │   - Unregister   │ - Another Activity is visible
                                │     observers    │ - May be destroyed or restarted
                                │   - Cleanup      │ - Good place for cleanup
                                └────────┬─────────┘
                                         │
                            ┌────────────┴────────────┐
                            │                         │
                      (reshow activity) (destroy)     │
                            │                         │
                    ┌───────▼──────────┐   ┌──────────▼──────────┐
                    │   onStart()      │   │   onDestroy()       │
                    │   (restart)      │   │   - Final cleanup   │
                    └──────────────────┘   │   - Unregister      │
                                           │   - Release all res │
                                           └─────────────────────┘
```

### Key Lifecycle States

| State | Visible | Foreground | Can Interact | Notes |
|-------|---------|-----------|--------------|-------|
| onCreate→onStart | NO | NO | NO | Initializing |
| onStart→onResume | YES | NO | NO | Partially visible, dialog on top |
| onResume | YES | YES | YES | Full control, user can interact |
| onPause→onStop | YES→NO | NO | NO | Losing visibility |
| onStop | NO | NO | NO | Invisible, may be killed |
| onDestroy | NO | NO | NO | Being destroyed |

### Important Activity Concepts

```kotlin
// Task and Back Stack
// When Activity A starts Activity B:
// Back Stack: [A] → [A, B]
// Press back: destroys B, returns to A

// Process Death - System can kill Activity in onStop() to free memory
// Save state in onSaveInstanceState()
override fun onSaveInstanceState(outState: Bundle) {
    super.onSaveInstanceState(outState)
    outState.putString("important_data", myData)
    // Automatically saved by OS
}

// Restore state in onCreate()
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    if (savedInstanceState != null) {
        myData = savedInstanceState.getString("important_data")
    }
}

// Modern approach using ViewModel (survives configuration changes)
class MyActivity : AppCompatActivity() {
    private val viewModel: MyViewModel by viewModels()
    // ViewModel survives Activity recreation from rotation
}
```

---

## 2. FRAGMENTS - Modular UI Components

### What is a Fragment?

A Fragment represents a reusable portion of an app's UI that has its own layout, lifecycle, and input handling. Fragments are always hosted by an Activity.

```kotlin
class UserDetailFragment : Fragment() {
    private val viewModel: UserDetailViewModel by viewModels()
    private var _binding: FragmentUserDetailBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentUserDetailBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Setup UI after view is created
        viewModel.user.observe(viewLifecycleOwner) { user ->
            binding.userName.text = user.name
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null // Prevent memory leaks
    }
}
```

### Fragment Lifecycle - Complete Flow

Fragments have MORE callbacks than Activities because they depend on their host Activity:

```
┌────────────────────────────────────────────┐
│   Host Activity created                    │
└──────────────┬───────────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │   onAttach()         │ - Fragment attached to Activity
    │   - Fragment added   │ - Access Activity available via getActivity()
    │   - Can access       │ - Fragment not yet initialized
    │     Activity         │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │   onCreate()         │ - Fragment initializing
    │   - Initialize vars  │ - savedInstanceState available
    │   - Not UI yet       │ - No ViewGroup parent yet
    │   - Get args         │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │ onCreateView()       │ - Inflate layout
    │ - Inflate layout     │ - Return root View
    │ - Build hierarchy    │ - Container is parent ViewGroup (nullable)
    │ - Return root View   │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │ onViewCreated()      │ - View hierarchy created
    │ - Access views       │ - Setup UI, animations
    │ - Setup listeners    │ - Setup observers (use viewLifecycleOwner)
    │ - Setup observers    │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │   onStart()          │ - Fragment becoming visible
    │   - Start observing  │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │   onResume()         │ - Fragment in foreground
    │   - Start animations │ - User can interact
    │   - Resume work      │
    └──────────┬───────────┘
               │
    ┌──────────┴────────────┐
    │  FRAGMENT ACTIVE      │
    │  (Interacting)        │
    └──────────┬────────────┘
               │
    ┌──────────▼────────────┐
    │ Fragment replacement  │
    │ or popBackStack()     │
    └──────────┬────────────┘
               │
               ▼
    ┌──────────────────────┐
    │   onPause()          │ - Fragment partially visible
    │   - Pause animations │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │   onStop()           │ - Fragment not visible
    │   - Stop observing   │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │ onDestroyView()      │ - View hierarchy destroyed
    │ - Cleanup views      │ - Fragment still exists
    │ - Clear references   │ - Activity still exists
    │ - Null binding       │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │   onDestroy()        │ - Fragment being destroyed
    │   - Cleanup vars     │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │   onDetach()         │ - Fragment detached from Activity
    │   - Fragment removed │ - Activity reference lost
    │   - Final cleanup    │
    └──────────────────────┘
```

### Fragment Lifecycle States

| State | View Exists | Visible | Foreground | Can Interact |
|-------|-------------|---------|-----------|--------------|
| onAttach→onCreate | NO | NO | NO | No (initializing) |
| onCreateView | Creating | NO | NO | No (view building) |
| onViewCreated→onStart | YES | NO | NO | No (background) |
| onResume | YES | YES | YES | YES (full control) |
| onPause→onStop | YES→NO | NO | NO | No (losing focus) |
| onDestroyView | NO | NO | NO | No (view removed) |
| onDestroy | NO | NO | NO | No (finalizing) |

### Fragment Transactions

```kotlin
// Add Fragment to Activity
supportFragmentManager.beginTransaction()
    .add(R.id.container, UserFragment(), "user_tag")
    .addToBackStack(null)
    .commit()

// Replace Fragment (old is removed)
supportFragmentManager.beginTransaction()
    .replace(R.id.container, DetailsFragment())
    .addToBackStack(null)
    .commit()

// Navigate back (pop from back stack)
supportFragmentManager.popBackStack()

// Important: Use commitNow() for immediate execution
// Use commit() for queued execution (safer, handles state loss)
```

### Fragment Arguments Pattern

```kotlin
class UserFragment : Fragment() {
    private val args: UserFragmentArgs by navArgs()

    // Or manual arguments
    companion object {
        const val USER_ID = "user_id"

        fun newInstance(userId: String) = UserFragment().apply {
            arguments = Bundle().apply {
                putString(USER_ID, userId)
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val userId = arguments?.getString(USER_ID)
    }
}
```

---

## 3. LIFECYCLE AWARENESS - Modern Best Practices

### Using Lifecycle-Aware Components (AndroidX)

```kotlin
// Modern approach: lifecycleScope
class UserFragment : Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Automatically respects Fragment lifecycle
        viewLifecycleOwner.lifecycleScope.launch {
            viewModel.userFlow
                .flowWithLifecycle(viewLifecycleOwner.lifecycle, Lifecycle.State.STARTED)
                .collect { user ->
                    updateUI(user)
                }
        }
    }
}

// Old approach (don't use - memory leaks):
// Regular coroutine scope doesn't respect lifecycle
// lifecycleScope.launch {
//     viewModel.user.observe(this) { ... }  // Wrong! Loses reference
// }
```

### Lifecycle-Aware Services

```kotlin
class LocationService : Service() {
    private val locationManager by lazy {
        getSystemService(Context.LOCATION_SERVICE) as LocationManager
    }

    override fun onCreate() {
        super.onCreate()
        // Service-level lifecycle awareness
        lifecycle.addObserver(object : LifecycleEventObserver {
            override fun onStateChanged(source: LifecycleOwner, event: Lifecycle.Event) {
                when (event) {
                    Lifecycle.Event.ON_START -> startLocationUpdates()
                    Lifecycle.Event.ON_STOP -> stopLocationUpdates()
                    else -> {}
                }
            }
        })
    }

    override fun onBind(intent: Intent): IBinder? = null
}
```

---

## 4. SERVICES - Background Work

### What is a Service?

A Service is an application component that runs in the background without a user interface. Services perform long-running operations.

### Service Types and Lifycycle

```
                    startService()
                         │
         ┌────────────────┴────────────────┐
         │                                 │
         ▼                                 ▼
    ┌─────────────┐              ┌──────────────┐
    │   onBind()  │              │ onCreate()   │
    │   (none)    │              │              │
    └─────────────┘              └──────┬───────┘
                                        │
                                        ▼
                                   ┌──────────────┐
                                   │ onStartCommand()│
                                   │ (keeps running)│
                                   └──────┬────────┘
                                          │
                        ┌─────────────────┴──────────────┐
                        │                                │
                   (continue)                       stopService()
                        │                            or stopSelf()
                        │                                │
         ┌──────────────▼──────────────┐      ┌────────▼────────┐
         │  Multiple onStartCommand()  │      │  onDestroy()    │
         │  calls (queued)             │      │  (cleanup)      │
         │                             │      └─────────────────┘
         └──────────────┬──────────────┘
                        │
```

### Service Types

#### 1. Started Service (Unbounded)

```kotlin
// Start a service
class LocationService : Service() {
    private val locationManager by lazy {
        getSystemService(Context.LOCATION_SERVICE) as LocationManager
    }

    override fun onCreate() {
        super.onCreate()
        // Initialize once
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Called each time startService() is called
        // startId is unique, used for stopSelfResult()

        val location = intent?.getStringExtra("location")
        startTracking(location)

        // Return how to behave if killed:
        // START_STICKY: Restart service, don't redelivery intent
        // START_NOT_STICKY: Don't restart service
        // START_REDELIVER_INTENT: Restart with original intent
        return START_STICKY
    }

    private fun startTracking(location: String) {
        // Background work
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        super.onDestroy()
        // Cleanup
    }
}

// In Activity:
val intent = Intent(this, LocationService::class.java)
    .putExtra("location", "home")
startService(intent)

stopService(intent)
```

#### 2. Bound Service

```kotlin
// Bind a service for IPC (Inter-Process Communication)
class MusicService : Service() {
    private val binder = MusicBinder()

    inner class MusicBinder : Binder() {
        fun getService(): MusicService = this@MusicService
    }

    fun playMusic() {
        // Play music
    }

    override fun onBind(intent: Intent?): IBinder = binder
}

// In Activity:
class MusicActivity : AppCompatActivity() {
    private lateinit var musicService: MusicService
    private var isBound = false

    private val connection = object : ServiceConnection {
        override fun onServiceConnected(
            name: ComponentName?,
            service: IBinder?
        ) {
            val binder = service as MusicService.MusicBinder
            musicService = binder.getService()
            isBound = true
        }

        override fun onServiceDisconnected(name: ComponentName?) {
            isBound = false
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val intent = Intent(this, MusicService::class.java)
        bindService(intent, connection, Context.BIND_AUTO_CREATE)
    }

    override fun onDestroy() {
        super.onDestroy()
        if (isBound) unbindService(connection)
    }
}
```

#### 3. Foreground Service (Notifications Required - API 31+)

```kotlin
class DownloadService : Service() {

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // For API 31+, must be called within 10 seconds
        createNotificationChannel()
        startForeground(NOTIFICATION_ID, createNotification())

        // Long-running operation
        downloadFile()

        return START_STICKY
    }

    private fun createNotification(): Notification {
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Download")
            .setContentText("Downloading file...")
            .setSmallIcon(R.drawable.ic_download)
            .setProgress(100, 50, false)
            .build()
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Downloads",
                NotificationManager.IMPORTANCE_DEFAULT
            )
            getSystemService(NotificationManager::class.java)
                .createNotificationChannel(channel)
        }
    }

    companion object {
        const val CHANNEL_ID = "download_channel"
        const val NOTIFICATION_ID = 1
    }
}
```

---

## 5. INTENT SYSTEM - Component Communication

### Explicit Intents (Direct Navigation)

```kotlin
// Navigate to specific Activity
val intent = Intent(this, DetailActivity::class.java)
intent.putExtra("user_id", 123)
intent.putExtra("user_name", "John")
startActivity(intent)

// Receive data in DetailActivity
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)

    val userId = intent.getIntExtra("user_id", -1)
    val userName = intent.getStringExtra("user_name")
}

// Return result from Activity
class DetailActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding.saveButton.setOnClickListener {
            val result = Intent().apply {
                putExtra("edited_name", "Jane")
            }
            setResult(RESULT_OK, result)
            finish()
        }
    }
}

// Handle result in original Activity
override fun onActivityResult(
    requestCode: Int,
    resultCode: Int,
    data: Intent?
) {
    super.onActivityResult(requestCode, resultCode, data)

    if (requestCode == REQUEST_CODE && resultCode == RESULT_OK) {
        val editedName = data?.getStringExtra("edited_name")
    }
}

// Modern approach: ActivityResultContracts
private val editUserLauncher = registerForActivityResult(
    ActivityResultContracts.StartActivityForResult()
) { result ->
    if (result.resultCode == RESULT_OK) {
        val editedName = result.data?.getStringExtra("edited_name")
    }
}

// Use it:
editUserLauncher.launch(Intent(this, DetailActivity::class.java))
```

### Implicit Intents (System Resolution)

```kotlin
// Open URL
val intent = Intent(Intent.ACTION_VIEW).apply {
    data = Uri.parse("https://example.com")
}
startActivity(intent)

// Send email
val intent = Intent(Intent.ACTION_SEND).apply {
    type = "message/rfc822"
    putExtra(Intent.EXTRA_EMAIL, arrayOf("recipient@example.com"))
    putExtra(Intent.EXTRA_SUBJECT, "Subject")
    putExtra(Intent.EXTRA_TEXT, "Email body")
}
startActivity(intent)

// Share content
val intent = Intent(Intent.ACTION_SEND).apply {
    type = "text/plain"
    putExtra(Intent.EXTRA_TEXT, "Check this out!")
}
startActivity(Intent.createChooser(intent, "Share via"))

// Make phone call
val intent = Intent(Intent.ACTION_CALL).apply {
    data = Uri.parse("tel:+1234567890")
}
startActivity(intent)
// Don't forget permission: <uses-permission android:name="android.permission.CALL_PHONE" />
```

### Intent Filters (AndroidManifest.xml)

```xml
<activity
    android:name=".MainActivity"
    android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
</activity>

<!-- Handle deep links -->
<activity
    android:name=".DetailActivity"
    android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="app" android:host="detail" />
    </intent-filter>
</activity>

<!-- Implicit intent handling -->
<activity
    android:name=".ShareActivity"
    android:exported="true">
    <intent-filter>
        <action android:name="android.intent.action.SEND" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="text/plain" />
    </intent-filter>
</activity>
```

---

## 6. BROADCAST RECEIVERS - System Notifications

### What is BroadcastReceiver?

A BroadcastReceiver is a component that receives system or app broadcasts.

```kotlin
// Register receiver to listen for broadcasts
class MyBroadcastReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        when (intent?.action) {
            Intent.ACTION_BATTERY_CHANGED -> {
                val level = intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
                Log.d("Battery", "Level: $level%")
            }
        }
    }
}

// Register in Activity (context-based)
val receiver = MyBroadcastReceiver()
val filter = IntentFilter(Intent.ACTION_BATTERY_CHANGED)
registerReceiver(receiver, filter)

// Unregister
unregisterReceiver(receiver)
```

### Local Broadcasts (Within App)

```kotlin
// Send local broadcast
LocalBroadcastManager.getInstance(context).sendBroadcast(
    Intent("com.example.action.UPDATE").apply {
        putExtra("data", "some data")
    }
)

// Receive local broadcast
class LocalReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        val data = intent?.getStringExtra("data")
    }
}

val filter = IntentFilter("com.example.action.UPDATE")
LocalBroadcastManager.getInstance(context).registerReceiver(localReceiver, filter)
```

---

## 7. CONTENT PROVIDERS - Data Sharing

### What is ContentProvider?

ContentProvider manages access to structured data and provides data to other apps.

```kotlin
// Query data from ContentProvider
val cursor = contentResolver.query(
    ContactsContract.Contacts.CONTENT_URI,
    arrayOf(
        ContactsContract.Contacts._ID,
        ContactsContract.Contacts.DISPLAY_NAME
    ),
    null,
    null,
    null
)

// Read results
cursor?.use {
    while (it.moveToNext()) {
        val id = it.getLong(it.getColumnIndex(ContactsContract.Contacts._ID))
        val name = it.getString(it.getColumnIndex(ContactsContract.Contacts.DISPLAY_NAME))
    }
}

// Insert data
val values = ContentValues().apply {
    put(ContactsContract.Contacts.DISPLAY_NAME, "John Doe")
}
val uri = contentResolver.insert(ContactsContract.Contacts.CONTENT_URI, values)
```

---

## 8. MANIFEST - Component Declaration

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.app">

    <!-- Permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.CALL_PHONE" />

    <!-- Features -->
    <uses-feature android:name="android.hardware.camera" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/AppTheme">

        <!-- Activities -->
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:label="@string/app_name">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <!-- Services -->
        <service
            android:name=".LocationService"
            android:exported="false" />

        <!-- BroadcastReceivers -->
        <receiver
            android:name=".BootReceiver"
            android:exported="false">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
            </intent-filter>
        </receiver>

        <!-- ContentProviders -->
        <provider
            android:name=".UserContentProvider"
            android:authorities="com.example.app.userprovider"
            android:exported="false" />

    </application>

</manifest>
```

---

## 9. Configuration Changes - Handling Rotation

### Problem: Activity Destroyed on Rotation

```
Rotation occurs
    │
    ▼
onPause() called
onStop() called
onDestroy() called
    │
    ▼
NEW Activity instance created
    │
    ▼
onCreate() called (savedInstanceState is NOT null)
onStart() called
onResume() called
```

### Solution 1: ViewModel (Recommended)

```kotlin
class MainViewModel : ViewModel() {
    private val _data = MutableLiveData<String>()
    val data: LiveData<String> = _data

    // ViewModel survives Activity recreation
}

class MainActivity : AppCompatActivity() {
    private val viewModel: MainViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // ViewModel data persists across configuration changes
        viewModel.data.observe(this) { value ->
            // Update UI
        }
    }
}
```

### Solution 2: onSaveInstanceState

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)

    if (savedInstanceState != null) {
        val savedData = savedInstanceState.getString("my_data")
    }
}

override fun onSaveInstanceState(outState: Bundle) {
    super.onSaveInstanceState(outState)
    outState.putString("my_data", myData)
    // Called before onStop()
}
```

### Solution 3: Prevent Destruction (Not Recommended)

```xml
<!-- In AndroidManifest.xml -->
<activity
    android:name=".MainActivity"
    android:configChanges="orientation|screenSize"
    android:label="@string/app_name" />
```

Then handle rotation:

```kotlin
override fun onConfigurationChanged(newConfig: Configuration) {
    super.onConfigurationChanged(newConfig)

    when (newConfig.orientation) {
        Configuration.ORIENTATION_PORTRAIT -> {
            // Handle portrait
        }
        Configuration.ORIENTATION_LANDSCAPE -> {
            // Handle landscape
        }
    }
}
```

---

## 10. Process Death & State Recovery

### Understanding Process Death

- System can kill app process in onStop() to free memory
- User doesn't see this (Activity stack exists)
- When user returns, system recreates Activity from saved state

```kotlin
// Prepare for death
override fun onSaveInstanceState(outState: Bundle) {
    super.onSaveInstanceState(outState)
    outState.putString("user_id", userId)
    outState.putInt("score", score)
}

// Recover from death
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)

    userId = savedInstanceState?.getString("user_id") ?: ""
    score = savedInstanceState?.getInt("score") ?: 0
}
```

### Modern State Management with SavedStateHandle

```kotlin
class MyViewModel(savedStateHandle: SavedStateHandle) : ViewModel() {
    // Automatically saves and restores across process death
    val userId: LiveData<String> = savedStateHandle.getLiveData("user_id", "")

    fun setUserId(id: String) {
        savedStateHandle["user_id"] = id
    }
}

// In Activity:
private val viewModel: MyViewModel by viewModels()
```

---

## 11. Fragment Communication

### Parent-Fragment Communication

```kotlin
// Fragment to Activity
interface UserListener {
    fun onUserSelected(userId: String)
}

class UserFragment : Fragment() {
    private var listener: UserListener? = null

    override fun onAttach(context: Context) {
        super.onAttach(context)
        listener = context as? UserListener
    }

    private fun notifyUserSelected(userId: String) {
        listener?.onUserSelected(userId)
    }

    override fun onDetach() {
        super.onDetach()
        listener = null
    }
}

// Activity implements interface
class MainActivity : AppCompatActivity(), UserListener {
    override fun onUserSelected(userId: String) {
        // Handle selection
    }
}
```

### Fragment-to-Fragment Communication (Recommended)

```kotlin
// Share ViewModel
class SharedViewModel : ViewModel() {
    private val _selectedUser = MutableLiveData<String>()
    val selectedUser: LiveData<String> = _selectedUser

    fun selectUser(userId: String) {
        _selectedUser.value = userId
    }
}

// Fragment 1 (List)
class UserListFragment : Fragment() {
    private val viewModel: SharedViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        userAdapter.onItemClick = { user ->
            viewModel.selectUser(user.id)
        }
    }
}

// Fragment 2 (Detail)
class UserDetailFragment : Fragment() {
    private val viewModel: SharedViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        viewModel.selectedUser.observe(viewLifecycleOwner) { userId ->
            loadUserDetails(userId)
        }
    }
}
```

---

## 12. Permission Handling

### Runtime Permissions (API 23+)

```kotlin
// Check if permission is granted
if (ContextCompat.checkSelfPermission(
    this,
    Manifest.permission.ACCESS_FINE_LOCATION
) == PackageManager.PERMISSION_GRANTED) {
    // Permission granted
    getLocation()
} else {
    // Request permission
    ActivityCompat.requestPermissions(
        this,
        arrayOf(Manifest.permission.ACCESS_FINE_LOCATION),
        PERMISSION_REQUEST_CODE
    )
}

// Handle response
override fun onRequestPermissionsResult(
    requestCode: Int,
    permissions: Array<String>,
    grantResults: IntArray
) {
    super.onRequestPermissionsResult(requestCode, permissions, grantResults)

    if (requestCode == PERMISSION_REQUEST_CODE) {
        if (grantResults.isNotEmpty() &&
            grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            getLocation()
        } else {
            // Permission denied
        }
    }
}

// Modern approach: RequestPermission contract
private val requestLocationPermission = registerForActivityResult(
    ActivityResultContracts.RequestPermission()
) { isGranted ->
    if (isGranted) {
        getLocation()
    }
}

// Use it:
requestLocationPermission.launch(Manifest.permission.ACCESS_FINE_LOCATION)
```

---

## Learning Hours Breakdown

- **Activities & Lifecycle**: 12-15 hours
  - Lifecycle methods and states
  - Task and back stack management
  - Activity recovery and state persistence
  - Configuration changes

- **Fragments & Fragment Lifecycle**: 12-15 hours
  - Fragment basics and transactions
  - Fragment lifecycle in depth
  - Fragment communication patterns
  - Nested fragments

- **Services**: 8-10 hours
  - Started services
  - Bound services and IPC
  - Foreground services
  - Service lifecycle

- **Intent System**: 6-8 hours
  - Explicit and implicit intents
  - Intent filters
  - Data passing between components
  - Deep linking

- **BroadcastReceiver & ContentProvider**: 6-8 hours
  - System broadcasts
  - Local broadcasts
  - Content provider basics
  - Data sharing

- **Modern Lifecycle-Aware Components**: 4-6 hours
  - lifecycleScope
  - flowWithLifecycle
  - Lifecycle observers
  - SavedStateHandle

- **Practical Implementation**: 10-15 hours
  - Building sample apps
  - Handling edge cases
  - Performance optimization
  - Testing

**Total: 58-77 hours** (8-10 weeks of study with 8 hours/week)

---

## Key Takeaways

1. ✅ Always respect lifecycle callbacks
2. ✅ Use ViewModel for state management across configuration changes
3. ✅ Implement Fragment communication via shared ViewModel
4. ✅ Use lifecycleScope for lifecycle-aware coroutines
5. ✅ Properly manage resources (cleanup in appropriate callbacks)
6. ✅ Handle process death with savedInstanceState or ViewModel
7. ✅ Use Navigation component for Fragment navigation
8. ✅ Request permissions at runtime (API 23+)
9. ✅ Implement proper error handling
10. ✅ Test with configuration changes (rotation)

---

## Essential Resources

- [Android Lifecycle Guide](https://developer.android.com/guide/components/activities/activity-lifecycle)
- [Fragment Documentation](https://developer.android.com/guide/fragments)
- [Service Components](https://developer.android.com/guide/components/services)
- [Intent System](https://developer.android.com/guide/components/intents-filters)
- [BroadcastReceiver](https://developer.android.com/guide/components/broadcasts)
- [ContentProvider Guide](https://developer.android.com/guide/topics/providers)
