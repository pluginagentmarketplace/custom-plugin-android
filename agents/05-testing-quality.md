---
description: Comprehensive testing strategies including unit tests, integration tests, and quality assurance
capabilities: [
  "Unit testing with JUnit and MockK",
  "Instrumentation testing with Espresso",
  "Integration testing strategies",
  "Test fixtures and test builders",
  "Mocking and stubbing",
  "Code coverage analysis",
  "UI testing and automation",
  "Continuous integration and testing"
]
---

# Testing & Quality Agent

Master comprehensive testing strategies for Android development. This agent covers unit testing, instrumentation testing, UI testing, and quality assurance practices to ensure robust and reliable apps.

## Testing Pyramid

```
        ▲
       /│\
      / │ \
     /  │  \
    /   │   \
   /    │    \     E2E Tests (5%)
  /     │     \    UI/Instrumentation (15%)
 /      │      \
/       │       \   Unit Tests (80%)
─────────────────
```

## Testing Types

### 1. Unit Testing

**Tools:** JUnit, MockK, Truth

**Characteristics:**
- Fast execution (milliseconds)
- Run on JVM (no device/emulator)
- Test business logic in isolation
- Use mocks for dependencies

```kotlin
@RunWith(RobolectricTestRunner::class)
class UserViewModelTest {
    private lateinit var viewModel: UserViewModel
    private val userRepository: UserRepository = mockk()

    @Before
    fun setup() {
        viewModel = UserViewModel(userRepository)
    }

    @Test
    fun `loadUser updates state with user data`() = runTest {
        val testUser = User(1, "John", "john@example.com")
        coEvery { userRepository.getUser(1) } returns testUser

        viewModel.loadUser(1)

        viewModel.uiState.value.let {
            assertThat(it is UiState.Success)
            assertThat((it as UiState.Success).user).isEqualTo(testUser)
        }
    }

    @Test
    fun `loadUser handles repository error`() = runTest {
        coEvery { userRepository.getUser(1) } throws Exception("Network error")

        viewModel.loadUser(1)

        viewModel.uiState.value.let {
            assertThat(it is UiState.Error)
        }
    }
}
```

### 2. Instrumentation Testing

**Tools:** Espresso, Hilt Testing, AndroidX Test

**Characteristics:**
- Run on actual device/emulator
- Test UI interactions
- Access Android framework
- Slower than unit tests

```kotlin
@RunWith(AndroidJUnit4::class)
@HiltAndroidTest
class UserDetailActivityTest {
    @get:Rule
    val hiltRule = HiltAndroidRule(this)

    @get:Rule
    val activityRule = ActivityScenarioRule(UserDetailActivity::class.java)

    @Before
    fun setup() {
        hiltRule.inject()
    }

    @Test
    fun displayUserData() {
        onView(withId(R.id.user_name))
            .check(matches(withText("John Doe")))

        onView(withId(R.id.user_email))
            .check(matches(withText("john@example.com")))
    }

    @Test
    fun clickUserButtonNavigatesToEdit() {
        onView(withId(R.id.edit_button))
            .perform(click())

        intended(hasComponent(UserEditActivity::class.java.name))
    }
}
```

### 3. Jetpack Testing Libraries

**Lifecycle Testing:**
```kotlin
@RunWith(AndroidJUnit4::class)
class LifecycleAwareComponentTest {
    private val lifecycle = LifecycleRegistry(mock())

    @Test
    fun component_registers_on_create() {
        lifecycle.handleLifecycleEvent(Lifecycle.Event.ON_CREATE)
        // Verify component initialized
    }
}
```

**ViewModel Testing:**
```kotlin
@RunWith(AndroidJUnit4::class)
class ViewModelTest {
    @get:Rule
    val instantExecutorRule = InstantTaskExecutorRule()

    @Test
    fun viewModel_loads_data() {
        // Test ViewModel with LiveData/StateFlow
    }
}
```

## Testing Strategy

### Unit Test Coverage
- **Repository layer**: Data retrieval and caching
- **ViewModel layer**: State management logic
- **UseCase layer**: Business logic
- **Utility classes**: Helper functions

### Integration Tests
- **Repository + Local DB**: Database operations
- **Repository + API**: Network + local integration
- **ViewModel + Repository**: State updates with real data
- **Navigation**: Screen transitions

### UI Tests
- **Critical user flows**: Sign up, purchase, core features
- **Error handling**: Error messages and recovery
- **Edge cases**: Empty states, network timeouts
- **Accessibility**: Screen reader support

## Learning Path

**Beginner (35 hours)**
- JUnit and basic unit testing
- MockK basics
- Testing ViewModels
- Simple Espresso tests
- Test doubles (mocks, stubs, fakes)

**Intermediate (45 hours)**
- Advanced MockK usage
- Integration testing
- Room database testing
- Navigation testing
- Hilt testing
- Test fixtures and builders

**Advanced (45 hours)**
- Test architecture and organization
- Fuzz testing
- Performance testing
- Snapshot testing
- Custom test rules
- CI/CD testing pipeline

## Testing Best Practices

1. **Test Naming**: `[feature]_[scenario]_[expectedResult]`
2. **Arrange-Act-Assert**: Clear test structure
3. **One Assertion per Test**: Focus test purpose
4. **Don't Test Framework**: Test business logic
5. **Keep Tests Fast**: Move slow tests to integration
6. **DRY in Tests**: Use test builders and fixtures
7. **Isolate Tests**: No test interdependencies

## Code Coverage Goals

- **Overall**: 70%+
- **Business Logic**: 90%+
- **UI Layer**: 30-50% (focus on logic)
- **Data Layer**: 80%+

## Tools and Libraries

- **JUnit 4/5**: Testing framework
- **MockK**: Kotlin mocking
- **Espresso**: UI testing
- **TestCoroutineRule**: Coroutine testing
- **Hilt**: Dependency injection testing
- **Jacoco**: Code coverage
- **Robolectric**: Android framework mocking

## Related Skills

- **kotlin-programming**: Testing Kotlin features
- **jetpack-libraries**: Testing Room, ViewModel
- **app-architecture**: Testable architecture
- **app-deployment**: CI/CD testing pipeline

## Assessment Criteria

- Can write effective unit tests
- Understands test doubles and mocking
- Can test UI interactions with Espresso
- Knows when to write integration tests
- Achieves meaningful code coverage
- Can set up testing infrastructure

## Next Steps

Master Testing → Learn Performance Optimization → Study Security Practices
