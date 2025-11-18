---
description: Data storage and persistence - Room ORM, SQLite, SharedPreferences, DataStore, encryption - Android data management strategies
capabilities: ["Room ORM", "SQLite database", "SharedPreferences", "DataStore preferences", "Encrypted storage", "Data migration", "Transaction management", "Database testing"]
---

# Data Management Agent

Master data persistence using Room ORM, SQLite, SharedPreferences, and modern DataStore for secure and efficient data storage.

## Room ORM (Recommended)

### Entity
```kotlin
@Entity(tableName = "users")
data class User(
    @PrimaryKey val id: Int,
    val name: String,
    @ColumnInfo(name = "email") val email: String
)
```

### DAO (Data Access Object)
```kotlin
@Dao
interface UserDao {
    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getUser(userId: Int): User?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: User)
    
    @Delete
    suspend fun deleteUser(user: User)
}
```

### Database
```kotlin
@Database(entities = [User::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
}
```

### Key Features
- Type-safe compile-time checks
- Suspend function support
- Flow integration for reactive queries
- Migration support
- Foreign key relationships

## SQLite

### Direct Queries
- ContentValues for insert/update
- Cursor for read operations
- WHERE clause filtering
- ORDER BY sorting
- JOIN operations

### When to Use
- Legacy codebase
- Complex queries
- Maximum flexibility

## SharedPreferences

### Key-Value Storage
```kotlin
val prefs = getSharedPreferences("app", Context.MODE_PRIVATE)
prefs.edit { putString("key", "value") }
val value = prefs.getString("key", "default")
```

### EncryptedSharedPreferences
```kotlin
val encryptedPrefs = EncryptedSharedPreferences.create(
    context, "secret",
    MasterKey.Builder(context).setKeyScheme(AES256_GCM).build(),
    AES256_SIV, AES256_GCM
)
```

## DataStore (Modern Alternative)

### Preferences DataStore
```kotlin
val dataStore = context.createDataStore(name = "settings")
val userPreferences = dataStore.data.map { preferences ->
    preferences[USER_NAME_KEY] ?: ""
}
```

### Advantages
- Coroutine-native
- Type-safe
- ACID transactions
- Reactive (Flow-based)

## Data Encryption

### EncryptedFile
```kotlin
val encryptedFile = EncryptedFile.Builder(
    context, File(filesDir, "secret.txt"),
    MasterKey.Builder(context).build(),
    AES256_GCM_HKDF_4KB
).build()

encryptedFile.openFileOutput().use { output ->
    output.write(sensitiveData.toByteArray())
}
```

## Transactions

### Atomic Operations
```kotlin
database.withTransaction {
    userDao.insertUser(user)
    historyDao.insertHistory(history)
}
```

## Database Migration

### Schema Versioning
```kotlin
val migration1to2 = object : Migration(1, 2) {
    override fun migrate(database: SupportSQLiteDatabase) {
        database.execSQL("ALTER TABLE users ADD COLUMN age INTEGER")
    }
}

Room.databaseBuilder(context, AppDatabase::class.java, "db")
    .addMigrations(migration1to2)
    .build()
```

## Testing

### In-Memory Database
```kotlin
val db = Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java)
    .allowMainThreadQueries()
    .build()
```

## Learning Outcomes
- Design effective database schemas
- Implement Room ORM correctly
- Secure sensitive data
- Handle migrations
- Test database operations

---

**Learning Hours**: 62 hours | **Level**: Intermediate
