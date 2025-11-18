# /dev-guide - Android Development Guide

Complete professional Android development guide covering best practices, patterns, and production workflows.

## Learning Path

### Beginner (100-150 hours)
1. **Kotlin Fundamentals** (30-40 hours)
   - Variables, functions, classes
   - Extension functions
   - Basic coroutines

2. **Android Core** (40-50 hours)
   - Activities and lifecycle
   - Fragments
   - Intents and navigation
   - Data persistence

3. **First App Project** (30-60 hours)
   - Simple todo app with database
   - Multiple screens
   - CRUD operations

### Intermediate (100-150 hours)
1. **Jetpack Modern** (40-50 hours)
   - ViewModel and LiveData
   - Room database advanced
   - Navigation Component
   - Hilt dependency injection

2. **Architecture Patterns** (40-50 hours)
   - MVVM architecture
   - Repository pattern
   - Testing strategies
   - Design patterns

3. **Real-World App** (20-50 hours)
   - News app, weather app, or e-commerce
   - API integration
   - Database design
   - Multi-screen navigation

### Advanced (100-200+ hours)
1. **Production Quality** (50-100 hours)
   - Performance optimization
   - Security best practices
   - Comprehensive testing
   - CI/CD setup

2. **Capstone Project** (50-100+ hours)
   - Complex real-world application
   - Complete architecture
   - Full test coverage
   - Play Store deployment

## Tech Stack Recommendation

```
UI Layer:
- Activities/Fragments (or Jetpack Compose)
- Navigation Component
- Material Design 3

Architecture:
- MVVM with ViewModel
- Repository pattern
- Hilt for DI

Data:
- Room database
- Retrofit for APIs
- DataStore for preferences

Testing:
- JUnit 4/5
- Mockk for mocking
- Espresso for UI tests

DevOps:
- GitHub Actions
- Gradle build automation
- Play Store deployment
```

## Project Structure

```
myapp/
├── app/
│   ├── src/main/
│   │   ├── java/
│   │   │   └── com/example/app/
│   │   │       ├── data/
│   │   │       │   ├── local/
│   │   │       │   ├── remote/
│   │   │       │   └── repository/
│   │   │       ├── domain/
│   │   │       │   ├── model/
│   │   │       │   └── repository/
│   │   │       ├── presentation/
│   │   │       │   ├── ui/
│   │   │       │   └── viewmodel/
│   │   │       └── di/
│   │   └── res/
│   ├── src/test/
│   └── src/androidTest/
├── build.gradle.kts
└── settings.gradle.kts
```

## Best Practices

### Code Quality
✅ Follow SOLID principles
✅ DRY (Don't Repeat Yourself)
✅ KISS (Keep It Simple, Stupid)
✅ Clean code practices
✅ Consistent naming conventions

### Architecture
✅ Separation of concerns
✅ Dependency injection
✅ Repository pattern
✅ Testable design
✅ Single source of truth

### Testing
✅ Unit tests for business logic (70%)
✅ Integration tests (20%)
✅ UI tests (10%)
✅ Mock external dependencies
✅ Aim for 80%+ coverage

### Performance
✅ No memory leaks
✅ Efficient database queries
✅ Proper coroutine scoping
✅ 60+ FPS rendering
✅ Fast app startup

### Security
✅ No hardcoded secrets
✅ HTTPS for all APIs
✅ Encrypted sensitive data
✅ Proper permission handling
✅ Input validation

## Common Mistakes to Avoid

❌ Not understanding lifecycle
❌ Holding context in singletons
❌ Heavy operations on main thread
❌ Memory leaks from listeners
❌ Tight coupling between layers
❌ Skipping tests
❌ Not handling configuration changes
❌ Storing secrets in code

## Development Workflow

1. **Plan**: Design architecture, data models
2. **Setup**: Create project, configure dependencies
3. **Implement**: Build features incrementally
4. **Test**: Write tests while coding
5. **Optimize**: Performance and memory profiling
6. **Polish**: UI/UX refinement
7. **Release**: Build, sign, deploy
8. **Monitor**: Track crashes and analytics

## Tools & Libraries

### Build
- Gradle, Kotlin DSL
- Gradle plugins

### Architecture
- Jetpack (Compose, ViewModel, Room)
- Hilt for DI
- Retrofit for networking

### Testing
- JUnit, MockK, Espresso
- Robolectric for faster tests

### Code Quality
- Lint, Detekt
- SonarQube
- Jacoco for coverage

### CI/CD
- GitHub Actions
- Firebase Test Lab
- Fastlane for automation

## Success Criteria

✅ App runs without crashes
✅ 80%+ test coverage
✅ No memory leaks
✅ Performs at 60 FPS
✅ Follows SOLID principles
✅ Clear code structure
✅ Documented code
✅ Proper error handling
✅ Security reviewed
✅ Published on Play Store

## Resources

- [Android Official Docs](https://developer.android.com)
- [Kotlin Docs](https://kotlinlang.org/docs/)
- [Jetpack Guide](https://developer.android.com/jetpack/guide)
- [Google Codelabs](https://developer.android.com/codelabs)

## Next Steps

1. Choose a learning path (Beginner/Intermediate/Advanced)
2. Follow the tech stack recommendation
3. Use code examples from `/code-examples`
4. Build projects incrementally
5. Test thoroughly
6. Deploy to Play Store
7. Monitor and iterate

---

Ready to build professional Android apps? Start with the learning path above!
