# Android Lifecycle Complete Guide

Understanding Android component lifecycles is essential for building stable, memory-efficient apps.

## Activity Lifecycle

### Lifecycle States

```
                    ┌─────────────┐
                    │   Created   │
                    └──────┬──────┘
                           │ onCreate()
                    ┌──────▼──────┐
                    │   Started   │◄────────┐
                    └──────┬──────┘         │
                           │ onStart()      │ onRestart()
                    ┌──────▼──────┐         │
                    │   Resumed   │         │
                    └──────┬──────┘         │
                           │ onPause()      │
                    ┌──────▼──────┐         │
                    │   Paused    │         │
                    └──────┬──────┘         │
                           │ onStop()       │
                    ┌──────▼──────┐─────────┘
                    │   Stopped   │
                    └──────┬──────┘
                           │ onDestroy()
                    ┌──────▼──────┐
                    │  Destroyed  │
                    └─────────────┘
```

### Callback Implementation

```kotlin
class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private val viewModel: MainViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // 1. Set up view binding
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // 2. Restore state if available
        savedInstanceState?.let {
            viewModel.restoreState(it.getParcelable("state"))
        }

        // 3. Set up UI
        setupUI()
        observeViewModel()
    }

    override fun onStart() {
        super.onStart()
        // Register receivers, start animations
    }

    override fun onResume() {
        super.onResume()
        // Resume playback, refresh data
    }

    override fun onPause() {
        super.onPause()
        // Pause playback, keep quick!
    }

    override fun onStop() {
        super.onStop()
        // Unregister receivers, save state
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putParcelable("state", viewModel.getCurrentState())
    }

    override fun onDestroy() {
        super.onDestroy()
        // Final cleanup
    }
}
```

## Fragment Lifecycle

### Fragment vs Activity Lifecycle

```
Fragment                    Activity
─────────                   ─────────
onAttach()
onCreate()           ←      onCreate()
onCreateView()
onViewCreated()
onStart()            ←      onStart()
onResume()           ←      onResume()
onPause()            ←      onPause()
onStop()             ←      onStop()
onDestroyView()
onDestroy()          ←      onDestroy()
onDetach()
```

### Safe Fragment Implementation

```kotlin
class UserFragment : Fragment(R.layout.fragment_user) {

    // ViewBinding - nullify in onDestroyView
    private var _binding: FragmentUserBinding? = null
    private val binding get() = _binding!!

    // Use viewLifecycleOwner for observers
    private val viewModel: UserViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        _binding = FragmentUserBinding.bind(view)

        // IMPORTANT: Use viewLifecycleOwner, NOT this
        viewModel.user.observe(viewLifecycleOwner) { user ->
            binding.userName.text = user.name
        }

        // For Flow collection
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.uiState.collect { state ->
                    updateUI(state)
                }
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        // CRITICAL: Nullify binding to prevent memory leaks
        _binding = null
    }
}
```

## ViewModel Lifecycle

### ViewModel Scope

```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {

    private val _state = MutableStateFlow<UiState>(UiState.Loading)
    val state: StateFlow<UiState> = _state.asStateFlow()

    init {
        loadUser()
    }

    private fun loadUser() {
        // Use viewModelScope - automatically cancelled when ViewModel cleared
        viewModelScope.launch {
            try {
                val user = repository.getUser()
                _state.value = UiState.Success(user)
            } catch (e: Exception) {
                _state.value = UiState.Error(e.message)
            }
        }
    }

    // Called when ViewModel is being destroyed
    override fun onCleared() {
        super.onCleared()
        // Cancel any ongoing work, close connections
    }
}
```

### ViewModel Survival

| Event | ViewModel Survives? |
|-------|---------------------|
| Rotation | ✅ Yes |
| Language Change | ✅ Yes |
| Back Press | ❌ No |
| Finish() | ❌ No |
| System Kill | ❌ No |

## Service Lifecycle

### Service Types

```kotlin
// Started Service
class DownloadService : Service() {
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Do work
        return START_STICKY // Restart if killed
    }

    override fun onBind(intent: Intent): IBinder? = null
}

// Bound Service
class DataService : Service() {
    private val binder = LocalBinder()

    inner class LocalBinder : Binder() {
        fun getService(): DataService = this@DataService
    }

    override fun onBind(intent: Intent): IBinder = binder
}

// Foreground Service
class MusicService : Service() {
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val notification = createNotification()
        startForeground(NOTIFICATION_ID, notification)
        // Play music
        return START_STICKY
    }
}
```

## Intent System

### Explicit vs Implicit Intents

```kotlin
// Explicit - specific component
val explicit = Intent(this, DetailActivity::class.java).apply {
    putExtra("user_id", 123)
}
startActivity(explicit)

// Implicit - action-based
val implicit = Intent(Intent.ACTION_VIEW).apply {
    data = Uri.parse("https://example.com")
}
startActivity(implicit)

// Intent with Result
val launcher = registerForActivityResult(
    ActivityResultContracts.StartActivityForResult()
) { result ->
    if (result.resultCode == RESULT_OK) {
        val data = result.data
    }
}
launcher.launch(intent)
```

## Best Practices

### 1. Configuration Changes
```kotlin
// ✅ Use ViewModel for data
class MyViewModel : ViewModel() {
    val data = MutableLiveData<Data>()
}

// ✅ Use savedInstanceState for UI state
override fun onSaveInstanceState(outState: Bundle) {
    outState.putInt("scroll_position", recyclerView.scrollY)
}

// ❌ Don't retain fragments
// fragment.retainInstance = true  // DEPRECATED
```

### 2. Memory Leaks Prevention
```kotlin
// ❌ Anonymous inner class holds Activity reference
button.setOnClickListener {
    // 'this' is Activity - potential leak
}

// ✅ WeakReference or lambda that doesn't capture this
class MyClickListener(activity: WeakReference<Activity>) : OnClickListener {
    override fun onClick(v: View) {
        activity.get()?.let { /* safe */ }
    }
}
```

### 3. Lifecycle-Aware Collection
```kotlin
// ✅ Correct - respects lifecycle
viewLifecycleOwner.lifecycleScope.launch {
    viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
        flow.collect { value ->
            updateUI(value)
        }
    }
}

// ❌ Wrong - collects in background, potential crashes
lifecycleScope.launch {
    flow.collect { value ->
        updateUI(value) // May crash if view destroyed
    }
}
```

## Resources

- [Activity Lifecycle](https://developer.android.com/guide/components/activities/activity-lifecycle)
- [Fragment Lifecycle](https://developer.android.com/guide/fragments/lifecycle)
- [ViewModel Overview](https://developer.android.com/topic/libraries/architecture/viewmodel)
- [Handling Lifecycle Events](https://developer.android.com/topic/libraries/architecture/lifecycle)
