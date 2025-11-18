---
description: Testing, Performance, Security, and Deployment - unit testing, performance optimization, security best practices, Play Store release - production-ready Android apps
capabilities: ["Unit testing", "Performance profiling", "Memory optimization", "Security implementation", "Play Store deployment", "Release management", "Crash analytics", "Monitoring"]
---

# Production Agent

Build production-ready Android applications with comprehensive testing, performance optimization, security implementation, and professional deployment.

## Unit Testing

### JUnit Framework
```kotlin
@Test
fun testAddition() {
    assertEquals(4, 2 + 2)
}
```

### Mockito Mocking
```kotlin
val mockRepository = mockk<UserRepository>()
coEvery { mockRepository.getUser(1) } returns User(1, "John")
```

### Espresso UI Testing
```kotlin
onView(withId(R.id.button)).perform(click())
onView(withText("Success")).check(matches(isDisplayed()))
```

### Coverage Goal
- Aim for 70-80% coverage minimum
- Focus on business logic coverage
- Not all code needs testing (trivial getters)

## Performance Optimization

### ANR Prevention
- Keep main thread responsive
- Move long operations to background
- Use coroutines, not AsyncTask

### Memory Management
```kotlin
// Avoid memory leaks
WeakReference<Context>(context)

// Unregister listeners
override fun onDestroy() {
    unregisterReceiver()
}
```

### Frame Rate
- Target 60 FPS minimum
- Monitor with Android Profiler
- Avoid janky animations

### APK Size
- Use App Bundle (Play Store optimization)
- WebP images (~25% smaller than JPEG)
- ProGuard/R8 minification
- Remove unused resources

## Security Best Practices

### Data Encryption
```kotlin
val encryptedPrefs = EncryptedSharedPreferences.create(
    context, "secret",
    MasterKey.Builder(context).build(),
    AES256_SIV, AES256_GCM
)
```

### SSL Pinning
```kotlin
CertificatePinner.Builder()
    .add("api.example.com", "sha256/...")
    .build()
```

### OWASP Mobile Top 10
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

### Code Obfuscation (ProGuard/R8)
```proguard
-keep public class com.example.** { *; }
-assumenosideeffects class android.util.Log {
    public static *** d(...);
}
```

## Play Store Deployment

### Pre-Launch Checklist
- [ ] Version code incremented
- [ ] Signed with production keystore
- [ ] ProGuard/R8 enabled
- [ ] Tested on multiple devices
- [ ] Privacy policy URL provided
- [ ] Screenshots and descriptions ready

### Release Tracks
1. **Internal Testing** (fastest review)
2. **Closed Testing/Beta** (14 days minimum)
3. **Open Testing** (public beta)
4. **Production** (full release)

### Signed Bundle
```bash
./gradlew bundleRelease
# Upload to Google Play Console
```

### Staged Rollout
- Start with 10% of users
- Monitor crash rate and ratings
- Gradually increase to 100%
- Ability to quick rollback

## Performance Monitoring

### Crash Analytics (Firebase)
```kotlin
FirebaseCrashlytics.getInstance().recordException(exception)
```

### Battery Usage
- Use WorkManager for background jobs
- Battery-aware constraints
- Efficient location updates

### Network Monitoring
- Monitor API response times
- Track failed requests
- Optimize data transfer

## Learning Outcomes
- Write comprehensive tests
- Optimize app performance
- Implement security correctly
- Deploy professionally
- Monitor production apps

---

**Learning Hours**: 95 hours | **Level**: Advanced
