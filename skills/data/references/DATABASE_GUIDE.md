# Room Database Complete Guide

Type-safe SQLite abstraction layer for Android.

## Room Components

### 1. Entity
```kotlin
@Entity(
    tableName = "users",
    indices = [Index(value = ["email"], unique = true)],
    foreignKeys = [ForeignKey(
        entity = TeamEntity::class,
        parentColumns = ["id"],
        childColumns = ["team_id"],
        onDelete = ForeignKey.CASCADE
    )]
)
data class UserEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,

    val name: String,

    @ColumnInfo(name = "email")
    val email: String,

    @ColumnInfo(name = "team_id")
    val teamId: Long?,

    @ColumnInfo(name = "created_at")
    val createdAt: Long = System.currentTimeMillis(),

    @Ignore
    val tempData: String? = null
)
```

### 2. DAO
```kotlin
@Dao
interface UserDao {
    // Flow - reactive updates
    @Query("SELECT * FROM users ORDER BY name")
    fun getAllUsers(): Flow<List<UserEntity>>

    // Suspend - one-shot
    @Query("SELECT * FROM users WHERE id = :id")
    suspend fun getUserById(id: Long): UserEntity?

    // Insert with conflict strategy
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(user: UserEntity): Long

    @Insert
    suspend fun insertAll(users: List<UserEntity>)

    // Update
    @Update
    suspend fun update(user: UserEntity)

    // Delete
    @Delete
    suspend fun delete(user: UserEntity)

    @Query("DELETE FROM users WHERE id = :id")
    suspend fun deleteById(id: Long)

    // Transaction
    @Transaction
    suspend fun replaceAll(users: List<UserEntity>) {
        deleteAll()
        insertAll(users)
    }
}
```

### 3. Database
```kotlin
@Database(
    entities = [UserEntity::class, TeamEntity::class],
    version = 2,
    exportSchema = true,
    autoMigrations = [
        AutoMigration(from = 1, to = 2)
    ]
)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
    abstract fun teamDao(): TeamDao
}
```

## Type Converters

```kotlin
class Converters {
    @TypeConverter
    fun fromTimestamp(value: Long?): Date? =
        value?.let { Date(it) }

    @TypeConverter
    fun dateToTimestamp(date: Date?): Long? =
        date?.time

    @TypeConverter
    fun fromStringList(value: List<String>): String =
        value.joinToString(",")

    @TypeConverter
    fun toStringList(value: String): List<String> =
        if (value.isEmpty()) emptyList() else value.split(",")

    @TypeConverter
    fun fromJson(value: String): MyData =
        Gson().fromJson(value, MyData::class.java)

    @TypeConverter
    fun toJson(data: MyData): String =
        Gson().toJson(data)
}
```

## Migrations

### Auto Migration
```kotlin
@Database(
    version = 2,
    autoMigrations = [
        AutoMigration(from = 1, to = 2, spec = Migration1To2::class)
    ]
)
abstract class AppDatabase : RoomDatabase()

@RenameColumn(tableName = "users", fromColumnName = "user_name", toColumnName = "name")
class Migration1To2 : AutoMigrationSpec
```

### Manual Migration
```kotlin
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(database: SupportSQLiteDatabase) {
        database.execSQL(
            "ALTER TABLE users ADD COLUMN avatar_url TEXT DEFAULT NULL"
        )
    }
}

val db = Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
    .addMigrations(MIGRATION_1_2)
    .build()
```

## Repository Pattern

```kotlin
class UserRepository @Inject constructor(
    private val userDao: UserDao,
    private val userApi: UserApi,
    private val dispatcher: CoroutineDispatcher = Dispatchers.IO
) {
    val users: Flow<List<User>> = userDao.getAllUsers()
        .map { entities -> entities.map { it.toUser() } }
        .flowOn(dispatcher)

    suspend fun refreshUsers() = withContext(dispatcher) {
        try {
            val remoteUsers = userApi.getUsers()
            userDao.replaceAll(remoteUsers.map { it.toEntity() })
        } catch (e: Exception) {
            // Handle error - maybe emit cached data
        }
    }

    suspend fun getUser(id: Long): User? = withContext(dispatcher) {
        userDao.getUserById(id)?.toUser()
    }
}
```

## DataStore (Modern SharedPreferences)

### Preferences DataStore
```kotlin
val Context.dataStore by preferencesDataStore(name = "settings")

class SettingsRepository @Inject constructor(
    private val dataStore: DataStore<Preferences>
) {
    private object Keys {
        val DARK_MODE = booleanPreferencesKey("dark_mode")
        val USER_TOKEN = stringPreferencesKey("user_token")
    }

    val darkMode: Flow<Boolean> = dataStore.data
        .map { preferences -> preferences[Keys.DARK_MODE] ?: false }

    suspend fun setDarkMode(enabled: Boolean) {
        dataStore.edit { preferences ->
            preferences[Keys.DARK_MODE] = enabled
        }
    }

    suspend fun clearAll() {
        dataStore.edit { it.clear() }
    }
}
```

## Encrypted Storage

```kotlin
// EncryptedSharedPreferences
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val encryptedPrefs = EncryptedSharedPreferences.create(
    context,
    "secure_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

// Save token
encryptedPrefs.edit { putString("auth_token", token) }

// Read token
val token = encryptedPrefs.getString("auth_token", null)
```

## Best Practices

1. **Use Flow for reactive data**
2. **Always use suspend for write operations**
3. **Implement proper migrations**
4. **Use indices for frequently queried columns**
5. **Keep entities simple (no business logic)**
6. **Use Repository pattern for abstraction**
7. **Encrypt sensitive data**
8. **Test database operations**

## Resources

- [Room Documentation](https://developer.android.com/training/data-storage/room)
- [DataStore Guide](https://developer.android.com/topic/libraries/architecture/datastore)
- [SQLite Best Practices](https://www.sqlite.org/bestpractice.html)
