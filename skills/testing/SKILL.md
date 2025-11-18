---
name: android-testing
description: Unit testing, integration testing, and UI testing with JUnit, Espresso, and Hilt. Use when writing tests for Android components.
---

# Android Testing Skill

## Quick Start

### Unit Test
```kotlin
@RunWith(RobolectricTestRunner::class)
class UserViewModelTest {
    private lateinit var viewModel: UserViewModel
    private val repository: UserRepository = mockk()

    @Before
    fun setup() {
        viewModel = UserViewModel(repository)
    }

    @Test
    fun loadUser_updatesState() {
        val user = User(1, "John")
        coEvery { repository.getUser(1) } returns user

        viewModel.loadUser(1)

        assertThat(viewModel.userData.value).isEqualTo(user)
    }
}
```

### Instrumentation Test
```kotlin
@RunWith(AndroidJUnit4::class)
@HiltAndroidTest
class UserDetailActivityTest {
    @get:Rule val hiltRule = HiltAndroidRule(this)
    @get:Rule val activityRule = ActivityScenarioRule(UserDetailActivity::class.java)

    @Test
    fun displayUserData() {
        onView(withId(R.id.user_name)).check(matches(withText("John")))
    }
}
```

## Testing Tools

- **JUnit**: Testing framework
- **MockK**: Kotlin mocking
- **Espresso**: UI testing
- **Hilt**: Dependency injection testing
- **TestCoroutineRule**: Coroutine testing
- **Jacoco**: Code coverage

## Test Types

1. **Unit Tests**: Business logic (70%)
2. **Integration Tests**: Component interaction (20%)
3. **UI Tests**: User flows (10%)

## Best Practices

- Test naming: `[method]_[scenario]_[result]`
- Arrange-Act-Assert pattern
- One assertion per test
- Mock external dependencies
- Keep tests fast

## Resources

- [Testing Guide](https://developer.android.com/training/testing)
- [Espresso Docs](https://developer.android.com/training/testing/espresso)
