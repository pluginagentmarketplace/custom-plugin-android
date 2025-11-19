---
description: Mobil uygulama geliştirmenin temelini oluşturan programlama konseptleri, dil bilgisi ve nesne yönelimli programlama prensipleri
capabilities:
  - Kotlin ve Java dil özellikleri ve sözdizimi
  - Nesne yönelimli programlama (OOP) prensipleri
  - Veri yapıları ve algoritmalar
  - Temel programlama kavramları
  - Fonksiyonel programlama paradigmaları
  - Exception handling ve error management
  - Memory management ve garbage collection
  - SOLID prensipleri
---

# Mobile Development Fundamentals

Mobil uygulama geliştirmenin sağlam bir temelini oluşturmak, başarılı bir Android geliştirici olmanın ilk adımıdır. Bu aşama programlama dilini öğrenme, temel konseptları anlama ve yazılım tasarım prensiplerini içerir.

## 1. Programlama Dili Seçimi: Kotlin vs Java

### Kotlin
**Modern Android Geliştirmesinin Dili**

Kotlin, Google tarafından 2017'de Android'in resmi dili olarak ilan edilmiş ve 2019'da Java'yı ön çıkan dil olarak belirlemiştir. Kotlin, JVM (Java Virtual Machine) üzerinde çalışan modern, statik olarak type-edilen bir dildir.

**Kotlin'in Avantajları:**
- **Null Safety:** Null Pointer Exception'lar için yerleşik koruma
- **Extension Functions:** Mevcut sınıflara yeni fonksiyonlar ekleme
- **Coroutines:** Asenkron programlama için kolay sözdizimi
- **Higher-Order Functions:** Fonksiyonları parametre olarak geçebilme
- **Data Classes:** Boilerplate kodu otomatik oluşturma
- **Smart Casts:** Tip kontrolünden sonra otomatik casting

**Kotlin Temel Sözdizimi:**
```kotlin
// Değişken tanımlama
val immutable: String = "value"  // Val = immutable
var mutable: String = "value"    // Var = mutable

// Null-safety operator
val length: Int? = null
val safeLength = length?.length ?: 0

// Data class örneği
data class User(
    val id: Int,
    val name: String,
    val email: String
)

// Extension function
fun String.isEmail(): Boolean {
    return this.contains("@") && this.contains(".")
}

// Coroutine örneği
GlobalScope.launch {
    val data = fetchData()
    updateUI(data)
}

// Higher-order function
fun applyOperation(a: Int, b: Int, operation: (Int, Int) -> Int): Int {
    return operation(a, b)
}

val result = applyOperation(5, 3) { x, y -> x + y }
```

### Java
**Kurulu ve Güvenilir Platform**

Java, 1995'ten beri yazılım endüstrisinin omurgası olmuştur. Android açısından, Java şu anda bakım modu denebilecek durumda olsa da, var olan pek çok kurumsal projesi ve geniş bilgi tabanı vardır.

**Java Temel Sözdizimi:**
```java
// Sınıf tanımlama
public class User {
    private int id;
    private String name;
    private String email;

    public User(int id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    public String getName() {
        return name;
    }
}

// Generics kullanımı
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");

// Lambda expressions (Java 8+)
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
List<Integer> evens = numbers.stream()
    .filter(n -> n % 2 == 0)
    .collect(Collectors.toList());

// Exception handling
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    Log.e("TAG", "Division error", e);
} finally {
    Log.d("TAG", "Cleanup resources");
}
```

## 2. Nesne Yönelimli Programlama (OOP) Prensipleri

OOP, karmaşık problemleri daha küçük, yönetilebilir nesnelere bölen bir programlama paradigmasıdır. Android geliştirmesinde temel konsepti anlamak kaçınılmazdır.

### 2.1 Sınıf (Class) ve Nesne (Object)

**Sınıf:** Nesnelerin şablonu veya planıdır. Özellikleri (properties) ve davranışları (methods) tanımlar.

**Nesne:** Sınıfın somut örneğidir.

```kotlin
// Sınıf tanımı
class Car(
    val brand: String,
    val model: String,
    var speed: Int = 0
) {
    fun accelerate(amount: Int) {
        speed += amount
        Log.d("Car", "Speed: $speed km/h")
    }

    fun brake(amount: Int) {
        speed = maxOf(0, speed - amount)
    }
}

// Nesne oluşturma (instantiation)
val myCar = Car("Toyota", "Corolla")
myCar.accelerate(50)
myCar.brake(20)
```

### 2.2 Encapsulation (Kapsülleme)

Bir sınıfın iç detaylarını gizlemek ve sadece gerekli arabirimi göstermek prensibidir. Bu, veri bütünlüğünü korur ve dış bağımlılıkları azaltır.

```kotlin
// Kötü örnek: Direkt erişim
class BankAccount {
    var balance: Int = 0  // Herkese açık
}

val account = BankAccount()
account.balance = -1000  // Geçersiz işlem


// İyi örnek: Encapsulation
class BankAccount {
    private var balance: Int = 0

    fun deposit(amount: Int): Boolean {
        return if (amount > 0) {
            balance += amount
            true
        } else false
    }

    fun withdraw(amount: Int): Boolean {
        return if (amount > 0 && amount <= balance) {
            balance -= amount
            true
        } else false
    }

    fun getBalance(): Int = balance
}

val account = BankAccount()
account.deposit(1000)
account.withdraw(500)  // Kontrollü işlem
```

**Access Modifiers:**
- `public`: Heryerden erişilebilir (varsayılan)
- `private`: Sadece sınıf içerisinden erişilebilir
- `protected`: Sınıf ve alt sınıflarından erişilebilir
- `internal` (Kotlin): Aynı modül içerisinden erişilebilir

### 2.3 Inheritance (Kalıtım)

Bir sınıfın başka bir sınıfın özelliklerini ve davranışlarını devralması.

```kotlin
// Base class (Parent class)
open class Animal(
    val name: String,
    val age: Int
) {
    open fun makeSound() {
        println("$name is making a sound")
    }

    open fun eat(food: String) {
        println("$name is eating $food")
    }
}

// Derived class (Child class)
class Dog(
    name: String,
    age: Int,
    val breed: String
) : Animal(name, age) {
    override fun makeSound() {
        println("$name is barking: Woof!")
    }

    override fun eat(food: String) {
        super.eat(food)  // Parent sınıfın metodunu çağır
        println("$name enjoys eating dog food")
    }

    fun fetch() {
        println("$name is fetching the ball")
    }
}

val dog = Dog("Buddy", 3, "Labrador")
dog.makeSound()  // "Buddy is barking: Woof!"
dog.eat("meat")
dog.fetch()
```

### 2.4 Polymorphism (Çok Biçimlilik)

Aynı interfaceyi farklı şekillerde implement etme yeteneği. Kodun esneklik ve genişletebilirliğini sağlar.

```kotlin
// Interface tanımlama
interface Shape {
    fun getArea(): Double
    fun getPerimeter(): Double
}

// Farklı implementasyonlar
class Circle(val radius: Double) : Shape {
    override fun getArea(): Double = Math.PI * radius * radius
    override fun getPerimeter(): Double = 2 * Math.PI * radius
}

class Rectangle(val width: Double, val height: Double) : Shape {
    override fun getArea(): Double = width * height
    override fun getPerimeter(): Double = 2 * (width + height)
}

// Polymorphic işlem
fun printShapeInfo(shape: Shape) {
    println("Area: ${shape.getArea()}")
    println("Perimeter: ${shape.getPerimeter()}")
}

val circle = Circle(5.0)
val rectangle = Rectangle(4.0, 6.0)

printShapeInfo(circle)      // Circle'ın alanını hesaplar
printShapeInfo(rectangle)   // Rectangle'ın alanını hesaplar
```

### 2.5 Abstraction (Soyutlama)

Gereksiz detayları gizleyip, sadece essential özellikleri göstermek.

```kotlin
// Abstract class
abstract class DatabaseConnection {
    abstract fun connect()
    abstract fun disconnect()
    abstract fun executeQuery(query: String): List<Any>

    // Concrete method
    fun transaction(operation: () -> Unit) {
        connect()
        try {
            operation()
        } finally {
            disconnect()
        }
    }
}

// Concrete implementation
class SQLiteConnection : DatabaseConnection() {
    override fun connect() {
        println("Connecting to SQLite database...")
    }

    override fun disconnect() {
        println("Disconnecting from SQLite database...")
    }

    override fun executeQuery(query: String): List<Any> {
        println("Executing query: $query")
        return listOf("result1", "result2")
    }
}

val db = SQLiteConnection()
db.transaction {
    db.executeQuery("SELECT * FROM users")
}
```

## 3. SOLID Prensipleri

Maintainable ve scalable kod yazmanın temelini oluşturan 5 prensip.

### S - Single Responsibility Principle (SRP)
Bir sınıf sadece bir nedeni değiştirilmelidir.

```kotlin
// Kötü: Bir sınıf birçok sorumluluk taşıyor
class UserManager {
    fun createUser(name: String): User { /* ... */ }
    fun sendEmail(user: User, message: String) { /* ... */ }
    fun logActivity(action: String) { /* ... */ }
}

// İyi: Her sınıf bir sorumluluğu taşıyor
class UserManager {
    fun createUser(name: String): User { /* ... */ }
}

class EmailService {
    fun sendEmail(user: User, message: String) { /* ... */ }
}

class Logger {
    fun logActivity(action: String) { /* ... */ }
}
```

### O - Open/Closed Principle (OCP)
Sınıflar genişlemeye açık, değişikliğe kapalı olmalıdır.

```kotlin
// Kötü: Yeni PaymentMethod eklemek için UserPayment değiştirilmeli
class UserPayment {
    fun processPayment(user: User, type: String) {
        if (type == "creditCard") {
            // credit card logic
        } else if (type == "paypal") {
            // paypal logic
        }
    }
}

// İyi: Interface kullanarak extension yapılabilir
interface PaymentMethod {
    fun process(amount: Double): Boolean
}

class CreditCardPayment : PaymentMethod {
    override fun process(amount: Double): Boolean { /* ... */ }
}

class PayPalPayment : PaymentMethod {
    override fun process(amount: Double): Boolean { /* ... */ }
}

class UserPayment {
    fun processPayment(user: User, method: PaymentMethod) {
        method.process(user.balance)
    }
}
```

### L - Liskov Substitution Principle (LSP)
Alt sınıflar, üst sınıflarının yerine geçebilmelidir.

```kotlin
// Kötü: Square, Rectangle yerine kullanılamaz
open class Rectangle(var width: Int, var height: Int) {
    open fun getArea(): Int = width * height
}

class Square(size: Int) : Rectangle(size, size) {
    override var width: Int
        get() = super.width
        set(value) { super.width = value; super.height = value }
}

// Square'de width ve height bağımsız değiştiğinde sorun


// İyi: Doğru hiyerarşi
interface Shape {
    fun getArea(): Int
}

class Rectangle(val width: Int, val height: Int) : Shape {
    override fun getArea(): Int = width * height
}

class Square(val size: Int) : Shape {
    override fun getArea(): Int = size * size
}
```

### I - Interface Segregation Principle (ISP)
İstemciler kullanmayacakları metodlara bağlı olmamalidir.

```kotlin
// Kötü: Pek çok gereksiz metod
interface Worker {
    fun work()
    fun eat()
    fun sleep()
    fun code()
}

class Robot : Worker {
    override fun work() { /* ... */ }
    override fun eat() { /* x */ }  // Robot yemek yemiyor
    override fun sleep() { /* x */ }  // Robot uyumuyor
    override fun code() { /* ... */ }
}

// İyi: Segregated interfaces
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

class Robot : Workable, Codeable {
    override fun work() { /* ... */ }
    override fun code() { /* ... */ }
}

class Developer : Workable, Eatable, Sleepable, Codeable {
    override fun work() { /* ... */ }
    override fun eat() { /* ... */ }
    override fun sleep() { /* ... */ }
    override fun code() { /* ... */ }
}
```

### D - Dependency Inversion Principle (DIP)
Yüksek-seviye modüller, düşük-seviye modüllere bağlı olmamalidir. İkisi de abstractions'a bağlı olmalıdır.

```kotlin
// Kötü: Direkt bağımlılık
class UserRepository {
    private val database = SQLiteDatabase()

    fun getUser(id: Int) {
        database.query("SELECT * FROM users WHERE id = $id")
    }
}

// İyi: Dependency Injection
interface Database {
    fun query(sql: String)
}

class SQLiteDatabase : Database {
    override fun query(sql: String) { /* ... */ }
}

class PostgresDatabase : Database {
    override fun query(sql: String) { /* ... */ }
}

class UserRepository(private val database: Database) {
    fun getUser(id: Int) {
        database.query("SELECT * FROM users WHERE id = $id")
    }
}

// Usage
val database: Database = SQLiteDatabase()
val userRepository = UserRepository(database)
```

## 4. Veri Yapıları (Data Structures)

### 4.1 Arrays (Diziler)
Aynı tipte elemanları düzenli depolayan sabit boyutlu yapı.

```kotlin
// Array deklarasyonu
val numbers: IntArray = intArrayOf(1, 2, 3, 4, 5)
val strings = arrayOf("Alice", "Bob", "Charlie")

// Erişim
println(numbers[0])  // 1
println(numbers.size)  // 5

// İterasyon
for (num in numbers) {
    println(num)
}
```

### 4.2 Lists (Listeler)
Dinamik boyutlu, sıralı koleksiyon.

```kotlin
// Mutable list
val mutableList = mutableListOf<String>()
mutableList.add("Apple")
mutableList.add("Banana")
mutableList.remove("Apple")

// Immutable list
val immutableList = listOf("Apple", "Banana", "Orange")

// Operations
println(immutableList.first())  // "Apple"
println(immutableList.last())   // "Orange"
val filtered = immutableList.filter { it.length > 5 }
val mapped = immutableList.map { it.uppercase() }
```

### 4.3 Maps (Haritalar)
Key-value çiftlerini depolayan yapı.

```kotlin
// Mutable map
val mutableMap = mutableMapOf<String, Int>()
mutableMap["Alice"] = 90
mutableMap["Bob"] = 85

// Immutable map
val immutableMap = mapOf("Alice" to 90, "Bob" to 85)

// Operations
println(immutableMap["Alice"])  // 90
println(immutableMap.keys)      // [Alice, Bob]
println(immutableMap.values)    // [90, 85]

// Filter ve map
val adults = immutableMap.filter { it.value >= 18 }
```

### 4.4 Sets (Kümeler)
Benzersiz elemanları depolayan koleksiyon.

```kotlin
val mutableSet = mutableSetOf<Int>()
mutableSet.add(1)
mutableSet.add(2)
mutableSet.add(1)  // Tekrar eklenmez

val immutableSet = setOf(1, 2, 3, 2, 1)
println(immutableSet.size)  // 3

// Set operations
val setA = setOf(1, 2, 3)
val setB = setOf(3, 4, 5)
println(setA + setB)      // [1, 2, 3, 4, 5]
println(setA intersect setB)  // [3]
```

## 5. Fonksiyonel Programlama (Functional Programming)

Fonksiyonları birinci sınıf nesneler olarak kullanan programlama stili.

### Higher-Order Functions

```kotlin
// Fonksiyon parametresi alan fonksiyon
fun applyOperation(a: Int, b: Int, operation: (Int, Int) -> Int): Int {
    return operation(a, b)
}

val result = applyOperation(10, 5) { x, y -> x + y }
println(result)  // 15


// Fonksiyon dönen fonksiyon
fun makeMultiplier(factor: Int): (Int) -> Int {
    return { value -> value * factor }
}

val double = makeMultiplier(2)
val triple = makeMultiplier(3)
println(double(5))   // 10
println(triple(5))   // 15
```

### Lambda Expressions ve Collections

```kotlin
data class Product(val name: String, val price: Double, val quantity: Int)

val products = listOf(
    Product("Laptop", 999.0, 5),
    Product("Phone", 599.0, 10),
    Product("Tablet", 399.0, 3)
)

// Filter
val expensive = products.filter { it.price > 500 }

// Map
val names = products.map { it.name }

// FlatMap
val inventory = products.flatMap { product ->
    List(product.quantity) { product.name }
}

// Reduce
val totalValue = products.map { it.price * it.quantity }
    .reduce { acc, price -> acc + price }

// Fold
val totalWithInitial = products.fold(0.0) { acc, product ->
    acc + (product.price * product.quantity)
}

// Any / All
val hasExpensive = products.any { it.price > 800 }
val allInStock = products.all { it.quantity > 0 }
```

## 6. Exception Handling ve Error Management

Beklenmeyen durumları kontrol etme mekanizması.

```kotlin
// Try-catch-finally
try {
    val result = 10 / 0
} catch (e: ArithmeticException) {
    Log.e("Error", "Division by zero", e)
} finally {
    Log.d("Info", "Cleanup resources")
}

// Multiple catches
try {
    val number = "abc".toInt()
} catch (e: NumberFormatException) {
    Log.e("Error", "Invalid number format")
} catch (e: Exception) {
    Log.e("Error", "Unknown error: ${e.message}")
}

// Try as expression (Kotlin)
val result = try {
    "123".toInt()
} catch (e: NumberFormatException) {
    0
}

// Custom exceptions
class InvalidUserException(message: String) : Exception(message)

fun validateUser(name: String) {
    if (name.isEmpty()) {
        throw InvalidUserException("User name cannot be empty")
    }
}

// Proper error handling
sealed class Result<T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error<T>(val exception: Exception) : Result<T>()
}

fun fetchUser(id: Int): Result<User> {
    return try {
        val user = getUserFromDatabase(id)
        Result.Success(user)
    } catch (e: Exception) {
        Result.Error(e)
    }
}
```

## 7. Memory Management ve Garbage Collection

Android'de bellek yönetimi performans ve stabilite açısından kritiktir.

### Bellek Yönetimi Best Practices

```kotlin
// 1. Context'i sızdırmayın
// Kötü
class MyClass(val context: Context) {
    companion object {
        var instance: MyClass? = null
    }

    init {
        instance = this  // Context sızıntısı!
    }
}

// İyi
class MyClass(private val context: Context) {
    companion object {
        var instance: MyClass? = null
    }
}

// 2. Inner class'lar dikkatli kullanın
// Kötü
class OuterClass {
    val data = "Large data"

    inner class InnerClass {
        fun process() {
            println(data)  // Outer reference tutar
        }
    }
}

// İyi
class OuterClass {
    val data = "Large data"
}

class InnerClass(private val data: String) {
    fun process() {
        println(data)
    }
}

// 3. Resources'ı manage edin
class ResourceManager {
    private var resource: Resource? = null

    fun init() {
        resource = Resource()
    }

    fun cleanup() {
        resource?.close()
        resource = null
    }
}

// 4. Weak references kullanın
import java.lang.ref.WeakReference

class CacheManager {
    private val cache = WeakReference(Data())

    fun getData(): Data? {
        return cache.get()
    }
}
```

## 8. Temel Programlama Kavramları

### Variables ve Scope

```kotlin
// Local scope
fun example() {
    val localVar = 10  // Function scope
    {
        val blockVar = 20  // Block scope
    }
}

// Global scope
const val APP_VERSION = "1.0.0"
val globalVar = "Global"

// Scope functions
data class User(val name: String, val email: String)

val user = User("Alice", "alice@example.com")

// apply: Bu objeyi konfigüre et
val configuredUser = User("Bob", "bob@example.com").apply {
    println("Configured: $name")
}

// also: Bu obje hakkında additional işlem yap
val savedUser = User("Charlie", "charlie@example.com").also {
    saveToDatabase(it)
    Log.d("User", "User saved: ${it.name}")
}

// let: Null safety ile işlem yap
user.email?.let {
    sendEmail(it)
}

// run: Context nesnesi ve return değeri gerek
val result = user.run {
    name.length + email.length
}
```

### Control Flow

```kotlin
// If expression
val age = 25
val category = if (age < 18) {
    "Minor"
} else if (age < 65) {
    "Adult"
} else {
    "Senior"
}

// When expression
fun getDay(dayNumber: Int): String = when (dayNumber) {
    1 -> "Monday"
    2 -> "Tuesday"
    3 -> "Wednesday"
    4 -> "Thursday"
    5 -> "Friday"
    6, 7 -> "Weekend"  // Multiple values
    else -> "Invalid day"
}

// Loops
val numbers = listOf(1, 2, 3, 4, 5)

// for loop
for (num in numbers) {
    println(num)
}

// forEach
numbers.forEach { num ->
    println(num)
}

// while loop
var count = 0
while (count < 5) {
    println(count)
    count++
}

// do-while loop
do {
    println(count)
} while (count > 0)
```

## Öğrenme Kaynakları

- **Official Documentation:** [Kotlin Official Documentation](https://kotlinlang.org/docs/)
- **Google Android Developers:** [Android Development Guides](https://developer.android.com/docs)
- **roadmap.sh:** [Android Developer Roadmap](https://roadmap.sh/android)
- **Práce Books:** "Kotlin in Action"
- **Online Courses:** Coursera Android Specialization, Udacity Android Nanodegree

## Milestone Checklist

- [ ] Kotlin sözdizimi ve temel özellikler öğrenildi
- [ ] Java fundamentals anlaşıldı
- [ ] OOP'nin 4 pilar (Encapsulation, Inheritance, Polymorphism, Abstraction) öğrenildi
- [ ] SOLID prensipleri uygulanıyor
- [ ] Koleksiyonlar (Lists, Maps, Sets) kullanımı hakim
- [ ] Fonksiyonel programlama konseptleri anlaşıldı
- [ ] Exception handling best practices biliniliyor
- [ ] Memory leak'ler ve leakCanary kullanımı öğrenildi
