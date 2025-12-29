---
name: 03-ui-development
description: UI Development - XML Layouts, ConstraintLayout, Jetpack Compose, Material Design 3, responsive design, accessibility (235 hours)
model: sonnet
tools: All tools
sasmp_version: "1.3.0"
eqhm_enabled: true
skills:
  - ui
triggers:
  - jetpack compose
  - xml layout
  - material design
  - UI design
  - accessibility
capabilities:
  - XML Layout design
  - ConstraintLayout mastery
  - Jetpack Compose
  - Material Design 3
  - Theme and styling
  - Layout optimization
  - Accessibility
  - RecyclerView patterns
  - Data binding
  - View binding
  - Responsive design
  - Performance optimization
prerequisites:
  - Fundamentals
  - Platform
keywords:
  - layout
  - constraint
  - compose
  - material
  - ui design
  - view binding
  - recyclerview
  - accessibility
  - theme
---

# UI Development Agent: Modern Android UI & Design Systems

Master building beautiful, responsive, and accessible user interfaces. Learn XML layouts, ConstraintLayout, Jetpack Compose, and Material Design 3. Understand the complete UI toolkit for modern Android development.

**Prerequisite**: Fundamentals & Platform agents
**Duration**: 235 hours | **Level**: Intermediate to Advanced
**Topics**: 8 major areas | **Code Examples**: 60+ real-world patterns

---

## 1. XML LAYOUTS FUNDAMENTALS

XML layouts define UI structure. Android provides several layout managers, each optimized for different scenarios.

### 1.1 Layout Types & Hierarchies

**LinearLayout: Sequential Arrangement**
```xml
<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">

    <!-- Children arranged vertically or horizontally -->
    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Title" />

    <EditText
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Enter text" />

    <!-- Layout weight distributes remaining space -->
    <Button
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:text="Submit" />
</LinearLayout>
```

**RelativeLayout: Positional Relationships**
```xml
<RelativeLayout
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <!-- Position relative to other views -->
    <ImageView
        android:id="@+id/image"
        android:layout_width="100dp"
        android:layout_height="100dp"
        android:src="@drawable/profile" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_toRightOf="@id/image"
        android:layout_alignTop="@id/image"
        android:text="John Doe" />
</RelativeLayout>
```

**FrameLayout: Layered (Z-Order)**
```xml
<FrameLayout
    android:layout_width="200dp"
    android:layout_height="200dp">

    <!-- Children stack on top of each other -->
    <ImageView
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:src="@drawable/background"
        android:scaleType="centerCrop" />

    <!-- Overlaid on top -->
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="center"
        android:text="Overlay Text"
        android:textColor="@android:color/white" />
</FrameLayout>
```

**GridLayout: Table-like Grid**
```xml
<GridLayout
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:columnCount="3"
    android:rowCount="3">

    <!-- 3x3 grid of buttons -->
    <Button
        android:layout_row="0"
        android:layout_column="0"
        android:text="1" />
    <!-- More buttons... -->
</GridLayout>
```

### 1.2 Layout Performance Optimization

**Problem 1: Excessive Nesting (Layout Thrashing)**
```xml
<!-- ❌ BAD: Deep nesting causes measurement overhead -->
<LinearLayout>
    <LinearLayout>
        <LinearLayout>
            <LinearLayout>
                <TextView android:text="Deep!" />
            </LinearLayout>
        </LinearLayout>
    </LinearLayout>
</LinearLayout>

<!-- ✅ GOOD: Flat hierarchy (max 4-5 levels) -->
<ConstraintLayout>
    <TextView android:text="Flat!" />
</ConstraintLayout>
```

**Problem 2: View Inflation Overhead**
```xml
<!-- ✅ Use <merge> to eliminate root layout -->
<merge>
    <Button android:text="One" />
    <Button android:text="Two" />
</merge>

<!-- ✅ Use <ViewStub> for conditional inflation -->
<ViewStub
    android:id="@+id/error_view"
    android:layout="@layout/error_message"
    android:layout_width="match_parent"
    android:layout_height="wrap_content" />
```

In code:
```kotlin
// Only inflate if needed
val stub = findViewById<ViewStub>(R.id.error_view)
if (hasError) {
    stub.inflate()  // Only now is the view created
}
```

---

## 2. CONSTRAINTLAYOUT MASTERY

ConstraintLayout is the modern standard for Android layouts. It provides flat hierarchies and powerful constraint system.

### 2.1 Constraint System

**Basic Constraints (Directional)**
```xml
<androidx.constraintlayout.widget.ConstraintLayout
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <ImageView
        android:id="@+id/profile_image"
        android:layout_width="100dp"
        android:layout_height="100dp"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        android:layout_marginStart="16dp"
        android:layout_marginTop="16dp" />

    <TextView
        android:id="@+id/name"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:text="John Doe"
        app:layout_constraintStart_toEndOf="@id/profile_image"
        app:layout_constraintTop_toTopOf="@id/profile_image"
        app:layout_constraintEnd_toEndOf="parent"
        android:layout_marginStart="16dp" />

    <TextView
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:text="john@example.com"
        app:layout_constraintStart_toEndOf="@id/profile_image"
        app:layout_constraintTop_toBottomOf="@id/name"
        app:layout_constraintEnd_toEndOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>
```

### 2.2 Advanced Constraint Concepts

**Chains: Distribute Views Evenly**
```xml
<!-- SPREAD: Distribute with equal spacing -->
<Button
    android:id="@+id/btn1"
    app:layout_constraintStart_toStartOf="parent"
    app:layout_constraintEnd_toStartOf="@id/btn2"
    app:layout_constraintHorizontal_chainStyle="spread" />

<Button
    android:id="@+id/btn2"
    app:layout_constraintStart_toEndOf="@id/btn1"
    app:layout_constraintEnd_toStartOf="@id/btn3" />

<Button
    android:id="@+id/btn3"
    app:layout_constraintStart_toEndOf="@id/btn2"
    app:layout_constraintEnd_toEndOf="parent" />

<!-- SPREAD_INSIDE: Chain respects margins -->
<!-- PACKED: Center chain, no spacing -->
```

**Guidelines: Percentage-based Positioning**
```xml
<!-- Vertical guideline at 60% of width -->
<androidx.constraintlayout.widget.Guideline
    android:id="@+id/vertical_guide"
    android:layout_width="wrap_content"
    android:layout_height="match_parent"
    android:orientation="vertical"
    app:layout_constraintGuide_percent="0.6" />

<Button
    app:layout_constraintEnd_toStartOf="@id/vertical_guide" />
```

**Barriers: Reference Multiple Views**
```xml
<!-- Barrier positioned after both views -->
<androidx.constraintlayout.widget.Barrier
    android:id="@+id/barrier"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    app:barrierDirection="end"
    app:constraint_referenced_ids="title,subtitle" />

<Button
    app:layout_constraintStart_toEndOf="@id/barrier" />
```

**Bias: Weighted Positioning**
```xml
<!-- Position 30% from start, 70% from end -->
<Button
    app:layout_constraintStart_toStartOf="parent"
    app:layout_constraintEnd_toEndOf="parent"
    app:layout_constraintHorizontal_bias="0.3" />
```

---

## 3. JETPACK COMPOSE: DECLARATIVE UI

Compose is Android's modern UI toolkit. It's declarative (you describe what UI should look like), composable (small reusable functions), and reactive (automatic recomposition on state changes).

### 3.1 Compose Basics

```kotlin
// 1. Basic composable function
@Composable
fun Greeting(name: String) {
    Text("Hello, $name!")
}

// 2. Layout with Column
@Composable
fun LoginScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            "Login",
            style = MaterialTheme.typography.headlineLarge
        )

        Spacer(modifier = Modifier.height(16.dp))

        TextField(
            value = "",
            onValueChange = {},
            label = { Text("Email") }
        )

        Spacer(modifier = Modifier.height(8.dp))

        Button(
            onClick = {},
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Sign In")
        }
    }
}

// 3. Use in Activity
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyAppTheme {
                LoginScreen()
            }
        }
    }
}
```

### 3.2 State Management in Compose

```kotlin
// 1. Local state with remember
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }

    Button(onClick = { count++ }) {
        Text("Clicked $count times")
    }
}

// 2. Lifting state for sharing
@Composable
fun Parent() {
    var count by remember { mutableStateOf(0) }

    Column {
        DisplayCount(count)
        IncrementButton(count) { count++ }
    }
}

@Composable
fun DisplayCount(count: Int) {
    Text("Count: $count")
}

@Composable
fun IncrementButton(count: Int, onIncrement: () -> Unit) {
    Button(onClick = onIncrement) {
        Text("Increment")
    }
}

// 3. ViewModel state (RECOMMENDED)
@HiltViewModel
class CounterViewModel @Inject constructor() : ViewModel() {
    private val _count = MutableStateFlow(0)
    val count: StateFlow<Int> = _count.asStateFlow()

    fun increment() {
        _count.value++
    }
}

@Composable
fun CounterScreen(viewModel: CounterViewModel = hiltViewModel()) {
    val count by viewModel.count.collectAsState()

    Button(onClick = { viewModel.increment() }) {
        Text("Count: $count")
    }
}
```

### 3.3 Modifier System (Styling & Layout)

```kotlin
@Composable
fun StyledButton() {
    Button(
        onClick = {},
        modifier = Modifier
            // Size
            .width(200.dp)
            .height(50.dp)
            // Padding (inside)
            .padding(16.dp)
            // Background & styling
            .background(
                color = Color.Blue,
                shape = RoundedCornerShape(8.dp)
            )
            // Border
            .border(
                width = 2.dp,
                color = Color.Gray,
                shape = RoundedCornerShape(8.dp)
            )
            // Shadow/elevation
            .shadow(
                elevation = 8.dp,
                shape = RoundedCornerShape(8.dp)
            )
            // Click ripple effect
            .clip(RoundedCornerShape(8.dp))
    ) {
        Text("Styled Button")
    }
}

// Common modifiers
@Composable
fun CommonModifiers() {
    Text(
        "Text",
        modifier = Modifier
            .fillMaxWidth()          // Match parent width
            .wrapContentHeight()     // Wrap content height
            .padding(start = 8.dp)   // Directional padding
            .alpha(0.8f)             // Transparency
            .rotate(15f)             // Rotation degrees
            .scale(1.2f)             // Scale factor
            .clickable { }           // Click handling
            .semantics { }           // Accessibility
    )
}
```

---

## 4. MATERIAL DESIGN 3 SYSTEM

Material Design 3 (Material You) provides a complete design system for beautiful, accessible apps.

### 4.1 Components

```kotlin
@Composable
fun MaterialComponents() {
    Column(modifier = Modifier.padding(16.dp)) {
        // Buttons (multiple styles)
        Button(onClick = {}) {
            Text("Filled Button")
        }

        OutlinedButton(onClick = {}) {
            Text("Outlined Button")
        }

        TextButton(onClick = {}) {
            Text("Text Button")
        }

        ElevatedButton(onClick = {}) {
            Text("Elevated Button")
        }

        // Cards
        Card(
            modifier = Modifier.fillMaxWidth(),
            elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Card Title")
                Text("Card content goes here")
            }
        }

        // Floating Action Button
        FloatingActionButton(onClick = {}) {
            Icon(Icons.Default.Add, contentDescription = "Add")
        }

        // Chips
        ElevatedAssistChip(
            onClick = {},
            label = { Text("Chip") },
            leadingIcon = { Icon(Icons.Default.Done, "") }
        )
    }
}
```

### 4.2 Theming & Color System

```kotlin
// Define custom color scheme
val lightColorScheme = lightColorScheme(
    primary = Color(0xFF6750a4),           // Brand color
    onPrimary = Color.White,               // Text on primary
    primaryContainer = Color(0xFFEaddff),  // Lighter primary
    onPrimaryContainer = Color(0xFF21005d),
    secondary = Color(0xFF625b71),
    tertiary = Color(0xFF7d5260),
    error = Color(0xFFb3261e),
    background = Color(0xFFFBF8FD),
    surface = Color.White
)

// Apply theme
@Composable
fun MyAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) darkColorScheme else lightColorScheme

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography(
            bodyLarge = TextStyle(
                fontFamily = FontFamily.Default,
                fontWeight = FontWeight.Normal,
                fontSize = 16.sp
            ),
            headlineLarge = TextStyle(
                fontFamily = FontFamily.Default,
                fontWeight = FontWeight.Bold,
                fontSize = 32.sp
            )
        ),
        content = content
    )
}

// Use theme colors
@Composable
fun ThemedButton() {
    Button(
        onClick = {},
        colors = ButtonDefaults.buttonColors(
            containerColor = MaterialTheme.colorScheme.primary,
            contentColor = MaterialTheme.colorScheme.onPrimary
        )
    ) {
        Text("Themed Button")
    }
}
```

### 4.3 Typography System

```kotlin
// Typography hierarchy
val typography = Typography(
    // Display: Large, eye-catching headings
    displayLarge = TextStyle(
        fontSize = 57.sp,
        fontWeight = FontWeight.Bold,
        lineHeight = 64.sp
    ),
    displayMedium = TextStyle(
        fontSize = 45.sp,
        fontWeight = FontWeight.Bold
    ),

    // Headline: Important content
    headlineLarge = TextStyle(
        fontSize = 32.sp,
        fontWeight = FontWeight.Bold
    ),
    headlineMedium = TextStyle(
        fontSize = 28.sp,
        fontWeight = FontWeight.Bold
    ),

    // Title: Section headers
    titleLarge = TextStyle(
        fontSize = 22.sp,
        fontWeight = FontWeight.Bold
    ),

    // Body: Main content
    bodyLarge = TextStyle(
        fontSize = 16.sp,
        fontWeight = FontWeight.Normal,
        lineHeight = 24.sp
    ),
    bodyMedium = TextStyle(
        fontSize = 14.sp,
        fontWeight = FontWeight.Normal
    ),

    // Label: Small interactive elements
    labelLarge = TextStyle(
        fontSize = 14.sp,
        fontWeight = FontWeight.Medium
    )
)

// Usage
@Composable
fun TypographyExample() {
    Column {
        Text("Display Large", style = MaterialTheme.typography.displayLarge)
        Text("Headline Large", style = MaterialTheme.typography.headlineLarge)
        Text("Body Large", style = MaterialTheme.typography.bodyLarge)
        Text("Label Large", style = MaterialTheme.typography.labelLarge)
    }
}
```

---

## 5. RECYCLERVIEW & LIST OPTIMIZATION

RecyclerView efficiently displays large lists by recycling views.

### 5.1 Complete RecyclerView Implementation

```kotlin
// Data model
data class User(
    val id: Int,
    val name: String,
    val email: String,
    val avatarUrl: String
)

// ViewHolder holds references to views
class UserViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
    private val nameText: TextView = itemView.findViewById(R.id.name)
    private val emailText: TextView = itemView.findViewById(R.id.email)
    private val avatarImage: ImageView = itemView.findViewById(R.id.avatar)

    fun bind(user: User) {
        nameText.text = user.name
        emailText.text = user.email
        // Load image (with coil or glide)
        avatarImage.load(user.avatarUrl)
    }
}

// Adapter connects data to views
class UserAdapter(
    private val users: MutableList<User> = mutableListOf(),
    private val onItemClick: (User) -> Unit = {}
) : RecyclerView.Adapter<UserViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): UserViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_user, parent, false)
        return UserViewHolder(view)
    }

    override fun onBindViewHolder(holder: UserViewHolder, position: Int) {
        val user = users[position]
        holder.bind(user)
        holder.itemView.setOnClickListener { onItemClick(user) }
    }

    override fun getItemCount() = users.size

    // Update list with DiffUtil for efficient updates
    fun updateUsers(newUsers: List<User>) {
        val diffCallback = UserDiffCallback(users, newUsers)
        val diffResult = DiffUtil.calculateDiff(diffCallback)
        users.clear()
        users.addAll(newUsers)
        diffResult.dispatchUpdatesTo(this)
    }
}

// DiffUtil callback for efficient updates
class UserDiffCallback(
    private val oldList: List<User>,
    private val newList: List<User>
) : DiffUtil.Callback() {

    override fun getOldListSize() = oldList.size
    override fun getNewListSize() = newList.size

    override fun areItemsTheSame(oldItemPosition: Int, newItemPosition: Int) =
        oldList[oldItemPosition].id == newList[newItemPosition].id

    override fun areContentsTheSame(oldItemPosition: Int, newItemPosition: Int) =
        oldList[oldItemPosition] == newList[newItemPosition]
}

// Use in Activity/Fragment
class UserListFragment : Fragment() {
    private val adapter = UserAdapter { user ->
        // Handle item click
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val recyclerView: RecyclerView = view.findViewById(R.id.recycler)
        recyclerView.apply {
            layoutManager = LinearLayoutManager(context)
            adapter = this@UserListFragment.adapter
            addItemDecoration(DividerItemDecoration(context, DividerItemDecoration.VERTICAL))
        }

        // Load and display users
        viewModel.users.observe(viewLifecycleOwner) { users ->
            adapter.updateUsers(users)
        }
    }
}
```

---

## 6. RESPONSIVE DESIGN FOR MULTIPLE SCREENS

Android runs on many device sizes. Responsive design ensures good UX everywhere.

### 6.1 Configuration Qualifiers

```
res/layout/
├── activity_main.xml          # Default (small phones)
├── activity_main-land.xml     # Landscape
└── activity_main-sw600dp.xml  # Tablets (min width 600dp)

res/values/
├── dimens.xml                 # Default dimensions
├── dimens-land.xml            # Landscape dimensions
└── dimens-sw600dp.xml         # Tablet dimensions
```

**dimens.xml (Phone)**
```xml
<dimen name="margin_small">8dp</dimen>
<dimen name="margin_large">16dp</dimen>
<dimen name="text_size_title">22sp</dimen>
<dimen name="column_width">match_parent</dimen>
```

**dimens-sw600dp.xml (Tablet)**
```xml
<dimen name="margin_small">12dp</dimen>
<dimen name="margin_large">24dp</dimen>
<dimen name="text_size_title">32sp</dimen>
<dimen name="column_width">600dp</dimen>
```

### 6.2 Responsive Compose Layout

```kotlin
@Composable
fun ResponsiveLayout() {
    val windowSize = currentWindowAdaptiveInfo().windowSizeClass

    when (windowSize.widthSizeClass) {
        WindowWidthSizeClass.Compact -> {
            // Phone: Single column
            Column(modifier = Modifier.fillMaxSize()) {
                // Vertical layout
            }
        }
        WindowWidthSizeClass.Medium -> {
            // Tablet landscape: Two columns
            Row(modifier = Modifier.fillMaxSize()) {
                Column(modifier = Modifier.weight(1f)) {
                    // Left column
                }
                Column(modifier = Modifier.weight(1f)) {
                    // Right column
                }
            }
        }
        else -> {
            // Large tablets
        }
    }
}
```

---

## 7. ACCESSIBILITY (A11Y)

Accessibility ensures your app works for everyone, including users with disabilities.

### 7.1 Key Accessibility Principles

```kotlin
@Composable
fun AccessibleCard(title: String, description: String) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
            // Minimum touch target size: 48dp
            .minimumInteractiveComponentSize()
            .semantics {
                // Describe for screen readers
                contentDescription = "$title: $description"
                // Mark as button if clickable
                role = Role.Button
            },
        onClick = {}
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                title,
                // Sufficient color contrast (WCAG AA: 4.5:1)
                color = Color.Black,
                style = MaterialTheme.typography.headlineSmall
            )
            Text(
                description,
                color = Color.DarkGray
            )
        }
    }
}

// Image with content description
@Composable
fun AccessibleImage() {
    Image(
        painter = painterResource(R.drawable.profile),
        contentDescription = "User profile photo of John Doe",  // REQUIRED!
        contentScale = ContentScale.Crop
    )
}

// Button with proper semantics
@Composable
fun AccessibleButton(text: String, onClick: () -> Unit) {
    Button(
        onClick = onClick,
        modifier = Modifier
            .semantics {
                // Help screen readers understand action
                contentDescription = "Button: $text"
            }
    ) {
        Text(text)
    }
}
```

### 7.2 XML Accessibility

```xml
<!-- Always provide contentDescription -->
<ImageView
    android:id="@+id/profile_image"
    android:layout_width="100dp"
    android:layout_height="100dp"
    android:contentDescription="@string/user_profile_image"
    android:src="@drawable/profile" />

<!-- Min 48dp touch targets -->
<Button
    android:layout_width="48dp"
    android:layout_height="48dp"
    android:contentDescription="@string/button_action" />

<!-- Proper semantic structure -->
<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:contentDescription="@string/user_card">

    <TextView
        android:text="@string/user_name"
        android:textSize="18sp" />

    <TextView
        android:text="@string/user_email"
        android:textSize="14sp" />
</LinearLayout>
```

---

## 8. BEST PRACTICES

✅ **Layouts**
- Use ConstraintLayout as default (flat hierarchy)
- Minimize layout nesting (max 5 levels)
- Use ViewBinding for type-safe references
- Profile with Layout Inspector in Android Studio

✅ **Compose**
- Use ViewModels for state management
- Avoid recomposition by extracting composables
- Use key() for lists to maintain state
- Profile with Compose Layout Inspector

✅ **Performance**
- Use RecyclerView for lists (never ListView)
- Apply DiffUtil for list updates
- Load images asynchronously (Coil/Glide)
- Preload images off-screen with LazyColumn

✅ **Accessibility**
- Always provide contentDescription for images
- Maintain minimum 48dp touch targets
- Use semantic hierarchy (H1, H2, etc.)
- Test with TalkBack and Accessibility Scanner

✅ **Theming**
- Define theme colors in Material Design 3
- Support dark mode with isSystemInDarkTheme()
- Use MaterialTheme colors, not hardcoded colors
- Test on multiple API levels

---

## 9. LEARNING PATH: 12 WEEKS (235 HOURS)

**Week 1-2 (20h): XML Layouts Foundation**
- LinearLayout, RelativeLayout, FrameLayout
- Layout nesting and performance
- ViewBinding and DataBinding
- Practice basic screens

**Week 3-4 (30h): ConstraintLayout Mastery**
- Constraint system, chains, guidelines
- Barriers and bias
- Responsive layouts
- Complex UI exercises

**Week 5-6 (35h): Jetpack Compose Basics**
- Composable functions
- State management (remember, ViewModel)
- Modifier system
- Building simple screens

**Week 7-8 (40h): Compose Advanced**
- Lists (LazyColumn, LazyRow)
- Animations and transitions
- Preview system
- Complex state management

**Week 9-10 (50h): Material Design 3**
- Complete component library
- Theming system
- Typography hierarchy
- Dark mode implementation

**Week 11-12 (60h): Advanced Topics**
- RecyclerView optimization with DiffUtil
- Responsive design patterns
- Accessibility (A11Y) standards
- Performance profiling

---

**Mastery Checkpoint**:
- Can build responsive layouts for phone & tablet
- Proficient with both XML and Compose
- Understand Material Design 3 system
- Create accessible UIs
- Optimize list rendering performance

---

**Learning Hours**: 235 hours | **Level**: Intermediate to Advanced
**Next Step**: Data Management agent (Room, SQLite, DataStore)
