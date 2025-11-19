# /agent-guide - Complete Agent Guide

Detailed guide to all 7 specialized agents in custom-plugin-android.

## 7 Agents Overview

### 🎯 Agent 1: Fundamentals
**Focus:** Kotlin, OOP, SOLID principles, algorithms
**Learning Hours:** 172 | **Level:** Beginner → Intermediate

**Topics Covered:**
- Kotlin language features (syntax, null safety, coroutines)
- Object-oriented programming (inheritance, polymorphism, abstraction)
- SOLID principles (5 principles with examples)
- Functional programming (lambdas, higher-order functions)
- Data structures (arrays, lists, maps, sets)
- Algorithms and complexity analysis

**Key Skills:** Write idiomatic Kotlin, understand OOP deeply, apply SOLID

---

### 📱 Agent 2: Platform  
**Focus:** Android components, lifecycle, services, permissions
**Learning Hours:** 78 | **Level:** Beginner → Intermediate

**Topics Covered:**
- Activities (lifecycle, back stack, state saving)
- Fragments (lifecycle, communication, transactions)
- Services (started, bound, foreground types)
- Intent system (explicit, implicit, filters, data passing)
- BroadcastReceiver (system, local, ordered broadcasts)
- Permissions (normal, dangerous, runtime requests)
- Process lifecycle (foreground, background, death handling)

**Key Skills:** Master component lifecycle, handle configuration changes, manage permissions

---

### 🎨 Agent 3: UI Development
**Focus:** Layouts, ConstraintLayout, Compose, Material Design
**Learning Hours:** 235 | **Level:** Intermediate → Advanced

**Topics Covered:**
- XML Layouts (LinearLayout, RelativeLayout, GridLayout, FrameLayout)
- ConstraintLayout (constraints, chains, guidelines, barriers, bias)
- Jetpack Compose (composables, state management, modifiers)
- Material Design 3 (components, theming, typography, icons)
- RecyclerView (adapters, view holders, optimization)
- Responsive design (screen qualifiers, dimension resources)
- Accessibility (touch targets, semantics, color contrast)

**Key Skills:** Design responsive UIs, implement Compose, apply Material Design

---

### 💾 Agent 4: Data Management
**Focus:** Room, SQLite, SharedPreferences, DataStore, encryption
**Learning Hours:** 62 | **Level:** Intermediate

**Topics Covered:**
- Room ORM (entities, DAOs, relationships, migrations)
- SQLite (direct queries, transactions, indexing)
- SharedPreferences (basic and encrypted versions)
- DataStore (preferences and proto DataStore)
- Data encryption (EncryptedFile, encrypted preferences)
- Transactions and atomic operations
- Database testing (in-memory databases)

**Key Skills:** Design database schemas, use Room correctly, encrypt sensitive data

---

### 🌐 Agent 5: Networking
**Focus:** Retrofit, OkHttp, REST APIs, network security
**Learning Hours:** 75 | **Level:** Intermediate

**Topics Covered:**
- REST API concepts (HTTP methods, status codes, design)
- Retrofit (interfaces, annotations, error handling, adapters)
- OkHttp (client configuration, interceptors, timeouts)
- JSON serialization (GSON, Moshi, annotations)
- Error handling and retry logic
- SSL/TLS and certificate pinning
- Network security best practices
- Network monitoring and optimization

**Key Skills:** Integrate APIs, secure network communication, handle errors

---

### 🏗️ Agent 6: Architecture
**Focus:** MVVM, Clean Architecture, Repository, SOLID
**Learning Hours:** 40 | **Level:** Advanced

**Topics Covered:**
- MVVM pattern (Model, View, ViewModel integration)
- Clean Architecture (4 layers, dependency direction)
- Repository pattern (data abstraction, multi-source)
- SOLID principles (implementation examples)
- Design patterns (factory, observer, strategy, adapter)
- Dependency injection (Hilt, modules)
- Testable architecture
- Layer separation and communication

**Key Skills:** Design scalable apps, implement enterprise patterns, apply SOLID

---

### 🚀 Agent 7: Production
**Focus:** Testing, Performance, Security, Deployment
**Learning Hours:** 95 | **Level:** Advanced

**Topics Covered:**
- Unit testing (JUnit, Mockito, test coverage)
- UI testing (Espresso, automation)
- Performance optimization (memory, battery, frame rate, APK size)
- Memory leak detection and prevention
- Security (encryption, SSL pinning, OWASP Top 10)
- Code obfuscation (ProGuard/R8)
- Play Store deployment (tracks, rollout, review process)
- Crash analytics and production monitoring

**Key Skills:** Write comprehensive tests, optimize apps, deploy professionally

---

## How to Use Agents

### For Learning
1. Choose starting agent based on your level
2. Study concepts thoroughly
3. Implement examples
4. Move to next agent sequentially

### For Reference
- Look up specific agent when needed
- Use agent skills for detailed reference
- Search agent content for solutions

### For Projects
- Apply multiple agents' knowledge
- Combine patterns and practices
- Build production-ready apps

---

## Agent Dependencies

```
1. Fundamentals
    ↓
2. Platform
    ↓
3. UI Development + 4. Data Management + 5. Networking
    ↓
6. Architecture (combines all above)
    ↓
7. Production (applies all)
```

## Quick Reference

| Need | Agent | Skill |
|------|-------|-------|
| Kotlin code | Fundamentals | kotlin-fundamentals |
| Activity/Fragment | Platform | android-platform |
| UI layouts | UI Development | ui-design |
| Database | Data Management | data-persistence |
| API calls | Networking | api-integration |
| App design | Architecture | app-architecture |
| Testing/Deploy | Production | production-quality |

---

Use `/quick-start` for immediate help with common tasks.
