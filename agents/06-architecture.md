---
description: Architecture patterns and design - MVVM, Clean Architecture, Repository Pattern, SOLID principles, dependency injection - enterprise-grade app structure
capabilities: ["MVVM pattern", "Clean Architecture", "Repository pattern", "Dependency injection", "SOLID principles", "Design patterns", "Testable architecture", "Layered design"]
---

# Architecture Agent

Design scalable and maintainable Android applications using MVVM, Clean Architecture, Repository Pattern, and SOLID principles.

## MVVM Pattern

### Three Layers
1. **Model**: Data and business logic
2. **View**: UI (Activity, Fragment)
3. **ViewModel**: State management and logic

### ViewModel
```kotlin
class UserViewModel(repository: UserRepository) : ViewModel() {
    private val _user = MutableLiveData<User>()
    val user: LiveData<User> = _user
    
    fun loadUser(id: Int) {
        viewModelScope.launch {
            _user.value = repository.getUser(id)
        }
    }
}
```

### Benefits
- Lifecycle awareness
- Configuration change handling
- Testable business logic
- Clear separation of concerns

## Clean Architecture

### Four Layers
1. **Domain**: Business rules (entities, interfaces)
2. **Application**: Use cases and orchestration
3. **Presentation**: UI and ViewModels
4. **Infrastructure**: Database, APIs, OS services

### Dependency Direction
All dependencies point inward toward Domain layer

### Benefits
- Framework independence
- Database independence
- UI independence
- Highly testable
- Business logic isolated

## Repository Pattern

### Purpose
Abstraction over data sources (local, remote, cache)

### Implementation
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
        return userDao.getUser(id) 
            ?: userApi.fetchUser(id).also { userDao.insert(it) }
    }
}
```

### Single Source of Truth
Local database as source of truth with remote sync

## SOLID Principles

### Single Responsibility
Each class has one reason to change

### Open/Closed
Open for extension, closed for modification

### Liskov Substitution
Subtypes substitutable for parent types

### Interface Segregation
Small, focused interfaces instead of fat ones

### Dependency Inversion
Depend on abstractions, not concrete classes

## Dependency Injection

### Hilt (Recommended)
```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel()

@Module
@InstallIn(SingletonComponent::class)
object RepositoryModule {
    @Provides
    fun provideUserRepository(
        dao: UserDao, api: UserApi
    ): UserRepository = UserRepositoryImpl(dao, api)
}
```

## Design Patterns

### Factory Pattern
Create objects without specifying exact classes

### Observer Pattern
(LiveData, Flow automatically implement this)

### Strategy Pattern
Interchangeable algorithms

### Adapter Pattern
Convert interface compatibility

## Testing Architecture

### Unit Test Example
```kotlin
@Test
fun loadUser_updates_state() = runTest {
    val user = User(1, "John")
    val mockRepository = mockk<UserRepository>()
    coEvery { mockRepository.getUser(1) } returns user
    
    val viewModel = UserViewModel(mockRepository)
    viewModel.loadUser(1)
    
    assertEquals(user, viewModel.user.value)
}
```

## Learning Outcomes
- Design enterprise-grade architecture
- Apply SOLID principles consistently
- Implement dependency injection
- Create testable code
- Choose appropriate patterns

---

**Learning Hours**: 40 hours | **Level**: Advanced
