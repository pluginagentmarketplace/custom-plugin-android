---
description: Modern Android development with Jetpack libraries - ViewModel, LiveData, Room, Navigation, Hilt
capabilities: ["ViewModel", "LiveData", "Room database", "Navigation Component", "Hilt DI", "WorkManager", "DataStore"]
---

# Jetpack Modern

Build production-grade Android apps with Google's recommended Jetpack libraries. These are essential for modern Android development.

## ViewModel & LiveData

```kotlin
class UserViewModel : ViewModel() {
    private val _user = MutableLiveData<User>()
    val user: LiveData<User> = _user

    fun loadUser(id: Int) {
        viewModelScope.launch {
            val result = repository.getUser(id)
            _user.value = result
        }
    }
}

// In Fragment
viewModel.user.observe(viewLifecycleOwner) { user ->
    nameTextView.text = user.name
}
```

## Room Database

```kotlin
@Entity
data class UserEntity(
    @PrimaryKey val id: Int,
    val name: String,
    val email: String
)

@Dao
interface UserDao {
    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getUser(userId: Int): UserEntity?

    @Insert
    suspend fun insertUser(user: UserEntity)
}

@Database(entities = [UserEntity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
}
```

## Navigation Component

```xml
<!-- nav_graph.xml -->
<navigation xmlns:android="http://schemas.android.com/apk/res/android">
    <fragment android:id="@+id/listFragment" />
    <fragment android:id="@+id/detailFragment" />
    <action
        android:id="@+id/action_list_to_detail"
        app:destination="@id/detailFragment" />
</navigation>
```

```kotlin
// In Fragment
findNavController().navigate(R.id.action_list_to_detail)
```

## Dependency Injection with Hilt

```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {
    // Implementation
}

@HiltAndroidApp
class MyApp : Application()

// In Fragment
class UserFragment : Fragment() {
    private val viewModel: UserViewModel by viewModels()
}
```

## WorkManager

```kotlin
class DataSyncWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {
    override suspend fun doWork(): Result {
        return try {
            syncData()
            Result.success()
        } catch (e: Exception) {
            Result.retry()
        }
    }
}

// Schedule work
WorkManager.getInstance(context).enqueueUniquePeriodicWork(
    "sync",
    ExistingPeriodicWorkPolicy.KEEP,
    PeriodicWorkRequestBuilder<DataSyncWorker>(
        15, TimeUnit.MINUTES
    ).build()
)
```

## DataStore

```kotlin
val userPreferences = context.dataStore.data
    .map { preferences ->
        preferences[USER_NAME_KEY] ?: ""
    }

userPreferences.collect { name ->
    // Use name
}
```

## Jetpack Architecture

```
Activity/Fragment (UI Layer)
    ↓
ViewModel (Presentation Logic)
    ↓
Repository (Data Abstraction)
    ↓
Room + API (Data Layer)
```

## Key Principles

✅ Lifecycle-aware components
✅ Reactive data flow
✅ Type-safe database queries
✅ Dependency injection
✅ Structured concurrency
✅ Testable architecture

## Common Patterns

- **MVVM**: ViewModel + LiveData for state
- **Repository**: Abstraction over data sources
- **Single Source of Truth**: Database as source
- **Coroutines**: For async operations
- **Dependency Injection**: Loose coupling

## Essential Resources

- [Jetpack Guide](https://developer.android.com/jetpack/guide)
- [ViewModel Documentation](https://developer.android.com/topic/libraries/architecture/viewmodel)
- [Room Documentation](https://developer.android.com/training/data-storage/room)
- [Hilt Documentation](https://developer.android.com/training/dependency-injection/hilt-android)
