---
name: app-security
description: Secure data storage, encryption, authentication, authorization, and secure network communication. Use when implementing security features.
---

# App Security Skill

## Quick Start

### Secure Data Storage
```kotlin
// ✅ Encrypted SharedPreferences
val encryptedPrefs = EncryptedSharedPreferences.create(
    context,
    "secret_prefs",
    MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build(),
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)
encryptedPrefs.edit { putString("password", token) }
```

### Authentication
```kotlin
// Biometric authentication
val biometricPrompt = BiometricPrompt(this, executor, callback)
biometricPrompt.authenticate(promptInfo)
```

### Network Security
```kotlin
// Certificate pinning
val certificatePinner = CertificatePinner.Builder()
    .add("api.example.com", "sha256/AAAA...")
    .build()

val okHttpClient = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()
```

## Security Principles

1. **Data Encryption**: Encrypt sensitive data
2. **HTTPS**: Always use HTTPS
3. **Permissions**: Request only needed permissions
4. **Input Validation**: Validate all inputs
5. **Error Handling**: Don't expose sensitive errors

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

## Security Checklist

- ✅ No hardcoded secrets
- ✅ Sensitive data encrypted
- ✅ HTTPS everywhere
- ✅ Proper permissions handling
- ✅ Input validation

## Resources

- [Android Security & Privacy](https://developer.android.com/privacy-and-security)
- [OWASP Mobile Top 10](https://owasp.org/www-project-mobile-top-10/)
