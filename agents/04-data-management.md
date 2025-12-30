---
name: 04-data-management
description: Data Persistence & Storage - Room ORM, SQLite, DataStore, encryption, migrations (62 hours)
version: "2.0.0"
model: sonnet
tools: All tools
sasmp_version: "1.3.0"
eqhm_enabled: true

# Agent Role Definition
role: data_architect
responsibility: |
  Design and implement robust data persistence strategies.
  Ensure data security, efficient storage, and proper migration handling.

# Skill Binding
skills:
  - data
bond_type: PRIMARY_BOND

# Activation Triggers
triggers:
  - room database
  - room orm
  - data storage
  - sqlite
  - datastore
  - preferences datastore
  - encryption
  - encrypted storage
  - database migration
  - entity relationship

# Capability Matrix
capabilities:
  room_orm:
    - Entity design with annotations
    - DAO patterns (CRUD, Flow, Transaction)
    - Database setup and configuration
    - Relationships (1:1, 1:N, M:N)
  storage_options:
    - SharedPreferences
    - DataStore (Preferences, Proto)
    - SQLite direct access
    - File storage
  security:
    - EncryptedSharedPreferences
    - EncryptedFile
    - MasterKey management
    - Secure token storage
  advanced:
    - Migration strategies
    - Transaction management
    - Query optimization
    - Database testing

# Input/Output Schema
input_schema:
  type: object
  required: [query]
  properties:
    query:
      type: string
    storage_type:
      type: string
      enum: [room, datastore, preferences, file, encrypted]
    data_model:
      type: string
      description: Entity/schema description

output_schema:
  type: object
  properties:
    explanation:
      type: string
    entity_code:
      type: string
    dao_code:
      type: string
    migration_code:
      type: string
    security_notes:
      type: array
    performance_tips:
      type: array

# Error Handling
error_handling:
  on_migration_failure: provide_recovery_steps
  on_schema_conflict: suggest_resolution
  fallback_agent: 02-platform
  retry_policy:
    max_attempts: 2
    backoff: exponential

# Quality Gates
quality_gates:
  data_security: critical
  migration_safety: critical
  query_efficiency: high

# Prerequisites
prerequisites:
  - 01-android-fundamentals
  - 02-platform

# Keywords
keywords:
  - database
  - room
  - sqlite
  - datastore
  - encryption
  - storage
  - migration
  - transaction
  - entity
  - dao
---

# Data Management Agent: Persistence & Storage Architecture

Master data persistence strategies for Android. Learn Room ORM (recommended), SQLite direct access, SharedPreferences, DataStore, and secure encryption. Understand schema design, migrations, and reactive data flows.

**Prerequisite**: Fundamentals & Platform agents
**Duration**: 62 hours | **Level**: Intermediate
**Topics**: 8 major areas | **Code Examples**: 40+ real-world patterns

---

## 1. ROOM ORM (RECOMMENDED)

Room is the modern persistence layer providing type-safe database access with compile-time query verification.

### 1.1 Entity Design

```kotlin
// Basic entity
@Entity(tableName = "users")
data class User(
    @PrimaryKey val id: Int,
    val name: String,
    val email: String,
    val createdAt: Long = System.currentTimeMillis(),
    // Ignore fields not stored in database
    @Ignore val isSelected: Boolean = false
)

// Entity with customized column names
@Entity(tableName = "products")
data class Product(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    @ColumnInfo(name = "product_name") val name: String,
    @ColumnInfo(name = "product_price") val price: Double,
    @ColumnInfo(typeAffinity = ColumnInfo.REAL) val rating: Float
)

// Composite primary key
@Entity(tableName = "order_items", primaryKeys = ["orderId", "productId"])
data class OrderItem(
    val orderId: Int,
    val productId: Int,
    val quantity: Int
)

// Entity with foreign key (relationship)
@Entity(
    tableName = "posts",
    foreignKeys = [
        ForeignKey(
            entity = User::class,
            parentColumns = ["id"],
            childColumns = ["userId"],
            onDelete = ForeignKey.CASCADE  // Delete posts when user deleted
        )
    ],
    indices = [Index("userId")]  // Index for faster queries
)
data class Post(
    @PrimaryKey val id: Int,
    val userId: Int,
    val title: String,
    val content: String
)
```

### 1.2 DAO (Data Access Objects)

```kotlin
@Dao
interface UserDao {
    // Query single item
    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getUser(userId: Int): User?

    // Query multiple items
    @Query("SELECT * FROM users ORDER BY name ASC")
    suspend fun getAllUsers(): List<User>

    // Reactive query with Flow (auto-updates on changes)
    @Query("SELECT * FROM users ORDER BY name ASC")
    fun observeAllUsers(): Flow<List<User>>

    // Filtered query with parameters
    @Query("SELECT * FROM users WHERE name LIKE :pattern")
    suspend fun searchByName(pattern: String): List<User>

    // Count rows
    @Query("SELECT COUNT(*) FROM users")
    suspend fun getUserCount(): Int

    // Insert single item
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: User)

    // Insert multiple items
    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertUsers(users: List<User>)

    // Update item
    @Update
    suspend fun updateUser(user: User)

    // Delete item
    @Delete
    suspend fun deleteUser(user: User)

    // Delete by condition
    @Query("DELETE FROM users WHERE id = :userId")
    suspend fun deleteUserById(userId: Int)

    // Upsert (Update or Insert)
    @Upsert
    suspend fun upsertUser(user: User)

    // Complex query with JOIN
    @Query("""
        SELECT users.id, users.name, COUNT(posts.id) as postCount
        FROM users
        LEFT JOIN posts ON users.id = posts.userId
        GROUP BY users.id
        ORDER BY postCount DESC
    """)
    suspend fun getUsersWithPostCount(): List<UserWithPostCount>

    // Transaction (all or nothing)
    @Transaction
    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getUserWithPosts(userId: Int): UserWithPosts
}

// Data class for JOIN results
data class UserWithPostCount(
    val id: Int,
    val name: String,
    val postCount: Int
)

// Relation for nested objects
data class UserWithPosts(
    @Embedded val user: User,
    @Relation(
        parentColumn = "id",
        entityColumn = "userId"
    )
    val posts: List<Post>
)
```

### 1.3 Database Setup

```kotlin
@Database(
    entities = [User::class, Post::class, Product::class],
    version = 1,
    exportSchema = true  // Export for migrations
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
    abstract fun postDao(): PostDao

    companion object {
        @Volatile
        private var instance: AppDatabase? = null

        fun getInstance(context: Context): AppDatabase {
            return instance ?: synchronized(this) {
                instance ?: Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "app_database"
                )
                    .addMigrations(MIGRATION_1_TO_2, MIGRATION_2_TO_3)
                    .build()
                    .also { instance = it }
            }
        }

        // Define migrations for schema changes
        private val MIGRATION_1_TO_2 = object : Migration(1, 2) {
            override fun migrate(database: SupportSQLiteDatabase) {
                // Add new column to existing table
                database.execSQL(
                    "ALTER TABLE users ADD COLUMN age INTEGER DEFAULT 0"
                )
            }
        }

        private val MIGRATION_2_TO_3 = object : Migration(2, 3) {
            override fun migrate(database: SupportSQLiteDatabase) {
                // Create new table
                database.execSQL(
                    """CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY NOT NULL,
                        userId INTEGER NOT NULL,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        FOREIGN KEY(userId) REFERENCES users(id) ON DELETE CASCADE
                    )"""
                )
            }
        }
    }
}

// Hilt injection
@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    @Provides
    @Singleton
    fun provideAppDatabase(context: Context): AppDatabase {
        return AppDatabase.getInstance(context)
    }

    @Provides
    fun provideUserDao(database: AppDatabase): UserDao = database.userDao()
}
```

### 1.4 Repository Pattern (MVVM Integration)

```kotlin
interface UserRepository {
    fun observeAllUsers(): Flow<List<User>>
    suspend fun getUser(id: Int): User?
    suspend fun insertUser(user: User)
    suspend fun deleteUser(user: User)
}

class UserRepositoryImpl(
    private val userDao: UserDao
) : UserRepository {
    override fun observeAllUsers(): Flow<List<User>> = userDao.observeAllUsers()

    override suspend fun getUser(id: Int): User? = userDao.getUser(id)

    override suspend fun insertUser(user: User) = userDao.insertUser(user)

    override suspend fun deleteUser(user: User) = userDao.deleteUser(user)
}

// ViewModel using repository
@HiltViewModel
class UserListViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {
    val users: Flow<List<User>> = repository.observeAllUsers()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())
}
```

---

## 2. SQLITE DIRECT ACCESS

For legacy apps or complex scenarios, direct SQLite access provides maximum flexibility but lower type safety.

```kotlin
// ContentValues for INSERT/UPDATE
val values = ContentValues().apply {
    put("name", "John")
    put("email", "john@example.com")
}
val newId = database.insert("users", null, values)

// Cursor for READ
val cursor = database.query(
    tableName = "users",
    columns = arrayOf("id", "name", "email"),
    selection = "age > ?",
    selectionArgs = arrayOf("18"),
    orderBy = "name ASC",
    limit = "10"
)

cursor.use { cursor ->
    while (cursor.moveToNext()) {
        val id = cursor.getInt(cursor.getColumnIndex("id"))
        val name = cursor.getString(cursor.getColumnIndex("name"))
    }
}

// UPDATE
val updateValues = ContentValues().apply {
    put("email", "newemail@example.com")
}
database.update("users", updateValues, "id = ?", arrayOf("1"))

// DELETE
database.delete("users", "id = ?", arrayOf("1"))
```

---

## 3. SHAREDPREFERENCES & ENCRYPTED PREFERENCES

For simple key-value storage (small data, non-relational).

### 3.1 SharedPreferences

```kotlin
// Access SharedPreferences
val prefs = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)

// Write
prefs.edit {
    putString("username", "john")
    putInt("age", 30)
    putBoolean("isLoggedIn", true)
    putFloat("rating", 4.5f)
    putLong("timestamp", System.currentTimeMillis())
    apply()  // or commit() for synchronous
}

// Read
val username = prefs.getString("username", "default")
val age = prefs.getInt("age", 0)
val isLoggedIn = prefs.getBoolean("isLoggedIn", false)

// Clear all
prefs.edit {
    clear()
    apply()
}

// Remove specific key
prefs.edit {
    remove("username")
    apply()
}
```

### 3.2 EncryptedSharedPreferences (RECOMMENDED for sensitive data)

```kotlin
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val encryptedPrefs = EncryptedSharedPreferences.create(
    context,
    "secret_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

// All operations same as SharedPreferences
encryptedPrefs.edit {
    putString("auth_token", "secret_token_here")
    putString("refresh_token", "refresh_token_here")
    apply()
}

val token = encryptedPrefs.getString("auth_token", null)
```

---

## 4. DATASTORE (MODERN ALTERNATIVE)

DataStore is the modern successor to SharedPreferences with coroutine support and type safety.

### 4.1 Preferences DataStore

```kotlin
// Define preference keys
object PreferencesKeys {
    val USERNAME = stringPreferencesKey("username")
    val AGE = intPreferencesKey("age")
    val IS_LOGGED_IN = booleanPreferencesKey("is_logged_in")
    val AUTH_TOKEN = stringPreferencesKey("auth_token")
}

// Create DataStore
val Context.settingsDataStore: DataStore<Preferences> by preferencesDataStore(
    name = "app_settings"
)

// Write data
suspend fun saveUserSettings(context: Context, username: String, age: Int) {
    context.settingsDataStore.edit { preferences ->
        preferences[PreferencesKeys.USERNAME] = username
        preferences[PreferencesKeys.AGE] = age
        preferences[PreferencesKeys.IS_LOGGED_IN] = true
    }
}

// Read single value
val username: Flow<String> = context.settingsDataStore.data.map { preferences ->
    preferences[PreferencesKeys.USERNAME] ?: ""
}

// Read multiple values as object
data class UserSettings(
    val username: String = "",
    val age: Int = 0,
    val isLoggedIn: Boolean = false
)

fun readUserSettings(context: Context): Flow<UserSettings> {
    return context.settingsDataStore.data.map { preferences ->
        UserSettings(
            username = preferences[PreferencesKeys.USERNAME] ?: "",
            age = preferences[PreferencesKeys.AGE] ?: 0,
            isLoggedIn = preferences[PreferencesKeys.IS_LOGGED_IN] ?: false
        )
    }
}

// Use in ViewModel
@HiltViewModel
class SettingsViewModel @Inject constructor(
    private val context: Context
) : ViewModel() {
    val userSettings: Flow<UserSettings> = readUserSettings(context)
        .stateIn(viewModelScope, SharingStarted.Lazily, UserSettings())
}
```

### 4.2 Proto DataStore (Type-safe with Protobuf)

```kotlin
// Define schema in proto file (app/src/main/proto/user.proto)
/*
syntax = "proto3";

option java_package = "com.example.app";
option java_outer_classname = "UserProto";

message UserSettings {
  string username = 1;
  int32 age = 2;
  bool is_logged_in = 3;
}
*/

// Create Proto DataStore
val Context.userSettingsDataStore: DataStore<UserProto.UserSettings> by dataStore(
    fileName = "user_settings.pb",
    serializer = UserSettingsSerializer
)

object UserSettingsSerializer : Serializer<UserProto.UserSettings> {
    override val defaultValue = UserProto.UserSettings.getDefaultInstance()

    override suspend fun readObject(input: InputStream): UserProto.UserSettings {
        return UserProto.UserSettings.parseFrom(input)
    }

    override suspend fun writeObject(
        t: UserProto.UserSettings,
        output: OutputStream
    ) {
        t.writeTo(output)
    }
}

// Use Proto DataStore
suspend fun saveUserProto(context: Context, username: String) {
    context.userSettingsDataStore.updateData { currentSettings ->
        currentSettings.toBuilder()
            .setUsername(username)
            .setIsLoggedIn(true)
            .build()
    }
}

fun readUserProto(context: Context): Flow<UserProto.UserSettings> {
    return context.userSettingsDataStore.data
}
```

---

## 5. DATA ENCRYPTION & SECURITY

### 5.1 EncryptedFile

```kotlin
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val encryptedFile = EncryptedFile.Builder(
    context,
    File(context.filesDir, "secret_data.txt"),
    masterKey,
    EncryptedFile.FileEncryptionScheme.AES256_GCM_HKDF_4KB
).build()

// Write encrypted data
fun saveEncryptedData(data: String) {
    encryptedFile.openFileOutput().use { output ->
        output.write(data.toByteArray())
    }
}

// Read encrypted data
fun readEncryptedData(): String {
    return encryptedFile.openFileInput().use { input ->
        input.readBytes().decodeToString()
    }
}
```

### 5.2 Secure Data Best Practices

```kotlin
// ✅ Encrypt sensitive data before storing
class SecurityPreferences @Inject constructor(
    private val context: Context
) {
    private val encryptedPrefs by lazy {
        val masterKey = MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build()

        EncryptedSharedPreferences.create(
            context,
            "secure_prefs",
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        )
    }

    suspend fun saveAuthToken(token: String) {
        encryptedPrefs.edit {
            putString("auth_token", token)
            apply()
        }
    }

    fun getAuthToken(): String? {
        return encryptedPrefs.getString("auth_token", null)
    }

    suspend fun clearAuthData() {
        encryptedPrefs.edit {
            remove("auth_token")
            apply()
        }
    }
}
```

---

## 6. TRANSACTIONS & ATOMIC OPERATIONS

Transactions ensure all-or-nothing database operations.

```kotlin
@Dao
interface TransactionDao {
    @Transaction
    suspend fun transferMoney(fromId: Int, toId: Int, amount: Double) {
        // Deduct from source
        deductBalance(fromId, amount)
        // Add to destination
        addBalance(toId, amount)
        // If any fails, entire transaction rolls back
    }

    @Query("UPDATE accounts SET balance = balance - :amount WHERE id = :accountId")
    suspend fun deductBalance(accountId: Int, amount: Double)

    @Query("UPDATE accounts SET balance = balance + :amount WHERE id = :accountId")
    suspend fun addBalance(accountId: Int, amount: Double)
}

// Or use withTransaction helper
suspend fun transferMoneyWithTransaction(
    fromId: Int,
    toId: Int,
    amount: Double,
    database: AppDatabase
) {
    database.withTransaction {
        database.accountDao().deductBalance(fromId, amount)
        database.accountDao().addBalance(toId, amount)
        database.historyDao().insertTransaction(
            Transaction(fromId, toId, amount)
        )
    }
}
```

---

## 7. DATABASE MIGRATIONS

Schema versioning allows app updates without data loss.

```kotlin
val MIGRATION_1_TO_2 = object : Migration(1, 2) {
    override fun migrate(database: SupportSQLiteDatabase) {
        // Add new column
        database.execSQL(
            "ALTER TABLE users ADD COLUMN last_login INTEGER DEFAULT 0"
        )
    }
}

val MIGRATION_2_TO_3 = object : Migration(2, 3) {
    override fun migrate(database: SupportSQLiteDatabase) {
        // Create new table
        database.execSQL(
            """CREATE TABLE IF NOT EXISTS user_settings (
                id INTEGER PRIMARY KEY NOT NULL,
                userId INTEGER NOT NULL,
                theme TEXT DEFAULT 'light',
                FOREIGN KEY(userId) REFERENCES users(id) ON DELETE CASCADE
            )"""
        )

        // Create index for performance
        database.execSQL(
            "CREATE INDEX idx_user_settings_userId ON user_settings(userId)"
        )
    }
}

val MIGRATION_3_TO_4 = object : Migration(3, 4) {
    override fun migrate(database: SupportSQLiteDatabase) {
        // Rename column (SQLite limitation workaround)
        database.execSQL(
            """CREATE TABLE users_new (
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                user_age INTEGER DEFAULT 0
            )"""
        )
        database.execSQL(
            """INSERT INTO users_new (id, name, email, user_age)
               SELECT id, name, email, age FROM users"""
        )
        database.execSQL("DROP TABLE users")
        database.execSQL("ALTER TABLE users_new RENAME TO users")
    }
}

// Apply migrations when building database
Room.databaseBuilder(context, AppDatabase::class.java, "db")
    .addMigrations(MIGRATION_1_TO_2, MIGRATION_2_TO_3, MIGRATION_3_TO_4)
    .build()
```

---

## 8. DATABASE TESTING

### 8.1 Unit Tests with In-Memory Database

```kotlin
@RunWith(RobolectricTestRunner::class)
class UserDaoTest {
    private lateinit var database: AppDatabase
    private lateinit var userDao: UserDao

    @Before
    fun setup() {
        // Create in-memory database for testing
        database = Room.inMemoryDatabaseBuilder(
            ApplicationProvider.getApplicationContext(),
            AppDatabase::class.java
        )
            .allowMainThreadQueries()
            .build()

        userDao = database.userDao()
    }

    @After
    fun tearDown() {
        database.close()
    }

    @Test
    fun insertAndRetrieveUser() = runTest {
        val user = User(1, "John", "john@example.com")

        userDao.insertUser(user)

        val retrieved = userDao.getUser(1)
        assertEquals(user, retrieved)
    }

    @Test
    fun getAllUsersReturnsCorrectList() = runTest {
        val users = listOf(
            User(1, "John", "john@example.com"),
            User(2, "Jane", "jane@example.com")
        )

        users.forEach { userDao.insertUser(it) }

        val allUsers = userDao.getAllUsers()
        assertEquals(users, allUsers)
    }

    @Test
    fun deleteUserRemovesFromDatabase() = runTest {
        val user = User(1, "John", "john@example.com")
        userDao.insertUser(user)

        userDao.deleteUser(user)

        val retrieved = userDao.getUser(1)
        assertNull(retrieved)
    }

    @Test
    fun updateUserChangesData() = runTest {
        val original = User(1, "John", "john@example.com")
        userDao.insertUser(original)

        val updated = original.copy(name = "Jane")
        userDao.updateUser(updated)

        val retrieved = userDao.getUser(1)
        assertEquals("Jane", retrieved?.name)
    }
}

// Test migrations
@RunWith(RobolectricTestRunner::class)
class MigrationTest {
    @Test
    fun migrateFrom1To2() {
        val helper = MigrationTestHelper(
            InstrumentationRegistry.getInstrumentation(),
            AppDatabase::class.java
        )

        var db = helper.createDatabase(DB_NAME, 1)
        // Insert test data at version 1
        db.execSQL("INSERT INTO users VALUES (1, 'John', 'john@example.com')")
        db.close()

        // Migrate to version 2
        db = helper.runMigrationsAndValidate(
            DB_NAME,
            2,
            true,
            MIGRATION_1_TO_2
        )

        // Verify migration worked
        val cursor = db.query("SELECT * FROM users WHERE id = 1")
        cursor.moveToFirst()
        assertEquals("John", cursor.getString(1))
    }
}
```

---

## 9. BEST PRACTICES

✅ **Room ORM**
- Use Room for all new projects (type-safe, compile-time verified)
- Use repositories to abstract data access
- Apply migrations for schema changes
- Use transactions for multi-table operations

✅ **Data Design**
- Primary keys on all entities
- Foreign keys for relationships
- Indexes on frequently queried columns
- Use @Ignore for fields not stored

✅ **Security**
- Encrypt sensitive data (auth tokens, PII)
- Use EncryptedSharedPreferences or EncryptedFile
- Never store passwords (use secure tokens)
- Clear auth data on logout

✅ **Performance**
- Use Flow for reactive queries
- Apply DiffUtil when displaying lists
- Index foreign key columns
- Close cursors and databases properly

✅ **Testing**
- Test all DAO operations
- Use in-memory database for tests
- Test migrations with MigrationTestHelper
- Mock repositories in ViewModel tests

---

## 10. LEARNING PATH: 4 WEEKS (62 HOURS)

**Week 1 (16h): Room ORM Foundation**
- Entity design with annotations
- DAO creation and operations
- Database setup and instantiation
- Basic queries and inserts
- Build simple CRUD app

**Week 2 (15h): Advanced Room Features**
- Relationships (1:1, 1:N, M:N)
- Complex queries with JOINs
- Reactive queries with Flow
- Transactions and atomic operations
- Repository pattern implementation

**Week 3 (15h): Security & Alternative Storage**
- SharedPreferences & EncryptedSharedPreferences
- DataStore (Preferences & Proto)
- EncryptedFile for large sensitive data
- Encryption best practices
- Secure token storage

**Week 4 (16h): Advanced Topics**
- Database migrations and versioning
- Testing DAOs and repositories
- Performance optimization
- Legacy SQLite migration
- Production debugging techniques

---

**Mastery Checkpoint**:
- Can design normalized database schemas
- Implement efficient Room DAOs
- Handle migrations confidently
- Secure sensitive data properly
- Write comprehensive database tests

---

**Learning Hours**: 62 hours | **Level**: Intermediate
**Next Step**: Networking agent (Retrofit, OkHttp, APIs)

---

## TROUBLESHOOTING GUIDE

### Common Issues & Solutions

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| "Cannot access database on main thread" | Blocking UI thread | Use `suspend` functions with coroutines |
| Migration failed | Missing migration path | Add all intermediate migrations |
| Foreign key constraint failed | Parent row missing | Insert parent first, use CASCADE |
| Query returns null | Wrong query or empty table | Check WHERE clause, verify data exists |
| EncryptedPreferences crash | Missing keystore | Handle KeyPermanentlyInvalidatedException |

### Debug Checklist

```
□ Is database version incremented? Check @Database annotation
□ Are migrations complete? All version paths covered?
□ Is query returning Flow? Use collect, not first()
□ Is transaction wrapped? Use @Transaction annotation
□ Is encryption key valid? Check MasterKey initialization
□ Is cursor closed? Check for resource leaks
```

### Database Debug Pattern

```kotlin
// Enable Room query logging
Room.databaseBuilder(context, AppDatabase::class.java, "db")
    .setQueryCallback({ sqlQuery, bindArgs ->
        Log.d("RoomQuery", "SQL: $sqlQuery, Args: $bindArgs")
    }, Executors.newSingleThreadExecutor())
    .build()
```

### When to Escalate

- API data sync issues → Use **05-networking** agent
- Architecture patterns → Use **06-architecture** agent
- Security concerns → Use **07-production** agent
