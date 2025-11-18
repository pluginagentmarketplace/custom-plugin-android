---
description: Security best practices, authentication, encryption, and deployment to Google Play Store
capabilities: [
  "Secure data storage and encryption",
  "Authentication and authorization",
  "API security and HTTPS",
  "Permissions and privacy",
  "Code obfuscation and signing",
  "Google Play Store deployment",
  "Build automation and CI/CD",
  "Crash reporting and analytics"
]
---

# Security & Deployment Agent

Master security best practices and deployment processes for production Android apps. This agent covers secure coding, authentication, encryption, and publishing to Google Play Store.

## Security Fundamentals

### 1. Data Security

**Sensitive Data Storage**

```kotlin
// ❌ INSECURE: Plain text storage
SharedPreferences.Editor().apply {
    putString("password", userPassword)
    putString("auth_token", token)
    apply()
}

// ✅ SECURE: Encrypted storage with DataStore + EncryptedSharedPreferences
val encryptedSharedPrefs = EncryptedSharedPreferences.create(
    context,
    "secret_shared_prefs",
    MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build(),
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

encryptedSharedPrefs.edit().apply {
    putString("password", userPassword)
    putString("auth_token", token)
    apply()
}
```

**File Encryption**
```kotlin
// ✅ Encrypt sensitive files
val encryptedFile = EncryptedFile.Builder(
    context,
    File(context.filesDir, "sensitive_data"),
    MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build(),
    EncryptedFile.FileEncryptionScheme.AES256_GCM_HKDF_4KB
).build()

// Write encrypted
encryptedFile.openFileOutput().use { output ->
    output.write(sensitiveData.toByteArray())
}

// Read encrypted
encryptedFile.openFileInput().use { input ->
    val decrypted = input.readBytes()
}
```

### 2. Authentication & Authorization

**JWT Token Management**
```kotlin
// ✅ Secure token storage with refresh
class AuthManager(private val context: Context) {
    private val encryptedPrefs = getEncryptedSharedPreferences(context)

    fun saveTokens(accessToken: String, refreshToken: String) {
        encryptedPrefs.edit {
            putString(ACCESS_TOKEN_KEY, accessToken)
            putString(REFRESH_TOKEN_KEY, refreshToken)
            putLong(EXPIRY_TIME_KEY, System.currentTimeMillis() + TOKEN_EXPIRY)
        }
    }

    fun getAccessToken(): String? {
        val token = encryptedPrefs.getString(ACCESS_TOKEN_KEY, null)
        val expiryTime = encryptedPrefs.getLong(EXPIRY_TIME_KEY, 0)

        return if (expiryTime > System.currentTimeMillis()) {
            token
        } else {
            refreshAccessToken()
        }
    }

    private suspend fun refreshAccessToken(): String? {
        val refreshToken = encryptedPrefs.getString(REFRESH_TOKEN_KEY, null) ?: return null
        return try {
            val newTokens = authApi.refreshToken(refreshToken)
            saveTokens(newTokens.accessToken, newTokens.refreshToken)
            newTokens.accessToken
        } catch (e: Exception) {
            clearTokens()
            null
        }
    }
}
```

**Biometric Authentication**
```kotlin
// ✅ Modern biometric authentication
val biometricPrompt = BiometricPrompt(
    this,
    executor,
    object : BiometricPrompt.AuthenticationCallback() {
        override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
            super.onAuthenticationSucceeded(result)
            // User authenticated
        }

        override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
            super.onAuthenticationError(errorCode, errString)
            // Handle error
        }
    }
)

val promptInfo = BiometricPrompt.PromptInfo.Builder()
    .setTitle("Authenticate")
    .setSubtitle("Use biometric to login")
    .setNegativeButtonText("Cancel")
    .build()

biometricPrompt.authenticate(promptInfo)
```

### 3. Network Security

**HTTPS & Certificate Pinning**
```kotlin
// ✅ Certificate pinning with OkHttp
val certificatePinner = CertificatePinner.Builder()
    .add("api.example.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
    .build()

val okHttpClient = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()

// ✅ Network security configuration (network_security_config.xml)
<domain-config cleartextTrafficPermitted="false">
    <domain includeSubdomains="true">api.example.com</domain>
    <pin-set>
        <pin digest="SHA-256">AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=</pin>
    </pin-set>
</domain-config>
```

### 4. Permissions

**Runtime Permissions**
```kotlin
// ✅ Request runtime permissions properly
class PermissionHelper(private val activity: Activity) {
    fun requestLocationPermission() {
        when {
            ContextCompat.checkSelfPermission(
                activity,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) == PackageManager.PERMISSION_GRANTED -> {
                // Permission granted
            }
            shouldShowRequestPermissionRationale(Manifest.permission.ACCESS_FINE_LOCATION) -> {
                // Show explanation
                ActivityCompat.requestPermissions(
                    activity,
                    arrayOf(Manifest.permission.ACCESS_FINE_LOCATION),
                    LOCATION_REQUEST_CODE
                )
            }
            else -> {
                // Request permission
                ActivityCompat.requestPermissions(
                    activity,
                    arrayOf(Manifest.permission.ACCESS_FINE_LOCATION),
                    LOCATION_REQUEST_CODE
                )
            }
        }
    }
}
```

## Code Security

### Obfuscation & ProGuard

**proguard-rules.pro**
```
# Keep public API
-keep public class * {
    public <methods>;
}

# Remove logging in production
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
}

# Optimize
-optimizationpasses 5
-dontusemixedcaseclassnames
-verbose
```

### Code Signing
```kotlin
// ✅ App signing with Play App Signing
// Configure in build.gradle
android {
    signingConfigs {
        release {
            storeFile = file(System.getenv("KEYSTORE_PATH"))
            storePassword = System.getenv("KEYSTORE_PASSWORD")
            keyAlias = System.getenv("KEY_ALIAS")
            keyPassword = System.getenv("KEY_PASSWORD")
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

## Google Play Store Deployment

### Build & Release Process

```
Local Build → Testing → Signed APK/AAB → Play Console Upload → Staged Rollout → Full Release
```

### Preparing Release Build

1. **Version Management**
```gradle
android {
    compileSdk = 34
    defaultConfig {
        targetSdk = 34
        minSdk = 24
        versionCode = 1
        versionName = "1.0.0"
    }
}
```

2. **Build Signed APK/AAB**
```bash
# Build signed bundle for Play Store
./gradlew bundleRelease

# Or signed APK for direct distribution
./gradlew assembleRelease
```

3. **Play Console Upload**
- Sign in to Google Play Console
- Create app
- Upload signed AAB
- Add app details, screenshots, description
- Configure pricing
- Submit for review

### Release Strategies

**Staged Rollout** (Recommended)
- 5% → 10% → 25% → 50% → 100%
- Monitor crash rates and ratings
- Roll back if issues found

**Beta Testing**
- Internal testing track (2-24 hours approval)
- Closed testing (limited testers)
- Open testing (public beta)

## Learning Path

**Beginner (35 hours)**
- OWASP Top 10 for mobile
- Secure data storage basics
- Permission handling
- HTTPS and network security
- Basic code obfuscation

**Intermediate (45 hours)**
- Encryption (DataStore, EncryptedSharedPreferences)
- Authentication flows
- Certificate pinning
- Code signing
- Play Store deployment process
- Beta testing strategies

**Advanced (50 hours)**
- Advanced encryption scenarios
- OAuth 2.0 and OpenID Connect
- Secure backend communication
- MAAS (Mobile Application Security)
- Enterprise security
- Advanced obfuscation and anti-reversing

## Security Checklist

- ✅ No hardcoded secrets (API keys, tokens)
- ✅ Sensitive data encrypted
- ✅ HTTPS for all network calls
- ✅ Certificate pinning implemented
- ✅ Proper permission handling
- ✅ Input validation and sanitization
- ✅ SQL injection prevention
- ✅ XSS prevention (WebView)
- ✅ Secure storage of authentication tokens
- ✅ Proper error handling (no sensitive data in logs)

## Deployment Checklist

- ✅ All tests passing
- ✅ ProGuard/R8 enabled
- ✅ Code obfuscation verified
- ✅ App signed with production key
- ✅ App tested on multiple devices
- ✅ Version code incremented
- ✅ Release notes prepared
- ✅ Privacy policy updated
- ✅ Screenshots and store listing ready
- ✅ Crash reporting configured

## OWASP Mobile Top 10

1. **Improper Platform Usage**: Misuse of APIs
2. **Insecure Data Storage**: Unencrypted data
3. **Insecure Communication**: Unencrypted network
4. **Insecure Authentication**: Weak auth mechanisms
5. **Insufficient Cryptography**: Weak encryption
6. **Insecure Authorization**: Access control bypasses
7. **Client Code Quality**: Security bugs in code
8. **Code Tampering**: App modification
9. **Reverse Engineering**: Code extraction
10. **Extraneous Functionality**: Test/debug code in production

## Related Skills

- **kotlin-programming**: Secure coding practices
- **jetpack-libraries**: DataStore security
- **app-architecture**: Secure data flow
- **performance-optimization**: Secure monitoring

## Assessment Criteria

- Can securely store sensitive data
- Implements proper authentication
- Secures network communication
- Handles permissions correctly
- Prepares secure release build
- Can deploy to Play Store
- Understands OWASP Top 10

## Next Steps

Master Security & Deployment → Build Real Apps → Share on Play Store
