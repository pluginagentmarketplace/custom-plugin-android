---
name: architecture-patterns
description: MVVM, Repository pattern, Dependency injection, SOLID principles. Use when designing app structure.
---

# Architecture Patterns Skill

## MVVM Pattern

```kotlin
// ViewModel (State + Logic)
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {
    private val _state = MutableLiveData<UiState>()
    val state: LiveData<UiState> = _state

    fun loadUser(id: Int) {
        viewModelScope.launch {
            _state.value = UiState.Loading
            val result = runCatching { repository.getUser(id) }
            _state.value = result.fold(
                onSuccess = { user -> UiState.Success(user) },
                onFailure = { error -> UiState.Error(error.message ?: "") }
            )
        }
    }
}

sealed class UiState {
    object Loading : UiState()
    data class Success(val user: User) : UiState()
    data class Error(val message: String) : UiState()
}

// View (UI)
viewModel.state.observe(this) { state ->
    when (state) {
        is UiState.Loading -> showLoading()
        is UiState.Success -> showUser(state.user)
        is UiState.Error -> showError(state.message)
    }
}
```

## Repository Pattern

```kotlin
interface UserRepository {
    suspend fun getUser(id: Int): User
    fun observeUsers(): Flow<List<User>>
}

class UserRepositoryImpl(
    private val userDao: UserDao,
    private val userApi: UserApi
) : UserRepository {
    override suspend fun getUser(id: Int): User {
        return userDao.getUser(id) ?: userApi.fetchUser(id).also {
            userDao.insertUser(it)
        }
    }

    override fun observeUsers() = userDao.observeAll()
}
```

## Dependency Injection

```kotlin
// With Hilt (Recommended)
@Module
@InstallIn(SingletonComponent::class)
object RepositoryModule {
    @Provides
    fun provideUserRepository(
        dao: UserDao,
        api: UserApi
    ): UserRepository {
        return UserRepositoryImpl(dao, api)
    }
}

@HiltViewModel
class MyViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel()
```

## SOLID Principles

### Single Responsibility
```kotlin
// ✅ One responsibility each
class UserViewModel(repository: UserRepository)
class UserRepository(dao: UserDao, api: UserApi)
class UserDao { }
```

### Open/Closed
```kotlin
// ✅ Open for extension, closed for modification
interface Repository {
    suspend fun getData(): Data
}

class ApiRepository : Repository { }
class MockRepository : Repository { }
```

### Liskov Substitution
```kotlin
// ✅ Subtypes interchangeable
interface Logger { fun log(msg: String) }
class ConsoleLogger : Logger
class FileLogger : Logger
// Use either interchangeably
```

### Interface Segregation
```kotlin
// ✅ Focused interfaces
interface UserRead { suspend fun getUser(id: Int): User }
interface UserWrite { suspend fun saveUser(user: User) }

// ❌ Fat interface
interface UserRepository {
    suspend fun getUser(id: Int): User
    suspend fun saveUser(user: User)
    suspend fun deleteUser(id: Int)
    // ... more methods
}
```

### Dependency Inversion
```kotlin
// ✅ Depend on abstractions
class ViewModel(repository: UserRepository)

// ❌ Depends on concrete class
class ViewModel(api: RetrofitApi)
```

## Design Patterns

### Factory
```kotlin
fun createRepository(): UserRepository {
    return UserRepositoryImpl(provideDao(), provideApi())
}
```

### Observer (LiveData/Flow)
```kotlin
viewModel.state.observe(this) { render(it) }
```

### Strategy
```kotlin
interface CacheStrategy { suspend fun fetch(): Data }
class NetworkFirst : CacheStrategy
class CacheFirst : CacheStrategy
```

## Testable Architecture

```kotlin
@Test
fun userViewModel_loadsUser() {
    val mockRepository = mockk<UserRepository>()
    coEvery { mockRepository.getUser(1) } returns User(1, "John")

    val viewModel = UserViewModel(mockRepository)
    viewModel.loadUser(1)

    assertEquals(UiState.Success(User(1, "John")), viewModel.state.value)
}
```

## Layer Separation

```
┌─────────────────┐
│ Presentation    │ ViewModel, Activities
├─────────────────┤
│ Domain          │ Entities, Repository interfaces
├─────────────────┤
│ Data            │ Repository impl, DAO, API
└─────────────────┘
```

## Common Mistakes

❌ Putting business logic in Activity
❌ Passing Context to Repository
❌ Direct database access in ViewModel
❌ Mixing layers
❌ Too many dependencies

## Principles

✅ Clear separation of concerns
✅ Depend on abstractions
✅ Single responsibility
✅ Testable code
✅ Reusable components

## Resources

- [Architecture Guide](https://developer.android.com/jetpack/guide)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Design Patterns](https://refactoring.guru/design-patterns)
