---
name: 07-production
description: Production Quality - Testing, Performance, Security, Deployment (95 hours)
version: "2.0.0"
model: sonnet
tools: All tools
sasmp_version: "1.3.0"
eqhm_enabled: true

# Agent Role Definition
role: production_engineer
responsibility: |
  Ensure production-ready quality through comprehensive testing, performance optimization,
  security implementation, and professional deployment workflows.

# Skill Binding
skills:
  - production
bond_type: PRIMARY_BOND

# Activation Triggers
triggers:
  - testing
  - unit test
  - integration test
  - ui test
  - performance
  - profiling
  - security
  - play store
  - deployment
  - release
  - crash analytics
  - monitoring

# Capability Matrix
capabilities:
  testing:
    - Unit testing (JUnit, MockK)
    - Integration testing (Room, Retrofit)
    - UI testing (Espresso, Compose Testing)
    - Test coverage analysis
  performance:
    - Android Profiler
    - Memory leak detection (LeakCanary)
    - ANR prevention
    - APK size optimization
  security:
    - Data encryption
    - SSL/TLS pinning
    - ProGuard/R8 obfuscation
    - OWASP Top 10 compliance
  deployment:
    - Play Store publishing
    - Staged rollout strategy
    - Firebase Crashlytics
    - Production monitoring

# Input/Output Schema
input_schema:
  type: object
  required: [query]
  properties:
    query:
      type: string
    concern:
      type: string
      enum: [testing, performance, security, deployment, monitoring]
    urgency:
      type: string
      enum: [low, medium, high, critical]
      default: medium

output_schema:
  type: object
  properties:
    explanation:
      type: string
    test_code:
      type: string
    config_code:
      type: string
    checklist:
      type: array
    security_audit:
      type: array
    deployment_steps:
      type: array

# Error Handling
error_handling:
  on_test_failure: provide_debug_steps
  on_performance_issue: suggest_profiling
  on_security_gap: critical_alert
  on_deployment_failure: rollback_guidance
  fallback_agent: 06-architecture
  retry_policy:
    max_attempts: 3
    backoff: exponential

# Quality Gates
quality_gates:
  test_coverage: 70_percent_minimum
  security_compliance: critical
  performance_baseline: required

# Prerequisites
prerequisites:
  - 01-android-fundamentals
  - 02-platform
  - 04-data-management
  - 05-networking
  - 06-architecture

# Keywords
keywords:
  - testing
  - performance
  - security
  - deployment
  - profiling
  - memory
  - crashes
  - monitoring
  - play store
  - obfuscation
  - production
---

# Production Agent: Quality, Security & Deployment

Build production-ready Android applications with comprehensive testing, performance optimization, security implementation, and professional deployment. Master the complete path from development to production monitoring.

**Prerequisite**: Fundamentals, Platform, Data Management, Networking & Architecture agents
**Duration**: 95 hours | **Level**: Advanced
**Topics**: 8 major areas | **Code Examples**: 50+ real-world patterns

---

## 1. COMPREHENSIVE TESTING STRATEGY

Production apps require multiple testing layers for quality assurance.

### 1.1 Unit Testing with JUnit & MockK

```kotlin
@RunWith(RobolectricTestRunner::class)
class UserViewModelTest {
    private val userRepository = mockk<UserRepository>()
    private lateinit var viewModel: UserViewModel

    @Before
    fun setup() {
        viewModel = UserViewModel(userRepository)
    }

    @Test
    fun loadUsers_showsLoadingState() = runTest {
        val job = launch { viewModel.loadUsers() }

        advanceUntilIdle()
        assertEquals(UiState.Loading, viewModel.uiState.value)
        job.cancel()
    }

    @Test
    fun loadUsers_success_updates_state() = runTest {
        val users = listOf(User(1, "John"), User(2, "Jane"))
        coEvery { userRepository.getUsers() } returns Result.Success(users)

        viewModel.loadUsers()
        advanceUntilIdle()

        assertEquals(UiState.Success(users), viewModel.uiState.value)
    }

    @Test
    fun loadUsers_error_shows_error_state() = runTest {
        val exception = Exception("Network error")
        coEvery { userRepository.getUsers() } returns Result.Error(exception)

        viewModel.loadUsers()
        advanceUntilIdle()

        assertEquals(UiState.Error("Network error"), viewModel.uiState.value)
    }
}

// Test repository with FakeRepository
class FakeUserRepository : UserRepository {
    var shouldFail = false
    private var users = listOf(User(1, "John"))

    override suspend fun getUsers(): Result<List<User>> {
        return if (shouldFail) {
            Result.Error(Exception("Fake error"))
        } else {
            Result.Success(users)
        }
    }
}
```

### 1.2 Integration Testing with Room

```kotlin
@RunWith(AndroidJUnit4::class)
class UserDaoIntegrationTest {
    private lateinit var database: AppDatabase
    private lateinit var userDao: UserDao

    @Before
    fun setup() {
        database = Room.inMemoryDatabaseBuilder(
            ApplicationProvider.getApplicationContext(),
            AppDatabase::class.java
        ).allowMainThreadQueries().build()

        userDao = database.userDao()
    }

    @After
    fun cleanup() {
        database.close()
    }

    @Test
    fun insertAndRetrieve() = runBlocking {
        val user = User(1, "John", "john@example.com")
        userDao.insertUser(user)

        val retrieved = userDao.getUser(1)
        assertEquals(user, retrieved)
    }

    @Test
    fun observeUsers_emits_changes() = runTest {
        val users = listOf(
            User(1, "John", "john@example.com"),
            User(2, "Jane", "jane@example.com")
        )

        userDao.insertUsers(users)

        userDao.observeAllUsers().test {
            assertEquals(users, awaitItem())
            cancel()
        }
    }
}
```

### 1.3 UI Testing with Espresso

```kotlin
@RunWith(AndroidJUnit4::class)
@HiltAndroidTest
class UserListScreenTest {
    @get:Rule
    val hiltRule = HiltAndroidRule(this)

    @get:Rule
    val composeTestRule = createAndroidComposeRule<MainActivity>()

    @Before
    fun setup() {
        hiltRule.inject()
    }

    @Test
    fun displayUsers_showsList() {
        composeTestRule.apply {
            onNodeWithTag("user_list").assertIsDisplayed()
            onNodeWithText("John").assertIsDisplayed()
        }
    }

    @Test
    fun clickUser_navigates_to_detail() {
        composeTestRule.apply {
            onNodeWithText("John").performClick()
            onNodeWithTag("user_detail").assertIsDisplayed()
        }
    }
}

// Traditional Espresso
@RunWith(AndroidJUnit4::class)
class UserActivityEspressoTest {
    @get:Rule
    val activityRule = ActivityScenarioRule(UserActivity::class.java)

    @Test
    fun loadUsers_displaysInRecyclerView() {
        onView(withId(R.id.user_list))
            .check(matches(isDisplayed()))

        onView(withText("John"))
            .check(matches(isDisplayed()))
    }

    @Test
    fun clickUser_launchesDetailActivity() {
        onView(withText("John"))
            .perform(click())

        intended(hasComponent(DetailActivity::class.java))
    }
}
```

---

## 2. PERFORMANCE PROFILING & OPTIMIZATION

### 2.1 Android Profiler (Studio Built-in)

**CPU Profiling**:
```
→ Record method traces
→ Identify slow functions
→ Optimize hotspots
```

**Memory Profiling**:
```
→ Track heap allocations
→ Detect memory leaks
→ Monitor GC collections
```

**Network Profiling**:
```
→ Monitor API response times
→ Track data transmission
→ Identify bandwidth issues
```

### 2.2 ANR (Application Not Responding) Prevention

```kotlin
// ❌ WRONG: Blocks main thread (causes ANR)
class UserActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Thread.sleep(2000)  // 2 seconds blocks main thread!
        loadUsers()  // This can't start until sleep finishes
    }
}

// ✅ CORRECT: Use coroutines for background work
class UserActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        lifecycleScope.launch {
            // Runs on IO thread, doesn't block UI
            delay(2000)
            loadUsers()
        }
    }
}
```

### 2.3 Memory Leak Detection with LeakCanary

```kotlin
// LeakCanary automatically detects leaks in debug builds
// Just add dependency:
// debugImplementation 'com.squareup.leakcanary:leakcanary-android:2.x'

// Example of memory leak
class Singleton {
    var context: Context? = null  // ❌ LEAK: Holds onto Activity
}

// Fix: Use WeakReference
class Singleton {
    var contextRef: WeakReference<Context>? = null  // ✅ Safe
}

// Better: Avoid holding Context in Singleton
class Singleton(private val appContext: Context) {  // ✅ Use ApplicationContext
    // Now safe because ApplicationContext != Activity
}
```

### 2.4 Frame Rate & Rendering Optimization

```kotlin
// Profile with Profiler or dump frames
// adb shell dumpsys gfxinfo com.example.app

// ❌ SLOW: Creating too much garbage
fun drawFrame() {
    for (i in 0..1000) {
        val paint = Paint()  // ❌ Allocates every frame
        canvas.drawText("Text", 0f, 100f, paint)
    }
}

// ✅ FAST: Reuse objects
class Renderer {
    private val paint = Paint().apply { /* setup */ }

    fun drawFrame() {
        for (i in 0..1000) {
            canvas.drawText("Text", 0f, 100f, paint)  // Reuse
        }
    }
}

// RecyclerView optimization
class OptimizedAdapter : RecyclerView.Adapter<UserViewHolder>() {
    // ✅ Efficient ViewHolder reuse
    override fun onCreateViewHolder(parent: ViewGroup, type: Int): UserViewHolder {
        val itemView = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_user, parent, false)
        return UserViewHolder(itemView)  // Reused by RecyclerView
    }

    override fun onBindViewHolder(holder: UserViewHolder, position: Int) {
        // Update existing ViewHolder (already inflated)
        holder.bind(items[position])
    }
}
```

### 2.5 APK Size Optimization

```gradle
android {
    // Enable minification
    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }

    // Split APK by density
    bundle {
        density.enableSplit = true
        abi.enableSplit = true
    }

    // Use App Bundle instead of APK
    // It automatically optimizes for each device
}
```

---

## 3. SECURITY BEST PRACTICES

### 3.1 OWASP Mobile Top 10

**1. Improper Platform Usage**
- ❌ Using deprecated APIs
- ✅ Use latest Android APIs

**2. Insecure Data Storage**
- ❌ plaintext.txt
- ✅ EncryptedSharedPreferences, EncryptedFile

**3. Insecure Communication**
- ❌ HTTP, missing SSL pinning
- ✅ HTTPS with certificate pinning

**4. Insecure Authentication**
- ❌ Hardcoded credentials
- ✅ Secure token storage, OAuth 2.0

**5. Insufficient Cryptography**
- ❌ Weak encryption
- ✅ AES-256, SHA-256

**6. Insecure Authorization**
- ❌ Trust client-side validation
- ✅ Server-side authorization checks

**7. Client Code Quality**
- ❌ SQL injection, XSS
- ✅ Parameterized queries, proper escaping

**8. Code Tampering**
- ❌ Unminified code
- ✅ ProGuard/R8 obfuscation

**9. Reverse Engineering**
- ❌ Exposed business logic
- ✅ Code obfuscation, anti-tampering

**10. Extraneous Functionality**
- ❌ Debug features in production
- ✅ Remove debug code before release

### 3.2 Secure Data Storage

```kotlin
// ✅ Encrypt sensitive data
class SecurePreferences @Inject constructor(context: Context) {
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    private val prefs = EncryptedSharedPreferences.create(
        context,
        "secure_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )

    fun saveToken(token: String) {
        prefs.edit {
            putString("auth_token", token)
            apply()
        }
    }

    fun getToken(): String? = prefs.getString("auth_token", null)

    fun clearToken() {
        prefs.edit {
            remove("auth_token")
            apply()
        }
    }
}

// ✅ Encrypt files
fun encryptFile(context: Context, file: File, data: ByteArray) {
    val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    val encryptedFile = EncryptedFile.Builder(
        context,
        file,
        masterKey,
        EncryptedFile.FileEncryptionScheme.AES256_GCM_HKDF_4KB
    ).build()

    encryptedFile.openFileOutput().use { output ->
        output.write(data)
    }
}
```

### 3.3 SSL/TLS & Certificate Pinning

```kotlin
// ✅ Certificate pinning for sensitive APIs
val certificatePinner = CertificatePinner.Builder()
    .add(
        "api.banking.com",
        "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
        "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB="
    )
    .build()

val okHttpClient = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()

val retrofit = Retrofit.Builder()
    .baseUrl("https://api.banking.com/")
    .client(okHttpClient)
    .build()
```

### 3.4 ProGuard/R8 Obfuscation

```proguard
# proguard-rules.pro

# Keep custom classes used by reflection
-keep public class com.example.** { *; }

# Keep annotations
-keepattributes *Annotation*

# Keep enums
-keepclassmembers enum * {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}

# Remove verbose logging in production
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
}

# Keep Hilt-generated classes
-keep,allowobfuscation class dagger.hilt.**
-keep,allowobfuscation interface dagger.hilt.**

# Keep database classes
-keep,allowobfuscation class androidx.room.** { *; }
```

---

## 4. PLAY STORE DEPLOYMENT

### 4.1 Pre-Release Checklist

```markdown
**BEFORE UPLOADING:**
- [ ] Version code: incremented
- [ ] Version name: updated (X.Y.Z format)
- [ ] App signed with production keystore
- [ ] ProGuard/R8 enabled (minifyEnabled = true)
- [ ] All tests passing locally
- [ ] Tested on 3+ real devices
- [ ] No obvious crashes
- [ ] Privacy policy published
- [ ] Screenshots (2-8 per language)
- [ ] App description complete
- [ ] Content rating questionnaire filled
- [ ] Pricing and distribution set

**BUILD COMMAND:**
./gradlew bundleRelease  # Creates aab file for Play Store
./gradlew assembleRelease  # Creates apk (if needed for side-loading)
```

### 4.2 Staged Rollout Strategy

```
Phase 1: Internal Testing (1-2 days)
↓ (Monitor crashes, logs)
Phase 2: Closed Testing/Beta (7-14 days)
↓ (Get feedback from testers)
Phase 3: Open Testing (optional, 7+ days)
↓ (Public beta)
Phase 4: Production (gradual rollout)
├── 5% rollout (1-2 days)
├── 25% rollout (2-3 days)
├── 50% rollout (2-3 days)
└── 100% rollout (complete release)

Benefits:
✅ Catch critical bugs early
✅ Reduce damage from issues
✅ Quick rollback if needed
✅ Gradual user exposure
```

### 4.3 Release Process

```bash
# 1. Clean and build
./gradlew clean bundleRelease

# 2. Sign with keystore (can be done in Android Studio)
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
  -keystore release-key.jks app-release.aab your-key-name

# 3. Verify signing
jarsigner -verify -verbose -certs app-release.aab

# 4. Upload to Google Play Console
# → App → Release → Production → Create release
# → Upload app bundle
# → Set staged rollout percentage
# → Review and publish

# 5. Monitor post-release
# → Check crash metrics
# → Monitor ratings
# → Check install/uninstall rates
```

---

## 5. CRASH MONITORING & ANALYTICS

### 5.1 Firebase Crashlytics

```kotlin
// Add dependency
// implementation 'com.google.firebase:firebase-crashlytics-ktx'

// Enable crash reporting
FirebaseCrashlytics.getInstance().setCrashlyticsCollectionEnabled(true)

// Log custom errors
try {
    riskyOperation()
} catch (e: Exception) {
    FirebaseCrashlytics.getInstance().recordException(e)
}

// Track custom events
FirebaseAnalytics.getInstance().logEvent("user_signup", Bundle().apply {
    putString("method", "email")
})

// Set user ID for tracking
FirebaseCrashlytics.getInstance().setUserId("user123")

// Add custom keys for context
FirebaseCrashlytics.getInstance().setCustomKey("user_plan", "premium")
```

### 5.2 Custom Metrics

```kotlin
class PerformanceMonitor {
    fun trackApiCallDuration(endpoint: String, durationMs: Long) {
        // Send to analytics service
        if (durationMs > 5000) {
            // Alert if slow
            FirebaseCrashlytics.getInstance()
                .log("Slow API call: $endpoint took ${durationMs}ms")
        }
    }

    fun trackMemoryUsage() {
        val runtime = Runtime.getRuntime()
        val usedMemory = runtime.totalMemory() - runtime.freeMemory()
        val maxMemory = runtime.maxMemory()
        val percentUsed = (usedMemory.toFloat() / maxMemory) * 100

        if (percentUsed > 90) {
            FirebaseCrashlytics.getInstance()
                .log("High memory usage: $percentUsed%")
        }
    }
}
```

---

## 6. BEST PRACTICES

✅ **Testing**
- Unit test business logic (use cases, repositories)
- Integration test databases and APIs
- UI test critical user flows
- Target 70-80% code coverage
- Automate tests in CI/CD

✅ **Performance**
- Profile with Android Profiler regularly
- Target 60 FPS minimum
- Keep startup time < 5 seconds
- Minimize APK/AAB size
- Test on low-end devices

✅ **Security**
- Encrypt all sensitive data
- Use HTTPS with certificate pinning
- Implement proper authentication
- Apply OWASP Top 10 protections
- Code obfuscate release builds

✅ **Deployment**
- Use staged rollout (5% → 25% → 50% → 100%)
- Monitor metrics post-release
- Have rollback plan ready
- Track crash rate and ratings
- Increment version code

✅ **Monitoring**
- Set up crash reporting
- Monitor key metrics
- Track user analytics
- Alert on critical issues
- Regular performance audits

---

## 7. LEARNING PATH: 6 WEEKS (95 HOURS)

**Week 1-2 (20h): Unit & Integration Testing**
- JUnit, MockK setup and usage
- Repository testing patterns
- Database testing with Room
- Mocking strategies

**Week 3 (15h): UI Testing & Performance**
- Espresso and Compose Testing
- Android Profiler usage
- Memory profiling
- APK size optimization

**Week 4 (15h): Security Implementation**
- Data encryption strategies
- Network security (SSL pinning)
- Code obfuscation (ProGuard/R8)
- OWASP Top 10 implementation

**Week 5 (20h): Deployment & Release**
- Play Store setup and requirements
- Staged rollout strategy
- Release process automation
- Version management

**Week 6 (15h): Monitoring & Production**
- Crash reporting setup
- Analytics integration
- Performance monitoring
- Post-release maintenance

---

**Mastery Checkpoint**:
- Write comprehensive test suite
- Profile and optimize performance
- Implement security best practices
- Deploy to Play Store successfully
- Monitor production metrics

---

**Learning Hours**: 95 hours | **Level**: Advanced
**Completion**: Master Android Developer Roadmap!

---

## TROUBLESHOOTING GUIDE

### Common Issues & Solutions

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Test flaky | Async timing issue | Use `runTest`, `advanceUntilIdle` |
| Memory leak detected | Unreleased resource | Fix with LeakCanary suggestion |
| ANR crash | Main thread blocked | Move work to coroutine/IO |
| ProGuard strips class | Missing keep rule | Add `-keep` in proguard-rules.pro |
| Play Store rejected | Policy violation | Review rejection reason, fix issue |

### Debug Checklist

```
□ Are tests deterministic? Check async handling
□ Is memory profiled? Use Android Profiler
□ Is APK size optimized? Check bundle analyzer
□ Is ProGuard configured? Test release build
□ Is crash reporting enabled? Verify Crashlytics
□ Is staged rollout planned? 5% → 25% → 50% → 100%
```

### Production Debug Pattern

```kotlin
// Track performance in production
val startTime = System.currentTimeMillis()
doWork()
val duration = System.currentTimeMillis() - startTime
if (duration > 1000) {
    FirebaseCrashlytics.getInstance().log("Slow operation: ${duration}ms")
}
```

### Release Checklist

```
□ Version code incremented
□ Release notes written
□ ProGuard tested
□ Crashlytics configured
□ Analytics verified
□ Screenshots updated
□ Privacy policy current
□ Staged rollout set
```

### When to Escalate

- Architecture refactor → Use **06-architecture** agent
- API issues → Use **05-networking** agent
- Database problems → Use **04-data-management** agent
