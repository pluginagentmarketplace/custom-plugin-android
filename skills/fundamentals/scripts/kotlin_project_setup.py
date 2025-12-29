#!/usr/bin/env python3
"""
Kotlin/Android Project Setup Script

Creates a clean Kotlin project structure following best practices.

Usage:
    python kotlin_project_setup.py --name MyApp --package com.example.myapp
"""

import os
import argparse
from pathlib import Path
from typing import Dict, List


class KotlinProjectSetup:
    """Sets up a clean Kotlin Android project structure."""

    GRADLE_VERSION = "8.5"
    KOTLIN_VERSION = "1.9.21"
    COMPOSE_BOM = "2024.01.00"
    MIN_SDK = 24
    TARGET_SDK = 34

    def __init__(self, name: str, package: str, output_dir: str = "."):
        self.name = name
        self.package = package
        self.package_path = package.replace(".", "/")
        self.output_dir = Path(output_dir) / name

    def create_structure(self) -> None:
        """Create project directory structure."""
        directories = [
            "app/src/main/kotlin/" + self.package_path,
            "app/src/main/kotlin/" + self.package_path + "/data/repository",
            "app/src/main/kotlin/" + self.package_path + "/data/local",
            "app/src/main/kotlin/" + self.package_path + "/data/remote",
            "app/src/main/kotlin/" + self.package_path + "/domain/model",
            "app/src/main/kotlin/" + self.package_path + "/domain/usecase",
            "app/src/main/kotlin/" + self.package_path + "/ui/theme",
            "app/src/main/kotlin/" + self.package_path + "/ui/components",
            "app/src/main/kotlin/" + self.package_path + "/ui/screens",
            "app/src/main/kotlin/" + self.package_path + "/di",
            "app/src/main/res/values",
            "app/src/test/kotlin/" + self.package_path,
            "app/src/androidTest/kotlin/" + self.package_path,
            "buildSrc/src/main/kotlin",
        ]

        for dir_path in directories:
            (self.output_dir / dir_path).mkdir(parents=True, exist_ok=True)
            print(f"Created: {dir_path}")

    def create_build_files(self) -> None:
        """Create Gradle build files."""
        # Root build.gradle.kts
        root_build = f'''plugins {{
    id("com.android.application") version "8.2.0" apply false
    id("com.android.library") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "{self.KOTLIN_VERSION}" apply false
    id("com.google.dagger.hilt.android") version "2.48" apply false
    id("com.google.devtools.ksp") version "{self.KOTLIN_VERSION}-1.0.15" apply false
}}

tasks.register("clean", Delete::class) {{
    delete(rootProject.layout.buildDirectory)
}}
'''
        self._write_file("build.gradle.kts", root_build)

        # App build.gradle.kts
        app_build = f'''plugins {{
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("com.google.dagger.hilt.android")
    id("com.google.devtools.ksp")
}}

android {{
    namespace = "{self.package}"
    compileSdk = {self.TARGET_SDK}

    defaultConfig {{
        applicationId = "{self.package}"
        minSdk = {self.MIN_SDK}
        targetSdk = {self.TARGET_SDK}
        versionCode = 1
        versionName = "1.0.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }}

    buildTypes {{
        release {{
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }}
    }}

    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }}

    kotlinOptions {{
        jvmTarget = "17"
    }}

    buildFeatures {{
        compose = true
    }}

    composeOptions {{
        kotlinCompilerExtensionVersion = "1.5.7"
    }}
}}

dependencies {{
    // Compose BOM
    val composeBom = platform("androidx.compose:compose-bom:{self.COMPOSE_BOM}")
    implementation(composeBom)
    androidTestImplementation(composeBom)

    // Compose
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    implementation("androidx.navigation:navigation-compose:2.7.6")

    // Hilt
    implementation("com.google.dagger:hilt-android:2.48")
    ksp("com.google.dagger:hilt-compiler:2.48")
    implementation("androidx.hilt:hilt-navigation-compose:1.1.0")

    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")

    // Room
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    ksp("androidx.room:room-compiler:2.6.1")

    // Retrofit
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")

    // Testing
    testImplementation("junit:junit:4.13.2")
    testImplementation("io.mockk:mockk:1.13.8")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    debugImplementation("androidx.compose.ui:ui-tooling")
}}
'''
        self._write_file("app/build.gradle.kts", app_build)

        # settings.gradle.kts
        settings = f'''pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}

dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google()
        mavenCentral()
    }}
}}

rootProject.name = "{self.name}"
include(":app")
'''
        self._write_file("settings.gradle.kts", settings)

    def create_application_class(self) -> None:
        """Create Application class with Hilt."""
        app_class = f'''package {self.package}

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class {self.name}Application : Application()
'''
        self._write_file(
            f"app/src/main/kotlin/{self.package_path}/{self.name}Application.kt",
            app_class
        )

    def create_main_activity(self) -> None:
        """Create MainActivity with Compose."""
        main_activity = f'''package {self.package}

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import dagger.hilt.android.AndroidEntryPoint
import {self.package}.ui.theme.{self.name}Theme

@AndroidEntryPoint
class MainActivity : ComponentActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContent {{
            {self.name}Theme {{
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {{
                    // Navigation or main content here
                }}
            }}
        }}
    }}
}}
'''
        self._write_file(
            f"app/src/main/kotlin/{self.package_path}/MainActivity.kt",
            main_activity
        )

    def create_manifest(self) -> None:
        """Create AndroidManifest.xml."""
        manifest = f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:name=".{self.name}Application"
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{self.name}">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.{self.name}">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
'''
        self._write_file("app/src/main/AndroidManifest.xml", manifest)

    def _write_file(self, path: str, content: str) -> None:
        """Write content to file."""
        file_path = self.output_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        print(f"Created: {path}")

    def setup(self) -> None:
        """Run full project setup."""
        print(f"\n=== Creating {self.name} Android Project ===\n")
        self.create_structure()
        self.create_build_files()
        self.create_application_class()
        self.create_main_activity()
        self.create_manifest()
        print(f"\n=== Project {self.name} created successfully! ===")
        print(f"Location: {self.output_dir.absolute()}")
        print("\nNext steps:")
        print("  1. cd " + str(self.output_dir))
        print("  2. Open in Android Studio")
        print("  3. Sync Gradle and run!")


def main():
    parser = argparse.ArgumentParser(description="Setup Kotlin Android project")
    parser.add_argument("--name", required=True, help="Project name (PascalCase)")
    parser.add_argument("--package", required=True, help="Package name (e.g., com.example.app)")
    parser.add_argument("--output", default=".", help="Output directory")
    args = parser.parse_args()

    setup = KotlinProjectSetup(args.name, args.package, args.output)
    setup.setup()


if __name__ == "__main__":
    main()
