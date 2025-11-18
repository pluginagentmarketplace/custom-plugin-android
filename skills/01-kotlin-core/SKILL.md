---
name: kotlin-core
description: Kotlin syntax, coroutines, scope functions, and functional programming. Use when working with Kotlin code.
---

# Kotlin Core Skill

## Syntax Essentials

```kotlin
// Variables
val immutable = "value"
var mutable = "value"

// Functions
fun add(a: Int, b: Int): Int = a + b
fun greet(name: String) = "Hello, $name"

// Classes
data class User(val id: Int, val name: String)
sealed class Result<T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Failure(val error: Exception) : Result<Nothing>()
}
```

## Coroutines

```kotlin
// Launch coroutine
viewModelScope.launch {
    val user = getUserAsync()
    updateUI(user)
}

// Async/await
val result = viewModelScope.async {
    repository.fetchData()
}.await()

// Collect Flow
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.state.collect { state ->
            render(state)
        }
    }
}
```

## Scope Functions

```kotlin
user.apply { age = 30 }              // Configure object
user.let { println(it) }             // Transform
user.run { println(name) }           // Execute block
user.also { it.save() }              // Side effect
with(user) { println(name) }         // Execute with context
```

## Functional Programming

```kotlin
// Higher-order functions
val numbers = listOf(1, 2, 3, 4, 5)
numbers.filter { it > 2 }            // [3, 4, 5]
numbers.map { it * 2 }               // [2, 4, 6, 8, 10]
numbers.reduce { a, b -> a + b }     // 15

// Extension functions
fun <T> List<T>.second() = this[1]
fun String.isEmail() = contains("@")

// Lambda
val multiply: (Int, Int) -> Int = { a, b -> a * b }
```

## Null Safety

```kotlin
// ? - Safe call
user?.name

// ?: - Elvis operator
val name = user?.name ?: "Unknown"

// !! - Not-null assertion (avoid)
user!!.name

// let for null-safe blocks
user?.let { u ->
    println(u.name)
}
```

## Collections

```kotlin
// Sequences (lazy)
list.asSequence()
    .filter { it > 0 }
    .map { it * 2 }
    .toList()

// Set and Map
val set = setOf(1, 2, 3)
val map = mapOf("a" to 1, "b" to 2)

// Destructuring
val (id, name) = user
```

## Common Patterns

✅ Use `val` by default
✅ Avoid null with optionals
✅ Master coroutines early
✅ Prefer data classes
✅ Use scope functions appropriately
✅ Functional over imperative

## Resources

- [Kotlin Docs](https://kotlinlang.org/docs/)
- [Kotlin Idioms](https://kotlinlang.org/docs/idioms.html)
- [Coroutines Guide](https://kotlinlang.org/docs/coroutines-overview.html)
