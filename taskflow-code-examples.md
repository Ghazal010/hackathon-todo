# TaskFlow - Component Code Examples

> **Purpose**: Yeh file mein exact Tailwind CSS classes hain jo Qwen use karega. Copy-paste ready code!

---

## 📦 Component 1: Header

```jsx
<header className={`fixed top-0 left-0 right-0 z-40 h-16 px-6 flex items-center justify-between transition-all ${
  darkMode 
    ? 'bg-[#0A0A0A]/80 backdrop-blur-xl' 
    : 'bg-white/80 backdrop-blur-xl shadow-[0_1px_3px_rgba(0,0,0,0.04)]'
}`}>
  {/* Left: Logo + Search */}
  <div className="flex items-center gap-6 flex-1">
    {/* Mobile Menu Toggle */}
    <button 
      onClick={() => setSidebarOpen(!sidebarOpen)}
      className={`lg:hidden p-2 rounded-lg transition-colors ${
        darkMode ? 'hover:bg-white/5' : 'hover:bg-black/5'
      }`}
    >
      {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
    </button>
    
    {/* Logo */}
    <div className="flex items-center gap-3">
      <div 
        className="w-9 h-9 rounded-lg flex items-center justify-center" 
        style={{ background: 'linear-gradient(135deg, #C880B7 0%, #9F6BA0 100%)' }}
      >
        <Check className="w-5 h-5 text-white stroke-[2.5]" />
      </div>
      <span className={`text-lg font-semibold tracking-tight ${
        darkMode ? 'text-white' : 'text-[#171717]'
      }`}>
        TaskFlow
      </span>
    </div>

    {/* Search Bar */}
    <div className="hidden md:flex items-center flex-1 max-w-md">
      <div className={`relative w-full rounded-lg transition-all ${
        darkMode 
          ? 'bg-white/5 hover:bg-white/8' 
          : 'bg-black/[0.02] hover:bg-black/[0.04]'
      }`}>
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-[18px] h-[18px] text-[#9F6BA0]" />
        <input 
          type="text" 
          placeholder="Search tasks..." 
          className={`w-full pl-10 pr-4 py-2.5 bg-transparent outline-none text-[15px] ${
            darkMode 
              ? 'text-white placeholder-white/30' 
              : 'text-[#171717] placeholder-black/30'
          }`}
        />
      </div>
    </div>
  </div>

  {/* Right: Actions */}
  <div className="flex items-center gap-2">
    {/* Dark Mode Toggle */}
    <button 
      onClick={() => setDarkMode(!darkMode)}
      className={`p-2.5 rounded-lg transition-colors ${
        darkMode ? 'hover:bg-white/5' : 'hover:bg-black/5'
      }`}
    >
      {darkMode ? 
        <Sun className="w-[18px] h-[18px] text-white/60" /> : 
        <Moon className="w-[18px] h-[18px] text-black/40" />
      }
    </button>
    
    {/* New Task Button */}
    <button 
      onClick={() => setShowModal(true)}
      className="px-4 py-2.5 rounded-lg font-medium text-[15px] transition-all text-white hover:opacity-90 flex items-center gap-2"
      style={{ background: 'linear-gradient(135deg, #C880B7 0%, #9F6BA0 100%)' }}
    >
      <Plus className="w-[18px] h-[18px]" />
      <span className="hidden sm:inline">New Task</span>
    </button>
  </div>
</header>
```

---

## 📦 Component 2: Sidebar

```jsx
<aside className={`fixed left-0 top-16 bottom-0 w-64 transition-all duration-300 ${
  sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
} ${darkMode ? 'bg-[#0A0A0A]' : 'bg-white'}`}>
  <nav className="p-4 space-y-8">
    {/* Views Section */}
    <div className="space-y-1">
      <p className={`text-xs font-semibold uppercase tracking-wider px-3 mb-3 ${
        darkMode ? 'text-white/30' : 'text-black/30'
      }`}>
        Views
      </p>
      {[
        { id: 'all', label: 'All Tasks', count: 5 },
        { id: 'active', label: 'Active', count: 3 },
        { id: 'completed', label: 'Completed', count: 2 }
      ].map(view => (
        <button
          key={view.id}
          onClick={() => setActiveFilter(view.id)}
          className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-[15px] font-medium transition-all ${
            activeFilter === view.id
              ? darkMode
                ? 'bg-white/8 text-white'
                : 'bg-[#F5CCE8] text-[#4A2040]'
              : darkMode 
                ? 'text-white/50 hover:bg-white/5 hover:text-white/80' 
                : 'text-black/50 hover:bg-black/[0.02] hover:text-black/80'
          }`}
        >
          <span>{view.label}</span>
          {view.count > 0 && (
            <span className={`text-xs px-2 py-0.5 rounded-full font-semibold ${
              activeFilter === view.id
                ? darkMode 
                  ? 'bg-white/10 text-white/80' 
                  : 'bg-white/60 text-[#4A2040]'
                : darkMode 
                  ? 'bg-white/5 text-white/30' 
                  : 'bg-black/5 text-black/30'
            }`}>
              {view.count}
            </span>
          )}
        </button>
      ))}
    </div>

    {/* Priority Section */}
    <div className="space-y-1">
      <p className={`text-xs font-semibold uppercase tracking-wider px-3 mb-3 ${
        darkMode ? 'text-white/30' : 'text-black/30'
      }`}>
        Priority
      </p>
      {[
        { id: 'high', label: 'High', color: '#EF4444' },
        { id: 'medium', label: 'Medium', color: '#F59E0B' },
        { id: 'low', label: 'Low', color: '#10B981' }
      ].map(priority => (
        <button
          key={priority.id}
          onClick={() => setActiveFilter(priority.id)}
          className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-[15px] font-medium transition-all ${
            activeFilter === priority.id
              ? darkMode
                ? 'bg-white/8 text-white'
                : 'bg-[#F5CCE8] text-[#4A2040]'
              : darkMode 
                ? 'text-white/50 hover:bg-white/5 hover:text-white/80' 
                : 'text-black/50 hover:bg-black/[0.02] hover:text-black/80'
          }`}
        >
          <div className="w-2 h-2 rounded-full" style={{ backgroundColor: priority.color }}></div>
          <span>{priority.label}</span>
        </button>
      ))}
    </div>
  </nav>
</aside>
```

---

## 📦 Component 3: Stats Cards

```jsx
<div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
  {[
    { 
      label: 'Total', 
      value: 5, 
      gradient: 'linear-gradient(135deg, #F5CCE8 0%, #EC9DED 100%)',
      textColor: darkMode ? '#EC9DED' : '#4A2040'
    },
    { 
      label: 'In Progress', 
      value: 3, 
      gradient: 'linear-gradient(135deg, #EC9DED 0%, #C880B7 100%)',
      textColor: '#F59E0B'
    },
    { 
      label: 'Completed', 
      value: 2, 
      gradient: 'linear-gradient(135deg, #C880B7 0%, #9F6BA0 100%)',
      textColor: '#10B981'
    }
  ].map((stat, idx) => (
    <div 
      key={idx}
      className={`p-5 rounded-xl transition-all hover:scale-[1.02] ${
        darkMode ? 'bg-white/5' : 'bg-white shadow-sm'
      }`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className={`text-sm font-medium mb-2 ${
            darkMode ? 'text-white/40' : 'text-black/40'
          }`}>
            {stat.label}
          </p>
          <p className="text-3xl font-bold" style={{ color: stat.textColor }}>
            {stat.value}
          </p>
        </div>
        <div 
          className="w-10 h-10 rounded-lg flex items-center justify-center" 
          style={{ background: stat.gradient }}
        >
          <CheckCircle2 className="w-5 h-5 text-white" />
        </div>
      </div>
    </div>
  ))}
</div>
```

---

## 📦 Component 4: Task Card

```jsx
<div 
  className={`group p-4 rounded-xl transition-all ${
    task.completed 
      ? darkMode 
        ? 'bg-white/[0.02]' 
        : 'bg-black/[0.01]'
      : darkMode 
        ? 'bg-white/5 hover:bg-white/8' 
        : 'bg-white hover:shadow-md shadow-sm'
  }`}
>
  <div className="flex items-start gap-4">
    {/* Checkbox */}
    <button 
      onClick={() => toggleTask(task.id)}
      className={`mt-0.5 flex-shrink-0 w-5 h-5 rounded-md flex items-center justify-center transition-all ${
        task.completed 
          ? 'bg-gradient-to-br from-[#C880B7] to-[#9F6BA0] shadow-sm' 
          : darkMode
            ? 'border-2 border-white/20 hover:border-[#9F6BA0]'
            : 'border-2 border-black/10 hover:border-[#C880B7]'
      }`}
    >
      {task.completed && <Check className="w-3 h-3 text-white stroke-[3]" />}
    </button>

    {/* Content */}
    <div className="flex-1 min-w-0">
      {/* Title */}
      <h3 className={`font-semibold mb-1.5 text-[15px] leading-snug ${
        task.completed 
          ? darkMode 
            ? 'line-through text-white/30' 
            : 'line-through text-black/30'
          : darkMode 
            ? 'text-white' 
            : 'text-[#171717]'
      }`}>
        {task.title}
      </h3>
      
      {/* Description */}
      <p className={`text-sm mb-3 line-clamp-1 ${
        darkMode ? 'text-white/40' : 'text-black/40'
      }`}>
        {task.description}
      </p>
      
      {/* Meta Info */}
      <div className="flex items-center gap-3">
        {/* Priority Badge */}
        <span 
          className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold ${
            task.priority === 'high' 
              ? darkMode ? 'bg-red-500/10 text-red-400' : 'bg-red-50 text-red-600'
              : task.priority === 'medium'
              ? darkMode ? 'bg-amber-500/10 text-amber-400' : 'bg-amber-50 text-amber-600'
              : darkMode ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600'
          }`}
        >
          <Circle className="w-1.5 h-1.5 fill-current" />
          {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
        </span>
        
        {/* Due Date */}
        <span className={`text-xs flex items-center gap-1.5 ${
          darkMode ? 'text-white/30' : 'text-black/30'
        }`}>
          <Calendar className="w-3.5 h-3.5" />
          {task.dueDate}
        </span>
      </div>
    </div>

    {/* Actions */}
    <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
      <button className={`p-2 rounded-lg transition-colors ${
        darkMode ? 'hover:bg-white/5' : 'hover:bg-black/5'
      }`}>
        <Edit2 className={`w-[18px] h-[18px] ${
          darkMode ? 'text-white/40' : 'text-black/40'
        }`} />
      </button>
      <button 
        onClick={() => deleteTask(task.id)}
        className={`p-2 rounded-lg transition-colors ${
          darkMode ? 'hover:bg-red-500/10' : 'hover:bg-red-50'
        }`}
      >
        <Trash2 className={`w-[18px] h-[18px] ${
          darkMode ? 'text-red-400' : 'text-red-500'
        }`} />
      </button>
    </div>
  </div>
</div>
```

---

## 📦 Component 5: Modal

```jsx
{showModal && (
  <div 
    className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm" 
    onClick={() => setShowModal(false)}
  >
    <div 
      className={`w-full max-w-lg rounded-2xl overflow-hidden ${
        darkMode ? 'bg-[#0A0A0A]' : 'bg-white'
      } shadow-2xl`}
      onClick={(e) => e.stopPropagation()}
    >
      {/* Modal Header */}
      <div className="p-6 pb-4">
        <h2 className={`text-2xl font-semibold ${
          darkMode ? 'text-white' : 'text-[#171717]'
        }`}>
          Create New Task
        </h2>
        <p className={`text-sm mt-1 ${
          darkMode ? 'text-white/40' : 'text-black/40'
        }`}>
          Add a new task to your workflow
        </p>
      </div>
      
      {/* Modal Body */}
      <div className="px-6 pb-6 space-y-5">
        {/* Title Input */}
        <div>
          <label className={`block text-sm font-semibold mb-2 ${
            darkMode ? 'text-white/80' : 'text-black/80'
          }`}>
            Title
          </label>
          <input 
            type="text" 
            className={`w-full px-4 py-3 rounded-xl outline-none transition-all ${
              darkMode 
                ? 'bg-white/5 text-white border-2 border-white/10 focus:border-[#9F6BA0]/50' 
                : 'bg-black/[0.02] text-[#171717] border-2 border-black/5 focus:border-[#C880B7]/50'
            }`}
            placeholder="Enter task title..."
            autoFocus
          />
        </div>

        {/* Description Textarea */}
        <div>
          <label className={`block text-sm font-semibold mb-2 ${
            darkMode ? 'text-white/80' : 'text-black/80'
          }`}>
            Description
          </label>
          <textarea 
            className={`w-full px-4 py-3 rounded-xl outline-none transition-all resize-none h-28 ${
              darkMode 
                ? 'bg-white/5 text-white border-2 border-white/10 focus:border-[#9F6BA0]/50' 
                : 'bg-black/[0.02] text-[#171717] border-2 border-black/5 focus:border-[#C880B7]/50'
            }`}
            placeholder="Add task details..."
          />
        </div>

        {/* Priority & Due Date */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className={`block text-sm font-semibold mb-2 ${
              darkMode ? 'text-white/80' : 'text-black/80'
            }`}>
              Priority
            </label>
            <select 
              className={`w-full px-4 py-3 rounded-xl outline-none transition-all ${
                darkMode 
                  ? 'bg-white/5 text-white border-2 border-white/10 focus:border-[#9F6BA0]/50' 
                  : 'bg-black/[0.02] text-[#171717] border-2 border-black/5 focus:border-[#C880B7]/50'
              }`}
            >
              <option>Low</option>
              <option>Medium</option>
              <option>High</option>
            </select>
          </div>
          <div>
            <label className={`block text-sm font-semibold mb-2 ${
              darkMode ? 'text-white/80' : 'text-black/80'
            }`}>
              Due Date
            </label>
            <input 
              type="date"
              className={`w-full px-4 py-3 rounded-xl outline-none transition-all ${
                darkMode 
                  ? 'bg-white/5 text-white border-2 border-white/10 focus:border-[#9F6BA0]/50' 
                  : 'bg-black/[0.02] text-[#171717] border-2 border-black/5 focus:border-[#C880B7]/50'
              }`}
            />
          </div>
        </div>
      </div>

      {/* Modal Footer */}
      <div className={`p-6 pt-4 flex gap-3 border-t ${
        darkMode ? 'border-white/5' : 'border-black/5'
      }`}>
        <button 
          onClick={() => setShowModal(false)}
          className={`flex-1 px-4 py-3 rounded-xl font-semibold transition-colors ${
            darkMode 
              ? 'bg-white/5 text-white/80 hover:bg-white/10' 
              : 'bg-black/[0.02] text-black/80 hover:bg-black/[0.04]'
          }`}
        >
          Cancel
        </button>
        <button 
          className="flex-1 px-4 py-3 rounded-xl font-semibold text-white transition-opacity hover:opacity-90"
          style={{ background: 'linear-gradient(135deg, #C880B7 0%, #9F6BA0 100%)' }}
        >
          Create Task
        </button>
      </div>
    </div>
  </div>
)}
```

---

## 📦 Component 6: Empty State

```jsx
<div className="text-center py-20">
  <div className={`w-16 h-16 mx-auto mb-4 rounded-2xl flex items-center justify-center ${
    darkMode ? 'bg-white/5' : 'bg-black/[0.02]'
  }`}>
    <CheckCircle2 className={`w-8 h-8 ${
      darkMode ? 'text-white/20' : 'text-black/20'
    }`} />
  </div>
  <h3 className={`text-lg font-semibold mb-2 ${
    darkMode ? 'text-white/60' : 'text-black/60'
  }`}>
    No tasks found
  </h3>
  <p className={`text-sm ${
    darkMode ? 'text-white/30' : 'text-black/30'
  }`}>
    Try adjusting your filters or create a new task
  </p>
</div>
```

---

## 🎨 Tailwind Config (tailwind.config.js)

```javascript
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Your purple palette
        primary: {
          50: '#F5CCE8',
          100: '#EC9DED',
          300: '#C880B7',
          500: '#9F6BA0',
          900: '#4A2040',
        },
      },
      spacing: {
        // 8px grid system
        '0.5': '2px',
        '1': '4px',
        '2': '8px',
        '3': '12px',
        '4': '16px',
        '5': '20px',
        '6': '24px',
        '8': '32px',
      },
      fontSize: {
        'xs': '12px',
        'sm': '14px',
        'base': '15px',
        'lg': '16px',
        'xl': '20px',
        '2xl': '24px',
        '3xl': '30px',
      },
    },
  },
  plugins: [],
}
```

---

## 📱 Responsive Utilities

```jsx
{/* Mobile: Hidden, Desktop: Visible */}
<div className="hidden md:flex">...</div>

{/* Mobile: Visible, Desktop: Hidden */}
<div className="md:hidden">...</div>

{/* Mobile: 1 column, Tablet+: 3 columns */}
<div className="grid grid-cols-1 sm:grid-cols-3 gap-4">...</div>

{/* Mobile: Full width button text hidden, Desktop: Show text */}
<button className="px-4 py-2.5">
  <Plus className="w-[18px] h-[18px]" />
  <span className="hidden sm:inline">New Task</span>
</button>
```

---

## ✅ Quick Implementation Steps

1. **Install Dependencies:**
```bash
npm install lucide-react
npm install -D tailwindcss
```

2. **Copy Tailwind Config** (above)

3. **Create Components** using code examples above

4. **Add Dark Mode State:**
```javascript
const [darkMode, setDarkMode] = useState(false);
```

5. **Apply to Root:**
```jsx
<div className={darkMode ? 'bg-[#0A0A0A]' : 'bg-[#FAFAFA]'}>
  {/* Your app */}
</div>
```

---

**Yeh sab code Qwen ko de do - exact implementation ready hai!** 🚀