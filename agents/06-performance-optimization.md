---
description: Memory optimization, battery efficiency, and performance monitoring for Android apps
capabilities: [
  "Memory management and leak detection",
  "Battery optimization and power profiling",
  "Rendering performance and frame rate",
  "Network optimization and caching",
  "App startup time optimization",
  "ANR detection and prevention",
  "Profiling with Android Profiler",
  "Performance monitoring and analytics"
]
---

# Performance Optimization Agent

Learn how to build fast, efficient Android apps that consume minimal memory and battery. This agent covers performance profiling, optimization techniques, and monitoring strategies.

## Performance Metrics

### Key Performance Indicators (KPIs)

**User Experience:**
- **Cold Start Time**: < 5 seconds
- **Hot Start Time**: < 2 seconds
- **Frame Rate**: 60 FPS (120 FPS for modern devices)
- **Jank Rate**: < 1% janky frames
- **Battery**: < 5% drain per hour

**Technical:**
- **Memory**: Avoid OOM, keep heap < 512MB
- **CPU Usage**: < 20% at idle
- **Networking**: Efficient data transfer
- **Disk I/O**: Minimal storage access

## Memory Optimization

### Common Memory Issues

1. **Memory Leaks**
```kotlin
// ❌ LEAK: Static reference to Context
object ApiManager {
    private lateinit var context: Context
    fun init(context: Context) {
        this.context = context
    }
}

// ✅ CORRECT: Use WeakReference
object ApiManager {
    private var contextRef: WeakReference<Context>? = null
    fun init(context: Context) {
        this.contextRef = WeakReference(context)
    }
}
```

2. **Activity Leaks**
```kotlin
// ❌ LEAK: Anonymous class holds activity reference
class MyActivity : AppCompatActivity() {
    private val handler = Handler(Looper.getMainLooper())

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        handler.postDelayed({
            // This runs after activity destroyed
            startActivity(Intent(this, OtherActivity::class.java))
        }, 5000)
    }
}

// ✅ CORRECT: Use WeakReference or cancel on destroy
class MyActivity : AppCompatActivity() {
    private val handler = Handler(Looper.getMainLooper())

    override fun onDestroy() {
        super.onDestroy()
        handler.removeCallbacksAndMessages(null)
    }
}
```

3. **Listener Leaks**
```kotlin
// ❌ LEAK: Listener not unregistered
class MyFragment : Fragment() {
    private val listener = object : SensorEventListener { }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        sensorManager.registerListener(listener, sensor, SensorManager.SENSOR_DELAY_UI)
    }
}

// ✅ CORRECT: Unregister in onPause
class MyFragment : Fragment() {
    override fun onPause() {
        super.onPause()
        sensorManager.unregisterListener(listener)
    }
}
```

### Memory Profiling Tools

- **Android Profiler**: Memory, CPU, Network tabs
- **LeakCanary**: Automatic leak detection
- **MAT (Memory Analyzer Tool)**: Heap dump analysis
- **Perfetto**: System-wide performance tracing

## Battery Optimization

### Battery Drains

1. **Wakelocks**: Prevent CPU sleep
```kotlin
// ✅ Efficient wakelock usage
val wakeLock = powerManager.newWakeLock(
    PowerManager.PARTIAL_WAKE_LOCK,
    "myapp:background_sync"
)

// Only hold when necessary, for short periods
wakeLock.acquire(10000) // 10 seconds max
try {
    performSync()
} finally {
    wakeLock.release()
}
```

2. **Location Updates**: Expensive, use conservatively
```kotlin
// ✅ Optimize location updates
val locationRequest = LocationRequest.create().apply {
    priority = LocationRequest.PRIORITY_BALANCED_POWER_ACCURACY
    interval = 60000 // 1 minute
    fastestInterval = 30000
}
```

3. **Network Access**: Batch requests, compress data
```kotlin
// ✅ Batch network requests
WorkManager.enqueueUniqueWork(
    "sync_data",
    ExistingWorkPolicy.KEEP,
    OneTimeWorkRequestBuilder<SyncWorker>()
        .setConstraints(Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .setRequiresBatteryNotLow(true)
            .build()
        )
        .build()
)
```

## Rendering Performance

### Frame Rate Issues

1. **Janky Frames**
```kotlin
// ❌ SLOW: Heavy operations on main thread
override fun onDraw(canvas: Canvas) {
    val bitmap = BitmapFactory.decodeFile(imagePath) // SLOW!
    canvas.drawBitmap(bitmap, 0f, 0f, null)
}

// ✅ FAST: Load on background thread
private var cachedBitmap: Bitmap? = null

override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    lifecycleScope.launch(Dispatchers.Default) {
        cachedBitmap = BitmapFactory.decodeFile(imagePath)
        runOnUiThread { invalidate() }
    }
}
```

2. **OverDraw**
```kotlin
// ❌ OVERDRAW: Unnecessary background layers
<FrameLayout>
    <View
        android:background="@color/white" />
    <View
        android:background="@color/white" />
    <RecyclerView />
</FrameLayout>

// ✅ EFFICIENT: Single background
<FrameLayout
    android:background="@color/white">
    <RecyclerView />
</FrameLayout>
```

### Profiling Rendering
- **GPU Profiler**: Track GPU usage
- **SysTrace**: System-level tracing
- **Profile GPU Rendering**: On-device profiler

## App Startup Optimization

### Cold Start Process
```
Startup → App Launch → Activity Creation → Content Loaded
   ↓
Slow: Long initialization, large assets, synchronous I/O
Fast: Lazy loading, async initialization, lightweight startup
```

### Optimization Strategies

1. **Lazy Initialization**
```kotlin
// ❌ SLOW: Initialize everything in onCreate
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    databaseHelper = DatabaseHelper(this) // Slow!
    imageLoader = ImageLoader() // Slow!
    analyticsManager = AnalyticsManager() // Slow!
}

// ✅ FAST: Lazy initialize
private val databaseHelper by lazy { DatabaseHelper(this) }
private val imageLoader by lazy { ImageLoader() }
private val analyticsManager by lazy { AnalyticsManager() }
```

2. **Async Initialization**
```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    setContentView(R.layout.activity_main)

    // Load analytics in background
    lifecycleScope.launch(Dispatchers.Default) {
        analyticsManager.initialize()
    }
}
```

## Learning Path

**Beginner (30 hours)**
- Understanding Android memory model
- Common memory leak patterns
- Basic profiling with Android Profiler
- Battery optimization basics
- Simple performance monitoring

**Intermediate (45 hours)**
- Advanced memory analysis
- Rendering performance tuning
- Network optimization
- App startup optimization
- LeakCanary integration
- Performance testing

**Advanced (50 hours)**
- System-level performance analysis
- Custom performance monitoring
- Advanced profiling with Perfetto
- Performance regression testing
- Production monitoring setup
- Enterprise performance optimization

## Performance Checklist

### Memory
- ✅ No memory leaks (verified with LeakCanary)
- ✅ Bitmap caching strategy
- ✅ Collections properly cleared
- ✅ Listeners unregistered

### Battery
- ✅ Efficient location updates
- ✅ Batched network requests
- ✅ Proper wakelock management
- ✅ Background job constraints

### Rendering
- ✅ 60+ FPS in normal usage
- ✅ Minimal overdraw (< 2x)
- ✅ Efficient layouts
- ✅ Smooth scrolling/animations

### Startup
- ✅ Cold start < 5 seconds
- ✅ Hot start < 2 seconds
- ✅ Lazy initialization
- ✅ Async heavy operations

## Related Skills

- **jetpack-libraries**: Room caching, WorkManager
- **kotlin-programming**: Coroutines for async
- **android-testing**: Performance benchmarking
- **app-architecture**: Efficient data flow

## Assessment Criteria

- Can identify and fix memory leaks
- Optimizes battery consumption
- Achieves 60+ FPS rendering
- Reduces app startup time
- Can use Android Profiler effectively
- Monitors production performance

## Next Steps

Master Performance → Learn Security Practices → Study Deployment & Release
