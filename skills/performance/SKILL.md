---
name: performance-tuning
description: Memory optimization, battery efficiency, rendering performance, and startup optimization. Use when optimizing app performance.
---

# Performance Tuning Skill

## Quick Start

### Memory Leaks
```kotlin
// ❌ LEAK
object ApiManager {
    lateinit var context: Context
}

// ✅ CORRECT
object ApiManager {
    var contextRef: WeakReference<Context>? = null
}
```

### Battery Optimization
```kotlin
// Efficient location updates
val locationRequest = LocationRequest.create().apply {
    priority = LocationRequest.PRIORITY_BALANCED_POWER_ACCURACY
    interval = 60000 // 1 minute
}
```

### Rendering Performance
```kotlin
// Load images on background thread
lifecycleScope.launch(Dispatchers.Default) {
    val bitmap = loadBitmapFromDisk()
    runOnUiThread { imageView.setImageBitmap(bitmap) }
}
```

## Performance Metrics

- Cold Start: < 5 seconds
- Frame Rate: 60 FPS
- Memory Heap: < 512 MB
- Battery Drain: < 5% per hour

## Profiling Tools

- **Android Profiler**: Memory, CPU, Network
- **LeakCanary**: Memory leak detection
- **Perfetto**: System-wide tracing

## Optimization Checklist

- ✅ No memory leaks
- ✅ Efficient battery usage
- ✅ 60+ FPS rendering
- ✅ Fast startup time
- ✅ Optimized network calls

## Resources

- [Performance Documentation](https://developer.android.com/topic/performance)
- [Android Profiler Guide](https://developer.android.com/studio/profile/android-profiler)
