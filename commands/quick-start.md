# /quick-start - Quick Start Guide

Essential resources and quick references for Android development.

## Getting Started

### Prerequisites
- Java/Kotlin knowledge (basic)
- Android Studio installed
- Familiarity with command line
- Git version control basics

### First Steps
1. Start with `/roadmap` for learning path
2. Use `/agent-guide` to understand agent expertise
3. Explore relevant agent when needed
4. Refer to skills for quick reference

---

## Essential Commands

### Build & Run
```bash
./gradlew build          # Build project
./gradlew assembleDebug  # Build debug APK
./gradlew bundleRelease  # Build release bundle
./gradlew connectedTest  # Run tests on device
```

### Common Gradle Tasks
```bash
./gradlew clean                    # Clean build
./gradlew dependencies             # Show dependencies
./gradlew lintDebug               # Run lint checks
./gradlew test                     # Run unit tests
./gradlew connectedAndroidTest    # Run instrumentation tests
```

---

## Quick Solutions

### "How do I..."

#### Create an Activity?
- See **Agent 2: Platform** for detailed guide
- Key: Extend `AppCompatActivity`, implement lifecycle callbacks

#### Make API calls?
- See **Agent 5: Networking** for complete reference
- Quick: Use Retrofit with suspend functions

#### Store data locally?
- See **Agent 4: Data Management** for all options
- Quick: Use Room ORM for complex data, DataStore for preferences

#### Design responsive UI?
- See **Agent 3: UI Development** for layouts
- Quick: Use ConstraintLayout or Jetpack Compose

#### Handle permissions?
- See **Agent 2: Platform** for permissions section
- Quick: Check and request at runtime (API 23+)

#### Improve app performance?
- See **Agent 7: Production** for optimization strategies
- Quick: Profile with Android Profiler, fix memory leaks

#### Deploy to Play Store?
- See **Agent 7: Production** for deployment guide
- Quick: Sign bundle, upload to Play Console, staged rollout

---

## Project Setup Checklist

- [ ] Create new Android Studio project
- [ ] Setup version control (git)
- [ ] Add Gradle dependencies
  - Jetpack (androidx)
  - Hilt for DI
  - Retrofit for networking
  - Room for database
  - Testing libraries
- [ ] Create package structure
- [ ] Setup base classes (Activity, Fragment, ViewModel)
- [ ] Implement first feature

---

## Architecture Template

```
app/
├── data/
│   ├── local/          (Room, SharedPreferences)
│   ├── remote/         (Retrofit APIs)
│   └── repository/     (Repository implementations)
├── domain/
│   ├── model/          (Data classes)
│   └── repository/     (Repository interfaces)
├── presentation/
│   ├── ui/            (Activities, Fragments)
│   ├── viewmodel/     (ViewModels)
│   └── adapter/       (RecyclerView adapters)
└── di/                (Hilt modules)
```

---

## Key Android APIs

### Core Components
- `AppCompatActivity`: Base for activities
- `Fragment`: Reusable UI component
- `Service`: Background operation
- `BroadcastReceiver`: Listen to events
- `ContentProvider`: Share data

### Jetpack Libraries
- `ViewModel`: UI state management
- `LiveData`: Observable data
- `Room`: Type-safe database
- `Navigation`: Fragment navigation
- `WorkManager`: Background jobs
- `DataStore`: Modern preferences

### Material Design
- `MaterialButton`: Material button
- `Card`: Material card component
- `TopAppBar`: Top navigation bar
- `Scaffold`: Basic Material layout
- `Navigation Drawer`: Side navigation

---

## Testing Quick Reference

### Unit Test Template
```kotlin
@Test
fun testFunction() {
    // Arrange
    val expected = "value"
    
    // Act
    val result = functionUnderTest()
    
    // Assert
    assertEquals(expected, result)
}
```

### UI Test Template
```kotlin
@Test
fun testButtonClick() {
    onView(withId(R.id.button)).perform(click())
    onView(withText("Success")).check(matches(isDisplayed()))
}
```

---

## Common Dependencies

```gradle
dependencies {
    // Core
    implementation "androidx.appcompat:appcompat:1.6.1"
    implementation "androidx.activity:activity-ktx:1.8.0"
    
    // Jetpack
    implementation "androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.1"
    implementation "androidx.room:room-runtime:2.5.2"
    implementation "androidx.datastore:datastore-preferences:1.0.0"
    implementation "androidx.navigation:navigation-fragment-ktx:2.7.2"
    
    // DI
    implementation "com.google.dagger:hilt-android:2.46"
    kapt "com.google.dagger:hilt-compiler:2.46"
    
    // Networking
    implementation "com.squareup.retrofit2:retrofit:2.9.0"
    implementation "com.squareup.okhttp3:okhttp:4.11.0"
    implementation "com.google.code.gson:gson:2.10.1"
    
    // Testing
    testImplementation "junit:junit:4.13.2"
    testImplementation "io.mockk:mockk:1.13.5"
    androidTestImplementation "androidx.test.espresso:espresso-core:3.5.1"
}
```

---

## Official Resources

- [Android Developer Docs](https://developer.android.com)
- [Kotlin Official Docs](https://kotlinlang.org/docs/)
- [Jetpack Architecture Guide](https://developer.android.com/jetpack/guide)
- [Material Design 3](https://m3.material.io/)
- [Google Play Console](https://play.google.com/console)

---

## Next Steps

1. Choose an agent from `/agent-guide`
2. Study its content thoroughly
3. Build a practice project
4. Review official documentation
5. Move to next agent

**Total Learning Time:** 37-45 weeks @ 2-4 hours/day to master all 7 steps

Good luck building awesome Android apps! 🚀
