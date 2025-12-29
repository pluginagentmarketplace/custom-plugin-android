<div align="center">

# Android Development Assistant

### Complete Android Mastery for Claude Code

**Master Kotlin, Jetpack Compose, MVVM architecture, and production deployment with 7 specialized agents and 7 production-ready skills**

[![Verified](https://img.shields.io/badge/Verified-Working-success?style=flat-square&logo=checkmarx)](https://github.com/pluginagentmarketplace/custom-plugin-android)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-blue?style=flat-square)](https://github.com/pluginagentmarketplace/custom-plugin-android)
[![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen?style=flat-square)](https://github.com/pluginagentmarketplace/custom-plugin-android)
[![Agents](https://img.shields.io/badge/Agents-7-orange?style=flat-square)](#agents-overview)
[![Skills](https://img.shields.io/badge/Skills-7-purple?style=flat-square)](#skills-reference)
[![SASMP](https://img.shields.io/badge/SASMP-v1.3.0-blueviolet?style=flat-square)](#)

[![Kotlin](https://img.shields.io/badge/Kotlin-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white)](skills/fundamentals/)
[![Jetpack Compose](https://img.shields.io/badge/Jetpack_Compose-4285F4?style=for-the-badge&logo=jetpackcompose&logoColor=white)](skills/ui/)
[![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)](skills/platform/)
[![Material Design](https://img.shields.io/badge/Material_Design-757575?style=for-the-badge&logo=materialdesign&logoColor=white)](skills/ui/)

[Quick Start](#quick-start) | [Agents](#agents-overview) | [Skills](#skills-reference) | [Commands](#commands)

</div>

---

## Verified Installation

> **This plugin has been tested and verified working on Claude Code.**
> Last verified: December 2025

---

## Quick Start

### Option 1: Install from GitHub (Recommended)

```bash
# Step 1: Add the marketplace from GitHub
/plugin add marketplace pluginagentmarketplace/custom-plugin-android

# Step 2: Install the plugin
/plugin install android-development-assistant@pluginagentmarketplace-android

# Step 3: Restart Claude Code to load new plugins
```

### Option 2: Clone and Load Locally

```bash
# Clone the repository
git clone https://github.com/pluginagentmarketplace/custom-plugin-android.git

# Navigate to the directory in Claude Code
cd custom-plugin-android

# Load the plugin
/plugin load .
```

After loading, restart Claude Code.

### Verify Installation

After restarting Claude Code, verify the plugin is loaded. You should see these agents available:

```
custom-plugin-android:01-fundamentals
custom-plugin-android:02-platform
custom-plugin-android:03-ui-development
custom-plugin-android:04-data-management
custom-plugin-android:05-networking
custom-plugin-android:06-architecture
custom-plugin-android:07-production
```

---

## Available Skills

Once installed, these 7 skills become available:

| Skill | Invoke Command | Description |
|-------|----------------|-------------|
| Kotlin Fundamentals | `Skill("android-development-assistant:kotlin-fundamentals")` | Language essentials, OOP, SOLID |
| Android Platform | `Skill("android-development-assistant:android-platform")` | Components, lifecycle, services |
| UI Design | `Skill("android-development-assistant:ui-design")` | Layouts, Compose, Material Design |
| Data Persistence | `Skill("android-development-assistant:data-persistence")` | Room, SQLite, DataStore |
| API Integration | `Skill("android-development-assistant:api-integration")` | Retrofit, OkHttp, networking |
| App Architecture | `Skill("android-development-assistant:app-architecture")` | MVVM, Clean Architecture |
| Production Quality | `Skill("android-development-assistant:production-quality")` | Testing, security, deployment |

---

## What This Plugin Does

This plugin provides **7 specialized agents** and **7 production-ready skills** covering 757+ hours of Android development content:

| Agent | Hours | Purpose |
|-------|-------|---------|
| **Fundamentals** | 172h | Kotlin, OOP, SOLID, algorithms |
| **Platform** | 78h | Activities, Fragments, Services, lifecycle |
| **UI Development** | 235h | Layouts, Compose, Material Design |
| **Data Management** | 62h | Room, SQLite, DataStore |
| **Networking** | 75h | Retrofit, OkHttp, APIs |
| **Architecture** | 40h | MVVM, Clean Architecture |
| **Production** | 95h | Testing, security, deployment |

---

## Agents Overview

### 7 Implementation Agents

Each agent is designed to **do the work**, not just explain:

| Agent | Capabilities | Example Prompts |
|-------|--------------|-----------------|
| **Fundamentals** | Kotlin syntax, coroutines, null safety | `"Explain coroutines"`, `"SOLID principles"` |
| **Platform** | Activities, Fragments, Services | `"Activity lifecycle"`, `"Intent handling"` |
| **UI Development** | Layouts, Compose, Material 3 | `"Create Compose UI"`, `"ConstraintLayout"` |
| **Data Management** | Room, DataStore, encryption | `"Room database"`, `"DataStore migration"` |
| **Networking** | Retrofit, OkHttp, caching | `"Setup Retrofit"`, `"API error handling"` |
| **Architecture** | MVVM, Clean Architecture, DI | `"MVVM pattern"`, `"Hilt injection"` |
| **Production** | Testing, ProGuard, Play Store | `"Unit testing"`, `"App signing"` |

---

## Commands

3 interactive commands for Android development workflows:

| Command | Usage | Description |
|---------|-------|-------------|
| `/roadmap` | `/roadmap` | View 7-step learning path with timeline |
| `/agent-guide` | `/agent-guide` | Detailed guide to all 7 agents |
| `/quick-start` | `/quick-start` | Essential resources and quick solutions |

---

## Skills Reference

Each skill includes **Golden Format** content:
- `assets/` - Configuration templates and setup files
- `scripts/` - Automation and validation scripts
- `references/` - Methodology guides and best practices

### All 7 Skills by Category

| Category | Skills |
|----------|--------|
| **Language** | kotlin-fundamentals |
| **Platform** | android-platform |
| **UI** | ui-design |
| **Data** | data-persistence |
| **Network** | api-integration |
| **Architecture** | app-architecture |
| **Production** | production-quality |

---

## Usage Examples

### Example 1: Create Jetpack Compose UI

```kotlin
// Before: XML layouts

// After (with UI Development agent):
Skill("android-development-assistant:ui-design")

// Generates:
// - Compose component structure
// - Material 3 theming
// - State management
// - Preview annotations
```

### Example 2: Setup Room Database

```kotlin
// Before: Manual SQLite

// After (with Data Management agent):
Skill("android-development-assistant:data-persistence")

// Provides:
// - Entity definitions
// - DAO interfaces
// - Database setup
// - Migration strategies
```

### Example 3: Implement MVVM Architecture

```kotlin
// Before: No architecture

// After (with Architecture agent):
Skill("android-development-assistant:app-architecture")

// Creates:
// - ViewModel setup
// - Repository pattern
// - Use cases
// - Hilt dependency injection
```

---

## Plugin Structure

```
custom-plugin-android/
├── .claude-plugin/
│   ├── plugin.json           # Plugin manifest
│   └── marketplace.json      # Marketplace config
├── agents/                   # 7 specialized agents
│   ├── 01-fundamentals.md
│   ├── 02-platform.md
│   ├── 03-ui-development.md
│   ├── 04-data-management.md
│   ├── 05-networking.md
│   ├── 06-architecture.md
│   └── 07-production.md
├── skills/                   # 7 skills (Golden Format)
│   ├── fundamentals/SKILL.md
│   ├── platform/SKILL.md
│   ├── ui/SKILL.md
│   ├── data/SKILL.md
│   ├── networking/SKILL.md
│   ├── architecture/SKILL.md
│   └── production/SKILL.md
├── commands/                 # 3 slash commands
│   ├── roadmap.md
│   ├── agent-guide.md
│   └── quick-start.md
├── hooks/hooks.json
├── README.md
├── CHANGELOG.md
└── LICENSE
```

---

## Technology Coverage

| Category | Technologies |
|----------|--------------|
| **Language** | Kotlin 1.9+, Coroutines, Flow |
| **UI** | Jetpack Compose, Material 3, ConstraintLayout |
| **Data** | Room, SQLite, DataStore, SharedPreferences |
| **Network** | Retrofit, OkHttp, Ktor, GraphQL |
| **DI** | Hilt, Koin, Dagger |
| **Architecture** | MVVM, MVI, Clean Architecture |
| **Testing** | JUnit, Espresso, Mockito, Compose Testing |
| **Security** | EncryptedSharedPreferences, SSL Pinning |

---

## Learning Paths

| Path | Duration | Focus |
|------|----------|-------|
| **Total** | 37-45 weeks | Complete Android mastery |
| @ 2 hours/day | 45+ weeks | Beginner friendly |
| @ 3 hours/day | 30+ weeks | Balanced approach |
| @ 4 hours/day | 19-24 weeks | Accelerated learning |

### Recommended Sequence
1. Fundamentals (8-10 weeks)
2. Platform (4-5 weeks)
3. UI Development (10-12 weeks)
4. Data Management (3-4 weeks)
5. Networking (4-5 weeks)
6. Architecture (2-3 weeks)
7. Production (5-6 weeks)

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Android Studio | 2022.1+ |
| Gradle | 7.0+ |
| Kotlin | 1.8+ |
| Android SDK | 24+ (min API) |
| Java | 11+ |

---

## Best Practices

- **SOLID Principles**: Applied in every agent
- **Testing**: Unit, integration, and UI testing
- **Security**: Encryption, HTTPS, permissions
- **Performance**: Memory, battery, startup optimization
- **Architecture**: MVVM, Clean Architecture patterns
- **Modern APIs**: AndroidX, Jetpack, Kotlin coroutines

---

## Metadata

| Field | Value |
|-------|-------|
| **Last Updated** | 2025-12-28 |
| **Maintenance Status** | Active |
| **SASMP Version** | 1.3.0 |
| **Support** | [Issues](../../issues) |

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Contributing

Contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Follow the Golden Format for new skills
4. Submit a pull request

---

## Contributors

**Authors:**
- **Dr. Umit Kacar** - Senior AI Researcher & Engineer
- **Muhsin Elcicek** - Senior Software Architect

---

<div align="center">

**Master Android development with AI assistance!**

[![Made for Android](https://img.shields.io/badge/Made%20for-Android%20Developers-3DDC84?style=for-the-badge&logo=android)](https://github.com/pluginagentmarketplace/custom-plugin-android)

**Built by Dr. Umit Kacar & Muhsin Elcicek**

*Based on [roadmap.sh/android](https://roadmap.sh/android)*

</div>
