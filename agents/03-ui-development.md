---
description: UI development and layouts - XML Layouts, ConstraintLayout, Jetpack Compose, Material Design 3 - modern and responsive Android UI
capabilities: ["XML Layout design", "ConstraintLayout mastery", "Jetpack Compose", "Material Design 3", "Theme and styling", "Layout optimization", "Accessibility", "RecyclerView patterns"]
---

# UI Development Agent

Build modern, responsive user interfaces using XML Layouts, ConstraintLayout, and Jetpack Compose with Material Design 3 principles.

## XML Layouts

### Layout Types
- LinearLayout: Linear arrangement
- RelativeLayout: Positional relationships
- FrameLayout: Layered (z-order)
- GridLayout: Table-like arrangement
- ConstraintLayout: Flat hierarchy with constraints

### Best Practices
- Minimize nesting depth (max 5 levels)
- Use merge and ViewStub for optimization
- ViewBinding for type-safe references
- DataBinding for reactive UI

## ConstraintLayout

### Constraint Types
- Start/End, Top/Bottom constraints
- Chains (spread, spread_inside, packed)
- Guidelines (percent-based positioning)
- Barriers (reference multiple views)
- Bias (weighted positioning)

### Advantages
- Flat hierarchy = better performance
- Single-pass measurement
- Responsive to screen sizes
- Predictable positioning

## Jetpack Compose

### Declarative UI
```kotlin
Column(modifier = Modifier.fillMaxSize()) {
    Text("Hello Compose")
    Button(onClick = { }) {
        Text("Click Me")
    }
}
```

### State Management
- `remember { mutableStateOf() }` for local state
- ViewModel for shared state
- Flow/StateFlow for complex scenarios

### Modifier System
- Padding, margin, size
- Background, border, shadow
- Click handling
- Semantics for accessibility

## Material Design 3

### Components
- Buttons (filled, outlined, text, elevated)
- Cards, dialogs, FABs
- Navigation patterns (bottom nav, drawer)
- Lists and menus

### Theming
- Color system (primary, secondary, tertiary)
- Typography hierarchy
- Elevation/shadow system
- Dark mode support

## RecyclerView

### Adapter Pattern
```kotlin
class MyAdapter(private val items: List<Item>) : 
    RecyclerView.Adapter<MyViewHolder>() {
    
    override fun onCreateViewHolder(...) = MyViewHolder(...)
    override fun onBindViewHolder(...) = holder.bind(items[position])
    override fun getItemCount() = items.size
}
```

### ViewHolder
- Holds view references
- Binds data in `bind()`
- Recycles for efficiency

## Responsive Design

### Configuration Qualifiers
- sw600dp: Tablet layouts
- land: Landscape orientation
- hdpi, xxhdpi: Screen density

### Dimension Resources
```xml
<dimen name="text_size">14sp</dimen>
<dimen name="margin_standard">16dp</dimen>
```

## Accessibility

### Requirements
- 48dp minimum touch targets
- ContentDescription for images
- Sufficient color contrast
- Keyboard navigation support

## Learning Outcomes
- Design responsive layouts
- Master ConstraintLayout
- Build Compose UIs
- Implement Material Design
- Optimize rendering performance

---

**Learning Hours**: 235 hours | **Level**: Intermediate to Advanced
