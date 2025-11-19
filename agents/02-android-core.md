---
description: Android platform fundamentals - Activities, Fragments, lifecycle, components, and navigation
capabilities: ["Activity lifecycle", "Fragment management", "Intent system", "Data persistence", "Services", "Permissions"]
---

# Android Core

Understand the Android platform fundamentals. Every Android developer must master Activities, Fragments, and the component lifecycle.

## Activities

```kotlin
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }

    override fun onStart() {
        super.onStart()
        // Resume observers
    }

    override fun onDestroy() {
        super.onDestroy()
        // Clean up resources
    }
}
```

## Fragments

```kotlin
class UserFragment : Fragment() {
    private val viewModel: UserViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        viewModel.user.observe(viewLifecycleOwner) { user ->
            updateUI(user)
        }
    }
}
```

## Lifecycle Management

Activity Lifecycle:
```
onCreate → onStart → onResume → (Running)
↓
onPause → onStop → onDestroy
```

Fragment Lifecycle:
```
onAttach → onCreate → onCreateView → onViewCreated → onStart → onResume
```

## Intent System

```kotlin
// Explicit intent
val intent = Intent(this, DetailActivity::class.java)
intent.putExtra("user_id", userId)
startActivity(intent)

// Implicit intent
val intent = Intent(Intent.ACTION_VIEW).apply {
    data = Uri.parse("https://example.com")
}
startActivity(intent)
```

## Data Persistence

```kotlin
// SharedPreferences
val prefs = getSharedPreferences("app", Context.MODE_PRIVATE)
prefs.edit { putString("key", "value") }

// File storage
openFileOutput("file.txt", Context.MODE_PRIVATE).use {
    it.write("content".toByteArray())
}
```

## Key Concepts

- **Lifecycle Awareness**: Respond to state changes
- **Fragment Communication**: Parent-child and sibling communication
- **Back Stack**: Navigation history management
- **Configuration Changes**: Handle rotation properly
- **Process Death**: Save and restore state

## Common Pitfalls

❌ Not unregistering listeners
❌ Holding Activity references in singletons
❌ Ignoring configuration changes
❌ Background operations on main thread
❌ Not handling permissions properly

## Essential Resources

- [Android Lifecycle](https://developer.android.com/guide/components/activities/activity-lifecycle)
- [Fragment Guide](https://developer.android.com/guide/fragments)
- [Intent System](https://developer.android.com/guide/components/intents-filters)
