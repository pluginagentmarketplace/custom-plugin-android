---
name: android-production
description: Testing, performance optimization, security, and Play Store deployment. Use when shipping production apps.
---

# Android Production Skill

## Unit Testing

```kotlin
@RunWith(RobolectricTestRunner::class)
class UserViewModelTest {
    private val repository = mockk<UserRepository>()
    private lateinit var viewModel: UserViewModel

    @Before
    fun setup() {
        viewModel = UserViewModel(repository)
    }

    @Test
    fun loadUser_updateState() {
        val user = User(1, "John")
        coEvery { repository.getUser(1) } returns user

        viewModel.loadUser(1)

        assertEquals(UiState.Success(user), viewModel.state.value)
    }
}
```

## UI Testing

```kotlin
@RunWith(AndroidJUnit4::class)
@HiltAndroidTest
class UserDetailActivityTest {
    @get:Rule
    val hiltRule = HiltAndroidRule(this)

    @get:Rule
    val activityRule = ActivityScenarioRule(UserDetailActivity::class.java)

    @Test
    fun displayUserData() {
        onView(withId(R.id.user_name))
            .check(matches(withText("John Doe")))
    }

    @Test
    fun clickEditNavigatesCorrectly() {
        onView(withId(R.id.edit_button))
            .perform(click())

        intended(hasComponent(UserEditActivity::class.java.name))
    }
}
```

## Performance Optimization

### Memory Leaks
```kotlin
// ❌ LEAK
object ApiManager {
    lateinit var context: Context
}

// ✅ FIX
object ApiManager {
    var contextRef: WeakReference<Context>? = null
}
```

### Battery Efficiency
```kotlin
// ✅ Batch network requests
WorkManager.enqueueUniquePeriodicWork(
    "sync",
    ExistingPeriodicWorkPolicy.KEEP,
    PeriodicWorkRequestBuilder<SyncWorker>(15, TimeUnit.MINUTES)
        .setConstraints(
            Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .setRequiresBatteryNotLow(true)
                .build()
        )
        .build()
)
```

### Rendering Performance
```kotlin
// ❌ SLOW - Main thread
override fun onDraw(canvas: Canvas) {
    val bitmap = BitmapFactory.decodeFile(path)
    canvas.drawBitmap(bitmap, 0f, 0f, null)
}

// ✅ FAST - Background thread
lifecycleScope.launch(Dispatchers.Default) {
    cachedBitmap = BitmapFactory.decodeFile(path)
    invalidate()
}
```

## Security Best Practices

### Secure Data Storage
```kotlin
// ✅ Encrypted storage
val encryptedPrefs = EncryptedSharedPreferences.create(
    context,
    "secret",
    MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build(),
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

encryptedPrefs.edit { putString("token", authToken) }
```

### Secure Network Communication
```kotlin
// ✅ Certificate pinning
val certificatePinner = CertificatePinner.Builder()
    .add("api.example.com", "sha256/AAAA...")
    .build()

val client = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()
```

### Permissions
```kotlin
// ✅ Check permissions before use
if (ContextCompat.checkSelfPermission(
    context,
    Manifest.permission.ACCESS_FINE_LOCATION
) == PackageManager.PERMISSION_GRANTED) {
    getLocation()
} else {
    requestPermission()
}
```

## Play Store Deployment

### Build Release APK/AAB
```gradle
// Configure signing
android {
    signingConfigs {
        release {
            storeFile = file(System.getenv("KEYSTORE"))
            storePassword = System.getenv("STORE_PASS")
            keyAlias = System.getenv("KEY_ALIAS")
            keyPassword = System.getenv("KEY_PASS")
        }
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.release
            minifyEnabled = true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

### Version Management
```gradle
android {
    defaultConfig {
        versionCode = 1          // Increment each release
        versionName = "1.0.0"    // User-visible version
    }
}
```

### ProGuard Rules
```
-keep public class * {
    public <methods>;
}

-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
}

-optimizationpasses 5
-dontusemixedcaseclassnames
```

## Crash Reporting

```kotlin
// Integrate Firebase Crashlytics
FirebaseCrashlytics.getInstance().recordException(exception)

// Log non-fatal issues
FirebaseCrashlytics.getInstance().log("Important event")
```

## Release Checklist

✅ All tests passing
✅ Code obfuscation enabled
✅ Version code incremented
✅ App signed correctly
✅ Tested on multiple devices
✅ Performance optimized
✅ Security reviewed
✅ Privacy policy updated
✅ Crash reporting configured
✅ Analytics integrated

## Performance Targets

- Cold start: < 5 seconds
- Hot start: < 2 seconds
- Frame rate: 60+ FPS
- Memory: < 512 MB
- Battery: < 5% per hour

## OWASP Mobile Top 10

1. Improper Platform Usage
2. Insecure Data Storage
3. Insecure Communication
4. Insecure Authentication
5. Insufficient Cryptography
6. Insecure Authorization
7. Client Code Quality
8. Code Tampering
9. Reverse Engineering
10. Extraneous Functionality

## Resources

- [Testing Guide](https://developer.android.com/training/testing)
- [Performance Docs](https://developer.android.com/topic/performance)
- [Security & Privacy](https://developer.android.com/privacy-and-security)
- [Play Console Help](https://support.google.com/googleplay)
