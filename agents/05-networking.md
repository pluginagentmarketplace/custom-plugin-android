---
description: API Integration & Networking - Retrofit, OkHttp, REST APIs, JSON, interceptors, SSL pinning (75 hours)
capabilities: ["Retrofit API client", "OkHttp networking", "REST API design", "JSON serialization", "Interceptors", "Error handling", "Retry logic", "SSL pinning", "Network monitoring", "Authentication", "Request/Response handling"]
prerequisites: ["Fundamentals", "Platform", "Data Management"]
keywords: ["retrofit", "okhttp", "api", "rest", "json", "network", "ssl", "interceptor", "authentication", "error handling"]
---

# Networking Agent: HTTP & REST API Integration

Master modern HTTP networking with Retrofit and OkHttp. Learn REST API design, JSON processing, security, error handling, and network resilience. Build robust communication between app and backend.

**Prerequisite**: Fundamentals, Platform & Data Management agents
**Duration**: 75 hours | **Level**: Intermediate
**Topics**: 8 major areas | **Code Examples**: 45+ real-world patterns

---

## 1. REST API FUNDAMENTALS

REST (Representational State Transfer) defines how to structure HTTP requests to a server.

### 1.1 HTTP Methods & Status Codes

**HTTP Methods:**
- **GET**: Retrieve resource (idempotent, cacheable)
- **POST**: Create new resource
- **PUT**: Replace entire resource
- **PATCH**: Partial resource update
- **DELETE**: Remove resource
- **HEAD**: Like GET but without response body

**HTTP Status Codes:**
```
2xx Success:
  200 OK: Request succeeded
  201 Created: Resource created
  204 No Content: Success with no response body

4xx Client Error:
  400 Bad Request: Invalid request
  401 Unauthorized: Authentication required
  403 Forbidden: No permission
  404 Not Found: Resource doesn't exist
  429 Too Many Requests: Rate limit exceeded

5xx Server Error:
  500 Internal Server Error
  503 Service Unavailable
```

### 1.2 RESTful Design Best Practices

```
Endpoint Design:
/users              → GET all users
/users/123          → GET user 123
/users              → POST create user
/users/123          → PUT update user 123
/users/123          → DELETE remove user 123
/users/123/posts    → GET user 123's posts
/posts?page=1&limit=10  → Paginated results

Request Format:
GET /api/v1/users/123 HTTP/1.1
Host: api.example.com
Authorization: Bearer token123
Content-Type: application/json

Response Format:
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 123,
  "name": "John",
  "email": "john@example.com"
}
```

---

## 2. RETROFIT: TYPE-SAFE HTTP CLIENT

Retrofit is the modern standard for API calls in Android, providing type safety and coroutine support.

### 2.1 API Interface Definition

```kotlin
// Data models
data class UserDto(
    @SerializedName("user_id")
    val id: Int,
    @SerializedName("full_name")
    val name: String,
    @SerializedName("email_address")
    val email: String,
    val createdAt: Long = System.currentTimeMillis()
)

data class CreateUserRequest(
    val name: String,
    val email: String,
    val password: String
)

data class ApiResponse<T>(
    val success: Boolean,
    val data: T?,
    val error: String?
)

// API interface
interface UserApi {
    // Simple GET
    @GET("/users")
    suspend fun getUsers(): List<UserDto>

    // GET with path parameter
    @GET("/users/{userId}")
    suspend fun getUser(@Path("userId") userId: Int): UserDto

    // GET with query parameters
    @GET("/users")
    suspend fun getUsersPaged(
        @Query("page") page: Int,
        @Query("limit") limit: Int = 20
    ): List<UserDto>

    // POST with request body
    @POST("/users")
    suspend fun createUser(@Body request: CreateUserRequest): ApiResponse<UserDto>

    // PUT to update
    @PUT("/users/{userId}")
    suspend fun updateUser(
        @Path("userId") userId: Int,
        @Body request: CreateUserRequest
    ): UserDto

    // PATCH for partial update
    @PATCH("/users/{userId}")
    suspend fun partialUpdate(
        @Path("userId") userId: Int,
        @Body updates: Map<String, Any>
    ): UserDto

    // DELETE
    @DELETE("/users/{userId}")
    suspend fun deleteUser(@Path("userId") userId: Int)

    // Multi-part file upload
    @Multipart
    @POST("/users/{userId}/avatar")
    suspend fun uploadAvatar(
        @Path("userId") userId: Int,
        @Part("description") description: RequestBody,
        @Part file: MultipartBody.Part
    ): ApiResponse<UserDto>

    // Complex response wrapper
    @GET("/posts/{postId}")
    suspend fun getPost(@Path("postId") postId: Int): Response<UserDto>
}
```

### 2.2 Retrofit Configuration & Dependency Injection

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .addCallAdapterFactory(HttpStatusCodeCallAdapterFactory())
            .build()
    }

    @Provides
    fun provideUserApi(retrofit: Retrofit): UserApi {
        return retrofit.create(UserApi::class.java)
    }
}

// Use in repository
@HiltViewModel
class UserViewModel @Inject constructor(
    private val userApi: UserApi
) : ViewModel() {
    val users = MutableLiveData<List<UserDto>>()

    fun loadUsers() {
        viewModelScope.launch {
            try {
                users.value = userApi.getUsers()
            } catch (e: Exception) {
                // Handle error
            }
        }
    }
}
```

---

## 3. OKHTTP: ADVANCED HTTP CONFIGURATION

OkHttp provides low-level control over HTTP requests with interceptors, caching, and connection management.

### 3.1 Complete OkHttpClient Setup

```kotlin
val okHttpClient = OkHttpClient.Builder()
    // Timeouts
    .connectTimeout(30, TimeUnit.SECONDS)
    .readTimeout(30, TimeUnit.SECONDS)
    .writeTimeout(30, TimeUnit.SECONDS)
    .callTimeout(40, TimeUnit.SECONDS)

    // Interceptors (execute in order)
    .addInterceptor(loggingInterceptor)  // Application interceptor
    .addNetworkInterceptor(networkLoggingInterceptor)  // Network interceptor
    .addInterceptor(authInterceptor)

    // Caching
    .cache(Cache(cacheDir, 10 * 1024 * 1024))  // 10MB cache

    // Retry
    .retryOnConnectionFailure(true)

    // Connection pool
    .connectionPool(ConnectionPool(maxIdleConnections = 5, keepAliveDuration = 5, TimeUnit.MINUTES))

    // SSL/TLS
    .certificatePinner(certificatePinner)
    .sslSocketFactory(customSSLSocketFactory, trustManager)

    // Proxy (optional)
    .proxy(Proxy.NO_PROXY)

    .build()
```

### 3.2 Interceptors: Request/Response Manipulation

```kotlin
// Logging Interceptor
val loggingInterceptor = HttpLoggingInterceptor { message ->
    Log.d("OkHttp", message)
}.apply {
    level = HttpLoggingInterceptor.Level.BODY  // NONE, BASIC, HEADERS, BODY
}

// Authentication Interceptor (Add auth to every request)
class AuthInterceptor @Inject constructor(
    private val tokenManager: TokenManager
) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val original = chain.request()

        // Add auth header to request
        val request = original.newBuilder()
            .header("Authorization", "Bearer ${tokenManager.getToken()}")
            .header("X-API-Version", "1.0")
            .build()

        return chain.proceed(request)
    }
}

// Retry Interceptor with exponential backoff
class RetryInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        var request = chain.request()
        var response: Response? = null
        var exception: Exception? = null

        for (i in 0..2) {  // Retry up to 3 times
            try {
                response = chain.proceed(request)
                if (response.isSuccessful || !response.code.isRetryable()) {
                    return response
                }
            } catch (e: Exception) {
                exception = e
            }

            // Exponential backoff: 1s, 2s, 4s
            val delayMs = (1000 * Math.pow(2.0, i.toDouble())).toLong()
            Thread.sleep(delayMs)
        }

        return response ?: throw exception!!
    }

    private fun Int.isRetryable() = this in listOf(408, 429, 500, 502, 503, 504)
}

// Request/Response Modification Interceptor
class HeaderInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request().newBuilder()
            .header("User-Agent", "MyApp/1.0")
            .header("Accept", "application/json")
            .removeHeader("X-Unwanted")
            .build()

        return chain.proceed(request)
    }
}
```

### 3.3 Caching Strategy

```kotlin
val cacheSize = 10L * 1024L * 1024L  // 10MB
val cache = Cache(cacheFile, cacheSize)

val okHttpClient = OkHttpClient.Builder()
    .cache(cache)
    .addNetworkInterceptor { chain ->
        val response = chain.proceed(chain.request())
        val cacheControl = CacheControl.Builder()
            .maxAge(5, TimeUnit.MINUTES)
            .build()

        response.newBuilder()
            .header("Cache-Control", cacheControl.toString())
            .build()
    }
    .build()
```

---

## 4. JSON SERIALIZATION

Convert between JSON and Kotlin objects automatically.

### 4.1 GSON (Google's JSON library)

```kotlin
// Field mapping with annotations
data class User(
    @SerializedName("user_id")
    val id: Int,
    @SerializedName("full_name")
    val name: String,
    @SerializedName("email_address")
    val email: String,
    @Expose  // Only this field is serialized
    val age: Int
)

// Custom serialization
class CustomDateSerializer : JsonSerializer<Date>, JsonDeserializer<Date> {
    private val format = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'")

    override fun serialize(src: Date, typeOfSrc: Type, context: JsonSerializationContext)
        = JsonPrimitive(format.format(src))

    override fun deserialize(json: JsonElement, typeOfT: Type, context: JsonDeserializationContext)
        = format.parse(json.asString)
}

val gson = GsonBuilder()
    .registerTypeAdapter(Date::class.java, CustomDateSerializer())
    .serializeNulls()
    .setPrettyPrinting()
    .create()
```

### 4.2 Moshi (Modern, type-safe)

```kotlin
@JsonClass(generateAdapter = true)
data class User(
    @Json(name = "user_id")
    val id: Int,
    @Json(name = "full_name")
    val name: String,
    val email: String
)

val moshi = Moshi.Builder()
    .addLast(KotlinJsonAdapterFactory())
    .build()

val retrofit = Retrofit.Builder()
    .baseUrl("https://api.example.com/")
    .addConverterFactory(MoshiConverterFactory.create(moshi))
    .build()
```

---

## 5. ERROR HANDLING & RESULT WRAPPER

Graceful error handling ensures app stability during network failures.

```kotlin
// Sealed class for type-safe result handling
sealed class Result<T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error<T>(val exception: NetworkException) : Result<T>()
    class Loading<T> : Result<T>()
}

sealed class NetworkException(message: String) : Exception(message) {
    data class ServerError(val code: Int, override val message: String) : NetworkException(message)
    data class ClientError(val code: Int, override val message: String) : NetworkException(message)
    data class NetworkError(override val message: String) : NetworkException(message)
    data class TimeoutError(override val message: String) : NetworkException(message)
    data class ParseError(override val message: String) : NetworkException(message)
}

// Safe API call wrapper
suspend inline fun <T> safeApiCall(
    crossinline apiCall: suspend () -> T
): Result<T> = withContext(Dispatchers.IO) {
    return@withContext try {
        Result.Success(apiCall())
    } catch (e: HttpException) {
        val errorBody = e.response()?.errorBody()?.string()
        when (e.code()) {
            in 400..499 -> Result.Error(
                NetworkException.ClientError(e.code(), errorBody ?: "Client error")
            )
            in 500..599 -> Result.Error(
                NetworkException.ServerError(e.code(), errorBody ?: "Server error")
            )
            else -> Result.Error(NetworkException.NetworkError("Unknown error"))
        }
    } catch (e: SocketTimeoutException) {
        Result.Error(NetworkException.TimeoutError("Request timeout"))
    } catch (e: IOException) {
        Result.Error(NetworkException.NetworkError("Network error: ${e.message}"))
    } catch (e: JsonSyntaxException) {
        Result.Error(NetworkException.ParseError("Failed to parse response"))
    } catch (e: Exception) {
        Result.Error(NetworkException.NetworkError(e.message ?: "Unknown error"))
    }
}

// Usage in repository
class UserRepository @Inject constructor(private val userApi: UserApi) {
    suspend fun getUsers(): Result<List<User>> = safeApiCall {
        userApi.getUsers()
    }
}

// Collect result in ViewModel
viewModelScope.launch {
    when (val result = userRepository.getUsers()) {
        is Result.Success -> users.value = result.data
        is Result.Error -> error.value = result.exception.message
        is Result.Loading -> loading.value = true
    }
}
```

---

## 6. AUTHENTICATION & TOKEN MANAGEMENT

```kotlin
interface TokenManager {
    fun getToken(): String?
    suspend fun refreshToken(): String?
    fun clearToken()
}

class TokenManagerImpl @Inject constructor(
    private val dataStore: DataStore<Preferences>
) : TokenManager {
    companion object {
        val ACCESS_TOKEN = stringPreferencesKey("access_token")
        val REFRESH_TOKEN = stringPreferencesKey("refresh_token")
    }

    override fun getToken(): String? {
        return runBlocking {
            dataStore.data.map { it[ACCESS_TOKEN] }.firstOrNull()
        }
    }

    override suspend fun refreshToken(): String? {
        // Call refresh API
        val newToken = // API call result
        dataStore.edit { it[ACCESS_TOKEN] = newToken }
        return newToken
    }

    override fun clearToken() {
        runBlocking {
            dataStore.edit {
                it.remove(ACCESS_TOKEN)
                it.remove(REFRESH_TOKEN)
            }
        }
    }
}

// Token refresh interceptor
class TokenRefreshInterceptor(
    private val tokenManager: TokenManager,
    private val userApi: UserApi
) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        var response = chain.proceed(chain.request())

        // If 401, try to refresh token
        if (response.code == 401) {
            synchronized(this) {
                val newToken = runBlocking { tokenManager.refreshToken() }
                if (newToken != null) {
                    val newRequest = chain.request().newBuilder()
                        .header("Authorization", "Bearer $newToken")
                        .build()
                    response.close()
                    response = chain.proceed(newRequest)
                }
            }
        }
        return response
    }
}
```

---

## 7. SSL/TLS & CERTIFICATE PINNING

Enhance security by pinning specific certificates.

```kotlin
// Certificate pinning (pin multiple certs for safety)
val certificatePinner = CertificatePinner.Builder()
    .add(
        "api.example.com",
        "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
        "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB="
    )
    .add(
        "backup.example.com",
        "sha256/CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC="
    )
    .build()

val okHttpClient = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()

// Get certificate hash:
// openssl s_client -connect api.example.com:443 < /dev/null | openssl x509 -noout -pubkey | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | openssl enc -base64
```

---

## 8. NETWORK CONNECTIVITY MONITORING

```kotlin
// Check if device has internet
class ConnectivityManager @Inject constructor(
    private val context: Context
) {
    fun isNetworkAvailable(): Boolean {
        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE)
                as android.net.ConnectivityManager
        val network = connectivityManager.activeNetwork ?: return false
        val capabilities = connectivityManager.getNetworkCapabilities(network) ?: return false
        return capabilities.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
    }

    fun observeNetworkStatus(): Flow<Boolean> = callbackFlow {
        val callback = object : NetworkCallback() {
            override fun onAvailable(network: Network) {
                trySend(true)
            }
            override fun onLost(network: Network) {
                trySend(false)
            }
        }

        val connectivityManager = context.getSystemService(android.net.ConnectivityManager::class.java)
        connectivityManager.registerDefaultNetworkCallback(callback)

        awaitClose {
            connectivityManager.unregisterNetworkCallback(callback)
        }
    }
}

// Use in ViewModel
@HiltViewModel
class UserViewModel @Inject constructor(
    private val connectivityManager: ConnectivityManager
) : ViewModel() {
    val isOnline = connectivityManager.observeNetworkStatus()
        .stateIn(viewModelScope, SharingStarted.Lazily, true)
}
```

---

## 9. BEST PRACTICES

✅ **API Design**
- Use meaningful endpoint paths (/api/v1/users not /getUsers)
- Version your API (/api/v1, /api/v2)
- Return consistent response format
- Use appropriate HTTP methods

✅ **Error Handling**
- Always handle network errors gracefully
- Implement retry logic for transient failures
- Provide user-friendly error messages
- Log errors for debugging

✅ **Security**
- Always use HTTPS
- Implement certificate pinning for sensitive APIs
- Never hardcode tokens in code
- Validate SSL certificates

✅ **Performance**
- Implement request/response caching
- Use connection pooling
- Compress large payloads with Gzip
- Paginate large datasets

✅ **Monitoring**
- Log all API calls in debug builds
- Monitor response times
- Track error rates
- Use analytics for API usage

---

## 10. LEARNING PATH: 5 WEEKS (75 HOURS)

**Week 1 (12h): REST API Fundamentals**
- HTTP methods and status codes
- RESTful design principles
- Request/response structure
- API documentation (Swagger/OpenAPI)

**Week 2 (15h): Retrofit Essentials**
- API interface creation
- Retrofit configuration
- Basic CRUD operations
- Type-safe API calls

**Week 3 (15h): OkHttp & Advanced Features**
- Interceptors (logging, auth, retry)
- Timeouts and connection management
- Caching strategies
- Connection pooling

**Week 4 (17h): Security & Error Handling**
- SSL/TLS and certificate pinning
- Authentication and token management
- Comprehensive error handling
- Network monitoring

**Week 5 (16h): Advanced Topics**
- File uploads (multipart)
- Complex response handling
- Performance optimization
- Testing API calls

---

**Mastery Checkpoint**:
- Can design and implement REST APIs
- Configure Retrofit and OkHttp comprehensively
- Handle all network error scenarios
- Implement secure authentication
- Monitor and optimize network calls

---

**Learning Hours**: 75 hours | **Level**: Intermediate
**Next Step**: Architecture agent (MVVM, Clean Architecture)
