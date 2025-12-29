# Android Architecture Guide

Building scalable, maintainable, and testable applications.

## MVVM Pattern

### Complete Implementation

```kotlin
// ViewModel
@HiltViewModel
class UserViewModel @Inject constructor(
    private val getUserUseCase: GetUserUseCase,
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _uiState = MutableStateFlow<UiState<User>>(UiState.Loading)
    val uiState: StateFlow<UiState<User>> = _uiState.asStateFlow()

    private val userId: Int = savedStateHandle["userId"] ?: 0

    init {
        loadUser()
    }

    fun loadUser() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            try {
                val user = getUserUseCase(userId)
                _uiState.value = UiState.Success(user)
            } catch (e: Exception) {
                _uiState.value = UiState.Error(e.message ?: "Unknown error")
            }
        }
    }

    fun retry() = loadUser()
}

// UI State
sealed class UiState<out T> {
    object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String) : UiState<Nothing>()
}

// Composable Screen
@Composable
fun UserScreen(viewModel: UserViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    when (val state = uiState) {
        is UiState.Loading -> LoadingIndicator()
        is UiState.Success -> UserContent(state.data)
        is UiState.Error -> ErrorMessage(state.message, onRetry = viewModel::retry)
    }
}
```

## Clean Architecture

### Layer Structure

```
┌─────────────────────────────────────┐
│         Presentation Layer          │
│   (UI, ViewModel, Navigation)       │
├─────────────────────────────────────┤
│           Domain Layer              │
│   (UseCases, Repository Interface,  │
│    Domain Models)                   │
├─────────────────────────────────────┤
│            Data Layer               │
│   (Repository Impl, DataSources,    │
│    DTOs, Entities)                  │
└─────────────────────────────────────┘
```

### UseCase Pattern
```kotlin
// Simple UseCase
class GetUserUseCase @Inject constructor(
    private val repository: UserRepository
) {
    suspend operator fun invoke(userId: Int): User {
        return repository.getUser(userId)
    }
}

// UseCase with Flow
class ObserveUsersUseCase @Inject constructor(
    private val repository: UserRepository
) {
    operator fun invoke(): Flow<List<User>> {
        return repository.observeUsers()
    }
}

// UseCase with Parameters
class SearchUsersUseCase @Inject constructor(
    private val repository: UserRepository
) {
    suspend operator fun invoke(params: Params): List<User> {
        return repository.searchUsers(params.query, params.page)
    }

    data class Params(val query: String, val page: Int = 1)
}
```

### Repository Pattern
```kotlin
// Domain Layer - Interface
interface UserRepository {
    suspend fun getUser(id: Int): User
    fun observeUsers(): Flow<List<User>>
    suspend fun saveUser(user: User)
    suspend fun deleteUser(id: Int)
}

// Data Layer - Implementation
class UserRepositoryImpl @Inject constructor(
    private val remoteDataSource: UserRemoteDataSource,
    private val localDataSource: UserLocalDataSource
) : UserRepository {

    override suspend fun getUser(id: Int): User {
        // Try cache first
        localDataSource.getUser(id)?.let { return it.toUser() }

        // Fetch from network
        val dto = remoteDataSource.getUser(id)
        localDataSource.saveUser(dto.toEntity())
        return dto.toUser()
    }

    override fun observeUsers(): Flow<List<User>> {
        return localDataSource.observeUsers()
            .map { entities -> entities.map { it.toUser() } }
    }
}
```

## Dependency Injection with Hilt

### Module Setup
```kotlin
@Module
@InstallIn(SingletonComponent::class)
object RepositoryModule {

    @Provides
    @Singleton
    fun provideUserRepository(
        remoteDataSource: UserRemoteDataSource,
        localDataSource: UserLocalDataSource
    ): UserRepository {
        return UserRepositoryImpl(remoteDataSource, localDataSource)
    }
}

@Module
@InstallIn(ViewModelComponent::class)
object UseCaseModule {

    @Provides
    @ViewModelScoped
    fun provideGetUserUseCase(
        repository: UserRepository
    ): GetUserUseCase {
        return GetUserUseCase(repository)
    }
}
```

### ViewModel Injection
```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val getUserUseCase: GetUserUseCase,
    private val updateUserUseCase: UpdateUserUseCase
) : ViewModel()
```

## Data Mapping

```kotlin
// DTO (Data Transfer Object) - from API
data class UserDto(
    @SerializedName("id") val id: Int,
    @SerializedName("full_name") val name: String,
    @SerializedName("email_address") val email: String
)

// Entity - for Room database
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey val id: Int,
    val name: String,
    val email: String,
    val cachedAt: Long = System.currentTimeMillis()
)

// Domain Model - business logic
data class User(
    val id: Int,
    val name: String,
    val email: String
)

// Mappers
fun UserDto.toUser() = User(id, name, email)
fun UserDto.toEntity() = UserEntity(id, name, email)
fun UserEntity.toUser() = User(id, name, email)
```

## Navigation Architecture

```kotlin
// Navigation Graph with Type-Safe Args
@Serializable
sealed class Screen {
    @Serializable
    object Home : Screen()

    @Serializable
    data class UserDetail(val userId: Int) : Screen()

    @Serializable
    data class Settings(val section: String? = null) : Screen()
}

@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(navController, startDestination = Screen.Home) {
        composable<Screen.Home> {
            HomeScreen(
                onUserClick = { userId ->
                    navController.navigate(Screen.UserDetail(userId))
                }
            )
        }
        composable<Screen.UserDetail> { backStackEntry ->
            val args = backStackEntry.toRoute<Screen.UserDetail>()
            UserDetailScreen(userId = args.userId)
        }
    }
}
```

## Error Handling Strategy

```kotlin
// Result wrapper
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: AppException) : Result<Nothing>()
}

// Custom exceptions
sealed class AppException : Exception() {
    data class Network(override val message: String) : AppException()
    data class Api(val code: Int, override val message: String) : AppException()
    data class Database(override val message: String) : AppException()
    object Unknown : AppException()
}

// Repository with error handling
class UserRepositoryImpl : UserRepository {
    override suspend fun getUser(id: Int): Result<User> {
        return try {
            val user = api.getUser(id).toUser()
            Result.Success(user)
        } catch (e: IOException) {
            Result.Error(AppException.Network("Network error"))
        } catch (e: HttpException) {
            Result.Error(AppException.Api(e.code(), e.message()))
        } catch (e: Exception) {
            Result.Error(AppException.Unknown)
        }
    }
}
```

## Best Practices

1. **Single Source of Truth** - Database is the source
2. **Unidirectional Data Flow** - State flows down, events up
3. **Separation of Concerns** - Each layer has its responsibility
4. **Immutability** - Prefer immutable data classes
5. **Dependency Injection** - Testable and modular
6. **Interface-Based Design** - Easy to mock and test

## Resources

- [Guide to App Architecture](https://developer.android.com/jetpack/guide)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Hilt Documentation](https://developer.android.com/training/dependency-injection/hilt-android)
