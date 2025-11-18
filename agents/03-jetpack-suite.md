---
description: Android Jetpack ecosystem and modern development libraries for productivity and best practices
capabilities: [
  "Lifecycle and LiveData for state management",
  "Room database ORM",
  "Navigation Component for screen transitions",
  "WorkManager for background jobs",
  "DataStore and preferences",
  "Compose for modern UI",
  "Hilt for dependency injection",
  "Testing libraries"
]
---

# Jetpack Suite Agent

Master the Android Jetpack ecosystem - Google's recommended set of libraries for robust, testable, and maintainable Android development. This agent covers all major Jetpack components.

## Core Libraries

### 1. Foundation Libraries
- **AppCompat**: Backward compatibility for Material Design
- **Android KTX**: Kotlin extensions for concise APIs
- **Multidex**: Support for apps with 64K+ methods
- **Emoji**: Emoji compatibility support

### 2. Architecture Components
- **Lifecycle**: Lifecycle-aware component management
- **LiveData**: Observable data holder with lifecycle awareness
- **ViewModel**: UI-agnostic component for data
- **SavedState**: State preservation across process death
- **Room**: Type-safe SQLite abstraction layer
- **DataStore**: Modern key-value storage

### 3. Navigation & UI
- **Navigation Component**: Type-safe navigation
- **Fragment**: Modern fragment implementation
- **CoordinatorLayout**: Advanced layout coordination
- **ConstraintLayout**: Flexible layouts with constraints
- **Compose**: Modern declarative UI toolkit

### 4. Asynchronous Processing
- **WorkManager**: Deferrable background job scheduling
- **Coroutines**: Structured concurrency
- **CallbacksToCoroutinesAdapter**: Legacy callback conversion

### 5. Dependency Injection
- **Hilt**: Compile-time safe DI for Android
- **ServiceLocator**: Manual service location

### 6. Security
- **Security Crypto**: Encrypted SharedPreferences
- **Biometric**: Fingerprint/face auth API

## Modern Development Stack

```
┌─────────────────────────────────┐
│  Compose UI (Declarative UI)   │
├─────────────────────────────────┤
│  Hilt (Dependency Injection)    │
├─────────────────────────────────┤
│  ViewModel + LiveData (State)   │
├─────────────────────────────────┤
│  Room + DataStore (Data Layer)  │
├─────────────────────────────────┤
│  WorkManager (Background Jobs)  │
├─────────────────────────────────┤
│  Navigation Component (Routing) │
└─────────────────────────────────┘
```

## Learning Path

**Beginner (35 hours)**
- Lifecycle and LiveData basics
- ViewModel for state management
- Room database setup and queries
- Basic Navigation Component
- DataStore for preferences

**Intermediate (45 hours)**
- Advanced ViewModel patterns
- Room relationships and migrations
- Jetpack Compose basics
- WorkManager job scheduling
- Advanced Navigation scenarios
- Hilt dependency injection

**Advanced (50 hours)**
- Custom ViewModel factories
- Room testing and transactions
- Compose advanced layouts
- WorkManager with constraints
- Custom Hilt modules
- Performance optimization

## Practical Examples

```kotlin
// ViewModel with LiveData
class UserViewModel : ViewModel() {
    private val _userData = MutableLiveData<User>()
    val userData: LiveData<User> = _userData

    fun loadUser(id: Int) {
        viewModelScope.launch {
            _userData.value = Repository.getUser(id)
        }
    }
}

// Room Entity and DAO
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey val id: Int,
    val name: String,
    val email: String
)

@Dao
interface UserDao {
    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getUser(userId: Int): UserEntity

    @Insert
    suspend fun insertUser(user: UserEntity)
}

// Hilt dependency injection
@HiltViewModel
class UserViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {
    val users = userRepository.getAllUsers()
}

// WorkManager background task
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
```

## Key Concepts

1. **Lifecycle Awareness**: Components respond to app lifecycle
2. **Reactive Programming**: LiveData and Flow for data updates
3. **Type Safety**: Room prevents SQL errors at compile-time
4. **Dependency Injection**: Loose coupling with Hilt
5. **Structured Concurrency**: Coroutines with proper scoping

## Integration Patterns

- **MVVM with Jetpack**: ViewModel + LiveData + Repository
- **Clean Architecture**: Separation of concerns
- **Dependency Injection**: Constructor injection with Hilt
- **Data Flow**: Repository pattern for data layer
- **Testing**: Testable components with DI

## Related Skills

- **kotlin-programming**: Coroutines and extensions
- **app-architecture**: Architectural patterns using Jetpack
- **android-testing**: Testing Jetpack components
- **app-security**: Secure data storage with DataStore

## Assessment Criteria

- Can structure apps with Jetpack components
- Understands ViewModel and LiveData patterns
- Can design Room database schemas
- Implements Hilt dependency injection
- Can navigate with Navigation Component

## Next Steps

Master Jetpack → Learn Architecture Patterns → Study Advanced Testing
