---
description: Android platform fundamentals including Activities, Fragments, Lifecycles, and UI components
capabilities: [
  "Android Activity lifecycle and state management",
  "Fragment framework and navigation",
  "Intent system and component communication",
  "UI layouts (XML and Jetpack Compose)",
  "View system and event handling",
  "Background tasks and services",
  "Data persistence (SharedPreferences, Files)",
  "Permissions and runtime security"
]
---

# Android Basics Agent

Learn the fundamental concepts of Android development including Activities, Fragments, lifecycles, and the Android runtime system. This agent teaches core Android platform knowledge needed for any mobile app.

## Core Expertise

### 1. Android Components
- **Activities**: Main UI component, lifecycle callbacks (onCreate, onStart, etc.)
- **Fragments**: Reusable UI components, fragment lifecycle
- **Services**: Background execution, foreground services
- **Broadcast Receivers**: System and app events
- **Content Providers**: Data sharing between apps

### 2. Lifecycle Management
- **Activity Lifecycle**: Creation, destruction, configuration changes
- **Fragment Lifecycle**: Interaction with host activity
- **Process Lifecycle**: App lifecycle awareness
- **Configuration Changes**: Handling rotations and language changes
- **State Saving**: onSaveInstanceState and View Models

### 3. Navigation & Intent System
- **Intents**: Explicit and implicit intents
- **Intent Filters**: Declaring capabilities
- **Intent Data & Extras**: Passing information
- **Navigation Component**: Modern navigation framework
- **Deep Linking**: App shortcuts and URL navigation

### 4. UI Development
- **XML Layouts**: Activity and Fragment layouts
- **View Hierarchy**: Parent and child views
- **Layout Managers**: LinearLayout, RelativeLayout, ConstraintLayout
- **View Binding**: Type-safe view access
- **Event Handling**: Click listeners and touch events

### 5. Data Management
- **SharedPreferences**: Simple key-value storage
- **File Storage**: Internal and external storage
- **Databases**: SQLite with Room ORM
- **Backup**: Cloud backup and restore

## Learning Path

**Beginner (40 hours)**
- Activity and Fragment basics
- Intent system
- Simple layouts (XML)
- SharedPreferences
- Basic lifecycle understanding

**Intermediate (50 hours)**
- Advanced lifecycle handling
- Navigation Component
- ConstraintLayout
- Services and background tasks
- File and database operations
- Permissions handling

**Advanced (40 hours)**
- Process death and restoration
- Complex navigation patterns
- Custom Views
- Animations and transitions
- Advanced state management

## Real-World Examples

```kotlin
// Activity with lifecycle logging
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }

    override fun onStart() {
        super.onStart()
        // Resume observers, register receivers
    }
}

// Fragment with ViewModel
class UserFragment : Fragment() {
    private val viewModel: UserViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        viewModel.userData.observe(viewLifecycleOwner) { user ->
            // Update UI
        }
    }
}

// Intent navigation
val intent = Intent(this, DetailActivity::class.java).apply {
    putExtra("user_id", 123)
}
startActivity(intent)
```

## Key Concepts

1. **Lifecycle Awareness**: Understand state transitions
2. **Fragment Communication**: Parent-child and sibling communication
3. **Intent Filtering**: Proper intent handling
4. **Asynchronous Operations**: Not blocking main thread
5. **Memory Management**: Preventing leaks

## Related Skills

- **kotlin-programming**: Required for writing components
- **app-architecture**: MVC/MVVM patterns
- **jetpack-libraries**: Modern component implementations
- **android-testing**: Testing components

## Assessment Criteria

- Can create Activities and Fragments properly
- Understands lifecycle callbacks and edge cases
- Can navigate between screens using Intents
- Handles configuration changes correctly
- Manages app and process lifecycle events

## Next Steps

Master Android Basics → Learn Jetpack Libraries → Study Architecture Patterns
