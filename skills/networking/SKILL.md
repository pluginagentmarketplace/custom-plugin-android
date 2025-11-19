---
name: api-integration
description: Retrofit, OkHttp, REST APIs, JSON serialization, network security. Use when making HTTP requests and integrating APIs.
---

# API Integration Skill

## Quick Start

### Retrofit Setup
```kotlin
interface UserApi {
    @GET("/users/{id}")
    suspend fun getUser(@Path("id") id: Int): UserDto
    
    @POST("/users")
    suspend fun createUser(@Body user: UserDto): UserDto
}

val retrofit = Retrofit.Builder()
    .baseUrl("https://api.example.com/")
    .addConverterFactory(GsonConverterFactory.create())
    .build()

val api = retrofit.create(UserApi::class.java)
```

### OkHttp Configuration
```kotlin
val client = OkHttpClient.Builder()
    .addInterceptor(HttpLoggingInterceptor())
    .connectTimeout(30, TimeUnit.SECONDS)
    .certificatePinner(CertificatePinner.Builder()
        .add("api.example.com", "sha256/...").build())
    .build()
```

### Error Handling
```kotlin
sealed class Result<T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error<T>(val exception: Exception) : Result<T>()
}
```

## Key Concepts

### HTTP Methods
- GET: Fetch data
- POST: Create resource
- PUT/PATCH: Update
- DELETE: Remove

### Retrofit Features
- Type-safe interfaces
- Automatic serialization
- Suspend function support
- Error callbacks

### Network Security
- HTTPS/TLS enforcement
- SSL pinning
- Certificate validation
- Secure token storage

## Best Practices

✅ Use HTTPS always
✅ Implement SSL pinning
✅ Handle errors gracefully
✅ Optimize request/response size
✅ Cache when possible

## Resources

- [Retrofit Guide](https://square.github.io/retrofit/)
- [OkHttp Documentation](https://square.github.io/okhttp/)
