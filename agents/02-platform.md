---
description: Android core components - Activities, Fragments, Services, Lifecycle, Intent system, Permissions - Android platform fundamentals
capabilities: ["Activity lifecycle management", "Fragment framework", "Service implementation", "Intent system", "BroadcastReceiver", "ContentProvider", "Permissions handling", "Process lifecycle"]
---

# Platform Agent

Master Android platform core components including Activities, Fragments, Services, and the complete component lifecycle management.

## Activities

### Lifecycle Callbacks
- `onCreate()`: Initial setup
- `onStart()`: Become visible
- `onResume()`: Gain focus
- `onPause()`: Lose focus
- `onStop()`: No longer visible
- `onDestroy()`: Final cleanup

### Key Concepts
- Back stack management
- Configuration changes (rotation)
- Activity launch modes
- State restoration

## Fragments

### Lifecycle
Fragment has 10 callbacks (includes onAttach, onDetach)

### Fragment Communication
- Shared ViewModel pattern
- Parent-child communication
- Arguments Bundle

## Services

### Types
- **Started Services**: `startService()`, runs indefinitely
- **Bound Services**: `bindService()`, client-based lifecycle
- **Foreground Services**: Visible notification required

## Intent System

### Intent Types
- **Explicit**: Direct activity launching
- **Implicit**: System chooses component
- Intent Filters in manifest
- Data extras and bundles

## BroadcastReceiver

### Broadcast Types
- System broadcasts (BATTERY_CHANGED, BOOT_COMPLETED)
- Local broadcasts (app internal)
- Ordered broadcasts
- Permissions required

## Permissions

### Types
- Normal permissions: Granted automatically
- Dangerous permissions: Runtime request required
- Declare in AndroidManifest.xml

### Runtime Permissions (API 23+)
```kotlin
if (ContextCompat.checkSelfPermission(this, permission) 
    != PackageManager.PERMISSION_GRANTED) {
    ActivityCompat.requestPermissions(this, arrayOf(permission), CODE)
}
```

## Process Lifecycle

### Process States
- Foreground (activity running)
- Visible (paused activity)
- Service (background service)
- Background (stopped activity)
- Empty (no components)

### Process Death
- System kills app to free memory
- Use ViewModel and savedInstanceState for recovery

## Learning Outcomes
- Understand complete lifecycle
- Handle configuration changes
- Implement multi-screen navigation
- Manage background operations

---

**Learning Hours**: 78 hours | **Level**: Beginner to Intermediate
