---
description: Architectural patterns for scalable Android apps including MVVM, Clean Architecture, and design patterns
capabilities: [
  "MVVM architecture pattern",
  "Clean Architecture principles",
  "Repository pattern and data layer",
  "Dependency injection strategies",
  "Design patterns (Singleton, Factory, Observer)",
  "Layer separation and abstraction",
  "Reactive programming patterns",
  "Testing-friendly architecture"
]
---

# Architecture Patterns Agent

Learn how to structure large-scale Android applications with proven architectural patterns. This agent teaches MVVM, Clean Architecture, and other design patterns that enable maintainability, testability, and scalability.

## Architectural Patterns

### 1. MVVM (Model-View-ViewModel)
- **Model**: Data and business logic
- **View**: UI components (Activity/Fragment)
- **ViewModel**: UI state and logic, lifecycle-aware

**Advantages:**
- Clear separation of concerns
- Testable business logic
- Lifecycle awareness
- Data binding support

**Key Components:**
- LiveData/StateFlow for observable state
- ViewModel for state management
- Repository for data abstraction
- UseCase/Interactor for business logic

### 2. Clean Architecture
```
┌──────────────────┐
│   Presentation   │  (Activities, Fragments, ViewModels)
├──────────────────┤
│   Domain         │  (UseCases, Entities, Repositories)
├──────────────────┤
│   Data           │  (Repositories, DataSources, APIs)
└──────────────────┘
```

**Principles:**
- Independence from frameworks
- Testability
- Independence from UI
- Independence from database
- Independence of any external agency

### 3. Repository Pattern
- Single source of truth for data
- Abstracts data sources (local, remote)
- Provides clean API for ViewModels
- Handles caching strategies

```kotlin
interface UserRepository {
    suspend fun getUser(id: Int): User
    suspend fun saveUser(user: User)
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
}
```

### 4. Design Patterns

**Creational:**
- **Factory Pattern**: Create objects without specifying classes
- **Singleton Pattern**: Single instance (use with DI)
- **Builder Pattern**: Complex object construction

**Structural:**
- **Adapter Pattern**: Interface compatibility
- **Decorator Pattern**: Add responsibilities dynamically
- **Facade Pattern**: Simplified interface

**Behavioral:**
- **Observer Pattern**: State change notifications (LiveData)
- **Strategy Pattern**: Interchangeable algorithms
- **State Pattern**: Object behavior based on state

## Learning Path

**Beginner (35 hours)**
- MVVM basics with ViewModel and LiveData
- Repository pattern
- Simple layer separation
- Basic design patterns

**Intermediate (50 hours)**
- Full Clean Architecture implementation
- Advanced MVVM with StateFlow
- UseCase/Interactor pattern
- Complex repository strategies
- Design patterns in practice
- Testing architecture

**Advanced (45 hours)**
- Enterprise architecture patterns
- Micro-architecture decisions
- Complex domain modeling
- CQRS and Event Sourcing
- Domain-Driven Design (DDD)
- Architecture testing

## Practical Example: Clean Architecture

```kotlin
// Domain Layer - Pure business logic
interface GetUserUseCase {
    suspend operator fun invoke(id: Int): Result<User>
}

class GetUserUseCaseImpl(
    private val userRepository: UserRepository
) : GetUserUseCase {
    override suspend fun invoke(id: Int) = userRepository.getUser(id)
}

// Presentation Layer - ViewModel
@HiltViewModel
class UserDetailViewModel @Inject constructor(
    private val getUserUseCase: GetUserUseCase
) : ViewModel() {
    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    fun loadUser(id: Int) {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            val result = getUserUseCase(id)
            _uiState.value = when {
                result.isSuccess -> UiState.Success(result.getOrNull()!!)
                else -> UiState.Error(result.exceptionOrNull()?.message ?: "Unknown error")
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
        userDao.getUser(id)?.let { return@runCatching it }
        userApi.fetchUser(id).also { user ->
            userDao.insertUser(user)
        }
    }
}
```

## Architectural Decision Records

### When to use MVVM
- Standard Android apps
- Complex UI state management
- Need for data binding
- Good testability required

### When to use Clean Architecture
- Large-scale applications
- Multiple teams working on same app
- Complex business logic
- Long-term maintenance critical

### When to use Repository Pattern
- Multiple data sources (local + remote)
- Complex caching strategies
- Need for data abstraction
- Testing data layer in isolation

## Key Concepts

1. **Separation of Concerns**: Each layer has single responsibility
2. **Dependency Inversion**: Depend on abstractions, not implementations
3. **Testability**: Business logic independent of framework
4. **Reusability**: Components usable across different contexts
5. **Maintainability**: Clear structure enables future changes

## Related Skills

- **kotlin-programming**: Coroutines and extensions
- **jetpack-libraries**: ViewModel, LiveData, Room
- **android-testing**: Testing each layer
- **performance-tuning**: Optimizing data flow

## Assessment Criteria

- Can design MVVM architecture
- Understands Clean Architecture principles
- Can implement Repository pattern
- Applies appropriate design patterns
- Creates testable, maintainable code

## Next Steps

Master Architectural Patterns → Study Performance Optimization → Learn Testing Strategies
