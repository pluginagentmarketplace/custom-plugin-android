---
description: API integration and networking - Retrofit, OkHttp, REST APIs, JSON processing, network security - HTTP communication for Android
capabilities: ["Retrofit API client", "OkHttp networking", "REST API design", "JSON serialization", "Interceptors", "Error handling", "SSL pinning", "Network monitoring"]
---

# Networking Agent

Master HTTP networking using Retrofit and OkHttp, REST API integration, JSON processing, and network security best practices.

## REST APIs

### HTTP Methods
- GET: Retrieve data
- POST: Create resource
- PUT: Replace resource
- DELETE: Remove resource
- PATCH: Partial update

### Status Codes
- 2xx: Success (200, 201, 204)
- 4xx: Client error (400, 401, 404)
- 5xx: Server error (500, 503)

## Retrofit

### API Interface
```kotlin
interface UserApi {
    @GET("/users")
    suspend fun getUsers(): List<UserDto>
    
    @GET("/users/{id}")
    suspend fun getUser(@Path("id") id: Int): UserDto
    
    @POST("/users")
    suspend fun createUser(@Body user: UserDto): UserDto
    
    @DELETE("/users/{id}")
    suspend fun deleteUser(@Path("id") id: Int)
}
```

### Setup
```kotlin
val retrofit = Retrofit.Builder()
    .baseUrl("https://api.example.com/")
    .addConverterFactory(GsonConverterFactory.create())
    .build()

val api = retrofit.create(UserApi::class.java)
```

### Features
- Type-safe API interfaces
- Automatic serialization/deserialization
- Suspend function support
- Error handling callbacks

## OkHttp

### Interceptors
```kotlin
val loggingInterceptor = HttpLoggingInterceptor().apply {
    level = HttpLoggingInterceptor.Level.BODY
}

val okHttpClient = OkHttpClient.Builder()
    .addInterceptor(loggingInterceptor)
    .connectTimeout(30, TimeUnit.SECONDS)
    .readTimeout(30, TimeUnit.SECONDS)
    .build()
```

### Features
- Connection pooling
- Gzip compression
- Caching support
- Retry policy
- Certificate pinning

## JSON Processing

### GSON Serialization
```kotlin
data class User(
    @SerializedName("user_id")
    val id: Int,
    @SerializedName("full_name")
    val name: String
)

val gson = Gson()
val json = gson.toJson(user)
val user = gson.fromJson(json, User::class.java)
```

### Moshi (Type-safe alternative)
```kotlin
@JsonClass(generateAdapter = true)
data class User(val id: Int, val name: String)
```

## Error Handling

### Response Wrapper
```kotlin
sealed class Result<T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error<T>(val exception: Exception) : Result<T>()
    class Loading<T> : Result<T>()
}
```

### Network Call
```kotlin
val result = try {
    Result.Success(api.getUsers())
} catch (e: Exception) {
    Result.Error(e)
}
```

## SSL Pinning

### Certificate Pinning
```kotlin
val certificatePinner = CertificatePinner.Builder()
    .add("api.example.com", "sha256/AAAA...")
    .build()

OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()
```

## Network Monitoring

### Connectivity Status
```kotlin
val connectivityManager = context.getSystemService(ConnectivityManager::class.java)
val network = connectivityManager.activeNetwork
val capabilities = connectivityManager.getNetworkCapabilities(network)
val isOnline = capabilities?.hasCapability(NET_CAPABILITY_INTERNET) == true
```

## Learning Outcomes
- Design and consume REST APIs
- Configure Retrofit and OkHttp
- Handle network errors gracefully
- Implement SSL pinning
- Monitor network activity

---

**Learning Hours**: 75 hours | **Level**: Intermediate
