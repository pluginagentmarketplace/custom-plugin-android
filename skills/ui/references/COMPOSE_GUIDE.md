# Jetpack Compose Complete Guide

Modern declarative UI toolkit for Android.

## Core Concepts

### Composable Functions
```kotlin
@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello, $name!",
        modifier = modifier
    )
}
```

### State Management
```kotlin
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }

    Column {
        Text("Count: $count")
        Button(onClick = { count++ }) {
            Text("Increment")
        }
    }
}
```

### State Hoisting
```kotlin
// Stateless - reusable
@Composable
fun Counter(
    count: Int,
    onIncrement: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier) {
        Text("Count: $count")
        Button(onClick = onIncrement) {
            Text("Increment")
        }
    }
}

// Stateful - holds state
@Composable
fun CounterScreen() {
    var count by remember { mutableStateOf(0) }
    Counter(count, onIncrement = { count++ })
}
```

## Layout System

### Basic Layouts
```kotlin
// Vertical arrangement
Column(
    modifier = Modifier.fillMaxSize(),
    verticalArrangement = Arrangement.Center,
    horizontalAlignment = Alignment.CenterHorizontally
) {
    Text("First")
    Text("Second")
}

// Horizontal arrangement
Row(
    modifier = Modifier.fillMaxWidth(),
    horizontalArrangement = Arrangement.SpaceBetween
) {
    Text("Left")
    Text("Right")
}

// Stacking
Box(contentAlignment = Alignment.Center) {
    Image(...)
    Text("Overlay")
}
```

### Lazy Lists
```kotlin
LazyColumn {
    items(users) { user ->
        UserCard(user)
    }

    item {
        Text("Footer")
    }

    itemsIndexed(items) { index, item ->
        Text("$index: $item")
    }
}
```

## Modifier Chain

```kotlin
Text(
    text = "Hello",
    modifier = Modifier
        .fillMaxWidth()
        .padding(16.dp)
        .background(Color.LightGray, RoundedCornerShape(8.dp))
        .clickable { onClick() }
        .padding(8.dp)  // Inner padding
)
```

### Common Modifiers
| Modifier | Purpose |
|----------|---------|
| `fillMaxSize()` | Fill parent |
| `size(width, height)` | Fixed size |
| `padding()` | Add spacing |
| `background()` | Background color/shape |
| `clickable()` | Handle clicks |
| `border()` | Add border |
| `weight()` | Proportional sizing |

## Material Design 3

### Theme Setup
```kotlin
@Composable
fun MyAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) darkColorScheme() else lightColorScheme()

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
```

### Common Components
```kotlin
// Buttons
Button(onClick = {}) { Text("Filled") }
OutlinedButton(onClick = {}) { Text("Outlined") }
TextButton(onClick = {}) { Text("Text") }
FloatingActionButton(onClick = {}) { Icon(Icons.Add, "Add") }

// Cards
Card(elevation = CardDefaults.cardElevation(4.dp)) {
    Column(Modifier.padding(16.dp)) {
        Text("Card Title", style = MaterialTheme.typography.titleLarge)
        Text("Card content")
    }
}

// Text Fields
var text by remember { mutableStateOf("") }
OutlinedTextField(
    value = text,
    onValueChange = { text = it },
    label = { Text("Email") },
    leadingIcon = { Icon(Icons.Email, null) }
)
```

## Navigation

```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(navController, startDestination = "home") {
        composable("home") {
            HomeScreen(
                onNavigateToDetail = { id ->
                    navController.navigate("detail/$id")
                }
            )
        }
        composable(
            route = "detail/{id}",
            arguments = listOf(navArgument("id") { type = NavType.IntType })
        ) { backStackEntry ->
            DetailScreen(
                id = backStackEntry.arguments?.getInt("id") ?: 0,
                onBack = { navController.popBackStack() }
            )
        }
    }
}
```

## Side Effects

```kotlin
// Run once when composable enters composition
LaunchedEffect(Unit) {
    viewModel.loadData()
}

// Run when key changes
LaunchedEffect(userId) {
    viewModel.loadUser(userId)
}

// Cleanup on dispose
DisposableEffect(lifecycle) {
    val observer = LifecycleEventObserver { _, event -> }
    lifecycle.addObserver(observer)
    onDispose {
        lifecycle.removeObserver(observer)
    }
}

// Remember across recompositions
val derivedValue = remember(input) {
    expensiveCalculation(input)
}
```

## Best Practices

### 1. Performance
```kotlin
// ✅ Stable parameters
@Composable
fun UserCard(user: User)  // Data class = stable

// ❌ Unstable parameters trigger recomposition
@Composable
fun UserCard(users: List<User>)  // List = unstable

// ✅ Make stable
@Composable
fun UserCard(users: ImmutableList<User>)
```

### 2. Reusability
```kotlin
// ✅ Accept Modifier as parameter
@Composable
fun CustomButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier  // First optional param
)

// Usage
CustomButton(
    text = "Click",
    onClick = {},
    modifier = Modifier.padding(16.dp)
)
```

### 3. Preview
```kotlin
@Preview(showBackground = true)
@Preview(uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun GreetingPreview() {
    MyAppTheme {
        Greeting("Android")
    }
}
```

## Resources

- [Compose Documentation](https://developer.android.com/develop/ui/compose)
- [Material 3 for Compose](https://m3.material.io/develop/android/jetpack-compose)
- [Compose Samples](https://github.com/android/compose-samples)
