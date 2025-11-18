---
name: app-deployment
description: Build processes, code signing, Google Play Store deployment, CI/CD, and release management. Use when preparing apps for production release.
---

# App Deployment Skill

## Quick Start

### Build Signed APK
```bash
./gradlew assembleRelease
```

### Build App Bundle
```bash
./gradlew bundleRelease
```

### Configure Signing
```gradle
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
            proguardFiles 'proguard-rules.pro'
        }
    }
}
```

## Release Process

1. Increase version code/name
2. Build signed bundle/APK
3. Test on multiple devices
4. Upload to Play Console
5. Configure listing (description, screenshots)
6. Set up staged rollout
7. Monitor crash rates
8. Gradually roll out to 100%

## Version Management

```gradle
versionCode = 1              // Incremented for each release
versionName = "1.0.0"        // User-facing version
```

## Play Console Steps

1. Create app
2. Upload AAB/APK
3. Add app details
4. Configure pricing & distribution
5. Set up beta tracks
6. Submit for review
7. Manage release rollout

## CI/CD Integration

- GitHub Actions
- GitLab CI
- Jenkins
- Fastlane

## ProGuard Configuration

```
-keep public class * { public <methods>; }
-assumenosideeffects class android.util.Log { *; }
-optimizationpasses 5
```

## Release Checklist

- ✅ All tests passing
- ✅ Code obfuscation enabled
- ✅ App signed with production key
- ✅ Version code incremented
- ✅ Tested on multiple devices
- ✅ Privacy policy updated
- ✅ Screenshots ready
- ✅ Crash reporting configured

## Resources

- [Google Play Console Help](https://support.google.com/googleplay/android-developer)
- [Build Configuration](https://developer.android.com/studio/build)
