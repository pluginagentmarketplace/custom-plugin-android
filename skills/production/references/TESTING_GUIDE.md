# Android Testing Complete Guide

Comprehensive testing strategy for production-ready apps.

## Testing Pyramid

```
        ┌─────────┐
       /  UI Tests \ 10%
      /─────────────\
     / Integration   \ 20%
    /─────────────────\
   /    Unit Tests     \ 70%
  /─────────────────────\
```

## Unit Testing

### ViewModel Testing
```kotlin
class UserViewModelTest {
    private val getUserUseCase = mockk<GetUserUseCase>()
    private lateinit var viewModel: UserViewModel

    @Before
    fun setup() {
        viewModel = UserViewModel(getUserUseCase)
    }

    @Test
    fun `loadUser updates state to Success`() = runTest {
        // Given
        val user = User(1, "John", "john@example.com")
        coEvery { getUserUseCase(1) } returns user

        // When
        viewModel.loadUser(1)
        advanceUntilIdle()

        // Then
        assertEquals(UiState.Success(user), viewModel.uiState.value)
    }

    @Test
    fun `loadUser updates state to Error on exception`() = runTest {
        // Given
        coEvery { getUserUseCase(any()) } throws IOException("Network error")

        // When
        viewModel.loadUser(1)
        advanceUntilIdle()

        // Then
        assertTrue(viewModel.uiState.value is UiState.Error)
    }
}
```

### Repository Testing
```kotlin
class UserRepositoryTest {
    private val api = mockk<UserApi>()
    private val dao = mockk<UserDao>(relaxed = true)
    private lateinit var repository: UserRepository

    @Before
    fun setup() {
        repository = UserRepositoryImpl(api, dao)
    }

    @Test
    fun `getUser returns cached data when available`() = runTest {
        // Given
        val entity = UserEntity(1, "John", "john@example.com")
        coEvery { dao.getUserById(1) } returns entity

        // When
        val result = repository.getUser(1)

        // Then
        assertEquals("John", result.name)
        coVerify(exactly = 0) { api.getUser(any()) }
    }

    @Test
    fun `getUser fetches from API when cache empty`() = runTest {
        // Given
        coEvery { dao.getUserById(1) } returns null
        coEvery { api.getUser(1) } returns UserDto(1, "John", "john@example.com")

        // When
        val result = repository.getUser(1)

        // Then
        assertEquals("John", result.name)
        coVerify { dao.insert(any()) }
    }
}
```

### UseCase Testing
```kotlin
class GetUserUseCaseTest {
    private val repository = mockk<UserRepository>()
    private val useCase = GetUserUseCase(repository)

    @Test
    fun `invoke returns user from repository`() = runTest {
        // Given
        val user = User(1, "John", "john@example.com")
        coEvery { repository.getUser(1) } returns user

        // When
        val result = useCase(1)

        // Then
        assertEquals(user, result)
    }
}
```

## Integration Testing

### Room Database Testing
```kotlin
@RunWith(AndroidJUnit4::class)
class UserDaoTest {
    private lateinit var db: AppDatabase
    private lateinit var dao: UserDao

    @Before
    fun createDb() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        db = Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java)
            .allowMainThreadQueries()
            .build()
        dao = db.userDao()
    }

    @After
    fun closeDb() {
        db.close()
    }

    @Test
    fun insertAndGetUser() = runTest {
        // Given
        val user = UserEntity(1, "John", "john@example.com")

        // When
        dao.insert(user)
        val result = dao.getUserById(1)

        // Then
        assertEquals("John", result?.name)
    }

    @Test
    fun observeUsers_emitsOnChange() = runTest {
        // Given
        val user = UserEntity(1, "John", "john@example.com")

        // When/Then
        dao.observeUsers().test {
            assertEquals(emptyList<UserEntity>(), awaitItem())

            dao.insert(user)
            assertEquals(listOf(user), awaitItem())

            cancelAndIgnoreRemainingEvents()
        }
    }
}
```

### API Testing with MockWebServer
```kotlin
class UserApiTest {
    private lateinit var mockWebServer: MockWebServer
    private lateinit var api: UserApi

    @Before
    fun setup() {
        mockWebServer = MockWebServer()
        api = Retrofit.Builder()
            .baseUrl(mockWebServer.url("/"))
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(UserApi::class.java)
    }

    @After
    fun tearDown() {
        mockWebServer.shutdown()
    }

    @Test
    fun `getUser returns user`() = runTest {
        // Given
        mockWebServer.enqueue(MockResponse()
            .setBody("""{"id": 1, "name": "John", "email": "john@example.com"}""")
            .setResponseCode(200))

        // When
        val result = api.getUser(1)

        // Then
        assertEquals("John", result.name)
    }

    @Test
    fun `getUser throws on 404`() = runTest {
        // Given
        mockWebServer.enqueue(MockResponse().setResponseCode(404))

        // When/Then
        assertThrows<HttpException> {
            api.getUser(999)
        }
    }
}
```

## UI Testing

### Compose Testing
```kotlin
class UserScreenTest {
    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun displayUserName() {
        // Given
        val user = User(1, "John Doe", "john@example.com")

        // When
        composeTestRule.setContent {
            UserContent(user = user)
        }

        // Then
        composeTestRule.onNodeWithText("John Doe").assertIsDisplayed()
    }

    @Test
    fun showLoadingIndicator() {
        composeTestRule.setContent {
            UserScreen(uiState = UiState.Loading)
        }

        composeTestRule.onNodeWithTag("loading_indicator").assertIsDisplayed()
    }

    @Test
    fun retryButtonClickable() {
        var clicked = false

        composeTestRule.setContent {
            ErrorMessage(
                message = "Error",
                onRetry = { clicked = true }
            )
        }

        composeTestRule.onNodeWithText("Retry").performClick()
        assertTrue(clicked)
    }
}
```

### Hilt Testing
```kotlin
@HiltAndroidTest
class UserFragmentTest {
    @get:Rule
    val hiltRule = HiltAndroidRule(this)

    @get:Rule
    val composeTestRule = createAndroidComposeRule<HiltTestActivity>()

    @Inject
    lateinit var userRepository: FakeUserRepository

    @Before
    fun setup() {
        hiltRule.inject()
    }

    @Test
    fun displayUser() {
        userRepository.setUser(User(1, "Test User", "test@example.com"))

        composeTestRule.setContent {
            UserScreen()
        }

        composeTestRule.onNodeWithText("Test User").assertIsDisplayed()
    }
}
```

## Performance Testing

### Baseline Profiles
```kotlin
@RunWith(AndroidJUnit4::class)
class BaselineProfileGenerator {
    @get:Rule
    val baselineRule = BaselineProfileRule()

    @Test
    fun generateProfile() {
        baselineRule.collectBaselineProfile(
            packageName = "com.example.app"
        ) {
            startActivityAndWait()
            device.findObject(By.text("Users")).click()
            device.waitForIdle()
        }
    }
}
```

### Benchmark Tests
```kotlin
@RunWith(AndroidJUnit4::class)
class UserDaoBenchmark {
    @get:Rule
    val benchmarkRule = BenchmarkRule()

    @Test
    fun insertUsers() {
        val users = (1..1000).map { UserEntity(it, "User$it", "user$it@test.com") }

        benchmarkRule.measureRepeated {
            runBlocking {
                dao.insertAll(users)
            }
        }
    }
}
```

## Deployment Checklist

### Pre-Release
- [ ] All tests passing
- [ ] No lint errors/warnings
- [ ] ProGuard rules verified
- [ ] Version code/name updated
- [ ] Changelog updated
- [ ] Screenshot updated

### Security
- [ ] API keys not in code
- [ ] SSL pinning enabled
- [ ] Debug features disabled
- [ ] Logs removed/disabled
- [ ] Backup disabled if needed

### Performance
- [ ] Baseline profile generated
- [ ] No ANRs in testing
- [ ] Memory leaks checked
- [ ] Startup time acceptable

### Monitoring
- [ ] Crashlytics configured
- [ ] Analytics events tracked
- [ ] Performance monitoring on
- [ ] Alerts configured

## Resources

- [Testing Documentation](https://developer.android.com/training/testing)
- [Compose Testing](https://developer.android.com/jetpack/compose/testing)
- [Hilt Testing Guide](https://developer.android.com/training/dependency-injection/hilt-testing)
- [Baseline Profiles](https://developer.android.com/topic/performance/baselineprofiles)
