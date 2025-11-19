---
description: Android'de veri depolama ve yönetimi için kapsamlı bir rehber. Room ORM, SQLite, SharedPreferences ve DataStore teknolojilerini detaylı olarak öğreten agent.
capabilities:
  - Room ORM Kütüphanesi
  - SQLite Veritabanı
  - SharedPreferences
  - DataStore (Proto & Preferences)
  - Veri Şifreleme
  - Batch İşlemler
  - Veri Migrasyonu
  - İlişkisel Veritabanı Tasarımı
  - Performans Optimizasyonu
---

# Android Data Management & Storage Agent

## 1. Room ORM (Recommended)

### Tanım ve Avantajları
Room, Google tarafından resmi olarak önerilen Android'in ORM (Object-Relational Mapping) kütüphanesidir. SQLite'ın üzerine built-in soyutlama katmanı sağlayarak type-safe veri erişimi sunmuştur.

### Room'un Temel Bileşenleri

#### 1.1 Entity (Varlık)
```kotlin
@Entity(tableName = "users")
data class User(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,

    @ColumnInfo(name = "user_name")
    val username: String,

    val email: String,

    @Ignore
    val profilePic: Bitmap? = null,

    val age: Int,
    val createdAt: Long = System.currentTimeMillis()
)
```

**Anotasyon Açıklamaları:**
- `@Entity`: Sınıfın veritabanı tablosuna karşılık geldiğini belirtir
- `@PrimaryKey`: Birincil anahtarı tanımlar (autoGenerate: otomatik artış)
- `@ColumnInfo`: Sütun ismini özelleştirir
- `@Ignore`: Alanın veritabanıya kaydedilmeyeceğini belirtir

#### 1.2 DAO (Data Access Object)
```kotlin
@Dao
interface UserDao {

    // CREATE
    @Insert
    suspend fun insert(user: User): Long

    // INSERT OR REPLACE
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOrReplace(user: User)

    // INSERT BATCH
    @Insert
    suspend fun insertAll(users: List<User>)

    // READ
    @Query("SELECT * FROM users WHERE id = :userId")
    suspend fun getUserById(userId: Int): User?

    @Query("SELECT * FROM users ORDER BY createdAt DESC")
    fun getAllUsers(): Flow<List<User>>

    @Query("SELECT * FROM users WHERE user_name LIKE '%' || :query || '%'")
    fun searchUsers(query: String): Flow<List<User>>

    // UPDATE
    @Update
    suspend fun update(user: User)

    @Query("UPDATE users SET email = :newEmail WHERE id = :userId")
    suspend fun updateEmail(userId: Int, newEmail: String)

    // DELETE
    @Delete
    suspend fun delete(user: User)

    @Query("DELETE FROM users WHERE id = :userId")
    suspend fun deleteById(userId: Int)

    // COUNT
    @Query("SELECT COUNT(*) FROM users")
    fun getUserCount(): Flow<Int>
}
```

#### 1.3 Database
```kotlin
@Database(
    entities = [User::class, Post::class, Comment::class],
    version = 3,
    exportSchema = true
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
    abstract fun postDao(): PostDao
    abstract fun commentDao(): CommentDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getInstance(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "app_database"
                )
                .addMigrations(MIGRATION_1_2, MIGRATION_2_3)
                .build()
                .also { INSTANCE = it }
            }
        }

        private val MIGRATION_1_2 = object : Migration(1, 2) {
            override fun migrate(database: SupportSQLiteDatabase) {
                database.execSQL(
                    "ALTER TABLE users ADD COLUMN age INTEGER NOT NULL DEFAULT 0"
                )
            }
        }

        private val MIGRATION_2_3 = object : Migration(2, 3) {
            override fun migrate(database: SupportSQLiteDatabase) {
                database.execSQL(
                    "CREATE TABLE new_users (id INTEGER PRIMARY KEY, username TEXT, email TEXT)"
                )
                database.execSQL(
                    "INSERT INTO new_users SELECT id, user_name, email FROM users"
                )
                database.execSQL("DROP TABLE users")
                database.execSQL("ALTER TABLE new_users RENAME TO users")
            }
        }
    }
}
```

### Room Avantajları
- **Type-Safe**: Compile-time sorgu doğrulaması
- **Flow Integration**: Reaktif veri güncellemeleri
- **Koroutine Support**: Async veri işlemleri
- **Migration Support**: Veritabanı versiyonlaması
- **DAO Pattern**: Clean architecture uygunluğu
- **Compile-time Verifiction**: Derleme zamanında hata bulma

### Room Repository Pattern
```kotlin
class UserRepository(private val userDao: UserDao) {

    val allUsers: Flow<List<User>> = userDao.getAllUsers()

    suspend fun insertUser(user: User) {
        userDao.insert(user)
    }

    fun searchUsers(query: String): Flow<List<User>> {
        return userDao.searchUsers(query)
    }

    suspend fun deleteUser(user: User) {
        userDao.delete(user)
    }
}
```

---

## 2. SQLite

### Tanım ve Kullanım
SQLite, Android'in native veritabanı motorudur. Room aracılığı ile erişilmesi önerilir, ancak direct erişim de mümkündür.

### Direct SQLite Kullanımı (Low Level)
```kotlin
class DatabaseHelper(context: Context) : SQLiteOpenHelper(
    context,
    DATABASE_NAME,
    null,
    DATABASE_VERSION
) {
    companion object {
        const val DATABASE_NAME = "my_database.db"
        const val DATABASE_VERSION = 1
        const val TABLE_USERS = "users"
        const val COLUMN_ID = "id"
        const val COLUMN_NAME = "name"
        const val COLUMN_EMAIL = "email"
    }

    override fun onCreate(db: SQLiteDatabase) {
        val createTable = """
            CREATE TABLE $TABLE_USERS (
                $COLUMN_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                $COLUMN_NAME TEXT NOT NULL,
                $COLUMN_EMAIL TEXT UNIQUE NOT NULL
            )
        """.trimIndent()
        db.execSQL(createTable)
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        db.execSQL("DROP TABLE IF EXISTS $TABLE_USERS")
        onCreate(db)
    }

    // INSERT
    fun insertUser(name: String, email: String): Long {
        val values = ContentValues().apply {
            put(COLUMN_NAME, name)
            put(COLUMN_EMAIL, email)
        }
        return writableDatabase.insert(TABLE_USERS, null, values)
    }

    // READ
    fun getAllUsers(): List<User> {
        val users = mutableListOf<User>()
        val cursor = readableDatabase.query(
            TABLE_USERS,
            null,
            null,
            null,
            null,
            null,
            null
        )

        with(cursor) {
            while (moveToNext()) {
                users.add(User(
                    id = getInt(getColumnIndexOrThrow(COLUMN_ID)),
                    name = getString(getColumnIndexOrThrow(COLUMN_NAME)),
                    email = getString(getColumnIndexOrThrow(COLUMN_EMAIL))
                ))
            }
            close()
        }
        return users
    }

    // UPDATE
    fun updateUser(id: Int, name: String): Int {
        val values = ContentValues().apply {
            put(COLUMN_NAME, name)
        }
        return writableDatabase.update(
            TABLE_USERS,
            values,
            "$COLUMN_ID = ?",
            arrayOf(id.toString())
        )
    }

    // DELETE
    fun deleteUser(id: Int): Int {
        return writableDatabase.delete(
            TABLE_USERS,
            "$COLUMN_ID = ?",
            arrayOf(id.toString())
        )
    }
}
```

### SQLite Performans İpuçları
- **Transaction Kullanımı**: Batch işlemler için
- **Index Oluşturma**: Sık sorgulanan sütunlar için
- **Cursor Yönetimi**: Memory leak'i önlemek için
- **WAL Mode**: Write-Ahead Logging ile performans iyileştirmesi

---

## 3. SharedPreferences

### Tanım ve Kullanım Alanları
SharedPreferences, basit anahtar-değer çiftlerini depolamak için kullanılan hafif bir storage mekanizmasıdır. Küçük ayarlar, flagi ve basit konfigürasyonlar için idealdir.

### Temel Kullanım
```kotlin
class PreferencesManager(context: Context) {
    private val sharedPref = context.getSharedPreferences(
        "app_preferences",
        Context.MODE_PRIVATE
    )

    companion object {
        private const val KEY_USER_ID = "user_id"
        private const val KEY_USERNAME = "username"
        private const val KEY_IS_LOGGED_IN = "is_logged_in"
        private const val KEY_THEME = "theme"
        private const val KEY_LAST_SYNC = "last_sync"
    }

    // SAVE
    fun saveUserId(userId: Int) {
        sharedPref.edit().putInt(KEY_USER_ID, userId).apply()
    }

    fun saveUsername(username: String) {
        sharedPref.edit().putString(KEY_USERNAME, username).apply()
    }

    fun setLoggedIn(isLoggedIn: Boolean) {
        sharedPref.edit().putBoolean(KEY_IS_LOGGED_IN, isLoggedIn).apply()
    }

    fun saveTheme(theme: String) {
        sharedPref.edit().putString(KEY_THEME, theme).apply()
    }

    // READ
    fun getUserId(): Int {
        return sharedPref.getInt(KEY_USER_ID, -1)
    }

    fun getUsername(): String? {
        return sharedPref.getString(KEY_USERNAME, null)
    }

    fun isLoggedIn(): Boolean {
        return sharedPref.getBoolean(KEY_IS_LOGGED_IN, false)
    }

    fun getTheme(): String {
        return sharedPref.getString(KEY_THEME, "light") ?: "light"
    }

    // DELETE
    fun clearUserData() {
        sharedPref.edit().apply {
            remove(KEY_USER_ID)
            remove(KEY_USERNAME)
            remove(KEY_IS_LOGGED_IN)
            apply()
        }
    }

    fun clearAll() {
        sharedPref.edit().clear().apply()
    }
}
```

### Encrypted SharedPreferences (Güvenli)
```kotlin
class EncryptedPreferencesManager(context: Context) {
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    private val encryptedSharedPref = EncryptedSharedPreferences.create(
        context,
        "encrypted_preferences",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )

    fun saveEncryptedToken(token: String) {
        encryptedSharedPref.edit().putString("auth_token", token).apply()
    }

    fun getEncryptedToken(): String? {
        return encryptedSharedPref.getString("auth_token", null)
    }
}
```

### SharedPreferences Avantajları ve Sınırlamaları
**Avantajları:**
- Basit anahtar-değer depolama
- Otomatik serializasyon
- Düşük overhead

**Sınırlamaları:**
- Yalnızca basit veri tipleri
- Karmaşık nesneler için JSON serializasyonu gerekli
- Büyük veri setsine uygun değil
- Disk I/O maliyeti

---

## 4. DataStore (Recommended for Preferences)

### Tanım ve Avantajları
DataStore, Google tarafından önerilen modern SharedPreferences alternatifidir. Koroutine-native ve Type-safe'tir.

### 4.1 Preferences DataStore
```kotlin
class PreferencesDataStore(context: Context) {
    private val dataStore: DataStore<Preferences> = PreferenceDataStoreFactory.create(
        serializer = PreferencesSerializer,
        produceFile = { context.filesDir.resolve(PREFERENCES_FILE_NAME) }
    )

    companion object {
        private const val PREFERENCES_FILE_NAME = "app_preferences.pb"

        private object PreferencesKeys {
            val USER_ID = intPreferencesKey("user_id")
            val USERNAME = stringPreferencesKey("username")
            val IS_LOGGED_IN = booleanPreferencesKey("is_logged_in")
            val THEME = stringPreferencesKey("theme")
            val LANGUAGE = stringPreferencesKey("language")
        }
    }

    // SAVE
    suspend fun saveUserId(userId: Int) {
        dataStore.edit { preferences ->
            preferences[PreferencesKeys.USER_ID] = userId
        }
    }

    suspend fun saveUserData(username: String, isLoggedIn: Boolean) {
        dataStore.edit { preferences ->
            preferences[PreferencesKeys.USERNAME] = username
            preferences[PreferencesKeys.IS_LOGGED_IN] = isLoggedIn
        }
    }

    suspend fun saveTheme(theme: String) {
        dataStore.edit { preferences ->
            preferences[PreferencesKeys.THEME] = theme
        }
    }

    // READ
    fun getUserId(): Flow<Int> {
        return dataStore.data
            .catch { exception ->
                if (exception is IOException) {
                    emit(emptyPreferences())
                } else {
                    throw exception
                }
            }
            .map { preferences ->
                preferences[PreferencesKeys.USER_ID] ?: -1
            }
    }

    fun getUsername(): Flow<String> {
        return dataStore.data
            .map { preferences ->
                preferences[PreferencesKeys.USERNAME] ?: ""
            }
    }

    fun getTheme(): Flow<String> {
        return dataStore.data
            .map { preferences ->
                preferences[PreferencesKeys.THEME] ?: "light"
            }
    }

    // DELETE
    suspend fun clearUserId() {
        dataStore.edit { preferences ->
            preferences.remove(PreferencesKeys.USER_ID)
        }
    }

    suspend fun clearAll() {
        dataStore.edit { preferences ->
            preferences.clear()
        }
    }
}
```

### 4.2 Proto DataStore (Type-Safe)
```kotlin
// settings.proto dosyası
syntax = "proto3";

option java_package = "com.example.app.proto";
option java_outer_classname = "UserSettingsProto";

message UserSettings {
  string theme = 1;
  string language = 2;
  bool notifications_enabled = 3;
  int32 user_id = 4;
}
```

```kotlin
class ProtoDataStore(context: Context) {
    private val dataStore: DataStore<UserSettings> = DataStoreFactory.create(
        serializer = UserSettingsSerializer,
        produceFile = { context.filesDir.resolve("user_settings.pb") }
    )

    object UserSettingsSerializer : Serializer<UserSettings> {
        override val defaultValue: UserSettings = UserSettings.getDefaultInstance()

        override suspend fun readFrom(input: InputStream): UserSettings {
            return UserSettings.parseFrom(input)
        }

        override suspend fun writeTo(t: UserSettings, output: OutputStream) {
            t.writeTo(output)
        }
    }

    fun getTheme(): Flow<String> {
        return dataStore.data
            .map { userSettings ->
                userSettings.theme
            }
    }

    suspend fun updateTheme(theme: String) {
        dataStore.updateData { currentSettings ->
            currentSettings.toBuilder()
                .setTheme(theme)
                .build()
        }
    }

    suspend fun updateUserSettings(
        theme: String,
        language: String,
        notificationsEnabled: Boolean
    ) {
        dataStore.updateData { currentSettings ->
            currentSettings.toBuilder()
                .setTheme(theme)
                .setLanguage(language)
                .setNotificationsEnabled(notificationsEnabled)
                .build()
        }
    }
}
```

### DataStore Avantajları
- **Type-Safe**: Compile-time type checking
- **Koroutine Native**: Suspend functions ile
- **Transaction Support**: Atomic updates
- **Flow Integration**: Reaktif veri akışı
- **Modern API**: SharedPreferences'tan daha iyi
- **Encryption Support**: EncryptedSharedPreferences benzeri güvenlik

---

## 5. Veri Migrasyonu ve Şifreleme

### SharedPreferences'tan DataStore'a Geçiş
```kotlin
suspend fun migrateToDataStore(
    context: Context,
    oldPrefs: SharedPreferences
) {
    val dataStore = PreferenceDataStoreFactory.create(
        serializer = PreferencesSerializer,
        produceFile = { context.filesDir.resolve("migrated_prefs.pb") }
    )

    dataStore.edit { newPreferences ->
        oldPrefs.all.forEach { (key, value) ->
            when (value) {
                is String -> newPreferences[stringPreferencesKey(key)] = value
                is Int -> newPreferences[intPreferencesKey(key)] = value
                is Boolean -> newPreferences[booleanPreferencesKey(key)] = value
                is Long -> newPreferences[longPreferencesKey(key)] = value
                is Float -> newPreferences[floatPreferencesKey(key)] = value
            }
        }
    }

    // Eski SharedPreferences'i temizle
    oldPrefs.edit().clear().apply()
}
```

### Veri Şifreleme
```kotlin
// EncryptedFile örneği
class EncryptedFileManager(context: Context) {
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    private val sensitiveFile = EncryptedFile.Builder(
        context,
        File(context.filesDir, "sensitive_data.txt"),
        masterKey,
        EncryptedFile.FileEncryptionScheme.AES256_GCM_HKDF_4KB
    ).build()

    fun writeSensitiveData(data: String) {
        sensitiveFile.openFileOutput().use { outputStream ->
            outputStream.write(data.toByteArray())
        }
    }

    fun readSensitiveData(): String {
        return sensitiveFile.openFileInput().bufferedReader().use {
            it.readText()
        }
    }
}
```

---

## 6. Performans ve En İyi Uygulamalar

### Room Performans Optimizasyonu
```kotlin
@Dao
interface OptimizedUserDao {

    // Batch insert - bulk işlemler için
    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertBatch(users: List<User>)

    // Transaction kullanımı
    @Transaction
    suspend fun replaceUsers(users: List<User>) {
        deleteAll()
        insertBatch(users)
    }

    // Index kullanımı
    @Query("SELECT * FROM users WHERE email = :email")
    suspend fun getUserByEmail(email: String): User?

    // Partial query - sadece ihtiyaç duyulan alanlar
    @Query("SELECT id, username FROM users")
    suspend fun getUserPreview(): List<UserPreview>
}

// Partial data class
data class UserPreview(
    val id: Int,
    val username: String
)
```

### Veri Boyutu Sınırlaması
```kotlin
// SharedPreferences/DataStore için
- Maksimum boyut: ~2MB (cihaza göre değişir)
- Sık güncellenen veriler için uygun değil

// Room için
- Terabyte ölçekli veri depolayabilir
- Kompleks sorgular için optimize edilmiş

// EncryptedSharedPreferences
- Şifreleme overhead'i vardır
- Küçük, hassas veriler için idealdir
```

---

## 7. Kullanım Senaryoları

| Teknoloji | Kullanım Alanı | Veri Boyutu | Örnek |
|-----------|-----------------|------------|--------|
| **SharedPreferences** | Basit ayarlar | < 1KB | Tema, Dil, Kullanıcı ID |
| **DataStore** | Modern ayarlar | < 10KB | Tercihleri, Bayraklar |
| **EncryptedSharedPreferences** | Güvenli veriler | < 1KB | Auth token, API key |
| **Room** | Kompleks veri | > 10KB | Kullanıcı listesi, Gönderiler |
| **SQLite Direct** | Legacy kod | Sınırsız | Eski projeler (önerilmez) |

---

## 8. Dependency Injection örneği (Hilt)

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object DataModule {

    @Provides
    @Singleton
    fun provideAppDatabase(context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "app_database"
        ).build()
    }

    @Provides
    @Singleton
    fun provideUserDao(database: AppDatabase): UserDao {
        return database.userDao()
    }

    @Provides
    @Singleton
    fun provideUserRepository(userDao: UserDao): UserRepository {
        return UserRepository(userDao)
    }

    @Provides
    @Singleton
    fun providePreferencesDataStore(context: Context): PreferencesDataStore {
        return PreferencesDataStore(context)
    }
}

@HiltViewModel
class UserViewModel @Inject constructor(
    private val userRepository: UserRepository,
    private val preferencesDataStore: PreferencesDataStore
) : ViewModel() {

    val allUsers: Flow<List<User>> = userRepository.allUsers
    val userTheme: Flow<String> = preferencesDataStore.getTheme()
}
```

---

## 9. Testing

```kotlin
// Room DAO Testing
@RunWith(AndroidJUnit4::class)
class UserDaoTest {

    private lateinit var database: AppDatabase
    private lateinit var userDao: UserDao

    @Before
    fun setup() {
        database = Room.inMemoryDatabaseBuilder(
            InstrumentationRegistry.getInstrumentation().targetContext,
            AppDatabase::class.java
        ).build()
        userDao = database.userDao()
    }

    @After
    fun teardown() {
        database.close()
    }

    @Test
    fun insertAndRetrieveUser() = runTest {
        val user = User(username = "john", email = "john@example.com")
        val id = userDao.insert(user)
        val retrieved = userDao.getUserById(id.toInt())

        assertThat(retrieved?.username).isEqualTo("john")
    }
}

// DataStore Testing
class PreferencesDataStoreTest {

    @get:Rule
    val tmpFolder = TemporaryFolder()

    @Test
    fun saveAndRetrievePreference() = runTest {
        val dataStore = PreferenceDataStoreFactory.create(
            serializer = PreferencesSerializer,
            produceFile = { tmpFolder.newFile("test_preferences.pb") }
        )

        dataStore.edit { preferences ->
            preferences[stringPreferencesKey("test_key")] = "test_value"
        }

        dataStore.data.test {
            val value = awaitItem()[stringPreferencesKey("test_key")]
            assertThat(value).isEqualTo("test_value")
        }
    }
}
```

---

## Öğrenme Kaynakları

### Official Documentation
- Room Persistence Library: https://developer.android.com/training/data-storage/room
- DataStore: https://developer.android.com/topic/libraries/architecture/datastore
- SharedPreferences: https://developer.android.com/training/data-storage/shared-preferences
- SQLite: https://developer.android.com/training/data-storage/sqlite

### Best Practices
1. **Room'u her zaman tercih et** - modern ve type-safe
2. **DataStore'ı SharedPreferences yerine kullan** - ayarlar ve basit veriler için
3. **EncryptedSharedPreferences** - hassas bilgiler için
4. **Flow ile reaktif tasarım** - UI güncellemelerinde
5. **Migration stratejisi planla** - veritabanı sürümlendirmesi için
6. **Testing yapısını oluştur** - in-memory database'lerle test et
