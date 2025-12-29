---
name: quick-help
description: help - Quick Help for Common Tasks
allowed-tools: Read
---

# /quick-help - Quick Help for Common Tasks

Fast reference for solving common Android development problems.

## I want to...

### Learn Android Development

**If you're a beginner:**
1. Start with `/dev-guide`
2. Review Kotlin Fundamentals agent
3. Study Android Core agent
4. Use `/code-examples` for reference

**If you have experience:**
1. Check Jetpack Modern agent
2. Review Architecture Patterns agent
3. Use `/code-examples` for patterns
4. Study Production Skill

### Build a New App

```
1. Plan architecture (MVVM, Repository pattern)
2. Set up project with:
   - Jetpack (ViewModel, Room, Navigation)
   - Hilt for dependency injection
   - Retrofit for APIs
3. Implement features incrementally
4. Write tests (Unit + UI)
5. Optimize performance
6. Deploy to Play Store
```

### Use ViewModel & LiveData

```kotlin
@HiltViewModel
class MyViewModel @Inject constructor(
    private val repository: MyRepository
) : ViewModel() {
    private val _state = MutableLiveData<State>()
    val state: LiveData<State> = _state

    fun doSomething() {
        viewModelScope.launch {
            _state.value = repository.getData()
        }
    }
}

// In Fragment
viewModel.state.observe(viewLifecycleOwner) { state ->
    updateUI(state)
}
```

### Setup Room Database

```kotlin
@Entity
data class Item(@PrimaryKey val id: Int, val name: String)

@Dao
interface ItemDao {
    @Query("SELECT * FROM Item")
    suspend fun getAll(): List<Item>

    @Insert
    suspend fun insert(item: Item)
}

@Database(entities = [Item::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun itemDao(): ItemDao
}
```

### Use Dependency Injection (Hilt)

```kotlin
@HiltAndroidApp
class MyApp : Application()

@HiltViewModel
class MyViewModel @Inject constructor(
    private val repository: MyRepository
) : ViewModel()

class MyFragment : Fragment() {
    private val viewModel: MyViewModel by viewModels()
}
```

### Make API Calls

```kotlin
interface ApiService {
    @GET("/items")
    suspend fun getItems(): List<Item>
}

val retrofit = Retrofit.Builder()
    .baseUrl("https://api.example.com/")
    .addConverterFactory(GsonConverterFactory.create())
    .build()

val api = retrofit.create(ApiService::class.java)
val items = api.getItems()  // In coroutine
```

### Handle Navigation

```kotlin
// Navigate
findNavController().navigate(R.id.action_go_to_detail)

// With arguments
findNavController().navigate(
    MyFragmentDirections.actionGoToDetail(itemId = 123)
)

// Pop back stack
findNavController().popBackStack()
```

### Write Unit Tests

```kotlin
@RunWith(RobolectricTestRunner::class)
class MyViewModelTest {
    private val repository = mockk<MyRepository>()
    private lateinit var viewModel: MyViewModel

    @Before
    fun setup() {
        viewModel = MyViewModel(repository)
    }

    @Test
    fun `test something`() {
        coEvery { repository.getData() } returns testData

        viewModel.doSomething()

        assertEquals(testData, viewModel.state.value)
    }
}
```

### Test UI

```kotlin
@RunWith(AndroidJUnit4::class)
@HiltAndroidTest
class MyActivityTest {
    @get:Rule
    val activityRule = ActivityScenarioRule(MyActivity::class.java)

    @Test
    fun testButton() {
        onView(withId(R.id.button))
            .perform(click())

        onView(withId(R.id.result))
            .check(matches(withText("Expected text")))
    }
}
```

### Store Sensitive Data

```kotlin
val encryptedPrefs = EncryptedSharedPreferences.create(
    context, "secret",
    MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build(),
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

encryptedPrefs.edit { putString("token", "secret_value") }
```

### Deploy to Play Store

```
1. Increment versionCode and versionName
2. Enable minification:
   minifyEnabled = true
3. Build release bundle:
   ./gradlew bundleRelease
4. Sign with keystore
5. Upload to Google Play Console
6. Configure app listing
7. Start staged rollout (5% → 25% → 100%)
```

### Fix Memory Leaks

```kotlin
// ❌ LEAK
object Singleton {
    lateinit var context: Context
}

// ✅ FIX
object Singleton {
    var context: WeakReference<Context>? = null
}

// ✅ Also unregister listeners
override fun onDestroy() {
    super.onDestroy()
    unregisterReceiver()
}
```

### Improve Performance

**Memory:**
- ✅ Avoid memory leaks
- ✅ Release large objects
- ✅ Use WeakReference when needed

**Battery:**
- ✅ Batch network requests
- ✅ Use WorkManager with constraints
- ✅ Optimize location updates

**Rendering:**
- ✅ Avoid main thread blocking
- ✅ Use RecyclerView for lists
- ✅ Lazy load images

### Common Errors

**"Can't create instance of ViewModel"**
- Add @HiltViewModel annotation
- Check constructor parameters are provided by Hilt

**"NullPointerException on view"**
- Check layout file has the view with correct ID
- Verify view binding is set correctly

**"Fragment not attached to context"**
- Use getViewLifecycleOwner() not getLifecycleOwner()
- Check fragment is still attached before operations

**"ANR (Application Not Responding)"**
- Move heavy operations to background thread
- Use coroutines properly
- Profile with Android Profiler

## Useful Commands

```bash
# Build debug APK
./gradlew assembleDebug

# Build release bundle
./gradlew bundleRelease

# Run tests
./gradlew test

# Run instrumentation tests
./gradlew connectedAndroidTest

# Check lint
./gradlew lint

# Profile app
./gradlew profileRelease
```

## Resources

**Official Docs:**
- [Android Developer Docs](https://developer.android.com)
- [Kotlin Documentation](https://kotlinlang.org/docs/)
- [Jetpack Guide](https://developer.android.com/jetpack/guide)

**Training:**
- [Google Codelabs](https://developer.android.com/codelabs)
- [Android Developers Blog](https://android-developers.googleblog.com)

**Tools:**
- [Android Studio](https://developer.android.com/studio)
- [Android Profiler](https://developer.android.com/studio/profile/android-profiler)
- [Firebase Test Lab](https://firebase.google.com/docs/test-lab)

## Quick Checklist

Before launching to Play Store:

- ✅ App runs without crashes
- ✅ All tests passing
- ✅ No memory leaks
- ✅ 60+ FPS rendering
- ✅ Fast startup (< 5 seconds)
- ✅ Security reviewed
- ✅ Code obfuscated
- ✅ Signed with production key
- ✅ Version code incremented
- ✅ Crash reporting configured

---

**Need more detailed help?**
- `/dev-guide` - Complete development guide
- `/code-examples` - Real-world code examples
- Use agents for specific topics: kotlin-essentials, android-core, jetpack-modern, architecture-solid
