# Networking & APIs - Android Development

---
description: |
  Android uygulamalarında HTTP istek/yanıt yönetimi, REST API entegrasyonu, JSON veri işleme ve ağ iletişimi için kapsamlı rehber. Retrofit, OkHttp gibi modern kütüphanelerle verimli API haberleşmesi, hata yönetimi, güvenlik ve performans optimizasyonu.
capabilities:
  - REST API tasarımı ve tüketimi
  - HTTP istek/yanıt yönetimi
  - JSON veri serileştirme/deserileştirme
  - Retrofit ile type-safe API tanımları
  - OkHttp konfigürasyonu ve interceptor'ları
  - Hata yönetimi ve retry stratejileri
  - SSL/TLS ve güvenlik ayarları
  - Ağ bağlantı durumu kontrol etme
  - Veri sıkıştırma ve performans optimizasyonu
  - Mock server'lar ile test etme

---

## 1. REST APIs Temelleri

### 1.1 REST Mimarisi
REST (Representational State Transfer), HTTP protokolü üzerinde kaynakları temsil eden ve standart HTTP metotlarını kullanan mimaridir.

**HTTP Metotları:**
- **GET**: Veri okuma (idempotent)
- **POST**: Yeni kaynak oluşturma
- **PUT**: Kaynağın tamamını güncelleme
- **PATCH**: Kaynağın bölümünü güncelleme
- **DELETE**: Kaynağı silme

**HTTP Durum Kodları:**
```
2xx: Başarı
  - 200 OK
  - 201 Created
  - 204 No Content

3xx: Yönlendirme
  - 301 Moved Permanently
  - 302 Found

4xx: İstemci Hatası
  - 400 Bad Request
  - 401 Unauthorized
  - 403 Forbidden
  - 404 Not Found

5xx: Sunucu Hatası
  - 500 Internal Server Error
  - 502 Bad Gateway
  - 503 Service Unavailable
```

### 1.2 API Design Best Practices

```
Endpoint Design:
GET    /api/v1/users              → Tüm kullanıcıları getir
GET    /api/v1/users/{id}         → Belirli kullanıcı
POST   /api/v1/users              → Yeni kullanıcı oluştur
PUT    /api/v1/users/{id}         → Kullanıcıyı güncelle
DELETE /api/v1/users/{id}         → Kullanıcıyı sil

Query Parameters:
GET /api/v1/users?page=2&limit=10&sort=name
GET /api/v1/users?filter=active&search=john
```

---

## 2. JSON - JavaScript Object Notation

### 2.1 JSON Temel Yapısı

```json
{
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "isActive": true,
    "tags": ["developer", "android"],
    "profile": {
      "bio": "Mobile Developer",
      "location": "Istanbul"
    }
  }
}
```

### 2.2 JSON Veri Tipleri

```json
{
  "string": "value",
  "number": 42,
  "float": 3.14,
  "boolean": true,
  "null": null,
  "array": [1, 2, 3],
  "object": { "key": "value" }
}
```

### 2.3 Android'de JSON İşleme

#### JSONObject ile Manual Parsing:
```kotlin
val jsonString = """{"name": "John", "age": 30}"""
val jsonObject = JSONObject(jsonString)

val name = jsonObject.getString("name")
val age = jsonObject.getInt("age")
```

#### JSONArray İşleme:
```kotlin
val jsonArray = JSONArray("[1, 2, 3, 4, 5]")
for (i in 0 until jsonArray.length()) {
    val value = jsonArray.getInt(i)
    Log.d("JSON", "Value: $value")
}
```

### 2.4 GSON ile Serileştirme/Deserileştirme

```gradle
dependencies {
    implementation 'com.google.code.gson:gson:2.10.1'
}
```

```kotlin
// Veri sınıfları
data class User(
    val id: Int,
    val name: String,
    val email: String,
    val age: Int
)

// JSON'dan nesneye
val gson = Gson()
val json = """{"id": 1, "name": "John", "email": "john@example.com", "age": 30}"""
val user = gson.fromJson(json, User::class.java)

// Nesneden JSON'a
val jsonOutput = gson.toJson(user)
```

### 2.5 Moshi - Type-Safe JSON Processing

```gradle
dependencies {
    implementation 'com.squareup.moshi:moshi-kotlin:1.15.0'
    implementation 'com.squareup.moshi:moshi-adapters:1.15.0'
}
```

```kotlin
val moshi = Moshi.Builder().build()
val userAdapter = moshi.adapter(User::class.java)

val user = userAdapter.fromJson(jsonString)
val json = userAdapter.toJson(user)
```

---

## 3. OkHttp - HTTP İstemci

### 3.1 OkHttp Temelleri

```gradle
dependencies {
    implementation 'com.squareup.okhttp3:okhttp:4.11.0'
    implementation 'com.squareup.okhttp3:logging-interceptor:4.11.0'
}
```

### 3.2 Basit GET İsteği

```kotlin
val client = OkHttpClient()

val request = Request.Builder()
    .url("https://api.example.com/users")
    .get()
    .build()

val response = client.newCall(request).execute()
val body = response.body?.string()
```

### 3.3 POST İsteği with JSON Body

```kotlin
val mediaType = "application/json; charset=utf-8".toMediaType()
val jsonBody = """
{
    "name": "John",
    "email": "john@example.com"
}
""".trimIndent()

val request = Request.Builder()
    .url("https://api.example.com/users")
    .post(RequestBody.create(mediaType, jsonBody))
    .build()

val response = client.newCall(request).execute()
```

### 3.4 Interceptor'lar

#### Logging Interceptor:
```kotlin
val logging = HttpLoggingInterceptor().apply {
    level = HttpLoggingInterceptor.Level.BODY
}

val client = OkHttpClient.Builder()
    .addInterceptor(logging)
    .build()
```

#### Custom Interceptor - Bearer Token Ekleme:
```kotlin
class AuthInterceptor(private val token: String) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()
        val newRequest = originalRequest.newBuilder()
            .header("Authorization", "Bearer $token")
            .build()
        return chain.proceed(newRequest)
    }
}

val client = OkHttpClient.Builder()
    .addInterceptor(AuthInterceptor("your_token"))
    .build()
```

### 3.5 OkHttp Konfigürasyonu

```kotlin
val client = OkHttpClient.Builder()
    // Timeout ayarları
    .connectTimeout(30, TimeUnit.SECONDS)
    .readTimeout(30, TimeUnit.SECONDS)
    .writeTimeout(30, TimeUnit.SECONDS)

    // Retry politikası
    .retryOnConnectionFailure(true)

    // Connection Pool
    .connectionPool(ConnectionPool(5, 5, TimeUnit.MINUTES))

    // SSL/TLS
    .addSecurityInterceptor()

    // Logging
    .addInterceptor(HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    })

    .build()
```

### 3.6 Hata Yönetimi

```kotlin
try {
    val response = client.newCall(request).execute()

    when {
        response.isSuccessful -> {
            val body = response.body?.string()
            Log.d("Success", body)
        }
        response.code == 401 -> {
            // Unauthorized - Token yenile
            refreshToken()
        }
        response.code == 404 -> {
            // Not Found
            Log.e("Error", "Resource not found")
        }
        response.code >= 500 -> {
            // Server Error - Retry
            retryRequest()
        }
        else -> {
            Log.e("Error", "Code: ${response.code}")
        }
    }
} catch (e: SocketTimeoutException) {
    Log.e("Error", "Connection timeout")
} catch (e: IOException) {
    Log.e("Error", "Network error: ${e.message}")
}
```

---

## 4. Retrofit - Type-Safe HTTP İstemci

### 4.1 Retrofit Kurulumu

```gradle
dependencies {
    implementation 'com.squareup.retrofit2:retrofit:2.10.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.10.0'
    implementation 'com.squareup.retrofit2:converter-moshi:2.10.0'
    implementation 'com.squareup.okhttp3:okhttp:4.11.0'
    implementation 'com.squareup.okhttp3:logging-interceptor:4.11.0'
}
```

### 4.2 API Interface Tanımı

```kotlin
// Veri modelleri
data class User(
    @SerializedName("id")
    val id: Int,
    @SerializedName("name")
    val name: String,
    @SerializedName("email")
    val email: String,
    @SerializedName("created_at")
    val createdAt: String
)

data class UserRequest(
    val name: String,
    val email: String
)

data class ApiResponse<T>(
    val success: Boolean,
    val data: T?,
    val message: String
)

// API Interface
interface UserService {

    @GET("users")
    suspend fun getUsers(): Response<List<User>>

    @GET("users/{id}")
    suspend fun getUserById(@Path("id") userId: Int): Response<User>

    @GET("users")
    suspend fun searchUsers(
        @Query("page") page: Int,
        @Query("limit") limit: Int,
        @Query("search") query: String?
    ): Response<List<User>>

    @POST("users")
    suspend fun createUser(@Body user: UserRequest): Response<User>

    @PUT("users/{id}")
    suspend fun updateUser(
        @Path("id") userId: Int,
        @Body user: UserRequest
    ): Response<User>

    @DELETE("users/{id}")
    suspend fun deleteUser(@Path("id") userId: Int): Response<Void>

    // File Upload
    @Multipart
    @POST("users/{id}/avatar")
    suspend fun uploadAvatar(
        @Path("id") userId: Int,
        @Part file: MultipartBody.Part
    ): Response<User>

    // Custom Headers
    @GET("users/{id}")
    suspend fun getUserWithHeaders(
        @Path("id") userId: Int,
        @Header("Authorization") token: String
    ): Response<User>
}
```

### 4.3 Retrofit Builder Konfigürasyonu

```kotlin
object RetrofitClient {
    private const val BASE_URL = "https://api.example.com/"

    private fun getOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            })
            .addInterceptor(AuthInterceptor(AuthManager.getToken()))
            .addNetworkInterceptor(ConnectivityInterceptor())
            .retryOnConnectionFailure(true)
            .build()
    }

    fun <T> createService(serviceClass: Class<T>): T {
        val retrofit = Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(getOkHttpClient())
            .addConverterFactory(GsonConverterFactory.create())
            .addCallAdapterFactory(RxJava3CallAdapterFactory.create())
            .addCallAdapterFactory(CoroutineCallAdapterFactory())
            .build()

        return retrofit.create(serviceClass)
    }
}

// Kullanım
val userService = RetrofitClient.createService(UserService::class.java)
```

### 4.4 Retrofit ile Coroutine Kullanımı

```kotlin
class UserRepository(private val userService: UserService) {

    suspend fun getUsers(): Result<List<User>> = withContext(Dispatchers.IO) {
        try {
            val response = userService.getUsers()
            if (response.isSuccessful) {
                Result.success(response.body() ?: emptyList())
            } else {
                Result.failure(
                    Exception("API Error: ${response.code()} - ${response.message()}")
                )
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getUserById(userId: Int): Result<User> = withContext(Dispatchers.IO) {
        try {
            val response = userService.getUserById(userId)
            if (response.isSuccessful) {
                response.body()?.let {
                    Result.success(it)
                } ?: Result.failure(Exception("Empty response"))
            } else {
                Result.failure(Exception("User not found"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun createUser(name: String, email: String): Result<User> {
        return try {
            val request = UserRequest(name, email)
            val response = userService.createUser(request)
            if (response.isSuccessful) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to create user"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

### 4.5 Error Handling Patterns

```kotlin
sealed class ApiResult<out T> {
    data class Success<T>(val data: T) : ApiResult<T>()
    data class Error(val exception: Exception) : ApiResult<Nothing>()
    object Loading : ApiResult<Nothing>()
}

class SafeApiCall {
    suspend fun <T> execute(
        apiCall: suspend () -> Response<T>
    ): ApiResult<T> {
        return try {
            val response = apiCall()
            when {
                response.isSuccessful -> {
                    response.body()?.let {
                        ApiResult.Success(it)
                    } ?: ApiResult.Error(Exception("Empty response"))
                }
                response.code() == 401 -> {
                    ApiResult.Error(Exception("Unauthorized"))
                }
                response.code() == 404 -> {
                    ApiResult.Error(Exception("Not found"))
                }
                response.code() >= 500 -> {
                    ApiResult.Error(Exception("Server error"))
                }
                else -> {
                    ApiResult.Error(Exception("Unknown error: ${response.code()}"))
                }
            }
        } catch (e: SocketTimeoutException) {
            ApiResult.Error(Exception("Connection timeout"))
        } catch (e: IOException) {
            ApiResult.Error(Exception("Network error"))
        } catch (e: Exception) {
            ApiResult.Error(e)
        }
    }
}
```

### 4.6 Retrofit Call Adapter'lar

```kotlin
// Flow ile reactive response
interface UserService {
    @GET("users")
    fun getUsersFlow(): Flow<List<User>>
}

// LiveData ile
interface UserService {
    @GET("users")
    fun getUsersLiveData(): LiveData<List<User>>
}

// RxJava ile
interface UserService {
    @GET("users")
    fun getUsersSingle(): Single<List<User>>

    @GET("users")
    fun getUsersObservable(): Observable<List<User>>
}
```

---

## 5. Ağ Bağlantı Yönetimi

### 5.1 Bağlantı Durumu Kontrol Etme

```kotlin
class ConnectivityManager(private val context: Context) {

    fun isNetworkConnected(): Boolean {
        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as android.net.ConnectivityManager
        val network = connectivityManager.activeNetwork ?: return false
        val capabilities = connectivityManager.getNetworkCapabilities(network) ?: return false

        return when {
            capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) -> true
            capabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) -> true
            capabilities.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET) -> true
            else -> false
        }
    }

    fun isWifiConnected(): Boolean {
        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as android.net.ConnectivityManager
        val network = connectivityManager.activeNetwork ?: return false
        val capabilities = connectivityManager.getNetworkCapabilities(network) ?: return false
        return capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)
    }
}
```

### 5.2 Network Callback ile Monitoring

```kotlin
class NetworkMonitor(private val context: Context) {

    private val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as android.net.ConnectivityManager
    private var networkCallback: ConnectivityManager.NetworkCallback? = null

    fun startMonitoring(callback: (Boolean) -> Unit) {
        networkCallback = object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: Network) {
                callback(true)
            }

            override fun onLost(network: Network) {
                callback(false)
            }
        }

        val request = NetworkRequest.Builder()
            .addCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
            .build()

        connectivityManager.registerNetworkCallback(request, networkCallback!!)
    }

    fun stopMonitoring() {
        networkCallback?.let {
            connectivityManager.unregisterNetworkCallback(it)
        }
    }
}
```

### 5.3 Connectivity Interceptor

```kotlin
class ConnectivityInterceptor(private val context: Context) : Interceptor {

    override fun intercept(chain: Interceptor.Chain): Response {
        if (!isNetworkConnected()) {
            throw NoInternetException("No internet connection")
        }

        return try {
            chain.proceed(chain.request())
        } catch (e: SocketTimeoutException) {
            throw NoInternetException("Connection timeout", e)
        }
    }

    private fun isNetworkConnected(): Boolean {
        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as android.net.ConnectivityManager
        val network = connectivityManager.activeNetwork ?: return false
        val capabilities = connectivityManager.getNetworkCapabilities(network) ?: return false

        return capabilities.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
    }
}

class NoInternetException(message: String, cause: Throwable? = null) : Exception(message, cause)
```

---

## 6. Güvenlik

### 6.1 SSL/TLS Konfigürasyonu

```kotlin
class SSLConfig {

    fun getSSLSocketFactory(): SSLSocketFactory {
        val trustAllCerts = arrayOf<TrustManager>(object : X509TrustManager {
            override fun getAcceptedIssuers(): Array<X509Certificate>? = null
            override fun checkClientTrusted(certs: Array<X509Certificate>, authType: String) {}
            override fun checkServerTrusted(certs: Array<X509Certificate>, authType: String) {}
        })

        val sslContext = SSLContext.getInstance("SSL")
        sslContext.init(null, trustAllCerts, java.security.SecureRandom())

        return sslContext.socketFactory
    }

    fun getUnsafeOkHttpClient(): OkHttpClient {
        val trustAllCerts = arrayOf<TrustManager>(object : X509TrustManager {
            override fun getAcceptedIssuers(): Array<X509Certificate>? = null
            override fun checkClientTrusted(certs: Array<X509Certificate>, authType: String) {}
            override fun checkServerTrusted(certs: Array<X509Certificate>, authType: String) {}
        })

        val sslContext = SSLContext.getInstance("SSL")
        sslContext.init(null, trustAllCerts, java.security.SecureRandom())

        return OkHttpClient.Builder()
            .sslSocketFactory(sslContext.socketFactory)
            .hostnameVerifier { _, _ -> true }
            .build()
    }
}
```

### 6.2 Token Yönetimi

```kotlin
class TokenManager(private val context: Context) {

    private val encryptedSharedPreferences = EncryptedSharedPreferences.create(
        context,
        "token_storage",
        MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build(),
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )

    fun saveToken(token: String) {
        encryptedSharedPreferences.edit().putString("access_token", token).apply()
    }

    fun getToken(): String? {
        return encryptedSharedPreferences.getString("access_token", null)
    }

    fun clearToken() {
        encryptedSharedPreferences.edit().remove("access_token").apply()
    }

    fun isTokenExpired(token: String): Boolean {
        // JWT decode ve expiration check
        return false
    }
}
```

### 6.3 Bearer Token Interceptor

```kotlin
class BearerTokenInterceptor(private val tokenManager: TokenManager) : Interceptor {

    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()
        val token = tokenManager.getToken()

        val newRequest = originalRequest.newBuilder()
            .header("Authorization", "Bearer $token")
            .header("Content-Type", "application/json")
            .build()

        var response = chain.proceed(newRequest)

        // 401 durumunda token refresh
        if (response.code == 401) {
            response.close()

            if (tokenManager.refreshToken()) {
                val refreshedToken = tokenManager.getToken()
                val retryRequest = originalRequest.newBuilder()
                    .header("Authorization", "Bearer $refreshedToken")
                    .build()

                response = chain.proceed(retryRequest)
            }
        }

        return response
    }
}
```

---

## 7. İleri Konular

### 7.1 Pagination

```kotlin
interface UserService {
    @GET("users")
    suspend fun getUsers(
        @Query("page") page: Int,
        @Query("per_page") perPage: Int = 20
    ): Response<PaginatedResponse<User>>
}

data class PaginatedResponse<T>(
    val data: List<T>,
    val pagination: Pagination
)

data class Pagination(
    val total: Int,
    val page: Int,
    val perPage: Int,
    val lastPage: Int,
    val hasMorePages: Boolean
)
```

### 7.2 File Upload/Download

```kotlin
interface FileService {
    @Multipart
    @POST("upload")
    suspend fun uploadFile(
        @Part("description") description: RequestBody,
        @Part file: MultipartBody.Part
    ): Response<FileResponse>

    @GET("download/{fileId}")
    suspend fun downloadFile(
        @Path("fileId") fileId: String
    ): Response<ResponseBody>
}

class FileDownloadHelper {
    suspend fun downloadFile(
        service: FileService,
        fileId: String,
        outputPath: String
    ) {
        try {
            val response = service.downloadFile(fileId)

            if (response.isSuccessful) {
                response.body()?.let { body ->
                    val file = File(outputPath)
                    val fos = FileOutputStream(file)
                    fos.write(body.bytes())
                    fos.close()
                }
            }
        } catch (e: Exception) {
            Log.e("Download", "Error: ${e.message}")
        }
    }
}
```

### 7.3 Request/Response Interceptors

```kotlin
class RequestInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request()

        Log.d("RequestInfo", """
            URL: ${request.url}
            Method: ${request.method}
            Headers: ${request.headers}
        """.trimIndent())

        val startTime = System.currentTimeMillis()
        val response = chain.proceed(request)
        val duration = System.currentTimeMillis() - startTime

        Log.d("ResponseInfo", """
            Status: ${response.code}
            Duration: ${duration}ms
        """.trimIndent())

        return response
    }
}

class ResponseInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val response = chain.proceed(chain.request())

        if (!response.isSuccessful && response.code >= 400) {
            val body = response.peekBody(Long.MAX_VALUE).string()
            Log.e("API Error", "Error Body: $body")
        }

        return response
    }
}
```

---

## 8. Testing

### 8.1 MockWebServer ile API Testing

```gradle
dependencies {
    testImplementation 'com.squareup.okhttp3:mockwebserver:4.11.0'
}
```

```kotlin
@RunWith(RobolectricTestRunner::class)
class UserServiceTest {

    private lateinit var mockWebServer: MockWebServer
    private lateinit var userService: UserService

    @Before
    fun setup() {
        mockWebServer = MockWebServer()
        mockWebServer.start()

        val retrofit = Retrofit.Builder()
            .baseUrl(mockWebServer.url("/"))
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        userService = retrofit.create(UserService::class.java)
    }

    @After
    fun teardown() {
        mockWebServer.shutdown()
    }

    @Test
    fun testGetUsers() = runTest {
        // Mock response hazırlama
        val mockResponse = MockResponse()
            .setBody("""[{"id": 1, "name": "John", "email": "john@example.com"}]""")
            .setResponseCode(200)

        mockWebServer.enqueue(mockResponse)

        // API çağırma
        val response = userService.getUsers()

        // Assertions
        assertTrue(response.isSuccessful)
        assertEquals(1, response.body()?.size)
        assertEquals("John", response.body()?.get(0)?.name)
    }

    @Test
    fun testGetUserById() = runTest {
        mockWebServer.enqueue(
            MockResponse()
                .setBody("""{"id": 1, "name": "John", "email": "john@example.com"}""")
                .setResponseCode(200)
        )

        val response = userService.getUserById(1)

        assertTrue(response.isSuccessful)
        assertEquals("John", response.body()?.name)
    }

    @Test
    fun testCreateUser() = runTest {
        mockWebServer.enqueue(
            MockResponse()
                .setBody("""{"id": 2, "name": "Jane", "email": "jane@example.com"}""")
                .setResponseCode(201)
        )

        val request = UserRequest("Jane", "jane@example.com")
        val response = userService.createUser(request)

        assertTrue(response.isSuccessful)
        assertEquals(201, response.code())
        assertEquals("Jane", response.body()?.name)
    }

    @Test
    fun testServerError() = runTest {
        mockWebServer.enqueue(
            MockResponse().setResponseCode(500)
        )

        val response = userService.getUsers()

        assertFalse(response.isSuccessful)
        assertEquals(500, response.code())
    }
}
```

### 8.2 Repository Testing

```kotlin
@RunWith(RobolectricTestRunner::class)
class UserRepositoryTest {

    private lateinit var userRepository: UserRepository
    private val mockUserService = mockk<UserService>()

    @Before
    fun setup() {
        userRepository = UserRepository(mockUserService)
    }

    @Test
    fun testGetUsersSuccess() = runTest {
        val mockUsers = listOf(
            User(1, "John", "john@example.com", "2023-01-01"),
            User(2, "Jane", "jane@example.com", "2023-01-02")
        )

        coEvery { mockUserService.getUsers() } returns Response.success(mockUsers)

        val result = userRepository.getUsers()

        assertTrue(result.isSuccess)
        assertEquals(2, result.getOrNull()?.size)
    }

    @Test
    fun testGetUsersFailure() = runTest {
        coEvery { mockUserService.getUsers() } throws Exception("Network error")

        val result = userRepository.getUsers()

        assertTrue(result.isFailure)
    }
}
```

---

## 9. Practical Examples

### 9.1 Complete API Integration Example

```kotlin
// Veri Katmanı
interface UserApi {
    @GET("users")
    suspend fun getUsers(): Response<List<User>>

    @GET("users/{id}")
    suspend fun getUserById(@Path("id") id: Int): Response<User>

    @POST("users")
    suspend fun createUser(@Body user: UserRequest): Response<User>
}

// Repository
class UserRepository(private val userApi: UserApi) {

    suspend fun getUsers(): Result<List<User>> = withContext(Dispatchers.IO) {
        try {
            val response = userApi.getUsers()
            if (response.isSuccessful) {
                Result.success(response.body() ?: emptyList())
            } else {
                Result.failure(Exception("API Error"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

// ViewModel
class UserViewModel(private val repository: UserRepository) : ViewModel() {

    private val _users = MutableLiveData<List<User>>()
    val users: LiveData<List<User>> = _users

    private val _loading = MutableLiveData<Boolean>()
    val loading: LiveData<Boolean> = _loading

    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> = _error

    fun getUsers() {
        _loading.value = true
        viewModelScope.launch {
            repository.getUsers().fold(
                onSuccess = { users ->
                    _users.value = users
                    _loading.value = false
                },
                onFailure = { exception ->
                    _error.value = exception.message
                    _loading.value = false
                }
            )
        }
    }
}

// UI Layer (Activity/Fragment)
class UserListActivity : AppCompatActivity() {

    private lateinit var viewModel: UserViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        viewModel.users.observe(this) { users ->
            updateUI(users)
        }

        viewModel.loading.observe(this) { isLoading ->
            // Show/hide progress bar
        }

        viewModel.error.observe(this) { errorMessage ->
            if (errorMessage != null) {
                showError(errorMessage)
            }
        }

        viewModel.getUsers()
    }
}
```

---

## Kaynaklar

- [Retrofit Documentation](https://square.github.io/retrofit/)
- [OkHttp Documentation](https://square.github.io/okhttp/)
- [Android Networking Best Practices](https://developer.android.com/training/connect-devices-wirelessly/network-ops)
- [JSON in Android](https://developer.android.com/guide/topics/data/data-storage)
- [HTTP Protocol Specifications](https://tools.ietf.org/html/rfc7231)
