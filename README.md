# Android Development Plugin for Claude Code

🚀 **Professional-grade Android development learning and reference plugin for Claude Code**

A comprehensive plugin providing structured learning paths, expert agents, and hands-on projects for mastering Android development from beginner to expert level.

## Features

### 📚 7 Specialized Agents

1. **Kotlin Fundamentals** - Master modern Kotlin programming
2. **Android Basics** - Learn platform fundamentals and lifecycle
3. **Jetpack Suite** - Modern Android libraries and architecture
4. **Architecture Patterns** - MVVM, Clean Architecture, design patterns
5. **Testing & Quality** - Comprehensive testing strategies
6. **Performance Optimization** - Memory, battery, and rendering optimization
7. **Security & Deployment** - Secure development and Play Store deployment

### 🎯 4 Interactive Slash Commands

- `/learn` - Guided learning paths (beginner → intermediate → advanced)
- `/browse-agent` - Explore all agents and their capabilities
- `/assess` - Knowledge assessment questionnaire (100 questions)
- `/projects` - 50+ hands-on projects by difficulty level

### 💾 7 Invokable Skills

- **kotlin-programming** - Kotlin syntax and features
- **jetpack-libraries** - Jetpack ecosystem guide
- **app-architecture** - Architectural patterns guide
- **android-testing** - Testing strategies guide
- **performance-tuning** - Performance optimization guide
- **app-security** - Security best practices guide
- **app-deployment** - Deployment and release guide

### 🎓 Learning Paths

**Beginner Track (150 hours)**
- Kotlin fundamentals
- Android basics
- Jetpack essentials
- First complete app

**Intermediate Track (200 hours)**
- Advanced Kotlin
- Advanced Android
- Architecture & design
- Jetpack advanced
- Testing strategies
- Integration projects

**Advanced Track (200+ hours)**
- Performance mastery
- Security expertise
- Advanced architecture
- Deployment & CI/CD
- Specializations
- Capstone projects

### 📋 50+ Hands-On Projects

| Level | Projects | Duration |
|-------|----------|----------|
| Beginner | 10 projects | 2-7 hours each |
| Intermediate | 15 projects | 15-35 hours each |
| Advanced | 15 projects | 35-80 hours each |
| Expert | 10 projects | 60-140 hours each |

## Quick Start

### Installation

#### Option 1: Local Directory
```bash
# Clone the repository
git clone https://github.com/pluginagentmarketplace/custom-plugin-android.git

# Load in Claude Code
# File → Load Plugin → custom-plugin-android (choose directory)
```

#### Option 2: Add from Marketplace
```bash
# In Claude Code
Plugin Marketplace → Search "Android Development" → Add Plugin
```

### First Steps

1. **Learn about your skill level:**
   ```
   /assess
   ```

2. **Choose a learning path:**
   ```
   /learn
   ```

3. **Explore available agents:**
   ```
   /browse-agent
   ```

4. **Find projects to build:**
   ```
   /projects
   ```

## Plugin Structure

```
custom-plugin-android/
├── .claude-plugin/
│   └── plugin.json                  # Plugin manifest
│
├── agents/                          # 7 Specialized agents
│   ├── 01-kotlin-fundamentals.md
│   ├── 02-android-basics.md
│   ├── 03-jetpack-suite.md
│   ├── 04-architecture-patterns.md
│   ├── 05-testing-quality.md
│   ├── 06-performance-optimization.md
│   └── 07-security-deployment.md
│
├── commands/                        # 4 Slash commands
│   ├── learn.md
│   ├── browse-agent.md
│   ├── assess.md
│   └── projects.md
│
├── skills/                          # 7 Invokable skills
│   ├── kotlin/SKILL.md
│   ├── jetpack/SKILL.md
│   ├── architecture/SKILL.md
│   ├── testing/SKILL.md
│   ├── performance/SKILL.md
│   ├── security/SKILL.md
│   └── deployment/SKILL.md
│
├── hooks/
│   └── hooks.json                   # Automation hooks
│
├── README.md                        # This file
└── LICENSE
```

## Command Reference

### /learn
Start your structured Android development journey.

**Usage:**
```
/learn                          # Show all learning paths
/learn beginner                 # Beginner path details
/learn intermediate             # Intermediate path details
/learn advanced                 # Advanced path details
```

### /browse-agent
Explore all 7 Android development agents.

**Usage:**
```
/browse-agent                   # List all agents
/browse-agent kotlin            # Kotlin agent details
/browse-agent android           # Android Basics agent
/browse-agent jetpack           # Jetpack Suite agent
/browse-agent architecture      # Architecture agent
/browse-agent testing           # Testing agent
/browse-agent performance       # Performance agent
/browse-agent security          # Security & Deployment agent
```

### /assess
Evaluate your Android knowledge (100 questions).

**Usage:**
```
/assess                         # Start assessment
/assess results                 # View assessment results
/assess report                  # Get detailed report
```

### /projects
Find hands-on projects by difficulty and interest.

**Usage:**
```
/projects                       # Show all projects
/projects beginner              # Beginner projects
/projects intermediate          # Intermediate projects
/projects advanced              # Advanced projects
/projects expert                # Expert projects
```

## Learning Content

### Total Content

- **1000+ hours** of learning material
- **100+ code examples** across all topics
- **7 specialized agents** covering different areas
- **50+ real-world projects**
- **100+ self-assessment questions**
- **Comprehensive documentation**

### Topics Covered

#### Kotlin Programming
- Syntax and language features
- Object-oriented programming
- Functional programming
- Coroutines and async
- Extension functions
- Type system and generics

#### Android Fundamentals
- Activities and lifecycle
- Fragments
- Intent system
- Layouts and views
- Data persistence
- Background tasks
- Permissions

#### Modern Android (Jetpack)
- ViewModel and LiveData
- Room database
- Navigation Component
- WorkManager
- DataStore
- Hilt dependency injection
- Jetpack Compose

#### Architecture & Design
- MVVM architecture
- Clean Architecture
- Repository pattern
- Dependency injection
- Design patterns
- Layer separation
- Testable architecture

#### Testing & Quality
- Unit testing
- Instrumentation testing
- Mocking and stubbing
- Test fixtures
- UI testing with Espresso
- Code coverage
- Test best practices

#### Performance Optimization
- Memory management
- Memory leak detection
- Battery optimization
- Rendering performance
- App startup optimization
- Profiling tools
- Performance monitoring

#### Security & Deployment
- Secure data storage
- Encryption
- Authentication
- Authorization
- Network security
- Code signing
- Play Store deployment
- CI/CD pipelines

## Using Skills

Skills are automatically invoked when relevant but can also be manually accessed:

```
# Kotlin programming help
claude help me with kotlin coroutines
# → kotlin-programming skill invoked

# Jetpack libraries reference
I need to use Room database
# → jetpack-libraries skill invoked

# Architecture guidance
How should I structure my app?
# → app-architecture skill invoked

# Testing strategies
I want to write better tests
# → android-testing skill invoked

# Performance optimization
My app is using too much memory
# → performance-tuning skill invoked

# Security implementation
How do I encrypt sensitive data?
# → app-security skill invoked

# Deployment process
How do I deploy to Google Play?
# → app-deployment skill invoked
```

## Recommended Learning Order

### For Complete Beginners
1. Kotlin Fundamentals (30-40 hours)
2. Android Basics (40-50 hours)
3. Build simple projects (20-30 hours)
4. Jetpack Suite (50-60 hours)
5. Intermediate projects (40-50 hours)

### For Intermediate Developers
1. Architecture Patterns (60-70 hours)
2. Testing & Quality (50-60 hours)
3. Advanced Jetpack (40-50 hours)
4. Real-world projects (40-50 hours)

### For Advanced Developers
1. Performance Optimization (50-60 hours)
2. Security & Deployment (50-60 hours)
3. Advanced projects (60-100+ hours)
4. Specializations and expert projects

## Assessment Criteria

Each agent includes comprehensive assessment criteria to help you:
- Evaluate your current skill level
- Identify knowledge gaps
- Track progress
- Focus on weak areas
- Prepare for professional development

## Project Showcase

Build portfolio-ready projects:
- Todo list app (20-30 hours)
- E-commerce platform (50-70 hours)
- Social network (40-60 hours)
- News reader app (18-25 hours)
- Real estate app (40-60 hours)
- And 45+ more!

## Best Practices Throughout

The plugin emphasizes:
- ✅ Clean code principles
- ✅ SOLID principles
- ✅ Design patterns
- ✅ Test-driven development
- ✅ Security best practices
- ✅ Performance optimization
- ✅ Professional workflows

## Resources & References

### Official Documentation
- [Android Official Docs](https://developer.android.com)
- [Kotlin Documentation](https://kotlinlang.org/docs/)
- [Jetpack Architecture Guides](https://developer.android.com/jetpack/guide)

### Learning Platforms
- [Google Codelabs](https://developer.android.com/codelabs)
- [Android Developers Blog](https://android-developers.googleblog.com)
- [Kotlin Playground](https://play.kotlinlang.org/)

### Community
- [r/androiddev](https://reddit.com/r/androiddev)
- [Android Discord Community](https://discord.gg/android)
- [Stack Overflow - Android Tag](https://stackoverflow.com/questions/tagged/android)

## Plugin Information

- **Version:** 1.0.0
- **Last Updated:** November 2024
- **Compatibility:** Claude Code
- **Repository:** [GitHub](https://github.com/pluginagentmarketplace/custom-plugin-android)
- **License:** MIT

## Contributing

Contributions are welcome! To improve this plugin:

1. Fork the repository
2. Create a feature branch
3. Make improvements
4. Submit a pull request

### Areas for Contribution
- Additional projects
- Expanded agent content
- Code examples and snippets
- Video tutorials links
- External resource links
- Translations

## Support & Feedback

- **Issues:** [GitHub Issues](https://github.com/pluginagentmarketplace/custom-plugin-android/issues)
- **Discussions:** [GitHub Discussions](https://github.com/pluginagentmarketplace/custom-plugin-android/discussions)
- **Feedback:** Use `/feedback` command in Claude Code

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Android team for excellent documentation
- Jetpack team for modern libraries
- Community for contributing examples
- Claude Code for the plugin platform

---

## Quick Tips

1. **Start small:** Don't try to learn everything at once
2. **Build projects:** Apply concepts with hands-on projects
3. **Read documentation:** Official docs are comprehensive
4. **Ask questions:** Use Claude Code to explore topics deeply
5. **Practice daily:** Consistency beats marathon sessions
6. **Join community:** Connect with other Android developers
7. **Stay updated:** Follow Android releases and best practices

---

**Ready to master Android development?** 🚀

Start with `/learn` or `/assess` right now!

---

Made with ❤️ for Android developers everywhere.
