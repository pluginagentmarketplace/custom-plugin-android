# custom-plugin-android

Professional Android development plugin for Claude Code. Complete reference and guidance for building production-grade Android applications.

## Features

### 4 Specialized Agents
- **Kotlin Essentials** - Master modern Kotlin programming
- **Android Core** - Platform fundamentals and lifecycle
- **Jetpack Modern** - Modern Android development libraries
- **Architecture SOLID** - MVVM, Clean Architecture, design patterns

### 3 Interactive Commands
- `/dev-guide` - Complete development best practices
- `/code-examples` - Production-ready code patterns
- `/quick-help` - Fast reference for common tasks

### 4 Invokable Skills
- **kotlin-core** - Kotlin syntax and coroutines
- **jetpack-essential** - ViewModel, LiveData, Room, Navigation
- **architecture-patterns** - MVVM, Repository, SOLID principles
- **android-production** - Testing, performance, security, deployment

## Quick Start

### Installation

```bash
# Load from directory in Claude Code
File → Load Plugin → custom-plugin-android
```

### First Steps

1. **Get oriented:**
   ```
   /dev-guide
   ```

2. **See code examples:**
   ```
   /code-examples
   ```

3. **Quick help on specific topic:**
   ```
   /quick-help
   ```

## Learning Path

### Beginner (100-150 hours)
1. Kotlin Fundamentals (30-40h)
2. Android Core (40-50h)
3. First App Project (30-60h)

### Intermediate (100-150 hours)
1. Jetpack Modern (40-50h)
2. Architecture Patterns (40-50h)
3. Real-World App (20-50h)

### Advanced (100-200+ hours)
1. Production Quality (50-100h)
2. Capstone Project (50-100+h)

## Tech Stack

**UI Layer:**
- Activities/Fragments or Jetpack Compose
- Navigation Component
- Material Design 3

**Architecture:**
- MVVM with ViewModel
- Repository pattern
- Hilt for dependency injection

**Data:**
- Room database
- Retrofit for APIs
- DataStore for preferences

**Testing:**
- JUnit 4/5
- Mockk for mocking
- Espresso for UI tests

**Production:**
- Performance optimization
- Security best practices
- Play Store deployment

## Plugin Structure

```
custom-plugin-android/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── 01-kotlin-essentials.md
│   ├── 02-android-core.md
│   ├── 03-jetpack-modern.md
│   └── 04-architecture-solid.md
├── commands/
│   ├── dev-guide.md
│   ├── code-examples.md
│   └── quick-help.md
├── skills/
│   ├── 01-kotlin-core/SKILL.md
│   ├── 02-jetpack-essential/SKILL.md
│   ├── 03-architecture-patterns/SKILL.md
│   └── 04-android-production/SKILL.md
├── README.md
└── LICENSE
```

## Agents

### Kotlin Essentials
Master Kotlin programming language - essential foundation for Android development.

**Topics:**
- Syntax and language features
- Coroutines and async
- Extension functions
- Functional programming
- Null safety and type system

### Android Core
Learn Android platform fundamentals including Activities, Fragments, lifecycle, and components.

**Topics:**
- Activity and Fragment lifecycle
- Intent system
- Data persistence
- Services and background tasks
- Permissions and security

### Jetpack Modern
Build with Google's recommended Jetpack libraries for modern Android development.

**Topics:**
- ViewModel and LiveData
- Room database
- Navigation Component
- Hilt dependency injection
- WorkManager and DataStore

### Architecture SOLID
Design scalable and maintainable applications with proven architectural patterns.

**Topics:**
- MVVM architecture
- Clean Architecture principles
- Repository pattern
- SOLID principles
- Design patterns for Android
- Testing and security

## Skills

### kotlin-core
Kotlin syntax, coroutines, scope functions, and functional programming patterns.

### jetpack-essential
ViewModel, LiveData, Room, Navigation, Hilt - essential Jetpack libraries.

### architecture-patterns
MVVM, Repository pattern, Dependency injection, and SOLID principles.

### android-production
Testing, performance optimization, security best practices, and Play Store deployment.

## Commands

### /dev-guide
Complete development guide covering:
- Learning paths (beginner → advanced)
- Recommended tech stack
- Project structure
- Best practices
- Development workflow
- Tools and libraries
- Success criteria

### /code-examples
Production-ready code examples for:
- Complete MVVM pattern
- Room database setup
- Repository pattern implementation
- Retrofit networking
- Hilt dependency injection
- Unit testing
- Navigation
- WorkManager
- Secure data storage

### /quick-help
Quick reference for:
- Learning Android development
- Building new apps
- Specific Android tasks
- Common errors
- Performance optimization
- Useful commands
- Resources

## Best Practices Summary

### Architecture
✅ MVVM with ViewModel
✅ Repository pattern for data
✅ Dependency injection with Hilt
✅ Clear separation of concerns
✅ SOLID principles

### Code Quality
✅ Follow clean code principles
✅ Unit test critical logic
✅ UI tests for critical flows
✅ 80%+ test coverage goal
✅ Lint and static analysis

### Performance
✅ No memory leaks
✅ 60+ FPS rendering
✅ Fast app startup (< 5s)
✅ Efficient database queries
✅ Proper coroutine scoping

### Security
✅ No hardcoded secrets
✅ HTTPS for all APIs
✅ Encrypted sensitive data
✅ Proper permission handling
✅ Input validation

## Development Workflow

1. **Plan** - Design architecture and data models
2. **Setup** - Create project and configure dependencies
3. **Implement** - Build features incrementally
4. **Test** - Write tests while coding
5. **Optimize** - Performance and memory profiling
6. **Polish** - UI/UX refinement
7. **Release** - Build, sign, and deploy
8. **Monitor** - Track crashes and analytics

## Common Issues

**"Can't create instance of ViewModel"**
- Add @HiltViewModel annotation
- Ensure constructor parameters are provided

**"Memory leak detected"**
- Unregister listeners in onDestroy()
- Avoid holding Context references
- Use WeakReference when needed

**"ANR - Application Not Responding"**
- Move heavy operations to background thread
- Use coroutines properly
- Profile with Android Profiler

**"Null pointer exception on view"**
- Verify layout file has view with correct ID
- Check view binding is initialized
- Use safe navigation (?.)

## Essential Resources

**Official Documentation:**
- [Android Developer Docs](https://developer.android.com)
- [Kotlin Official Docs](https://kotlinlang.org/docs/)
- [Jetpack Architecture Guide](https://developer.android.com/jetpack/guide)

**Training:**
- [Google Codelabs](https://developer.android.com/codelabs)
- [Android Developers Blog](https://android-developers.googleblog.com)

**Tools:**
- [Android Studio](https://developer.android.com/studio)
- [Firebase Test Lab](https://firebase.google.com/docs/test-lab)
- [Google Play Console](https://play.google.com/console)

## Release Checklist

Before deploying to Google Play:

- ✅ All tests passing
- ✅ No crashes or leaks
- ✅ 60+ FPS rendering
- ✅ Security reviewed
- ✅ Code obfuscated
- ✅ Version code incremented
- ✅ App signed correctly
- ✅ Tested on multiple devices
- ✅ Crash reporting configured
- ✅ Analytics integrated

## Success Metrics

- App runs without crashes
- 80%+ test coverage
- No memory leaks
- 60+ FPS performance
- < 5 second cold start
- Follows SOLID principles
- Clear code structure
- Proper error handling
- Security reviewed
- Published on Play Store

## Contributing

Contributions are welcome! Areas for improvement:
- Additional code examples
- More detailed agents
- Video tutorial links
- Translations
- Additional resources

## License

MIT License - See LICENSE file

## About

This plugin provides professional guidance for Android development using modern best practices, proven architectural patterns, and production-ready code examples.

Built for developers who want to write high-quality, maintainable Android applications.

---

**Ready to build professional Android apps?**

Start with `/dev-guide` or `/quick-help`!
