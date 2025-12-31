<div align="center">

<!-- Animated Typing Banner -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=1000&color=2E9EF7&center=true&vCenter=true&multiline=true&repeat=true&width=600&height=100&lines=Android+Assistant;7+Agents+%7C+7+Skills;Claude+Code+Plugin" alt="Android Assistant" />

<br/>

<!-- Badge Row 1: Status Badges -->
[![Version](https://img.shields.io/badge/Version-2.0.0-blue?style=for-the-badge)](https://github.com/pluginagentmarketplace/custom-plugin-android/releases)
[![License](https://img.shields.io/badge/License-Custom-yellow?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen?style=for-the-badge)](#)
[![SASMP](https://img.shields.io/badge/SASMP-v1.3.0-blueviolet?style=for-the-badge)](#)

<!-- Badge Row 2: Content Badges -->
[![Agents](https://img.shields.io/badge/Agents-7-orange?style=flat-square&logo=robot)](#-agents)
[![Skills](https://img.shields.io/badge/Skills-7-purple?style=flat-square&logo=lightning)](#-skills)
[![Commands](https://img.shields.io/badge/Commands-6-green?style=flat-square&logo=terminal)](#-commands)

<br/>

<!-- Quick CTA Row -->
[📦 **Install Now**](#-quick-start) · [🤖 **Explore Agents**](#-agents) · [📖 **Documentation**](#-documentation) · [⭐ **Star this repo**](https://github.com/pluginagentmarketplace/custom-plugin-android)

---

### What is this?

> **Android Assistant** is a Claude Code plugin with **7 agents** and **7 skills** for android development.

</div>

---

## 📑 Table of Contents

<details>
<summary>Click to expand</summary>

- [Quick Start](#-quick-start)
- [Features](#-features)
- [Agents](#-agents)
- [Skills](#-skills)
- [Commands](#-commands)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

</details>

---

## 🚀 Quick Start

### Prerequisites

- Claude Code CLI v2.0.27+
- Active Claude subscription

### Installation (Choose One)

<details open>
<summary><strong>Option 1: From Marketplace (Recommended)</strong></summary>

```bash
# Step 1️⃣ Add the marketplace
/plugin add marketplace pluginagentmarketplace/custom-plugin-android

# Step 2️⃣ Install the plugin
/plugin install android-development-assistant@pluginagentmarketplace-android

# Step 3️⃣ Restart Claude Code
# Close and reopen your terminal/IDE
```

</details>

<details>
<summary><strong>Option 2: Local Installation</strong></summary>

```bash
# Clone the repository
git clone https://github.com/pluginagentmarketplace/custom-plugin-android.git
cd custom-plugin-android

# Load locally
/plugin load .

# Restart Claude Code
```

</details>

### ✅ Verify Installation

After restart, you should see these agents:

```
android-development-assistant:01-kotlin-essentials
android-development-assistant:04-architecture-solid
android-development-assistant:01-fundamentals
android-development-assistant:02-android-core
android-development-assistant:05-networking
... and 7 more
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **7 Agents** | Specialized AI agents for android tasks |
| 🛠️ **7 Skills** | Reusable capabilities with Golden Format |
| ⌨️ **6 Commands** | Quick slash commands |
| 🔄 **SASMP v1.3.0** | Full protocol compliance |

---

## 🤖 Agents

### 7 Specialized Agents

| # | Agent | Purpose |
|---|-------|---------|
| 1 | **01-kotlin-essentials** | Master Kotlin language fundamentals, syntax, coroutines, and |
| 2 | **04-architecture-solid** | MVVM, Clean Architecture, SOLID principles, design patterns, |
| 3 | **01-fundamentals** | Kotlin & Java programming fundamentals, OOP, SOLID principle |
| 4 | **02-android-core** | Android platform fundamentals - Activities, Fragments, lifec |
| 5 | **05-networking** | API Integration & Networking - Retrofit, OkHttp, REST APIs,  |
| 6 | **03-jetpack-modern** | Modern Android development with Jetpack libraries - ViewMode |
| 7 | **06-architecture** | Architecture & Design Patterns - MVVM, Clean Architecture, R |
| 8 | **04-data-management** | Data Persistence & Storage - Room ORM, SQLite, DataStore, en |
| 9 | **data-management-storage** | Android'de veri depolama ve yönetimi için kapsamlı bir rehbe |
| 10 | **02-platform** | Android core components - Activities, Fragments, Services, L |
| ... | **+2 more** | See agents/ directory |

---

## 🛠️ Skills

### Available Skills

| Skill | Description | Invoke |
|-------|-------------|--------|
| `ui` | XML layouts, ConstraintLayout, Jetpack Compose, Material Des | `Skill("android-development-assistant:ui")` |
| `fundamentals` | Master Kotlin syntax, OOP principles, SOLID practices, funct | `Skill("android-development-assistant:fundamentals")` |
| `networking` | Retrofit, OkHttp, REST APIs, JSON serialization, network sec | `Skill("android-development-assistant:networking")` |
| `platform` | Android core components lifecycle, Activities, Fragments, Se | `Skill("android-development-assistant:platform")` |
| `03-architecture-patterns` | MVVM, Repository pattern, Dependency injection, SOLID princi | `Skill("android-development-assistant:03-architecture-patterns")` |
| `architecture` | MVVM pattern, Clean Architecture, Repository pattern, depend | `Skill("android-development-assistant:architecture")` |
| `02-jetpack-essential` | ViewModel, LiveData, Room database, Navigation Component, Hi | `Skill("android-development-assistant:02-jetpack-essential")` |
| `04-android-production` | Testing, performance optimization, security, and Play Store  | `Skill("android-development-assistant:04-android-production")` |
| `production` | Unit testing, performance optimization, security implementat | `Skill("android-development-assistant:production")` |
| `01-kotlin-core` | Kotlin syntax, coroutines, scope functions, and functional p | `Skill("android-development-assistant:01-kotlin-core")` |
| ... | +1 more | See skills/ directory |

---

## ⌨️ Commands

| Command | Description |
|---------|-------------|
| `/code-examples` | examples - Real-World Code Examples |
| `/dev-guide` | guide - Android Development Guide |
| `/quick-start` | start - Quick Start Guide |
| `/quick-help` | help - Quick Help for Common Tasks |
| `/agent-guide` | guide - Complete Agent Guide |
| `/roadmap` | Android Development Roadmap |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [LICENSE](LICENSE) | License information |

---

## 📁 Project Structure

<details>
<summary>Click to expand</summary>

```
custom-plugin-android/
├── 📁 .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── 📁 agents/              # 7 agents
├── 📁 skills/              # 7 skills (Golden Format)
├── 📁 commands/            # 6 commands
├── 📁 hooks/
├── 📄 README.md
├── 📄 CHANGELOG.md
└── 📄 LICENSE
```

</details>

---

## 📅 Metadata

| Field | Value |
|-------|-------|
| **Version** | 2.0.0 |
| **Last Updated** | 2025-12-29 |
| **Status** | Production Ready |
| **SASMP** | v1.3.0 |
| **Agents** | 7 |
| **Skills** | 7 |
| **Commands** | 6 |

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

1. Fork the repository
2. Create your feature branch
3. Follow the Golden Format for new skills
4. Submit a pull request

---

## ⚠️ Security

> **Important:** This repository contains third-party code and dependencies.
>
> - ✅ Always review code before using in production
> - ✅ Check dependencies for known vulnerabilities
> - ✅ Follow security best practices
> - ✅ Report security issues privately via [Issues](../../issues)

---

## 📝 License

Copyright © 2025 **Dr. Umit Kacar** & **Muhsin Elcicek**

Custom License - See [LICENSE](LICENSE) for details.

---

## 👥 Contributors

<table>
<tr>
<td align="center">
<strong>Dr. Umit Kacar</strong><br/>
Senior AI Researcher & Engineer
</td>
<td align="center">
<strong>Muhsin Elcicek</strong><br/>
Senior Software Architect
</td>
</tr>
</table>

---

<div align="center">

**Made with ❤️ for the Claude Code Community**

[![GitHub](https://img.shields.io/badge/GitHub-pluginagentmarketplace-black?style=for-the-badge&logo=github)](https://github.com/pluginagentmarketplace)

</div>
