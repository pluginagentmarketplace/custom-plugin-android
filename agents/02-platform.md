---
description: Android core components - Activities, Fragments, Services, Lifecycle, Intent system, Permissions - Android platform fundamentals (78 hours)
capabilities: ["Activity lifecycle management", "Fragment framework", "Service implementation", "Intent system", "BroadcastReceiver", "ContentProvider", "Permissions handling", "Process lifecycle", "Configuration changes", "Back stack management"]
prerequisites: ["Fundamentals"]
keywords: ["activity", "fragment", "service", "intent", "lifecycle", "permission", "broadcast", "content provider"]
---

# Platform Agent: Android Core Components & Lifecycle Management

Master Android's component model and lifecycle management. Understand Activities, Fragments, Services, and how they interact through Intents. Learn to handle configuration changes, manage background operations, and implement proper permission handling.

**Prerequisite**: Fundamentals agent (Kotlin, OOP, SOLID)
**Duration**: 78 hours | **Level**: Beginner to Intermediate
**Topics**: 8 major areas | **Code Examples**: 35+ real-world patterns

---

## 1. ACTIVITY LIFECYCLE & MANAGEMENT

Activities are the visible UI component lifecycle. Understanding the complete lifecycle is critical for proper state management.

### 1.1 Complete Activity Lifecycle (6 States)

```
onCreate → onStart → onResume → [USER INTERACTION]
                              ↓
                         onPause → onStop → onDestroy
                              ↑_________|
                         (User returns)
```

**Complete Lifecycle with Callbacks:**

```kotlin
class MainActivity : AppCompatActivity() {

    // 1. onCreate(): Called when activity is first created
    // When: Process created OR activity created (not killed)
    // State: Activity NOT visible, can initialize UI and restore state
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Initialize UI components
        val viewModel: MainViewModel by viewModels()

        // Restore saved instance state
        savedInstanceState?.let {
            val savedValue = it.getString("key")
        }
    }

    // 2. onStart(): Called when activity becomes visible
    // When: After onCreate OR after onStop
    // State: Activity visible but NOT in foreground
    // Note: onStart ↔ onStop protect "visible" resource acquisition
    override fun onStart() {
        super.onStart()
        registerSensorListener()  // Acquire resources
    }

    // 3. onResume(): Called when activity gains focus
    // When: After onStart OR after onPause
    // State: Activity in foreground, receives user input
    // Note: onResume ↔ onPause protect "focused" resource acquisition
    override fun onResume() {
        super.onResume()
        startCamera()      // Camera requires focus
        startAnimation()   // Resume animations
    }

    // 4. onPause(): Called when activity loses focus
    // When: Another activity gains focus (transparent or translucent)
    // State: Activity partially visible but NOT in foreground
    // Critical: Keep this short! Next activity won't start until this finishes
    override fun onPause() {
        super.onPause()
        stopCamera()       // Release focus-dependent resources
        pauseAnimation()   // Pause animations
    }

    // 5. onStop(): Called when activity is no longer visible
    // When: Another activity fully covers this OR user navigates away
    // State: Activity NOT visible to user
    override fun onStop() {
        super.onStop()
        unregisterSensorListener()  // Release resources
        saveSessionData()
    }

    // 6. onDestroy(): Called before activity is destroyed
    // When: Activity finishing OR system destroying to free memory
    // State: Activity being removed from memory
    override fun onDestroy() {
        super.onDestroy()
        viewModel.cleanup()  // Final cleanup
    }
}
```

### 1.2 Configuration Changes (Rotation, Locale, etc.)

By default, configuration change (e.g., rotation) destroys and recreates activity:

```
[Current State] → onPause → onStop → onDestroy
                           → onCreate → onStart → onResume
                           [NEW State]
```

**Problem**: User data lost! **Solution**: Save/Restore state

**Option 1: Handle in onSaveInstanceState**

```kotlin
class DataActivity : AppCompatActivity() {
    private var userData: String = ""

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        // Called BEFORE onStop, guaranteed to be called before destroy
        outState.putString("user_data", userData)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        savedInstanceState?.let {
            userData = it.getString("user_data", "")
        }
    }
}
```

**Option 2: Prevent Recreation with configChanges**

```xml
<!-- AndroidManifest.xml -->
<activity
    android:name=".MainActivity"
    android:configChanges="orientation|screenSize"
    android:screenOrientation="portrait" />
```

When handled:
```
[Current State] → onPause → onStop → onConfigurationChanged
                                   → onStart → onResume
                        [State Preserved!]
```

**Option 3: Use ViewModel (RECOMMENDED)**

```kotlin
@HiltViewModel
class DataViewModel @Inject constructor(
    private val repository: DataRepository
) : ViewModel() {
    // ViewModel survives configuration changes!
    private val _userData = MutableLiveData<User>()
    val userData: LiveData<User> = _userData
}

class DataActivity : AppCompatActivity() {
    private val viewModel: DataViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // ViewModel already has data from previous configuration
        viewModel.userData.observe(this) { user ->
            updateUI(user)
        }
    }
}
```

### 1.3 Activity Launch Modes

Control how activity instances are created and managed in back stack:

**Mode 1: STANDARD (Default)**
```
Intent → [Activity A] → [Activity B] → [Activity B] → [Activity B]
         ↑              ↑              ↑              ↑
         1st            2nd            3rd            4th instance
```
Always creates new instance regardless of stack contents.

**Mode 2: SINGLE_TOP**
```
If activity at top of stack → onNewIntent() called instead of onCreate()

Intent → [Activity A] → [Activity B]
         ↑              ↑
         [Duplicate B sent]

Result:  [Activity A] → [Activity B]  (NO new instance created)
                       onNewIntent() called
```

**Mode 3: SINGLE_TASK**
```
If activity exists in stack → clear everything above it → onNewIntent()

Stack: [A] → [B] → [C] → [D]
Intent to B with SINGLE_TASK:
Result: [A] → [B]
        (C and D removed, B's onNewIntent() called)
```

**Mode 4: SINGLE_INSTANCE**
```
Activity in isolated stack. Always only one instance.

App A Stack: [A] → [B]
App B Stack: [SingletonService]
```

**Declaration in AndroidManifest.xml**:
```xml
<activity
    android:name=".DetailActivity"
    android:launchMode="singleTop" />
```

**Or with Intent Flags**:
```kotlin
val intent = Intent(this, DetailActivity::class.java).apply {
    flags = Intent.FLAG_ACTIVITY_SINGLE_TOP
}
startActivity(intent)
```

### 1.4 Back Stack Management

Android maintains a back stack (LIFO - Last In First Out):

```kotlin
// Standard back navigation
override fun onBackPressed() {
    super.onBackPressed()  // Pops current activity
}

// Navigate with back stack
val intent = Intent(this, DetailActivity::class.java)
startActivity(intent)  // Pushed to back stack

// Pop back stack
onBackPressedDispatcher.onBackPressed()

// Control back behavior
override fun onBackPressed() {
    if (shouldShowConfirmation()) {
        showExitConfirmation()
    } else {
        super.onBackPressed()  // Default behavior
    }
}
```

---

## 2. FRAGMENT LIFECYCLE & COMMUNICATION

Fragments are reusable UI components with their own lifecycle, dependent on host Activity's lifecycle.

### 2.1 Complete Fragment Lifecycle (10 Callbacks)

```
onAttach → onCreate → onCreateView → onViewCreated → onStart → onResume
                                 [USER INTERACTION]
                              ↓
onPause → onStop → onDestroyView → onDestroy → onDetach
```

**All 10 Callbacks with Explanations**:

```kotlin
class DetailFragment : Fragment() {

    // 1. onAttach(): Fragment attached to Activity
    // When: Before onCreate
    // Use: Get reference to hosting activity
    override fun onAttach(context: Context) {
        super.onAttach(context)
        // context is the hosting Activity
    }

    // 2. onCreate(): Fragment being created (NOT UI yet)
    // When: After onAttach
    // Use: Initialize non-UI state, arguments retrieval
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Retrieve arguments safely
        val itemId = arguments?.getInt("item_id") ?: 0
    }

    // 3. onCreateView(): Inflate fragment layout
    // When: After onCreate, before onViewCreated
    // Returns: Root view of fragment
    // Critical: THIS is where you create UI
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_detail, container, false)
    }

    // 4. onViewCreated(): Called right after onCreateView
    // When: Fragment view created and attached
    // Use: Initialize UI elements, set listeners
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val textView: TextView = view.findViewById(R.id.text)
        textView.text = "Fragment created"
    }

    // 5. onStart(): Fragment becoming visible
    // When: After onViewCreated
    // Similar to Activity.onStart()
    override fun onStart() {
        super.onStart()
    }

    // 6. onResume(): Fragment in foreground
    // When: After onStart
    // Fragment receives user input
    override fun onResume() {
        super.onResume()
    }

    // 7. onPause(): Fragment losing focus
    override fun onPause() {
        super.onPause()
    }

    // 8. onStop(): Fragment no longer visible
    override fun onStop() {
        super.onStop()
    }

    // 9. onDestroyView(): Fragment view being destroyed
    // When: Fragment being removed or replaced
    // Use: Clean up view references (important for preventing leaks!)
    override fun onDestroyView() {
        super.onDestroyView()
        // Clear view references to prevent memory leaks
        binding = null  // if using view binding
    }

    // 10. onDestroy(): Fragment being destroyed
    override fun onDestroy() {
        super.onDestroy()
    }

    // 11. onDetach(): Fragment detached from Activity
    // When: Final callback, after onDestroy
    override fun onDetach() {
        super.onDetach()
    }
}
```

### 2.2 Fragment Communication Patterns

**Pattern 1: Shared ViewModel (RECOMMENDED)**

```kotlin
// Shared between Activity and Fragments
@HiltViewModel
class SharedViewModel @Inject constructor() : ViewModel() {
    private val _selectedItem = MutableLiveData<Item>()
    val selectedItem: LiveData<Item> = _selectedItem

    fun selectItem(item: Item) {
        _selectedItem.value = item
    }
}

// Fragment 1: Select item
class ListFragment : Fragment() {
    private val viewModel: SharedViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        listView.setOnItemClickListener { item ->
            viewModel.selectItem(item)  // Broadcast to other fragments
        }
    }
}

// Fragment 2: Listen to selection
class DetailFragment : Fragment() {
    private val viewModel: SharedViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        viewModel.selectedItem.observe(viewLifecycleOwner) { item ->
            displayItem(item)
        }
    }
}
```

**Pattern 2: Fragment Arguments Bundle**

```kotlin
// Create fragment with arguments
class DetailFragment : Fragment() {
    companion object {
        fun newInstance(itemId: Int): DetailFragment {
            return DetailFragment().apply {
                arguments = Bundle().apply {
                    putInt("item_id", itemId)
                }
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val itemId = arguments?.getInt("item_id") ?: 0
    }
}

// Use it
val fragment = DetailFragment.newInstance(itemId = 123)
supportFragmentManager.beginTransaction()
    .replace(R.id.fragment_container, fragment)
    .addToBackStack(null)
    .commit()
```

**Pattern 3: Interface Listener (Legacy)**

```kotlin
interface OnItemSelectedListener {
    fun onItemSelected(item: Item)
}

class ListFragment : Fragment() {
    private var listener: OnItemSelectedListener? = null

    override fun onAttach(context: Context) {
        super.onAttach(context)
        listener = context as? OnItemSelectedListener
    }

    override fun onDetach() {
        super.onDetach()
        listener = null
    }
}
```

### 2.3 Fragment Transactions

```kotlin
supportFragmentManager.beginTransaction().apply {
    // Replace fragment
    replace(R.id.container, newFragment)

    // Add to back stack for back navigation
    addToBackStack("detail")

    // Transitions
    setCustomAnimations(
        android.R.anim.fade_in,
        android.R.anim.fade_out,
        android.R.anim.fade_in,
        android.R.anim.fade_out
    )

    // Commit transaction
    commit()  // or commitNow() for immediate execution
}.also {
    it.executePendingTransactions()
}
```

---

## 3. SERVICES & BACKGROUND OPERATIONS

Services enable background operations without UI visibility.

### 3.1 Started Services

Runs indefinitely until explicitly stopped:

```kotlin
class MusicService : Service() {

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Start playing music
        playMusic()

        // Return how to restart if killed:
        // START_STICKY: Restart service, null intent
        // START_NOT_STICKY: Don't restart
        // START_REDELIVER_INTENT: Restart with original intent
        return START_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null  // Not bindable

    override fun onDestroy() {
        stopMusic()
        super.onDestroy()
    }
}

// Start service
val intent = Intent(this, MusicService::class.java)
startService(intent)

// Stop service
stopService(intent)
```

### 3.2 Bound Services

Clients connect to service, lifecycle tied to bindings:

```kotlin
class LocalService : Service() {
    private val binder = LocalBinder()

    inner class LocalBinder : Binder() {
        fun getService(): LocalService = this@LocalService
    }

    override fun onBind(intent: Intent?): IBinder = binder

    fun getData(): String = "Service data"
}

// In Activity/Fragment
class MainActivity : AppCompatActivity() {
    private lateinit var service: LocalService
    private var isBound = false

    private val connection = object : ServiceConnection {
        override fun onServiceConnected(name: ComponentName?, service: IBinder?) {
            val binder = service as LocalService.LocalBinder
            this@MainActivity.service = binder.getService()
            isBound = true
        }

        override fun onServiceDisconnected(name: ComponentName?) {
            isBound = false
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Bind to service
        val intent = Intent(this, LocalService::class.java)
        bindService(intent, connection, Context.BIND_AUTO_CREATE)
    }

    override fun onDestroy() {
        if (isBound) {
            unbindService(connection)
        }
        super.onDestroy()
    }
}
```

### 3.3 Foreground Services (API 26+)

Services with visible notification, higher priority:

```kotlin
class ForegroundService : Service() {

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val notification = createNotification()
        startForeground(NOTIFICATION_ID, notification)

        // Do actual work
        doHeavyWork()

        return START_STICKY
    }

    private fun createNotification(): Notification {
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Service Running")
            .setContentText("Processing...")
            .setSmallIcon(R.drawable.ic_service)
            .build()
    }
}

// In AndroidManifest.xml
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
```

---

## 4. INTENT SYSTEM

Intents are messages for starting components or triggering actions.

### 4.1 Explicit Intents (Direct Component)

```kotlin
// Start activity
val intent = Intent(this, DetailActivity::class.java).apply {
    putExtra("item_id", 123)
    putExtra("user_name", "John")
    putExtra("user_data", User("John", 30))  // Parcelable
}
startActivity(intent)

// In receiving activity
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)

    val itemId = intent.getIntExtra("item_id", -1)
    val userName = intent.getStringExtra("user_name")
    val user = intent.getParcelableExtra<User>("user_data")
}

// Start service
startService(Intent(this, MyService::class.java))

// Get result
startActivityForResult(intent, REQUEST_CODE)

override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
    super.onActivityResult(requestCode, resultCode, data)
    if (requestCode == REQUEST_CODE && resultCode == RESULT_OK) {
        val result = data?.getStringExtra("result")
    }
}
```

### 4.2 Implicit Intents (Action-based)

System chooses component matching intent filter:

```kotlin
// Open web URL
val intent = Intent(Intent.ACTION_VIEW).apply {
    data = Uri.parse("https://example.com")
}
startActivity(intent)

// Send email
val intent = Intent(Intent.ACTION_SEND).apply {
    type = "text/plain"
    putExtra(Intent.EXTRA_EMAIL, arrayOf("user@example.com"))
    putExtra(Intent.EXTRA_SUBJECT, "Hello")
    putExtra(Intent.EXTRA_TEXT, "Message body")
}
startActivity(intent)

// Take photo
val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
startActivityForResult(intent, REQUEST_IMAGE_CAPTURE)

// Receive implicit intents in AndroidManifest.xml
<activity android:name=".DetailActivity">
    <intent-filter>
        <action android:name="com.example.ACTION_DETAIL" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:scheme="https" android:host="example.com" />
    </intent-filter>
</activity>
```

---

## 5. BROADCAST RECEIVER

Components for receiving system broadcasts or app broadcasts.

```kotlin
// Broadcast receiver
class BatteryReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        when(intent?.action) {
            Intent.ACTION_BATTERY_LOW -> {
                Log.d(TAG, "Battery low!")
            }
            Intent.ACTION_BATTERY_OKAY -> {
                Log.d(TAG, "Battery okay")
            }
        }
    }
}

// Register in Activity
val receiver = BatteryReceiver()
val filter = IntentFilter().apply {
    addAction(Intent.ACTION_BATTERY_LOW)
    addAction(Intent.ACTION_BATTERY_OKAY)
}
registerReceiver(receiver, filter)

// Unregister (IMPORTANT!)
override fun onDestroy() {
    unregisterReceiver(receiver)
    super.onDestroy()
}
```

---

## 6. PERMISSIONS (Normal & Dangerous)

### 6.1 Normal Permissions (Auto-granted)

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

### 6.2 Dangerous Permissions (Runtime Required)

```kotlin
class MainActivity : AppCompatActivity() {

    private fun requestPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.CAMERA
            ) != PackageManager.PERMISSION_GRANTED) {

                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(Manifest.permission.CAMERA),
                    PERMISSION_REQUEST_CODE
                )
            }
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)

        if (requestCode == PERMISSION_REQUEST_CODE) {
            if (grantResults.isNotEmpty() &&
                grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Permission granted
            } else {
                // Permission denied
            }
        }
    }
}
```

---

## 7. PROCESS & APP LIFECYCLE

How Android manages processes and prioritizes them.

### 7.1 Process Priority (Importance Levels)

1. **Foreground Process** (Highest): Activity in foreground, service in foreground, broadcast being handled
2. **Visible Process**: Paused activity visible or running foreground service
3. **Service Process**: Service running
4. **Background Process**: Stopped activity (lowest, killed first)
5. **Empty Process**: (Lowest): No components, killed first

### 7.2 Process Death Recovery

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)

    // Check if app was killed and recreated
    if (savedInstanceState != null) {
        // App was killed, restore state
        val savedData = savedInstanceState.getString("key")
    } else {
        // Fresh start
        loadInitialData()
    }
}

override fun onSaveInstanceState(outState: Bundle) {
    super.onSaveInstanceState(outState)
    // Save state for potential process death
    outState.putString("key", currentData)
}
```

---

## 8. BEST PRACTICES

✅ **Activity Lifecycle**
- Keep onCreate/onResume short
- Release resources in onDestroy
- Save state in onSaveInstanceState
- Use ViewModel for configuration change survival

✅ **Fragments**
- Always use fragment arguments, never pass data directly
- Use view lifecycle observer (viewLifecycleOwner), not fragment lifecycle
- Clear view bindings in onDestroyView
- Use Shared ViewModel for inter-fragment communication

✅ **Services**
- Always unregister receivers and listeners
- Foreground services require FOREGROUND_SERVICE permission
- Bound services: always unbind in onDestroy
- Use WorkManager for background tasks

✅ **Intents**
- Pass Parcelable for complex objects, not Serializable
- Always check for null extras
- Use intent filters properly
- Never pass large bitmaps through intents

✅ **Permissions**
- Always check permissions before accessing protected resources
- Handle permission denials gracefully
- Request permissions at point of use
- Use ActivityResultContracts for cleaner API

✅ **Memory Management**
- Unregister all receivers
- Release listeners
- Clear context references
- Close resources (database, files)

---

## 9. LEARNING PATH: 6 WEEKS (78 HOURS)

**Week 1 (12h): Activity Lifecycle Foundation**
- Understand 6 lifecycle callbacks
- Practice onCreate/onDestroy sequence
- Handle onSaveInstanceState
- Create 3 simple activities with navigation

**Week 2 (12h): Configuration Changes & Back Stack**
- Handle orientation changes
- Use ViewModel for state survival
- Manage back stack behavior
- Debug lifecycle with Logcat

**Week 3 (14h): Fragment Mastery**
- All 10 lifecycle callbacks
- Fragment transactions and animations
- Shared ViewModel pattern
- Fragment-to-Fragment communication

**Week 4 (15h): Services & Background Operations**
- Started vs Bound services
- Foreground service implementation
- Background job scheduling
- IntentService patterns

**Week 5 (15h): Intent System & Permissions**
- Explicit intents with data passing
- Implicit intents and intent filters
- Normal vs dangerous permissions
- Runtime permission handling

**Week 6 (10h): Advanced Topics**
- BroadcastReceiver implementation
- ContentProvider basics
- Process lifecycle understanding
- Production debugging techniques

---

**Mastery Checkpoint**:
- Can explain activity lifecycle without looking
- Handle all configuration changes properly
- Implement fragment communication patterns
- Manage permissions correctly
- Understand when process death occurs

---

**Learning Hours**: 78 hours | **Level**: Beginner to Intermediate
**Next Step**: UI Development agent (Layouts, Compose, Material Design)
