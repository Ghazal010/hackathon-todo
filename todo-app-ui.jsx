import React, { useState, useEffect } from 'react';
import { Plus, Check, Trash2, Edit3, Circle, CheckCircle2, Calendar, Tag, Search, Filter, Star, Moon, Sun } from 'lucide-react';

export default function TodoApp() {
  const [tasks, setTasks] = useState([
    { id: 1, title: 'Design new landing page', completed: false, priority: 'high', tags: ['work'], dueDate: '2024-02-15' },
    { id: 2, title: 'Morning meditation', completed: true, priority: 'medium', tags: ['personal'], dueDate: '2024-02-10' },
    { id: 3, title: 'Grocery shopping', completed: false, priority: 'low', tags: ['errands'], dueDate: '2024-02-12' }
  ]);
  const [newTask, setNewTask] = useState('');
  const [filter, setFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);

  const addTask = () => {
    if (newTask.trim()) {
      setTasks([...tasks, {
        id: Date.now(),
        title: newTask,
        completed: false,
        priority: 'medium',
        tags: [],
        dueDate: new Date().toISOString().split('T')[0]
      }]);
      setNewTask('');
      setShowAddForm(false);
    }
  };

  const toggleTask = (id) => {
    setTasks(tasks.map(task =>
      task.id === id ? { ...task, completed: !task.completed } : task
    ));
  };

  const deleteTask = (id) => {
    setTasks(tasks.filter(task => task.id !== id));
  };

  const filteredTasks = tasks.filter(task => {
    const matchesFilter = filter === 'all' ? true :
      filter === 'active' ? !task.completed :
      filter === 'completed' ? task.completed : true;
    const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const stats = {
    total: tasks.length,
    completed: tasks.filter(t => t.completed).length,
    active: tasks.filter(t => !t.completed).length
  };

  return (
    <div className={`min-h-screen transition-all duration-700 ${darkMode ? 'dark' : ''}`}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=Quicksand:wght@300;400;500;600;700&display=swap');
        
        :root {
          --rose-mist: #EAC8CA;
          --lavender-dream: #F2D5F8;
          --orchid-whisper: #E6C0E9;
          --purple-haze: #BFABCB;
          --slate-purple: #8D89A6;
          --shadow-soft: rgba(191, 171, 203, 0.15);
          --shadow-medium: rgba(141, 137, 166, 0.2);
        }

        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        body {
          font-family: 'Quicksand', sans-serif;
        }

        .glass-effect {
          background: rgba(255, 255, 255, 0.7);
          backdrop-filter: blur(20px);
          border: 1px solid rgba(255, 255, 255, 0.8);
        }

        .dark .glass-effect {
          background: rgba(141, 137, 166, 0.2);
          border: 1px solid rgba(191, 171, 203, 0.3);
        }

        .gradient-bg {
          background: linear-gradient(135deg, 
            var(--lavender-dream) 0%, 
            var(--orchid-whisper) 50%, 
            var(--rose-mist) 100%);
        }

        .dark .gradient-bg {
          background: linear-gradient(135deg, 
            #1a1625 0%, 
            #2a2435 50%, 
            #3a3445 100%);
        }

        .floating-animation {
          animation: floating 6s ease-in-out infinite;
        }

        @keyframes floating {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-20px); }
        }

        .slide-in {
          animation: slideIn 0.5s ease-out;
        }

        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .task-enter {
          animation: taskEnter 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }

        @keyframes taskEnter {
          0% {
            opacity: 0;
            transform: scale(0.8) translateY(30px);
          }
          100% {
            opacity: 1;
            transform: scale(1) translateY(0);
          }
        }

        .hover-lift {
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .hover-lift:hover {
          transform: translateY(-4px);
          box-shadow: 0 12px 40px var(--shadow-medium);
        }

        .checkbox-custom {
          position: relative;
          cursor: pointer;
        }

        .checkbox-custom input {
          position: absolute;
          opacity: 0;
        }

        .checkbox-mark {
          width: 24px;
          height: 24px;
          border: 2px solid var(--purple-haze);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.3s ease;
          background: white;
        }

        .dark .checkbox-mark {
          background: rgba(255, 255, 255, 0.1);
          border-color: var(--orchid-whisper);
        }

        .checkbox-custom input:checked ~ .checkbox-mark {
          background: linear-gradient(135deg, var(--orchid-whisper), var(--purple-haze));
          border-color: var(--purple-haze);
        }

        .ripple {
          position: relative;
          overflow: hidden;
        }

        .ripple::after {
          content: '';
          position: absolute;
          top: 50%;
          left: 50%;
          width: 0;
          height: 0;
          border-radius: 50%;
          background: rgba(191, 171, 203, 0.4);
          transform: translate(-50%, -50%);
          transition: width 0.6s, height 0.6s;
        }

        .ripple:active::after {
          width: 300px;
          height: 300px;
        }

        .priority-high {
          border-left: 4px solid #ff6b6b;
        }

        .priority-medium {
          border-left: 4px solid #feca57;
        }

        .priority-low {
          border-left: 4px solid #48dbfb;
        }

        .tag-pill {
          background: var(--lavender-dream);
          color: var(--slate-purple);
          padding: 4px 12px;
          border-radius: 20px;
          font-size: 11px;
          font-weight: 600;
          letter-spacing: 0.5px;
          text-transform: uppercase;
        }

        .dark .tag-pill {
          background: rgba(230, 192, 233, 0.2);
          color: var(--lavender-dream);
        }

        .decorative-blob {
          position: absolute;
          border-radius: 50%;
          filter: blur(60px);
          opacity: 0.3;
          animation: blobFloat 20s ease-in-out infinite;
        }

        @keyframes blobFloat {
          0%, 100% { transform: translate(0, 0) scale(1); }
          33% { transform: translate(30px, -30px) scale(1.1); }
          66% { transform: translate(-20px, 20px) scale(0.9); }
        }

        .stat-card {
          position: relative;
          overflow: hidden;
        }

        .stat-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: -100%;
          width: 100%;
          height: 100%;
          background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
          transition: left 0.5s;
        }

        .stat-card:hover::before {
          left: 100%;
        }

        .search-glow {
          box-shadow: 0 0 0 0 rgba(230, 192, 233, 0.7);
          transition: box-shadow 0.3s ease;
        }

        .search-glow:focus {
          box-shadow: 0 0 0 4px rgba(230, 192, 233, 0.3);
        }

        .title-text {
          font-family: 'Cormorant Garamond', serif;
          font-weight: 600;
          letter-spacing: 1px;
        }

        .button-gradient {
          background: linear-gradient(135deg, var(--orchid-whisper), var(--purple-haze));
          transition: all 0.3s ease;
        }

        .button-gradient:hover {
          background: linear-gradient(135deg, var(--purple-haze), var(--slate-purple));
          transform: scale(1.05);
        }

        .smooth-scroll {
          scroll-behavior: smooth;
        }

        ::-webkit-scrollbar {
          width: 8px;
        }

        ::-webkit-scrollbar-track {
          background: var(--lavender-dream);
          border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
          background: var(--purple-haze);
          border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
          background: var(--slate-purple);
        }
      `}</style>

      {/* Background with decorative blobs */}
      <div className="gradient-bg min-h-screen relative overflow-hidden">
        <div className="decorative-blob w-96 h-96 bg-purple-300 top-10 -left-20" style={{animationDelay: '0s'}}></div>
        <div className="decorative-blob w-80 h-80 bg-pink-300 bottom-20 -right-20" style={{animationDelay: '7s'}}></div>
        <div className="decorative-blob w-72 h-72 bg-purple-200 top-1/2 left-1/3" style={{animationDelay: '14s'}}></div>

        <div className="relative z-10 container mx-auto px-4 py-8 max-w-5xl">
          {/* Header */}
          <div className="text-center mb-12 floating-animation">
            <div className="flex items-center justify-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-purple-300 to-purple-400 flex items-center justify-center shadow-lg">
                <CheckCircle2 className="w-7 h-7 text-white" />
              </div>
              <h1 className="title-text text-5xl dark:text-white" style={{color: '#8D89A6'}}>
                Dream<span style={{color: '#E6C0E9'}}>Flow</span>
              </h1>
            </div>
            <p className="text-slate-600 dark:text-slate-300 text-sm tracking-wide">
              Your elegant task companion
            </p>
          </div>

          {/* Dark Mode Toggle */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="fixed top-6 right-6 w-12 h-12 rounded-full glass-effect flex items-center justify-center hover-lift shadow-lg ripple z-50"
          >
            {darkMode ? (
              <Sun className="w-5 h-5" style={{color: '#F2D5F8'}} />
            ) : (
              <Moon className="w-5 h-5" style={{color: '#8D89A6'}} />
            )}
          </button>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {[
              { label: 'Total Tasks', value: stats.total, icon: Circle, color: '#BFABCB' },
              { label: 'Completed', value: stats.completed, icon: CheckCircle2, color: '#E6C0E9' },
              { label: 'Active', value: stats.active, icon: Star, color: '#EAC8CA' }
            ].map((stat, idx) => (
              <div
                key={stat.label}
                className="stat-card glass-effect rounded-3xl p-6 hover-lift slide-in"
                style={{animationDelay: `${idx * 0.1}s`}}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-slate-500 dark:text-slate-400 mb-1 uppercase tracking-wider font-medium">
                      {stat.label}
                    </p>
                    <p className="text-4xl font-bold title-text" style={{color: stat.color}}>
                      {stat.value}
                    </p>
                  </div>
                  <div
                    className="w-16 h-16 rounded-2xl flex items-center justify-center shadow-md"
                    style={{backgroundColor: stat.color + '30'}}
                  >
                    <stat.icon className="w-8 h-8" style={{color: stat.color}} />
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Search and Filter Bar */}
          <div className="glass-effect rounded-3xl p-6 mb-8 slide-in" style={{animationDelay: '0.3s'}}>
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5" style={{color: '#BFABCB'}} />
                <input
                  type="text"
                  placeholder="Search your dreams..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-3 rounded-2xl border-2 border-transparent bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow transition-all dark:text-white"
                  style={{borderColor: 'transparent'}}
                />
              </div>
              <div className="flex gap-2">
                {['all', 'active', 'completed'].map((f) => (
                  <button
                    key={f}
                    onClick={() => setFilter(f)}
                    className={`px-6 py-3 rounded-2xl font-medium transition-all ripple capitalize ${
                      filter === f
                        ? 'button-gradient text-white shadow-lg'
                        : 'bg-white/50 dark:bg-slate-800/50 hover:bg-white/80 dark:hover:bg-slate-700/50'
                    }`}
                    style={filter !== f ? {color: '#8D89A6'} : {}}
                  >
                    {f}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Add Task Button/Form */}
          {!showAddForm ? (
            <button
              onClick={() => setShowAddForm(true)}
              className="w-full glass-effect rounded-3xl p-6 mb-8 hover-lift flex items-center justify-center gap-3 ripple group slide-in"
              style={{animationDelay: '0.4s'}}
            >
              <div className="w-12 h-12 rounded-2xl button-gradient flex items-center justify-center shadow-lg">
                <Plus className="w-6 h-6 text-white" />
              </div>
              <span className="text-lg font-semibold" style={{color: '#8D89A6'}}>
                Add a New Dream
              </span>
            </button>
          ) : (
            <div className="glass-effect rounded-3xl p-6 mb-8 task-enter">
              <div className="flex gap-3">
                <input
                  type="text"
                  placeholder="What's on your mind?"
                  value={newTask}
                  onChange={(e) => setNewTask(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && addTask()}
                  autoFocus
                  className="flex-1 px-4 py-3 rounded-2xl border-2 bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow dark:text-white"
                  style={{borderColor: '#E6C0E9'}}
                />
                <button
                  onClick={addTask}
                  className="px-8 py-3 rounded-2xl button-gradient text-white font-semibold hover-lift shadow-lg ripple"
                >
                  Add
                </button>
                <button
                  onClick={() => setShowAddForm(false)}
                  className="px-6 py-3 rounded-2xl bg-white/50 dark:bg-slate-800/50 hover:bg-white/80 dark:hover:bg-slate-700/50 ripple"
                  style={{color: '#8D89A6'}}
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          {/* Tasks List */}
          <div className="space-y-4 smooth-scroll">
            {filteredTasks.length === 0 ? (
              <div className="glass-effect rounded-3xl p-12 text-center slide-in">
                <div className="w-24 h-24 rounded-3xl mx-auto mb-6 flex items-center justify-center" style={{backgroundColor: '#F2D5F8'}}>
                  <CheckCircle2 className="w-12 h-12" style={{color: '#BFABCB'}} />
                </div>
                <p className="text-xl font-semibold mb-2" style={{color: '#8D89A6'}}>
                  {searchQuery ? 'No tasks found' : filter === 'completed' ? 'No completed tasks yet' : 'Your canvas is blank'}
                </p>
                <p className="text-slate-500 dark:text-slate-400">
                  {searchQuery ? 'Try a different search term' : 'Start by adding your first dream'}
                </p>
              </div>
            ) : (
              filteredTasks.map((task, idx) => (
                <div
                  key={task.id}
                  className={`glass-effect rounded-3xl p-6 hover-lift task-enter priority-${task.priority}`}
                  style={{animationDelay: `${idx * 0.05}s`}}
                >
                  <div className="flex items-start gap-4">
                    <label className="checkbox-custom mt-1">
                      <input
                        type="checkbox"
                        checked={task.completed}
                        onChange={() => toggleTask(task.id)}
                      />
                      <div className="checkbox-mark">
                        {task.completed && <Check className="w-4 h-4 text-white" />}
                      </div>
                    </label>

                    <div className="flex-1">
                      <h3
                        className={`text-lg font-semibold mb-2 transition-all ${
                          task.completed ? 'line-through opacity-50' : ''
                        }`}
                        style={{color: darkMode ? '#F2D5F8' : '#8D89A6'}}
                      >
                        {task.title}
                      </h3>
                      <div className="flex flex-wrap items-center gap-3">
                        {task.tags.map((tag) => (
                          <span key={tag} className="tag-pill">
                            {tag}
                          </span>
                        ))}
                        {task.dueDate && (
                          <div className="flex items-center gap-1 text-sm" style={{color: '#BFABCB'}}>
                            <Calendar className="w-4 h-4" />
                            <span>{new Date(task.dueDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</span>
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <button
                        onClick={() => deleteTask(task.id)}
                        className="w-10 h-10 rounded-xl bg-white/50 dark:bg-slate-800/50 hover:bg-red-100 dark:hover:bg-red-900/30 flex items-center justify-center transition-all ripple group"
                      >
                        <Trash2 className="w-4 h-4 text-slate-400 group-hover:text-red-500 transition-colors" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer */}
          <div className="text-center mt-12 py-6">
            <p className="text-sm" style={{color: '#BFABCB'}}>
              Made with ✨ for dreamers and doers
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
