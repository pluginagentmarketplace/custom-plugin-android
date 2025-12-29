# Retrofit & OkHttp Complete Guide

Modern HTTP client stack for Android.

## Retrofit Setup

### API Interface
```kotlin
interface UserApi {
    @GET("users")
    suspend fun getUsers(): List<UserDto>

    @GET("users/{id}")
    suspend fun getUser(@Path("id") id: Int): UserDto

    @POST("users")
    suspend fun createUser(@Body user: CreateUserRequest): UserDto

    @PUT("users/{id}")
    suspend fun updateUser(
        @Path("id") id: Int,
        @Body user: UpdateUserRequest
    ): UserDto

    @DELETE("users/{id}")
    suspend fun deleteUser(@Path("id") id: Int)

    @GET("users")
    suspend fun searchUsers(
        @Query("q") query: String,
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20
    ): PaginatedResponse<UserDto>

    @Multipart
    @POST("users/{id}/avatar")
    suspend fun uploadAvatar(
        @Path("id") id: Int,
        @Part image: MultipartBody.Part
    ): AvatarResponse

    @Headers("Cache-Control: max-age=3600")
    @GET("config")
    suspend fun getConfig(): ConfigDto
}
```

### Retrofit Builder
```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    fun provideOkHttpClient(
        authInterceptor: AuthInterceptor,
        @ApplicationContext context: Context
    ): OkHttpClient {
        return OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .addInterceptor(authInterceptor)
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = if (BuildConfig.DEBUG)
                    HttpLoggingInterceptor.Level.BODY
                else
                    HttpLoggingInterceptor.Level.NONE
            })
            .cache(Cache(context.cacheDir, 10 * 1024 * 1024))
            .build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
        return Retrofit.Builder()
            .baseUrl(BuildConfig.API_BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    @Provides
    @Singleton
    fun provideUserApi(retrofit: Retrofit): UserApi {
        return retrofit.create(UserApi::class.java)
    }
}
```

## Interceptors

### Auth Interceptor
```kotlin
class AuthInterceptor @Inject constructor(
    private val tokenManager: TokenManager
) : Interceptor {

    override fun intercept(chain: Interceptor.Chain): Response {
        val original = chain.request()

        val token = tokenManager.getAccessToken()
        val request = if (token != null) {
            original.newBuilder()
                .header("Authorization", "Bearer $token")
                .build()
        } else {
            original
        }

        val response = chain.proceed(request)

        // Handle token refresh
        if (response.code == 401) {
            synchronized(this) {
                val newToken = tokenManager.refreshToken()
                if (newToken != null) {
                    response.close()
                    val newRequest = original.newBuilder()
                        .header("Authorization", "Bearer $newToken")
                        .build()
                    return chain.proceed(newRequest)
                }
            }
        }

        return response
    }
}
```

### Retry Interceptor
```kotlin
class RetryInterceptor(
    private val maxRetries: Int = 3
) : Interceptor {

    override fun intercept(chain: Interceptor.Chain): Response {
        var request = chain.request()
        var response: Response? = null
        var exception: IOException? = null

        var retryCount = 0
        while (retryCount < maxRetries) {
            try {
                response?.close()
                response = chain.proceed(request)

                if (response.isSuccessful) {
                    return response
                }

                if (response.code !in listOf(408, 500, 502, 503, 504)) {
                    return response
                }
            } catch (e: IOException) {
                exception = e
            }

            retryCount++
            Thread.sleep((1000 * retryCount).toLong())
        }

        throw exception ?: IOException("Max retries reached")
    }
}
```

## Error Handling

### Result Wrapper
```kotlin
sealed class ApiResult<out T> {
    data class Success<T>(val data: T) : ApiResult<T>()
    data class Error(val code: Int, val message: String) : ApiResult<Nothing>()
    data class Exception(val e: Throwable) : ApiResult<Nothing>()
}

suspend fun <T> safeApiCall(
    apiCall: suspend () -> T
): ApiResult<T> {
    return try {
        ApiResult.Success(apiCall())
    } catch (e: HttpException) {
        val errorBody = e.response()?.errorBody()?.string()
        ApiResult.Error(e.code(), errorBody ?: e.message())
    } catch (e: IOException) {
        ApiResult.Exception(e)
    } catch (e: Exception) {
        ApiResult.Exception(e)
    }
}
```

### Repository Usage
```kotlin
class UserRepository @Inject constructor(
    private val api: UserApi
) {
    suspend fun getUser(id: Int): ApiResult<User> = safeApiCall {
        api.getUser(id).toUser()
    }

    suspend fun createUser(request: CreateUserRequest): ApiResult<User> =
        safeApiCall {
            api.createUser(request).toUser()
        }
}
```

## SSL Pinning

```kotlin
val certificatePinner = CertificatePinner.Builder()
    .add("api.example.com", "sha256/AAAAAAA...")
    .add("api.example.com", "sha256/BBBBBBB...") // Backup
    .build()

val client = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()
```

## File Upload

```kotlin
suspend fun uploadImage(file: File): ApiResult<ImageResponse> {
    val requestBody = file.asRequestBody("image/*".toMediaType())
    val multipart = MultipartBody.Part.createFormData(
        "image",
        file.name,
        requestBody
    )
    return safeApiCall {
        api.uploadImage(multipart)
    }
}
```

## Caching

```kotlin
// Network-first, cache fallback
val cacheInterceptor = Interceptor { chain ->
    val response = try {
        chain.proceed(chain.request())
    } catch (e: IOException) {
        val cacheRequest = chain.request().newBuilder()
            .cacheControl(CacheControl.FORCE_CACHE)
            .build()
        chain.proceed(cacheRequest)
    }
    response
}

// Cache-first for slow networks
val offlineInterceptor = Interceptor { chain ->
    var request = chain.request()
    if (!isNetworkAvailable()) {
        request = request.newBuilder()
            .cacheControl(CacheControl.FORCE_CACHE)
            .build()
    }
    chain.proceed(request)
}
```

## Best Practices

1. **Use suspend functions** for all API calls
2. **Implement proper error handling** with sealed classes
3. **Add logging interceptor** for debugging
4. **Use SSL pinning** for security
5. **Implement token refresh** logic
6. **Cache responses** when appropriate
7. **Set reasonable timeouts**
8. **Use proper threading** (Dispatchers.IO)

## Resources

- [Retrofit Documentation](https://square.github.io/retrofit/)
- [OkHttp Documentation](https://square.github.io/okhttp/)
- [Network Security Config](https://developer.android.com/training/articles/security-config)
