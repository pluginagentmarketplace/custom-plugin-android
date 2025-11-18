# /code-examples - Real-World Code Examples

Production-ready code examples for common Android development patterns and tasks.

## Complete MVVM Example

```kotlin
// ViewModel
@HiltViewModel
class UserListViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {
    private val _state = MutableLiveData<UiState>()
    val state: LiveData<UiState> = _state

    fun loadUsers() {
        viewModelScope.launch {
            _state.value = UiState.Loading
            val result = runCatching {
                userRepository.getUsers()
            }
            _state.value = result.fold(
                onSuccess = { users -> UiState.Success(users) },
                onFailure = { error -> UiState.Error(error.message ?: "") }
            )
        }
    }
}

sealed class UiState {
    object Loading : UiState()
    data class Success(val users: List<User>) : UiState()
    data class Error(val message: String) : UiState()
}

// Fragment
class UserListFragment : Fragment(R.layout.fragment_user_list) {
    private val viewModel: UserListViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        viewModel.state.observe(viewLifecycleOwner) { state ->
            when (state) {
                is UiState.Loading -> showLoading()
                is UiState.Success -> showUsers(state.users)
                is UiState.Error -> showError(state.message)
            }
        }

        viewModel.loadUsers()
    }
}
```

## Database with Room

```kotlin
// Entity
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey val id: Int,
    val name: String,
    val email: String,
    val createdAt: Long
)

// DAO
@Dao
interface UserDao {
    @Query("SELECT * FROM users ORDER BY name ASC")
    fun observeAllUsers(): Flow<List<UserEntity>>

    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getUser(userId: Int): UserEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUsers(users: List<UserEntity>)

    @Delete
    suspend fun deleteUser(user: UserEntity)

    @Query("DELETE FROM users")
    suspend fun deleteAll()
}

// Database
@Database(entities = [UserEntity::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao

    companion object {
        @Volatile
        private var instance: AppDatabase? = null

        fun getInstance(context: Context): AppDatabase =
            instance ?: synchronized(this) {
                instance ?: Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "app_database"
                ).build().also { instance = it }
            }
    }
}
```

## Repository Pattern

```kotlin
interface UserRepository {
    suspend fun getUsers(): List<User>
    fun observeUsers(): Flow<List<User>>
    suspend fun getUser(id: Int): User
    suspend fun saveUser(user: User)
}

class UserRepositoryImpl(
    private val userDao: UserDao,
    private val userApi: UserApi
) : UserRepository {
    override suspend fun getUsers(): List<User> {
        return try {
            userApi.fetchUsers().also { users ->
                userDao.insertUsers(users.map { it.toEntity() })
            }.map { it.toDomain() }
        } catch (e: Exception) {
            userDao.getAllUsers().map { it.toDomain() }
        }
    }

    override fun observeUsers(): Flow<List<User>> {
        return userDao.observeAllUsers().map { entities ->
            entities.map { it.toDomain() }
        }
    }

    override suspend fun getUser(id: Int): User {
        return userDao.getUser(id)?.toDomain()
            ?: userApi.fetchUser(id).toDomain()
    }

    override suspend fun saveUser(user: User) {
        userDao.insertUser(user.toEntity())
    }
}
```

## Network with Retrofit

```kotlin
interface UserApi {
    @GET("/users")
    suspend fun fetchUsers(): List<UserDto>

    @GET("/users/{id}")
    suspend fun fetchUser(@Path("id") id: Int): UserDto

    @POST("/users")
    suspend fun createUser(@Body user: CreateUserRequest): UserDto
}

data class UserDto(
    @SerializedName("id")
    val id: Int,
    @SerializedName("name")
    val name: String,
    @SerializedName("email")
    val email: String
) {
    fun toDomain() = User(id, name, email)
}

// Hilt Module
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides
    fun provideOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .build()
    }

    @Provides
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com")
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    @Provides
    fun provideUserApi(retrofit: Retrofit): UserApi {
        return retrofit.create(UserApi::class.java)
    }
}
```

## Dependency Injection with Hilt

```kotlin
@HiltAndroidApp
class MyApp : Application()

@Module
@InstallIn(SingletonComponent::class)
object RepositoryModule {
    @Provides
    fun provideUserRepository(
        userDao: UserDao,
        userApi: UserApi
    ): UserRepository {
        return UserRepositoryImpl(userDao, userApi)
    }
}

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    @Provides
    @Singleton
    fun provideAppDatabase(context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "app_database"
        ).build()
    }

    @Provides
    fun provideUserDao(database: AppDatabase): UserDao {
        return database.userDao()
    }
}
```

## Unit Testing

```kotlin
@RunWith(RobolectricTestRunner::class)
class UserListViewModelTest {
    private val repository = mockk<UserRepository>()
    private lateinit var viewModel: UserListViewModel

    @Before
    fun setup() {
        viewModel = UserListViewModel(repository)
    }

    @Test
    fun `loadUsers success updates state`() = runTest {
        val users = listOf(User(1, "John", "john@example.com"))
        coEvery { repository.getUsers() } returns users

        viewModel.loadUsers()

        assertEquals(UiState.Success(users), viewModel.state.value)
    }

    @Test
    fun `loadUsers failure shows error`() = runTest {
        val error = Exception("Network error")
        coEvery { repository.getUsers() } throws error

        viewModel.loadUsers()

        assertEquals(UiState.Error("Network error"), viewModel.state.value)
    }
}
```

## Navigation

```kotlin
// navGraph.xml
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/nav_graph"
    app:startDestination="@id/userListFragment">

    <fragment
        android:id="@+id/userListFragment"
        android:name=".presentation.ui.UserListFragment"
        android:label="Users" />

    <fragment
        android:id="@+id/userDetailFragment"
        android:name=".presentation.ui.UserDetailFragment"
        android:label="User Details">
        <argument
            android:name="userId"
            app:argType="integer" />
    </fragment>

    <action
        android:id="@+id/action_list_to_detail"
        app:destination="@id/userDetailFragment" />
</navigation>

// In Fragment
findNavController().navigate(
    UserListFragmentDirections.actionListToDetail(userId = 123)
)
```

## WorkManager for Background Jobs

```kotlin
class SyncDataWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {
    @Inject
    lateinit var dataRepository: DataRepository

    override suspend fun doWork(): Result {
        return try {
            dataRepository.syncData()
            Result.success()
        } catch (e: Exception) {
            if (runAttemptCount < 3) {
                Result.retry()
            } else {
                Result.failure()
            }
        }
    }
}

// Schedule work
WorkManager.getInstance(context).enqueueUniquePeriodicWork(
    "data_sync",
    ExistingPeriodicWorkPolicy.REPLACE,
    PeriodicWorkRequestBuilder<SyncDataWorker>(
        15, TimeUnit.MINUTES
    ).setConstraints(
        Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .setRequiresBatteryNotLow(true)
            .build()
    ).build()
)
```

## Secure Data Storage

```kotlin
// Encrypted SharedPreferences
val encryptedSharedPrefs = EncryptedSharedPreferences.create(
    context,
    "secret_prefs",
    MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build(),
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

encryptedSharedPrefs.edit {
    putString("auth_token", token)
    putString("refresh_token", refreshToken)
}

// Retrieve
val token = encryptedSharedPrefs.getString("auth_token", null)
```

## Tips

✅ Always use coroutines for async operations
✅ Never perform database operations on main thread
✅ Use LiveData/Flow for reactive UI updates
✅ Mock all external dependencies in tests
✅ Keep Views and Activities simple
✅ Put business logic in ViewModel or Repository
✅ Use strict null safety
✅ Handle errors explicitly
✅ Test edge cases
✅ Profile before optimizing

---

These examples follow production best practices. Use them as templates for your projects!
