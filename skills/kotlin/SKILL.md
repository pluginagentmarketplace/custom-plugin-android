---
name: kotlin-programming
description: Master Kotlin language features, syntax, coroutines, and idioms for Android development. Use when working with Kotlin code, async operations, or modern language features.
---

# Kotlin Programming Skill

## Quick Start

### Basic Syntax
```kotlin
// Variables
val immutable = "value"
var mutable = "value"

// Functions
fun greet(name: String): String = "Hello, $name"

// Classes
data class User(val id: Int, val name: String)

// When expression
val message = when (value) {
    1 -> "One"
    2 -> "Two"
    else -> "Other"
}
```

### Coroutines

```kotlin
// Launch coroutine
viewModelScope.launch {
    val user = getUserAsync() // Suspend function
    updateUI(user)
}

// Async/await
val users = viewModelScope.async {
    userRepository.getAllUsers()
}.await()

// Scope functions
person.apply { age = 30 }
```

## Key Concepts

- **Null Safety**: ? and !! operators prevent NPE
- **Extension Functions**: Add methods to existing classes
- **Higher-Order Functions**: Functions as parameters/return values
- **Coroutines**: Non-blocking async operations
- **Type Inference**: Compiler deduces types
- **Properties**: Getters/setters integrated in syntax

## Common Patterns

1. **Safe Navigation**: `obj?.property`
2. **Elvis Operator**: `value ?: defaultValue`
3. **Lambda**: `{ x -> x * 2 }`
4. **Scope Functions**: `let`, `apply`, `run`, `with`, `also`

## Resources

- [Kotlin Official Docs](https://kotlinlang.org/docs/)
- [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-overview.html)
- [Android Kotlin Style Guide](https://android.googlesource.com/platform/frameworks/base/+/master/STYLE_GUIDE.md)
