---
name: jetpack-libraries
description: Android Jetpack ecosystem including Room, LiveData, ViewModel, Navigation, and Compose. Use when building modern Android apps with Jetpack components.
---

# Jetpack Libraries Skill

## Quick Start

### ViewModel & LiveData
```kotlin
class UserViewModel : ViewModel() {
    private val _userData = MutableLiveData<User>()
    val userData: LiveData<User> = _userData

    fun loadUser(id: Int) {
        viewModelScope.launch {
            _userData.value = repository.getUser(id)
        }
    }
}
```

### Room Database
```kotlin
@Entity
data class UserEntity(
    @PrimaryKey val id: Int,
    val name: String
)

@Dao
interface UserDao {
    @Query("SELECT * FROM users")
    suspend fun getAllUsers(): List<UserEntity>

    @Insert
    suspend fun insertUser(user: UserEntity)
}

@Database(entities = [UserEntity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
}
```

### Navigation Component
```kotlin
// Navigation graph (nav_graph.xml)
<navigation xmlns:android="http://schemas.android.com/apk/res/android">
    <fragment android:id="@+id/listFragment" />
    <fragment android:id="@+id/detailFragment" />
    <action android:id="@+id/action_list_to_detail" />
</navigation>

// In Fragment
findNavController().navigate(R.id.action_list_to_detail)
```

## Key Libraries

1. **Lifecycle**: Lifecycle-aware components
2. **ViewModel**: UI state management
3. **LiveData**: Observable data
4. **Room**: Database abstraction
5. **Navigation**: Screen navigation
6. **WorkManager**: Background jobs
7. **Hilt**: Dependency injection
8. **DataStore**: Modern preferences

## Best Practices

- Use ViewModel for UI state
- Never hold Context in ViewModel
- Use LiveData for UI updates
- Implement Repository pattern
- Use Hilt for dependency injection
- Prefer Flow over LiveData for complex streams

## Resources

- [Android Jetpack](https://developer.android.com/jetpack)
- [Architecture Guides](https://developer.android.com/jetpack/guide)
