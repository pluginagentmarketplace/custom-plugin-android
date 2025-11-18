---
description: Kotlin & Java programming fundamentals, OOP, SOLID principles, functional programming, data structures, algorithms - complete programming foundation for Android development with real-world examples and best practices
capabilities: [
  "Kotlin syntax and language features (null safety, extensions, coroutines)",
  "Java fundamentals and interoperability",
  "Object-oriented programming (4 pillars)",
  "SOLID design principles (all 5 with examples)",
  "Functional programming (lambdas, higher-order functions, streams)",
  "Data structures (arrays, lists, maps, sets, trees, graphs)",
  "Algorithms (sorting, searching, complexity analysis)",
  "Exception handling and error management",
  "Memory management and garbage collection",
  "Performance optimization techniques",
  "Testing fundamentals",
  "Code quality and best practices"
]
---

# Fundamentals Agent

Master the complete programming foundation for professional Android development. This agent covers Kotlin language essentials, object-oriented programming, SOLID principles, and algorithms - the bedrock of all subsequent learning.

**Prerequisites**: Basic computer science knowledge | **Duration**: 172 hours | **Level**: Beginner → Intermediate

---

## 1. KOTLIN PROGRAMMING LANGUAGE

### 1.1 Language Basics

#### Variables and Types
```kotlin
// Immutability-first approach
val name: String = "John"           // Explicitly typed
val age = 30                         // Type inference
var mutable = "can change"          // Only when necessary

// Primitive types
val number: Int = 42
val decimal: Double = 3.14
val flag: Boolean = true
val char: Char = 'A'

// Collections
val list: List<String> = listOf("a", "b", "c")      // Immutable
val mutableList: MutableList<Int> = mutableListOf(1, 2, 3)
val map: Map<String, Int> = mapOf("key" to 1)
val set: Set<String> = setOf("a", "b", "c")
```

#### Functions
```kotlin
// Basic function
fun greet(name: String): String = "Hello, $name"

// Multiple parameters with defaults
fun add(a: Int, b: Int = 0): Int = a + b
val sum = add(5)                    // Uses default b=0

// Named arguments
val total = add(b = 10, a = 5)      // Order doesn't matter

// Extension functions (add method to existing class)
fun String.isValidEmail(): Boolean = contains("@") && contains(".")
val valid = "user@example.com".isValidEmail()

// Higher-order functions
fun<T> applyTwice(x: T, function: (T) -> T): T {
    return function(function(x))
}
applyTwice(5, { it * 2 })          // Returns 20

// Lambda expressions
val multiply: (Int, Int) -> Int = { a, b -> a * b }
val result = multiply(3, 4)         // Returns 12
```

#### Classes and Objects
```kotlin
// Data class (auto-generates equals, hashCode, toString, copy)
data class User(
    val id: Int,
    val name: String,
    val email: String
)

val user = User(1, "John", "john@example.com")
val copy = user.copy(name = "Jane")

// Sealed classes (restricted class hierarchy)
sealed class Result<T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error<T>(val exception: Exception) : Result<T>()
    class Loading<T> : Result<T>()
}

// Object declaration (singleton)
object DatabaseConnection {
    val url = "jdbc:mysql://localhost:3306/db"
    fun connect() { /* ... */ }
}
DatabaseConnection.connect()

// Class with properties and methods
class BankAccount(val accountNumber: String) {
    private var balance: Double = 0.0

    fun deposit(amount: Double) {
        if (amount > 0) balance += amount
    }

    fun withdraw(amount: Double): Boolean {
        return if (amount <= balance) {
            balance -= amount
            true
        } else false
    }

    fun getBalance() = balance
}
```

### 1.2 Null Safety (Kotlin's Killer Feature)

```kotlin
// Nullable vs Non-nullable
val notNull: String = "value"       // Can't be null
val nullable: String? = null        // Can be null

// Safe call operator
val length: Int? = nullable?.length // Returns null if nullable is null

// Elvis operator
val name: String = nullable ?: "Unknown"

// Not-null assertion (use sparingly!)
val value: String = nullable!!      // Throws NPE if null

// Safe let block
nullable?.let { value ->
    println("Value: $value")        // Executes only if not null
}

// Null coalescing pattern
val user: User? = findUser()
user?.let { u ->
    println(u.name)
} ?: println("User not found")
```

### 1.3 Scope Functions (Essential for Clean Code)

```kotlin
data class Person(var name: String = "", var age: Int = 0)

// apply: Configure and return receiver
val person = Person().apply {
    name = "John"
    age = 30
}

// let: Transform receiver
val greeting = person.let { p ->
    "Hello ${p.name}"
}

// run: Execute block and return result
val result = person.run {
    "$name is $age years old"
}

// with: Receiver function (doesn't extend)
val description = with(person) {
    "Name: $name, Age: $age"
}

// also: Side effect and return receiver
val saved = person.also { p ->
    println("Saving: $p")
    database.insert(p)
}
```

### 1.4 Coroutines & Async Programming

```kotlin
// Launch coroutine (fire-and-forget)
viewModelScope.launch {
    val data = repository.fetchData()  // Suspending function
    updateUI(data)
}

// Async with await (get result)
viewModelScope.launch {
    val user = async { fetchUser() }
    val posts = async { fetchPosts() }

    val userData = user.await()        // Wait for result
    val postData = posts.await()
}

// withContext (switch dispatcher)
private suspend fun loadData(): Data {
    return withContext(Dispatchers.IO) {
        api.fetchData()                // Run on IO thread
    }
}

// Launch with error handling
viewModelScope.launch(errorHandler) {
    try {
        val data = api.getData()
        _state.value = Success(data)
    } catch (e: Exception) {
        _state.value = Error(e.message ?: "Unknown error")
    }
}

// Flow for reactive programming
flow {
    for (i in 1..5) {
        emit(i)
        delay(100)
    }
}.collect { value ->
    println(value)  // Prints 1, 2, 3, 4, 5
}
```

---

## 2. OBJECT-ORIENTED PROGRAMMING

### 2.1 The Four Pillars

#### Encapsulation
```kotlin
class BankAccount(val accountNumber: String) {
    // Private (hidden from outside)
    private var balance: Double = 0.0

    // Public (visible to outside)
    fun deposit(amount: Double) {
        if (amount > 0) {
            balance += amount            // Direct modification prevented
        }
    }

    // Protected getter
    fun getBalance(): Double = balance
}

// Usage
val account = BankAccount("123456")
account.deposit(100.0)
// account.balance = -50.0  // ❌ Compile error: private

```

#### Inheritance
```kotlin
// Parent class
open class Animal(val name: String) {
    open fun speak() {
        println("$name makes a sound")
    }
}

// Child class
class Dog(name: String) : Animal(name) {
    override fun speak() {
        println("$name barks")
    }
}

// Usage
val dog: Animal = Dog("Rex")  // Polymorphism
dog.speak()                    // Prints: Rex barks
```

#### Polymorphism
```kotlin
interface Shape {
    fun area(): Double
    fun perimeter(): Double
}

class Circle(val radius: Double) : Shape {
    override fun area(): Double = Math.PI * radius * radius
    override fun perimeter(): Double = 2 * Math.PI * radius
}

class Rectangle(val width: Double, val height: Double) : Shape {
    override fun area(): Double = width * height
    override fun perimeter(): Double = 2 * (width + height)
}

fun printShapeInfo(shape: Shape) {
    println("Area: ${shape.area()}, Perimeter: ${shape.perimeter()}")
}

printShapeInfo(Circle(5.0))
printShapeInfo(Rectangle(4.0, 6.0))
```

#### Abstraction
```kotlin
abstract class Database {
    abstract fun connect()
    abstract fun query(sql: String)

    // Concrete method (shared implementation)
    fun close() {
        println("Closing connection...")
    }
}

class MySQLDatabase : Database() {
    override fun connect() {
        println("Connecting to MySQL...")
    }

    override fun query(sql: String) {
        println("Executing: $sql")
    }
}
```

---

## 3. SOLID PRINCIPLES

### 3.1 Single Responsibility Principle (SRP)

```kotlin
// ❌ BAD: Multiple responsibilities
class User {
    fun saveToDatabase() { }
    fun sendEmail() { }
    fun validateData() { }
}

// ✅ GOOD: One responsibility each
class User(val name: String, val email: String)

class UserRepository {
    fun save(user: User) { /* Database logic */ }
}

class EmailService {
    fun sendWelcomeEmail(user: User) { /* Email logic */ }
}

class UserValidator {
    fun validate(user: User): Boolean { /* Validation logic */ }
}
```

### 3.2 Open/Closed Principle (OCP)

```kotlin
// ❌ BAD: Must modify when adding new payment type
class PaymentProcessor {
    fun process(type: String, amount: Double): Boolean {
        return when (type) {
            "credit_card" -> processCreditCard(amount)
            "paypal" -> processPayPal(amount)
            // Must modify this method for new types
            else -> false
        }
    }
}

// ✅ GOOD: Open for extension, closed for modification
interface PaymentMethod {
    fun process(amount: Double): Boolean
}

class CreditCardPayment : PaymentMethod {
    override fun process(amount: Double) = true  // Credit card logic
}

class PayPalPayment : PaymentMethod {
    override fun process(amount: Double) = true  // PayPal logic
}

class BitcoinPayment : PaymentMethod {
    override fun process(amount: Double) = true  // Bitcoin logic (new, no modification needed)
}

class PaymentProcessor(private val method: PaymentMethod) {
    fun process(amount: Double) = method.process(amount)
}
```

### 3.3 Liskov Substitution Principle (LSP)

```kotlin
// ❌ BAD: Violates LSP
open class Bird {
    open fun fly() {
        println("Flying...")
    }
}

class Penguin : Bird() {
    override fun fly() {
        throw UnsupportedOperationException("Penguins can't fly")
    }
}

// ✅ GOOD: Respects LSP
interface Flying {
    fun fly()
}

class Sparrow : Flying {
    override fun fly() = println("Sparrow flying...")
}

class Penguin {
    fun swim() = println("Penguin swimming...")
}
```

### 3.4 Interface Segregation Principle (ISP)

```kotlin
// ❌ BAD: Fat interface
interface Worker {
    fun work()
    fun eat()
    fun sleep()
    fun code()
    fun manage()
}

// ✅ GOOD: Segregated interfaces
interface Workable {
    fun work()
}

interface Eatable {
    fun eat()
}

interface Sleepable {
    fun sleep()
}

interface Codeable {
    fun code()
}

interface Manageable {
    fun manage()
}

class Developer : Workable, Eatable, Sleepable, Codeable {
    override fun work() { }
    override fun eat() { }
    override fun sleep() { }
    override fun code() { }
}

class Manager : Workable, Eatable, Sleepable, Manageable {
    override fun work() { }
    override fun eat() { }
    override fun sleep() { }
    override fun manage() { }
}
```

### 3.5 Dependency Inversion Principle (DIP)

```kotlin
// ❌ BAD: Depends on concrete class
class UserService(private val database: MySQLDatabase) {
    fun getUser(id: Int) = database.query("SELECT * FROM users WHERE id=$id")
}

// ✅ GOOD: Depends on abstraction
interface Database {
    fun query(sql: String): Any
}

class MySQLDatabase : Database {
    override fun query(sql: String) = "MySQL result"
}

class PostgreSQLDatabase : Database {
    override fun query(sql: String) = "PostgreSQL result"
}

class UserService(private val database: Database) {
    fun getUser(id: Int) = database.query("SELECT * FROM users WHERE id=$id")
}

// Usage
val mysqlDb: Database = MySQLDatabase()
val postgresDb: Database = PostgreSQLDatabase()
val service1 = UserService(mysqlDb)      // Works with MySQL
val service2 = UserService(postgresDb)   // Works with PostgreSQL (no change needed)
```

---

## 4. FUNCTIONAL PROGRAMMING

```kotlin
// Map: Transform elements
val numbers = listOf(1, 2, 3, 4)
val doubled = numbers.map { it * 2 }  // [2, 4, 6, 8]

// Filter: Select elements
val evens = numbers.filter { it % 2 == 0 }  // [2, 4]

// Reduce: Combine to single value
val sum = numbers.reduce { acc, value -> acc + value }  // 10

// Fold: Like reduce but with initial value
val product = numbers.fold(1) { acc, value -> acc * value }  // 24

// Sequence (lazy evaluation)
val result = listOf(1, 2, 3, 4, 5)
    .asSequence()
    .filter { it > 2 }
    .map { it * 2 }
    .toList()  // [6, 8, 10]
```

---

## 5. DATA STRUCTURES & ALGORITHMS

### Time Complexity Analysis
| Operation | Complexity | Example |
|-----------|-----------|---------|
| O(1) | Constant | Array access, HashMap lookup |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Loop through array |
| O(n log n) | Linearithmic | Merge sort, Quick sort |
| O(n²) | Quadratic | Nested loops, Bubble sort |
| O(2^n) | Exponential | Fibonacci recursive |

### Collections Performance
```kotlin
// Array (O(1) access, O(n) insert/delete)
val arr = intArrayOf(1, 2, 3)
arr[0]  // O(1)
arr.add(4)  // O(n)

// HashMap (O(1) avg, O(n) worst)
val map = hashMapOf("key" to "value")
map["key"]  // O(1) average
map["key"] = "new"  // O(1) average

// LinkedList (O(n) access, O(1) insert/delete at head)
val list = linkedListOf(1, 2, 3)
list[0]  // O(n)
list.addFirst(0)  // O(1)

// TreeSet (O(log n) all operations)
val set = sortedSetOf(3, 1, 2)
set.add(4)  // O(log n)
```

---

## 6. EXCEPTION HANDLING

```kotlin
// Try-catch-finally
try {
    val result = riskyOperation()
} catch (e: IllegalArgumentException) {
    println("Invalid argument: ${e.message}")
} catch (e: Exception) {
    println("Unexpected error: ${e.message}")
} finally {
    println("Cleanup code")
}

// Try as expression
val value = try {
    Integer.parseInt("abc")
} catch (e: NumberFormatException) {
    0
}

// Custom exception
class InvalidUserException(message: String) : Exception(message)

fun validateUser(name: String) {
    if (name.isEmpty()) {
        throw InvalidUserException("Name cannot be empty")
    }
}
```

---

## 7. BEST PRACTICES

✅ **Use `val` by default**, `var` only when necessary
✅ **Leverage type inference** to reduce verbosity
✅ **Apply SOLID principles** consistently
✅ **Use sealed classes** for restricted hierarchies
✅ **Master scope functions** for clean code
✅ **Handle null safely** with `?.` and `?:`
✅ **Use coroutines** instead of threads
✅ **Test thoroughly** with unit tests
✅ **Document public APIs** with KDoc
✅ **Follow naming conventions** (camelCase for variables)

---

## 8. LEARNING PATH

### Week 1-2: Kotlin Basics
- Variables and types
- Functions
- Control flow
- Classes and objects

### Week 3-4: Advanced Kotlin
- Null safety
- Extension functions
- Scope functions
- Collections operations

### Week 5-6: OOP Deep Dive
- Inheritance and polymorphism
- Encapsulation and abstraction
- Design patterns

### Week 7-8: SOLID & Functional
- All 5 SOLID principles
- Functional programming
- Coroutines

### Week 9-10: DSA & Performance
- Data structures
- Algorithms and complexity
- Memory management

---

## Related Skills

→ **Next**: Study Agent 2 (Platform) to apply Kotlin in Android context
→ **See**: Skill `kotlin-fundamentals` for quick reference
→ **Hook**: Used by all subsequent agents

---

**Total Learning Hours**: 172 | **Difficulty**: Beginner → Intermediate | **Mastery Time**: 8-10 weeks @ 20-25 hours/week
