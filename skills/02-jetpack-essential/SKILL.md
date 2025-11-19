---
name: jetpack-essential
description: ViewModel, LiveData, Room database, Navigation Component, Hilt. Use when building with Jetpack.
---

# Jetpack Essential Skill

## ViewModel & LiveData

```kotlin
class UserViewModel : ViewModel() {
    private val _user = MutableLiveData<User>()
    val user: LiveData<User> = _user

    fun loadUser(id: Int) {
        viewModelScope.launch {
            _user.value = repository.getUser(id)
        }
    }
}

// In Fragment
viewModel.user.observe(viewLifecycleOwner) { user ->
    textView.text = user.name
}
```

## Room Database

```kotlin
@Entity
data class UserEntity(
    @PrimaryKey val id: Int,
    val name: String
)

@Dao
interface UserDao {
    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getUser(userId: Int): UserEntity?

    @Insert
    suspend fun insertUser(user: UserEntity)

    @Delete
    suspend fun deleteUser(user: UserEntity)
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
    <fragment android:id="@+id/listFragment" android:name=".ListFragment" />
    <fragment android:id="@+id/detailFragment" android:name=".DetailFragment" />
    <action android:id="@+id/action_list_to_detail" app:destination="@id/detailFragment" />
</navigation>
```

```kotlin
findNavController().navigate(R.id.action_list_to_detail)
```

## Hilt Dependency Injection

```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel()

@HiltAndroidApp
class MyApp : Application()

// In Fragment
class UserFragment : Fragment() {
    private val viewModel: UserViewModel by viewModels()
}
```

## WorkManager

```kotlin
class SyncWorker(context: Context, params: WorkerParameters) : CoroutineWorker(context, params) {
    override suspend fun doWork(): Result {
        return try {
            syncData()
            Result.success()
        } catch (e: Exception) {
            Result.retry()
        }
    }
}

// Schedule
WorkManager.getInstance(context).enqueueUniquePeriodicWork(
    "sync",
    ExistingPeriodicWorkPolicy.KEEP,
    PeriodicWorkRequestBuilder<SyncWorker>(15, TimeUnit.MINUTES).build()
)
```

## DataStore (Modern Preferences)

```kotlin
val userPreferences = context.dataStore.data
    .map { preferences ->
        preferences[USER_NAME_KEY] ?: ""
    }

lifecycleScope.launch {
    userPreferences.collect { name ->
        println(name)
    }
}
```

## Best Practices

✅ Never hold Context in ViewModel
✅ Use ViewBinding for UI references
✅ LiveData for UI state
✅ Room for persistence
✅ Hilt for dependency injection
✅ WorkManager for background tasks
✅ DataStore for preferences

## Architecture Pattern

```
Activity/Fragment → ViewModel → Repository → Room + API
```

## Common Mistakes

❌ Putting business logic in Activity
❌ Holding Activity references in ViewModel
❌ Direct database access in Views
❌ Not using DI

## Resources

- [Jetpack Guide](https://developer.android.com/jetpack/guide)
- [ViewModel Docs](https://developer.android.com/topic/libraries/architecture/viewmodel)
- [Room Docs](https://developer.android.com/training/data-storage/room)
