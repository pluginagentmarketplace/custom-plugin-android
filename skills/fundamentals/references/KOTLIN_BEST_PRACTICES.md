# Kotlin Best Practices Guide

Essential patterns and practices for professional Kotlin development.

## 1. Null Safety

### Use Elvis Operator for Defaults
```kotlin
// ✅ Good
val name = user?.name ?: "Unknown"

// ❌ Avoid
val name = if (user?.name != null) user.name else "Unknown"
```

### Safe Calls with let
```kotlin
// ✅ Good - null-safe block execution
user?.let { u ->
    updateUI(u.name)
    saveUser(u)
}

// ❌ Avoid
if (user != null) {
    updateUI(user.name)
    saveUser(user)
}
```

### Avoid !! (Non-null assertion)
```kotlin
// ✅ Good
val user = repository.getUser() ?: throw UserNotFoundException()

// ❌ Avoid - crashes with NullPointerException
val user = repository.getUser()!!
```

## 2. Data Classes

### Use for Value Objects
```kotlin
// ✅ Good - auto-generates equals, hashCode, toString, copy
data class User(
    val id: Int,
    val name: String,
    val email: String
)

// Usage
val copy = user.copy(name = "New Name")
val (id, name, _) = user  // Destructuring
```

### Sealed Classes for State
```kotlin
// ✅ Exhaustive when expression
sealed class UiState<out T> {
    object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String) : UiState<Nothing>()
}

when (state) {
    is UiState.Loading -> showLoading()
    is UiState.Success -> showData(state.data)
    is UiState.Error -> showError(state.message)
}
```

## 3. Extension Functions

### Extend Existing Types
```kotlin
// Add validation to String
fun String.isValidEmail(): Boolean =
    Patterns.EMAIL_ADDRESS.matcher(this).matches()

fun String.isValidPassword(): Boolean =
    length >= 8 && any { it.isDigit() } && any { it.isUpperCase() }

// Usage
if (email.isValidEmail()) { ... }
```

### Context Extensions for Android
```kotlin
fun Context.showToast(message: String) =
    Toast.makeText(this, message, Toast.LENGTH_SHORT).show()

fun Context.dpToPx(dp: Int): Int =
    (dp * resources.displayMetrics.density).toInt()
```

## 4. Scope Functions

| Function | Object Reference | Return Value | Use Case |
|----------|-----------------|--------------|----------|
| `let` | `it` | Lambda result | Null checks, transformations |
| `run` | `this` | Lambda result | Object config + compute |
| `with` | `this` | Lambda result | Grouping calls on object |
| `apply` | `this` | Object itself | Object configuration |
| `also` | `it` | Object itself | Side effects |

### Examples
```kotlin
// apply: Configure object
val user = User().apply {
    name = "John"
    age = 30
}

// let: Transform or null-safe
val length = name?.let { it.length } ?: 0

// also: Side effects (logging, validation)
user.also { println("Created user: $it") }

// run: Compute result with object context
val fullName = person.run { "$firstName $lastName" }
```

## 5. Coroutines

### Use Appropriate Dispatchers
```kotlin
// UI operations
withContext(Dispatchers.Main) {
    updateUI(data)
}

// Network/Database
withContext(Dispatchers.IO) {
    fetchFromNetwork()
}

// CPU-intensive
withContext(Dispatchers.Default) {
    processLargeData()
}
```

### Structured Concurrency
```kotlin
// ✅ Good - scoped to ViewModel lifecycle
viewModelScope.launch {
    val result = repository.fetchData()
    _state.value = result
}

// ❌ Avoid - leaks coroutines
GlobalScope.launch { ... }
```

### Exception Handling
```kotlin
viewModelScope.launch {
    try {
        val data = withContext(Dispatchers.IO) {
            repository.fetchData()
        }
        _state.value = UiState.Success(data)
    } catch (e: Exception) {
        _state.value = UiState.Error(e.message ?: "Unknown error")
    }
}
```

## 6. Collections

### Prefer Immutable Collections
```kotlin
// ✅ Good - immutable by default
val list = listOf(1, 2, 3)
val map = mapOf("key" to "value")

// Only when needed
val mutableList = mutableListOf<Int>()
```

### Functional Operations
```kotlin
users
    .filter { it.isActive }
    .sortedBy { it.name }
    .map { it.email }
    .distinct()
    .take(10)
```

### Use Sequences for Large Collections
```kotlin
// ✅ Lazy evaluation - efficient for large data
largeList.asSequence()
    .filter { it > 0 }
    .map { it * 2 }
    .take(100)
    .toList()
```

## 7. Kotlin Idioms

### Smart Casts
```kotlin
fun process(input: Any) {
    if (input is String) {
        // input is automatically cast to String
        println(input.length)
    }
}
```

### Default Arguments
```kotlin
// ✅ Good - single function with defaults
fun connect(
    url: String,
    timeout: Int = 30000,
    retries: Int = 3
)

// Usage
connect("api.example.com")
connect("api.example.com", timeout = 5000)
```

### Named Arguments
```kotlin
// Clear and self-documenting
createUser(
    name = "John",
    email = "john@example.com",
    isAdmin = false
)
```

## 8. Common Patterns

### Result Pattern
```kotlin
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Exception) : Result<Nothing>()
}

// Usage in repository
suspend fun getUser(id: Int): Result<User> = try {
    Result.Success(api.fetchUser(id))
} catch (e: Exception) {
    Result.Error(e)
}
```

### Builder Pattern with DSL
```kotlin
class DialogBuilder {
    var title: String = ""
    var message: String = ""
    private var onConfirm: () -> Unit = {}

    fun onConfirm(action: () -> Unit) {
        onConfirm = action
    }

    fun build(): Dialog = Dialog(title, message, onConfirm)
}

fun dialog(init: DialogBuilder.() -> Unit): Dialog =
    DialogBuilder().apply(init).build()

// Usage
val dialog = dialog {
    title = "Confirm"
    message = "Are you sure?"
    onConfirm { deleteItem() }
}
```

## 9. Testing Best Practices

### Use MockK for Mocking
```kotlin
@Test
fun `load user updates state`() = runTest {
    val mockRepo = mockk<UserRepository>()
    coEvery { mockRepo.getUser(1) } returns User(1, "John")

    val viewModel = UserViewModel(mockRepo)
    viewModel.loadUser(1)

    assertEquals("John", viewModel.state.value?.name)
}
```

### Test Coroutines
```kotlin
@Test
fun `async operation completes`() = runTest {
    val result = repository.fetchData()
    advanceUntilIdle()
    assertTrue(result.isSuccess)
}
```

## 10. Performance Tips

1. **Use `inline` for higher-order functions** with lambdas
2. **Prefer `forEach` over `for`** for collections
3. **Use `lazy` for expensive initialization**
4. **Avoid object creation in loops**
5. **Use `StringBuilder` for string concatenation**

```kotlin
// Lazy initialization
val expensiveResource by lazy {
    computeExpensiveResource()
}

// Inline for performance
inline fun <T> measureTime(block: () -> T): Pair<T, Long> {
    val start = System.currentTimeMillis()
    val result = block()
    return result to (System.currentTimeMillis() - start)
}
```

## Resources

- [Kotlin Official Style Guide](https://kotlinlang.org/docs/coding-conventions.html)
- [Kotlin Idioms](https://kotlinlang.org/docs/idioms.html)
- [Coroutines Best Practices](https://developer.android.com/kotlin/coroutines/coroutines-best-practices)
