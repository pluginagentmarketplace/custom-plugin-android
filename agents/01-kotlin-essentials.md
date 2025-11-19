---
description: Master Kotlin language fundamentals, syntax, coroutines, and idioms
capabilities: ["Kotlin syntax", "Coroutines", "Extension functions", "Functional programming", "Type system", "Null safety"]
---

# Kotlin Essentials

Modern Android development requires mastering Kotlin. This agent covers language fundamentals, advanced features, and best practices.

## Core Language

### Variables & Functions
```kotlin
val immutable = "value"
var mutable = "value"
fun greet(name: String) = "Hello, $name"
```

### Classes & Objects
```kotlin
data class User(val id: Int, val name: String)
sealed class Result<T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Exception) : Result<Nothing>()
}
```

### Scope Functions
```kotlin
user.apply { age = 30 }  // Configure
user.let { println(it) }  // Transform
user.also { it.save() }   // Side effect
```

## Coroutines

```kotlin
viewModelScope.launch {
    val user = withContext(Dispatchers.IO) {
        fetchUser()
    }
}

lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.state.collect { state ->
            updateUI(state)
        }
    }
}
```

## Advanced Features

- **Extension Functions**: Extend existing classes
- **Higher-Order Functions**: Functions as parameters
- **Generics**: Type-safe collections and functions
- **Delegation**: Reduce boilerplate code
- **DSL Building**: Domain-specific languages

## Best Practices

✅ Use immutable (val) by default
✅ Leverage type inference
✅ Master coroutines early
✅ Prefer data classes
✅ Use scope functions appropriately
✅ Avoid null - use optionals

## Essential Resources

- [Kotlin Official Docs](https://kotlinlang.org/docs/)
- [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-overview.html)
- [Kotlin Idioms](https://kotlinlang.org/docs/idioms.html)
