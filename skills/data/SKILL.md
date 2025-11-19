---
name: data-persistence
description: Room ORM, SQLite, SharedPreferences, DataStore, encryption. Use when implementing data storage and database operations.
---

# Data Persistence Skill

## Quick Start

### Room Entity & DAO
```kotlin
@Entity
data class User(@PrimaryKey val id: Int, val name: String)

@Dao
interface UserDao {
    @Query("SELECT * FROM User")
    suspend fun getAllUsers(): List<User>
    
    @Insert
    suspend fun insert(user: User)
}
```

### EncryptedSharedPreferences
```kotlin
val prefs = EncryptedSharedPreferences.create(context, "secret",
    MasterKey.Builder(context).setKeyScheme(AES256_GCM).build(),
    AES256_SIV, AES256_GCM)

prefs.edit { putString("token", value) }
```

### DataStore
```kotlin
val dataStore = context.createDataStore("settings")
val preferences = dataStore.data.map { it[KEY] ?: "" }
```

## Key Concepts

### Room Advantages
- Type-safe queries
- Compile-time checks
- Suspend/Flow support
- Migration management

### SharedPreferences
- Simple key-value store
- Use Encrypted version for sensitive data
- Limited to small data

### DataStore
- Modern SharedPreferences
- Coroutine-native
- Type-safe
- ACID transactions

## Best Practices

✅ Use Room for complex data
✅ Encrypt sensitive data
✅ Implement proper migrations
✅ Handle database errors
✅ Test database operations

## Resources

- [Room Documentation](https://developer.android.com/training/data-storage/room)
- [DataStore Guide](https://developer.android.com/topic/libraries/architecture/datastore)
