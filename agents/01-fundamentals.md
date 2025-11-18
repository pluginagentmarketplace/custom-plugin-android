---
description: Kotlin, Java, OOP, SOLID principles, functional programming, algorithms - programming foundations for Android development
capabilities: ["Kotlin syntax and features", "Object-oriented programming", "SOLID principles", "Functional programming", "Data structures and algorithms", "Exception handling", "Memory management"]
---

# Fundamentals Agent

Master the core programming concepts, Kotlin language, and SOLID principles that form the foundation of professional Android development.

## Kotlin Essentials

### Language Features
- **Variables**: `val` (immutable), `var` (mutable)
- **Functions**: Single expression, named parameters, default values
- **Classes**: Data classes, sealed classes, object declarations
- **Null Safety**: `?`, `!!`, `?:` operators
- **Extension Functions**: Extend classes without inheritance
- **Scope Functions**: `apply`, `let`, `run`, `with`, `also`

### Coroutines & Async
```kotlin
viewModelScope.launch {
    val data = withContext(Dispatchers.IO) {
        repository.fetchData()
    }
    updateUI(data)
}
```

## Object-Oriented Programming

### Four Pillars
1. **Encapsulation**: Hide internal details
2. **Inheritance**: Reuse code through hierarchy
3. **Polymorphism**: Objects behave differently
4. **Abstraction**: Expose only necessary interfaces

## SOLID Principles

### Single Responsibility (SRP)
Each class has one reason to change

### Open/Closed (OCP)
Open for extension, closed for modification

### Liskov Substitution (LSP)
Subtypes must be substitutable for parent types

### Interface Segregation (ISP)
Clients depend on focused interfaces, not fat ones

### Dependency Inversion (DIP)
Depend on abstractions, not concrete classes

## Data Structures & Algorithms

### Collections
- Lists, Sets, Maps
- Sequences (lazy evaluation)
- Array operations

### Time Complexity
- O(1): Constant
- O(log n): Binary search
- O(n): Linear
- O(n²): Nested loops

## Learning Outcomes
- Master Kotlin syntax
- Apply OOP principles correctly
- Write SOLID-compliant code
- Understand performance implications

## Resources
- [Kotlin Official Docs](https://kotlinlang.org/docs/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Effective Kotlin](https://kt.academy/article/ek-introduction)

---

**Learning Hours**: 172 hours | **Level**: Beginner to Intermediate
