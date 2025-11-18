---
name: app-architecture
description: Architectural patterns for Android apps including MVVM, Clean Architecture, and design patterns. Use when designing app structure and organizing code layers.
---

# App Architecture Skill

## Quick Start

### MVVM Pattern
```kotlin
// Model
data class User(val id: Int, val name: String)

// ViewModel
class UserViewModel(repository: UserRepository) : ViewModel() {
    val userData: LiveData<User> = repository.getUser()
}

// View
class UserActivity : AppCompatActivity() {
    val viewModel: UserViewModel by viewModels()
    override fun onCreate(savedInstanceState: Bundle?) {
        viewModel.userData.observe(this) { user ->
            updateUI(user)
        }
    }
}
```

### Repository Pattern
```kotlin
interface UserRepository {
    suspend fun getUser(id: Int): User
}

class UserRepositoryImpl(
    private val userDao: UserDao,
    private val userApi: UserApi
) : UserRepository {
    override suspend fun getUser(id: Int) =
        userDao.getUser(id) ?: userApi.fetchUser(id)
}
```

### Dependency Injection
```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel()
```

## Architectural Layers

```
Presentation (UI, ViewModels)
    ↓
Domain (UseCases, Entities, Repositories)
    ↓
Data (DataSources, Repositories)
```

## Design Patterns

- **MVVM**: Separation of UI and business logic
- **Repository**: Abstract data sources
- **Singleton**: Single instance (use with DI)
- **Factory**: Object creation
- **Observer**: State change notifications

## Best Practices

- Keep layers independent
- Inject dependencies
- Use interfaces for abstraction
- Test business logic separately
- Avoid circular dependencies

## Resources

- [Architecture Guide](https://developer.android.com/jetpack/guide)
- [Clean Architecture](https://blog.cleancoder.com/)
