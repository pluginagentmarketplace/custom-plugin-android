---
description: MVVM, Clean Architecture, SOLID principles, design patterns, and production-ready app structure
capabilities: ["MVVM architecture", "Clean Architecture", "Repository pattern", "SOLID principles", "Design patterns", "Testable code", "Performance optimization", "Security best practices"]
---

# Architecture & SOLID

Build scalable, maintainable, and testable Android applications with proven architectural patterns.

## MVVM Architecture

```
┌─────────────┐
│ Activity    │
│ Fragment    │  (UI Layer)
└──────┬──────┘
       │
┌──────▼──────────┐
│ ViewModel       │  (Presentation)
│ + LiveData      │  (State Management)
└──────┬──────────┘
       │
┌──────▼──────────┐
│ Repository      │  (Data Abstraction)
└──────┬──────────┘
       │
┌──────▼──────────┐
│ Room + API      │  (Data Sources)
└─────────────────┘
```

## Clean Architecture

```kotlin
// Domain Layer - Pure business logic
interface UserRepository {
    suspend fun getUser(id: Int): Result<User>
}

// Presentation Layer - UI logic
@HiltViewModel
class UserDetailViewModel @Inject constructor(
    private val getUserUseCase: GetUserUseCase
) : ViewModel() {
    private val _state = MutableLiveData<UiState>()
    val state: LiveData<UiState> = _state

    fun loadUser(id: Int) {
        viewModelScope.launch {
            _state.value = UiState.Loading
            val result = getUserUseCase(id)
            _state.value = when {
                result.isSuccess -> UiState.Success(result.getOrNull()!!)
                else -> UiState.Error(result.exceptionOrNull()?.message ?: "Error")
            }
        }
    }
}

sealed class UiState {
    object Loading : UiState()
    data class Success(val user: User) : UiState()
    data class Error(val message: String) : UiState()
}

// Data Layer - Repository implementation
@Inject
class UserRepositoryImpl(
    private val userDao: UserDao,
    private val userApi: UserApi
) : UserRepository {
    override suspend fun getUser(id: Int): Result<User> = runCatching {
        userDao.getUser(id) ?: userApi.fetchUser(id).also {
            userDao.insertUser(it)
        }
    }
}
```

## Repository Pattern

```kotlin
interface DataRepository {
    suspend fun fetchData(): Result<Data>
    fun observeData(): Flow<Data>
}

class DataRepositoryImpl(
    private val localDataSource: LocalDataSource,
    private val remoteDataSource: RemoteDataSource
) : DataRepository {
    override suspend fun fetchData(): Result<Data> = runCatching {
        try {
            val remoteData = remoteDataSource.fetchData()
            localDataSource.save(remoteData)
            remoteData
        } catch (e: Exception) {
            localDataSource.getData()
        }
    }

    override fun observeData(): Flow<Data> {
        return localDataSource.observeData()
    }
}
```

## SOLID Principles

### Single Responsibility
```kotlin
// ✅ GOOD - Each class has one reason to change
class UserViewModel(userRepository: UserRepository)
class UserRepository(userDao: UserDao, userApi: UserApi)

// ❌ BAD - Class responsible for too much
class UserManager {
    fun loadUser() { }
    fun saveUser() { }
    fun deleteUser() { }
    fun syncWithServer() { }
    fun calculateStatistics() { }
}
```

### Open/Closed Principle
```kotlin
// ✅ Open for extension, closed for modification
interface Logger {
    fun log(message: String)
}

class ConsoleLogger : Logger {
    override fun log(message: String) = println(message)
}

class FileLogger : Logger {
    override fun log(message: String) { }
}
```

### Liskov Substitution
```kotlin
// ✅ Subtypes must be substitutable
interface UserRepository {
    suspend fun getUser(id: Int): User
}

class LocalUserRepository : UserRepository { }
class RemoteUserRepository : UserRepository { }
// Both can be used interchangeably
```

### Interface Segregation
```kotlin
// ✅ GOOD - Focused interfaces
interface UserRepository {
    suspend fun getUser(id: Int): User
}

interface UserPersistence {
    suspend fun saveUser(user: User)
}

// ❌ BAD - Fat interface
interface Repository {
    suspend fun getUser(id: Int): User
    suspend fun saveUser(user: User)
    suspend fun deleteUser(id: Int): Boolean
    suspend fun searchUsers(query: String): List<User>
    // ... more unrelated methods
}
```

### Dependency Inversion
```kotlin
// ✅ Depend on abstractions
class UserViewModel(
    private val repository: UserRepository  // Abstraction
) : ViewModel()

// ❌ Depends on concrete implementation
class UserViewModel(
    private val db: SQLiteDatabase
) : ViewModel()
```

## Design Patterns

### Factory Pattern
```kotlin
class RepositoryFactory {
    fun createUserRepository(): UserRepository {
        return UserRepositoryImpl(
            Room.databaseBuilder(context, AppDatabase::class.java, "db").build().userDao(),
            ApiService.create()
        )
    }
}
```

### Observer Pattern
```kotlin
// LiveData / Flow are observers
viewModel.user.observe(this) { user ->
    updateUI(user)
}
```

### Strategy Pattern
```kotlin
interface CacheStrategy {
    suspend fun fetchData(): Data
}

class NetworkFirst : CacheStrategy { }
class CacheFirst : CacheStrategy { }

class DataRepository(private val strategy: CacheStrategy)
```

## Testing Architecture

```kotlin
// Testable because of DI and interface abstraction
@Test
fun loadUser_updates_state() {
    val mockRepository = mockk<UserRepository>()
    coEvery { mockRepository.getUser(1) } returns User(1, "John")

    val viewModel = UserViewModel(mockRepository)
    viewModel.loadUser(1)

    assertEquals(UiState.Success(User(1, "John")), viewModel.state.value)
}
```

## Performance & Security

### Performance
- ✅ Lazy initialization of heavy objects
- ✅ Caching strategies in Repository
- ✅ Efficient database queries with Room
- ✅ Background operations with WorkManager

### Security
- ✅ Encrypted data storage
- ✅ HTTPS for all API calls
- ✅ Certificate pinning for sensitive APIs
- ✅ Secure token management

## Checklist

✅ Clear separation of layers
✅ SOLID principles applied
✅ Dependency injection configured
✅ Repository pattern implemented
✅ Testing setup ready
✅ Error handling in place
✅ Lifecycle awareness
✅ Null safety enforced
✅ No hardcoded secrets
✅ Performance optimized

## Essential Resources

- [Android Architecture Guide](https://developer.android.com/jetpack/guide)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Design Patterns](https://refactoring.guru/design-patterns)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
