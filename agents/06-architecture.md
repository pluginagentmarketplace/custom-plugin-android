---
name: 06-architecture
description: Architecture & Design Patterns - MVVM, Clean Architecture, Repository, SOLID, Hilt DI (40 hours)
model: sonnet
tools: All tools
sasmp_version: "1.3.0"
eqhm_enabled: true
skills:
  - architecture
triggers:
  - MVVM
  - clean architecture
  - repository pattern
  - dependency injection
  - hilt
capabilities:
  - MVVM pattern
  - Clean Architecture
  - Repository pattern
  - Dependency injection
  - SOLID principles
  - Design patterns
  - Testable architecture
  - Layered design
  - Use cases
  - Data flow
prerequisites:
  - Fundamentals
  - Platform
  - Data Management
  - Networking
keywords:
  - architecture
  - mvvm
  - clean architecture
  - repository
  - solid
  - hilt
  - dependency injection
  - design pattern
---

# Architecture Agent: Scalable & Maintainable App Design

Design enterprise-grade Android applications using MVVM, Clean Architecture, Repository Pattern, and SOLID principles. Build scalable, testable, and maintainable codebases using proven architectural patterns.

**Prerequisite**: Fundamentals, Platform, Data Management & Networking agents
**Duration**: 40 hours | **Level**: Advanced
**Topics**: 7 major areas | **Code Examples**: 35+ real-world patterns

---

## 1. MVVM ARCHITECTURE

MVVM (Model-View-ViewModel) separates concerns and enables testable, lifecycle-aware UI logic.

### 1.1 Complete MVVM Implementation

```kotlin
// Domain: Business data
data class User(
    val id: Int,
    val name: String,
    val email: String
)

// ViewModel: State management & logic
@HiltViewModel
class UserListViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    init {
        loadUsers()
    }

    fun loadUsers() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            when (val result = userRepository.getUsers()) {
                is Result.Success -> _uiState.value = UiState.Success(result.data)
                is Result.Error -> _uiState.value = UiState.Error(result.exception.message)
            }
        }
    }

    fun deleteUser(user: User) {
        viewModelScope.launch {
            userRepository.deleteUser(user)
            loadUsers()
        }
    }
}

sealed class UiState {
    object Loading : UiState()
    data class Success(val users: List<User>) : UiState()
    data class Error(val message: String) : UiState()
}

// View: UI & user interaction
class UserListFragment : Fragment() {
    private val viewModel: UserListViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.uiState.collect { state ->
                    when (state) {
                        is UiState.Loading -> showLoading()
                        is UiState.Success -> showUsers(state.users)
                        is UiState.Error -> showError(state.message)
                    }
                }
            }
        }
    }
}
```

### 1.2 MVVM Benefits

- **Lifecycle Awareness**: ViewModel survives configuration changes
- **Separation of Concerns**: UI logic separate from business logic
- **Testability**: ViewModel can be tested without UI
- **Reactive**: LiveData/StateFlow automatic UI updates
- **State Management**: Clear data flow from ViewModel to View

---

## 2. CLEAN ARCHITECTURE

Four concentric layers with strict dependency rules - dependencies point inward toward Domain.

### 2.1 Layer Structure

```
┌─────────────────────────────────────────────┐
│  PRESENTATION LAYER (UI, ViewModels)       │
│  ↓ depends on                               │
├─────────────────────────────────────────────┤
│  APPLICATION LAYER (Use Cases, Orchestration)
│  ↓ depends on                               │
├─────────────────────────────────────────────┤
│  DOMAIN LAYER (Business Rules, Entities)   │
│  ↑ depended on by all layers                │
├─────────────────────────────────────────────┤
│  INFRASTRUCTURE LAYER (DB, APIs, Services) │
└─────────────────────────────────────────────┘
```

### 2.2 Domain Layer (Framework-independent)

```kotlin
// Domain entities
data class User(
    val id: Int,
    val name: String,
    val email: String
)

// Domain interfaces (no implementation details!)
interface UserRepository {
    suspend fun getUsers(): Result<List<User>>
    suspend fun getUser(id: Int): Result<User>
    suspend fun saveUser(user: User): Result<Unit>
    suspend fun deleteUser(id: Int): Result<Unit>
}

// Domain use cases (business logic)
class GetUsersUseCase(
    private val userRepository: UserRepository
) {
    suspend operator fun invoke(): Result<List<User>> {
        return userRepository.getUsers()
    }
}

class GetUserUseCase(
    private val userRepository: UserRepository
) {
    suspend operator fun invoke(id: Int): Result<User> {
        return userRepository.getUser(id)
    }
}
```

### 2.3 Application Layer (Use Cases)

```kotlin
// Use case orchestration
@HiltViewModel
class UserListViewModel @Inject constructor(
    private val getUsersUseCase: GetUsersUseCase,
    private val deleteUserUseCase: DeleteUserUseCase
) : ViewModel() {

    private val _state = MutableStateFlow<UiState>(UiState.Loading)
    val state: StateFlow<UiState> = _state.asStateFlow()

    fun loadUsers() {
        viewModelScope.launch {
            when (val result = getUsersUseCase()) {
                is Result.Success -> _state.value = UiState.Success(result.data)
                is Result.Error -> _state.value = UiState.Error(result.exception)
            }
        }
    }
}
```

### 2.4 Infrastructure Layer (Implementation Details)

```kotlin
// Room database
@Entity
data class UserEntity(
    @PrimaryKey val id: Int,
    val name: String,
    val email: String
) {
    fun toDomain() = User(id, name, email)
}

@Dao
interface UserDao {
    @Query("SELECT * FROM users")
    suspend fun getAllUsers(): List<UserEntity>
}

// Retrofit API
interface UserApi {
    @GET("/users")
    suspend fun getUsers(): List<UserDto>
}

// Repository implementation
@Singleton
class UserRepositoryImpl @Inject constructor(
    private val userDao: UserDao,
    private val userApi: UserApi
) : UserRepository {

    override suspend fun getUsers(): Result<List<User>> = safeCall {
        // Try network first, fallback to database
        try {
            val remoteUsers = userApi.getUsers().map { it.toDomain() }
            userDao.insertAll(remoteUsers.map { it.toEntity() })
            remoteUsers
        } catch (e: Exception) {
            userDao.getAllUsers().map { it.toDomain() }
        }
    }

    override suspend fun getUser(id: Int): Result<User> = safeCall {
        userDao.getUser(id)?.toDomain() ?: userApi.getUser(id).toDomain()
    }

    override suspend fun saveUser(user: User): Result<Unit> = safeCall {
        userDao.insert(user.toEntity())
    }

    override suspend fun deleteUser(id: Int): Result<Unit> = safeCall {
        userDao.delete(id)
    }

    private suspend inline fun <T> safeCall(crossinline block: suspend () -> T): Result<T> {
        return try {
            Result.Success(block())
        } catch (e: Exception) {
            Result.Error(e)
        }
    }
}
```

### 2.5 Presentation Layer (UI)

```kotlin
@HiltViewModel
class UserListViewModel @Inject constructor(
    private val getUsersUseCase: GetUsersUseCase
) : ViewModel() {
    val uiState: StateFlow<UiState> = // ...
}

class UserListFragment : Fragment() {
    private val viewModel: UserListViewModel by viewModels()
    // ... UI code
}
```

---

## 3. REPOSITORY PATTERN

Single point of data access abstraction across multiple sources.

```kotlin
// Repository controls data flow
class UserRepository @Inject constructor(
    private val localDataSource: UserLocalDataSource,
    private val remoteDataSource: UserRemoteDataSource
) {
    // Local-first strategy: Always check local first
    suspend fun getUser(id: Int): User {
        val localUser = localDataSource.getUser(id)
        return if (localUser != null) {
            localUser
        } else {
            val remoteUser = remoteDataSource.getUser(id)
            localDataSource.saveUser(remoteUser)
            remoteUser
        }
    }

    // Reactive: Observe local database
    fun observeUsers(): Flow<List<User>> =
        localDataSource.observeAllUsers()
            .onEach { users ->
                // Background sync with remote
                try {
                    val remoteUsers = remoteDataSource.getUsers()
                    localDataSource.saveUsers(remoteUsers)
                } catch (e: Exception) {
                    // Use local data if sync fails
                }
            }
}
```

---

## 4. SOLID PRINCIPLES

### 4.1 Single Responsibility Principle

```kotlin
// ❌ BAD: Multiple reasons to change
class UserManager {
    fun loadUsers() { }      // Reason 1: API changes
    fun saveToDatabase() { } // Reason 2: DB schema changes
    fun updateUI() { }       // Reason 3: UI changes
    fun validateEmail() { }  // Reason 4: Business logic changes
}

// ✅ GOOD: Single responsibility each
class UserRepository {       // Only: Data access
    fun getUsers() { }
}

class UserValidator {        // Only: Business logic
    fun isValidEmail(email: String) { }
}

class UserViewModel {        // Only: State management
    fun loadUsers() { }
}
```

### 4.2 Open/Closed Principle

```kotlin
// ❌ BAD: Must modify class for new payment types
class PaymentProcessor {
    fun processPayment(type: String, amount: Double) {
        when (type) {
            "credit_card" -> processCreditCard(amount)
            "paypal" -> processPayPal(amount)
            // Add new method every time new payment type added
        }
    }
}

// ✅ GOOD: Extend without modifying
interface PaymentProcessor {
    fun process(amount: Double)
}

class CreditCardProcessor : PaymentProcessor {
    override fun process(amount: Double) { }
}

class PayPalProcessor : PaymentProcessor {
    override fun process(amount: Double) { }
}

// Easy to add new processor without modifying existing code
```

### 4.3 Liskov Substitution Principle

```kotlin
// ❌ BAD: Subclass violates contract
abstract class Bird {
    abstract fun fly()
}

class Penguin : Bird() {
    override fun fly() {
        throw NotImplementedError("Penguins can't fly!")
    }
}

// ✅ GOOD: Proper hierarchy
abstract class Bird {
    abstract fun move()
}

class Sparrow : Bird() {
    override fun move() { /* fly */ }
}

class Penguin : Bird() {
    override fun move() { /* swim */ }
}
```

### 4.4 Interface Segregation Principle

```kotlin
// ❌ BAD: Fat interface
interface Worker {
    fun work()
    fun eat()
    fun sleep()
    fun buildReport()  // Not all workers need this
}

// ✅ GOOD: Segregated interfaces
interface Worker {
    fun work()
}

interface Eater {
    fun eat()
}

interface Sleeper {
    fun sleep()
}

interface Reportable {
    fun buildReport()
}

class Developer : Worker, Eater, Sleeper, Reportable {
    override fun work() { }
    override fun eat() { }
    override fun sleep() { }
    override fun buildReport() { }
}

class Robot : Worker {
    override fun work() { }
    // Robot doesn't need eat/sleep/report
}
```

### 4.5 Dependency Inversion Principle

```kotlin
// ❌ BAD: Depends on concrete implementation
class UserViewModel {
    private val database = MySQLDatabase()  // Depends on MySQL!
    fun loadUsers() {
        val users = database.query("SELECT * FROM users")
    }
}

// ✅ GOOD: Depends on abstraction
interface Database {
    suspend fun query(sql: String): Any
}

class UserViewModel(private val database: Database) {  // Injected!
    fun loadUsers() {
        val users = database.query("SELECT * FROM users")
    }
}

// Can swap MySQL, SQLite, Firebase easily
class MySQLDatabase : Database { }
class FirebaseDatabase : Database { }
```

---

## 5. DEPENDENCY INJECTION WITH HILT

Automatic dependency management using annotations.

```kotlin
// 1. Mark app class
@HiltAndroidApp
class MyApp : Application()

// 2. Provide dependencies
@Module
@InstallIn(SingletonComponent::class)
object RepositoryModule {
    @Provides
    @Singleton
    fun provideUserRepository(
        userDao: UserDao,
        userApi: UserApi
    ): UserRepository = UserRepositoryImpl(userDao, userApi)

    @Provides
    fun provideGetUsersUseCase(
        repository: UserRepository
    ) = GetUsersUseCase(repository)
}

// 3. Inject where needed
@HiltViewModel
class UserListViewModel @Inject constructor(
    private val getUsersUseCase: GetUsersUseCase
) : ViewModel()

class UserListFragment : Fragment() {
    private val viewModel: UserListViewModel by viewModels()
}
```

---

## 6. DESIGN PATTERNS

### 6.1 Factory Pattern

```kotlin
interface DataSourceFactory {
    fun createUserDataSource(): UserDataSource
}

class AndroidDataSourceFactory : DataSourceFactory {
    override fun createUserDataSource(): UserDataSource {
        return RoomUserDataSource()  // Platform-specific
    }
}

// Usage: No coupling to specific implementation
val dataSource = factory.createUserDataSource()
```

### 6.2 Strategy Pattern

```kotlin
// Different authentication strategies
interface AuthStrategy {
    suspend fun authenticate(username: String, password: String): AuthResult
}

class OAuthStrategy : AuthStrategy {
    override suspend fun authenticate(...) = /* OAuth flow */
}

class BasicAuthStrategy : AuthStrategy {
    override suspend fun authenticate(...) = /* Username/password */
}

// Use strategy based on configuration
class AuthManager(private val strategy: AuthStrategy) {
    suspend fun login(u: String, p: String) = strategy.authenticate(u, p)
}
```

### 6.3 Observer Pattern

```kotlin
// LiveData / Flow implement observer pattern
class UserViewModel : ViewModel() {
    private val _user = MutableLiveData<User>()
    val user: LiveData<User> = _user

    // Observers automatically notified of changes
    _user.value = User(1, "John")
}

class UserFragment : Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        viewModel.user.observe(viewLifecycleOwner) { user ->
            // Automatically called when user changes
            updateUI(user)
        }
    }
}
```

---

## 7. BEST PRACTICES

✅ **Architecture**
- Use Clean Architecture for complex apps
- Keep domain layer pure (no Android dependencies)
- Repository pattern for all data access
- Use cases for business logic

✅ **SOLID**
- One class = one reason to change
- Extend, don't modify (Open/Closed)
- Substitute subtypes safely (Liskov)
- Segregate interfaces properly
- Always depend on abstractions

✅ **Dependency Injection**
- Use Hilt for automatic DI
- Inject interfaces, not implementations
- Constructor injection preferred
- Mock dependencies in tests

✅ **Testing**
- Test use cases and ViewModels
- Mock repositories in tests
- Use FakeRepository for integration tests
- Avoid testing UI directly

---

## 8. LEARNING PATH: 3 WEEKS (40 HOURS)

**Week 1 (14h): MVVM & Clean Architecture**
- MVVM pattern with ViewModel
- Clean Architecture 4 layers
- Dependency direction rules
- Practice building layered app

**Week 2 (13h): Repository & SOLID**
- Repository pattern implementation
- Local-first data strategy
- All 5 SOLID principles
- Design patterns overview

**Week 3 (13h): Hilt & Advanced**
- Hilt dependency injection setup
- Module creation and provides
- Testing architecture
- Production-quality patterns

---

**Mastery Checkpoint**:
- Can design clean architecture
- Apply all SOLID principles
- Use Hilt effectively
- Write testable code
- Choose appropriate patterns

---

**Learning Hours**: 40 hours | **Level**: Advanced
**Next Step**: Production Quality agent (Testing, Security, Deployment)
