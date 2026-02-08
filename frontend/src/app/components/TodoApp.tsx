'use client';

import React, { useState, useEffect } from 'react';
import { Plus, Check, Trash2, Calendar, Search, Filter, Star, Moon, Sun, Circle, CheckCircle2, Clock } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useRouter } from 'next/navigation';

interface Subtask {
  id: string;
  title: string;
  completed: boolean;
}

interface Task {
  id: number;
  title: string;
  completed: boolean;
  priority: 'high' | 'medium' | 'low';
  tags: string[];
  dueDate: string;
  category: string;
  createdAt: string;
  recurring: string | null;
  progress: number; // 0-100 percentage
  subtasks: Subtask[]; // Array of subtasks
  notifyBefore: number | null; // Minutes before deadline to notify
  updatedAt?: string;
  user_id: number; // Required field for user association
}

export default function TodoApp() {
  const { isAuthenticated, user } = useAuth();
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([
    {
      id: 1,
      title: 'Design new landing page',
      completed: false,
      priority: 'high',
      tags: ['work'],
      dueDate: '2024-02-15',
      category: 'work',
      createdAt: '2024-01-29',
      recurring: null,
      progress: 30,
      subtasks: [
        {id: '1', title: 'Research design trends', completed: true},
        {id: '2', title: 'Create wireframes', completed: false}
      ],
      notifyBefore: 30,
      user_id: 1
    },
    {
      id: 2,
      title: 'Morning meditation',
      completed: true,
      priority: 'medium',
      tags: ['personal'],
      dueDate: '2024-02-10',
      category: 'personal',
      createdAt: '2024-01-29',
      recurring: 'daily',
      progress: 100,
      subtasks: [],
      notifyBefore: null,
      user_id: 1
    },
    {
      id: 3,
      title: 'Grocery shopping',
      completed: false,
      priority: 'low',
      tags: ['errands'],
      dueDate: '2024-02-12',
      category: 'errands',
      createdAt: '2024-01-29',
      recurring: null,
      progress: 0,
      subtasks: [],
      notifyBefore: 60,
      user_id: 1
    }
  ]);

  const [newTask, setNewTask] = useState('');
  const [newTaskCategory, setNewTaskCategory] = useState('personal');
  const [newTaskDueDate, setNewTaskDueDate] = useState('');
  const [newTaskPriority, setNewTaskPriority] = useState<'high' | 'medium' | 'low'>('medium');
  const [newTaskTags, setNewTaskTags] = useState<string[]>([]);
  const [newTaskTagInput, setNewTaskTagInput] = useState('');
  const [newTaskRecurring, setNewTaskRecurring] = useState<string | null>(null);
  const [newTaskProgress, setNewTaskProgress] = useState<number>(0);
  const [newTaskSubtasks, setNewTaskSubtasks] = useState<Subtask[]>([]);
  const [newTaskNotifyBefore, setNewTaskNotifyBefore] = useState<number | null>(null);
  const [newSubtaskTitle, setNewSubtaskTitle] = useState('');
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  const addTask = () => {
    if (newTask.trim()) {
      const task: Task = {
        id: Date.now(),
        title: newTask,
        completed: false,
        priority: newTaskPriority,
        tags: newTaskTags,
        dueDate: newTaskDueDate || new Date().toISOString().split('T')[0],
        category: newTaskCategory,
        createdAt: new Date().toISOString().split('T')[0],
        recurring: newTaskRecurring || null,
        progress: newTaskProgress,
        subtasks: newTaskSubtasks,
        notifyBefore: newTaskNotifyBefore,
        user_id: user?.id || 1  // Use actual user ID from auth context, fallback to 1
      };
      setTasks([...tasks, task]);
      setNewTask('');
      setNewTaskCategory('personal');
      setNewTaskDueDate('');
      setNewTaskPriority('medium');
      setNewTaskTags([]);
      setNewTaskTagInput('');
      setNewTaskRecurring(null);
      setNewTaskProgress(0);
      setNewTaskSubtasks([]);
      setNewTaskNotifyBefore(null);
      setNewSubtaskTitle('');
      setShowAddForm(false);
    }
  };

  const toggleTask = (id: number) => {
    setTasks(tasks.map(task =>
      task.id === id ? { ...task, completed: !task.completed } : task
    ));
  };

  const deleteTask = (id: number) => {
    setTasks(tasks.filter(task => task.id !== id));
  };

  const addSubtask = () => {
    if (newSubtaskTitle.trim()) {
      const newSubtask: Subtask = {
        id: Date.now().toString(),
        title: newSubtaskTitle,
        completed: false
      };
      setNewTaskSubtasks([...newTaskSubtasks, newSubtask]);
      setNewSubtaskTitle('');
    }
  };

  const toggleSubtask = (subtaskId: string) => {
    setNewTaskSubtasks(newTaskSubtasks.map(subtask =>
      subtask.id === subtaskId ? { ...subtask, completed: !subtask.completed } : subtask
    ));
  };

  const removeSubtask = (subtaskId: string) => {
    setNewTaskSubtasks(newTaskSubtasks.filter(subtask => subtask.id !== subtaskId));
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

  if (!isAuthenticated) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-center">
          <p>Redirecting to login...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen transition-all duration-700 ${darkMode ? 'dark' : ''}`}>
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
                Dream<span style={{color: '#BFABCB'}}>Flow</span>
              </h1>
            </div>
            <p className="text-slate-600 dark:text-slate-300 text-sm tracking-wide">
              Your elegant task companion
            </p>
          </div>

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
                  className="w-full pl-12 pr-4 py-3 rounded-xl border-2 border-transparent bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow transition-all dark:text-white"
                  style={{borderColor: 'transparent'}}
                />
              </div>
              <div className="flex gap-2">
                {['all', 'active', 'completed'].map((f) => (
                  <button
                    key={f}
                    onClick={() => setFilter(f as 'all' | 'active' | 'completed')}
                    className={`px-4 py-2 rounded-lg transition-colors flex items-center space-x-2 ${
                      f === filter
                        ? 'bg-white/20 text-white'
                        : 'hover:bg-white/10'
                    }`}
                    style={f !== filter ? {color: '#8D89A6'} : {}}
                  >
                    <Filter className="w-4 h-4" />
                    <span className="capitalize">{f}</span>
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
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="col-span-2">
                  <input
                    type="text"
                    placeholder="What's on your mind?"
                    value={newTask}
                    onChange={(e) => setNewTask(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl border-2 bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow dark:text-white"
                    style={{borderColor: '#E6C0E9'}}
                    autoFocus
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2" style={{color: '#8D89A6'}}>Category</label>
                  <select
                    value={newTaskCategory}
                    onChange={(e) => setNewTaskCategory(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl border-2 bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow dark:text-white"
                    style={{borderColor: '#E6C0E9'}}
                  >
                    <option value="personal">Personal</option>
                    <option value="work">Work</option>
                    <option value="health">Health</option>
                    <option value="finance">Finance</option>
                    <option value="education">Education</option>
                    <option value="errands">Errands</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2" style={{color: '#8D89A6'}}>Priority</label>
                  <select
                    value={newTaskPriority}
                    onChange={(e) => setNewTaskPriority(e.target.value as 'high' | 'medium' | 'low')}
                    className="w-full px-4 py-3 rounded-xl border-2 bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow dark:text-white"
                    style={{borderColor: '#E6C0E9'}}
                  >
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2" style={{color: '#8D89A6'}}>Due Date</label>
                  <div className="relative">
                    <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5" style={{color: '#BFABCB'}} />
                    <input
                      type="date"
                      value={newTaskDueDate}
                      onChange={(e) => setNewTaskDueDate(e.target.value)}
                      className="w-full pl-10 pr-4 py-3 rounded-xl border-2 bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow dark:text-white"
                      style={{borderColor: '#E6C0E9'}}
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2" style={{color: '#8D89A6'}}>Progress</label>
                  <div className="flex items-center gap-2">
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={newTaskProgress}
                      onChange={(e) => setNewTaskProgress(parseInt(e.target.value))}
                      className="flex-1"
                    />
                    <span className="text-sm w-10" style={{color: '#8D89A6'}}>{newTaskProgress}%</span>
                  </div>
                </div>

                <div className="col-span-2">
                  <label className="block text-sm font-medium mb-2" style={{color: '#8D89A6'}}>Tags</label>
                  <div className="flex gap-2 mb-2">
                    <input
                      type="text"
                      placeholder="Add a tag"
                      value={newTaskTagInput}
                      onChange={(e) => setNewTaskTagInput(e.target.value)}
                      onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          if (newTaskTagInput.trim() && !newTaskTags.includes(newTaskTagInput.trim())) {
                            setNewTaskTags([...newTaskTags, newTaskTagInput.trim()]);
                            setNewTaskTagInput('');
                          }
                        }
                      }}
                      className="flex-1 px-4 py-3 rounded-xl border-2 bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow dark:text-white"
                      style={{borderColor: '#E6C0E9'}}
                    />
                    <button
                      type="button"
                      onClick={() => {
                        if (newTaskTagInput.trim() && !newTaskTags.includes(newTaskTagInput.trim())) {
                          setNewTaskTags([...newTaskTags, newTaskTagInput.trim()]);
                          setNewTaskTagInput('');
                        }
                      }}
                      className="px-4 py-3 rounded-xl bg-white/50 dark:bg-slate-800/50 hover:bg-white/80 dark:hover:bg-slate-700/50 ripple"
                      style={{color: '#8D89A6'}}
                    >
                      Add
                    </button>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {newTaskTags.map((tag, index) => (
                      <span
                        key={index}
                        className="tag-pill flex items-center gap-1 px-3 py-1 rounded-full text-sm"
                        style={{backgroundColor: '#BFABCB' + '30', color: '#8D89A6'}}
                      >
                        {tag}
                        <button
                          type="button"
                          onClick={() => setNewTaskTags(newTaskTags.filter((_, i) => i !== index))}
                          className="ml-1 text-red-500 hover:text-red-700"
                        >
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
                </div>

                <div className="col-span-2">
                  <label className="block text-sm font-medium mb-2" style={{color: '#8D89A6'}}>Subtasks</label>
                  <div className="flex gap-2 mb-2">
                    <input
                      type="text"
                      placeholder="Add a subtask"
                      value={newSubtaskTitle}
                      onChange={(e) => setNewSubtaskTitle(e.target.value)}
                      onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          addSubtask();
                        }
                      }}
                      className="flex-1 px-4 py-3 rounded-xl border-2 bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow dark:text-white"
                      style={{borderColor: '#E6C0E9'}}
                    />
                    <button
                      type="button"
                      onClick={addSubtask}
                      className="px-4 py-3 rounded-xl bg-white/50 dark:bg-slate-800/50 hover:bg-white/80 dark:hover:bg-slate-700/50 ripple"
                      style={{color: '#8D89A6'}}
                    >
                      Add
                    </button>
                  </div>
                  <div className="space-y-2">
                    {newTaskSubtasks.map((subtask) => (
                      <div key={subtask.id} className="flex items-center gap-2 p-2 bg-white/30 dark:bg-slate-700/30 rounded-lg">
                        <input
                          type="checkbox"
                          checked={subtask.completed}
                          onChange={() => toggleSubtask(subtask.id)}
                          className="w-5 h-5 rounded"
                        />
                        <span className={`${subtask.completed ? 'line-through opacity-50' : ''}`} style={{color: '#8D89A6'}}>
                          {subtask.title}
                        </span>
                        <button
                          type="button"
                          onClick={() => removeSubtask(subtask.id)}
                          className="ml-auto text-red-500 hover:text-red-700"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="col-span-2 flex gap-3 justify-end">
                  <button
                    onClick={addTask}
                    className="px-8 py-3 rounded-xl button-gradient text-white font-semibold hover:opacity-90 transition-opacity shadow-lg ripple"
                  >
                    Add Task
                  </button>
                  <button
                    onClick={() => setShowAddForm(false)}
                    className="px-6 py-3 rounded-xl bg-white/50 dark:bg-slate-800/50 hover:bg-white/80 dark:hover:bg-slate-700/50 ripple"
                    style={{color: '#8D89A6'}}
                  >
                    Cancel
                  </button>
                </div>
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
              filteredTasks.map((task) => (
                <div
                  key={task.id}
                  className={`glass-effect rounded-3xl p-6 hover-lift task-enter priority-${task.priority}`}
                  style={{animationDelay: `${task.id * 0.05}s`}}
                >
                  <div className="flex items-start gap-4">
                    <button
                      onClick={() => toggleTask(task.id)}
                      className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${
                        task.completed
                          ? 'bg-gradient-to-br from-purple-400 to-purple-500 border-transparent'
                          : 'border-purple-300 hover:border-purple-400'
                      }`}
                    >
                      {task.completed && <Check className="w-4 h-4 text-white" />}
                    </button>

                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-1">
                        <span className="text-xs px-2 py-1 rounded-full text-white font-medium"
                          style={{
                            backgroundColor: task.category === 'work' ? '#BFABCB' :
                                            task.category === 'personal' ? '#E6C0E9' :
                                            task.category === 'health' ? '#48DBFB' :
                                            task.category === 'finance' ? '#FECB57' :
                                            task.category === 'education' ? '#1DD1A1' :
                                            task.category === 'errands' ? '#FF9FF3' : '#BFABCB'
                          }}
                        >
                          {task.category}
                        </span>
                        <span className={`text-xs px-2 py-1 rounded-full text-white font-medium ${
                          task.priority === 'high' ? 'bg-red-500' :
                          task.priority === 'medium' ? 'bg-yellow-500' : 'bg-blue-500'
                        }`}>
                          {task.priority}
                        </span>
                        {task.dueDate && (
                          <span className="text-xs px-2 py-1 rounded-full bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-200 flex items-center gap-1">
                            <Calendar className="w-3 h-3" />
                            {new Date(task.dueDate).toLocaleDateString()}
                          </span>
                        )}
                      </div>
                      <h3
                        className={`text-lg font-semibold mb-2 transition-all ${
                          task.completed ? 'line-through opacity-50' : ''
                        }`}
                        style={{color: darkMode ? '#F2D5F8' : '#8D89A6'}}
                      >
                        {task.title}
                      </h3>

                      {/* Progress bar */}
                      {task.progress > 0 && (
                        <div className="mb-2">
                          <div className="flex justify-between text-sm mb-1" style={{color: '#BFABCB'}}>
                            <span>Progress</span>
                            <span>{task.progress}%</span>
                          </div>
                          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                            <div
                              className="h-2 rounded-full"
                              style={{
                                width: `${task.progress}%`,
                                backgroundColor: task.progress < 30 ? '#FF6B6B' :
                                                task.progress < 70 ? '#FECB57' : '#1DD1A1'
                              }}
                            ></div>
                          </div>
                        </div>
                      )}

                      {/* Subtasks */}
                      {task.subtasks && task.subtasks.length > 0 && (
                        <div className="mb-2">
                          <div className="flex items-center gap-2 text-sm mb-1" style={{color: '#BFABCB'}}>
                            <CheckCircle2 className="w-4 h-4" />
                            <span>
                              {task.subtasks.filter(st => st.completed).length}/{task.subtasks.length} subtasks
                            </span>
                          </div>
                          <div className="ml-2">
                            {task.subtasks.slice(0, 2).map((subtask, idx) => (
                              <div key={subtask.id} className="flex items-center gap-1 text-xs" style={{color: '#BFABCB'}}>
                                <Check className={`w-3 h-3 ${subtask.completed ? 'text-green-500' : 'text-gray-400'}`} />
                                <span className={subtask.completed ? 'line-through' : ''}>
                                  {subtask.title}
                                </span>
                              </div>
                            ))}
                            {task.subtasks.length > 2 && (
                              <div className="text-xs" style={{color: '#BFABCB'}}>
                                +{task.subtasks.length - 2} more
                              </div>
                            )}
                          </div>
                        </div>
                      )}

                      <div className="flex flex-wrap items-center gap-3">
                        {task.tags.map((tag) => (
                          <span key={tag} className="tag-pill">
                            #{tag}
                          </span>
                        ))}
                        {task.dueDate && (
                          <div className="flex items-center gap-1 text-sm" style={{color: '#BFABCB'}}>
                            <Calendar className="w-4 h-4" />
                            <span>Due: {new Date(task.dueDate).toLocaleDateString()}</span>
                          </div>
                        )}
                        {task.recurring && (
                          <div className="flex items-center gap-1 text-sm" style={{color: '#BFABCB'}}>
                            <Clock className="w-4 h-4" />
                            <span>Recurring: {task.recurring}</span>
                          </div>
                        )}
                        {task.notifyBefore && (
                          <div className="flex items-center gap-1 text-sm" style={{color: '#BFABCB'}}>
                            <Clock className="w-4 h-4" />
                            <span>Notify: {task.notifyBefore} min before</span>
                          </div>
                        )}
                      </div>
                    </div>

                    <button
                      onClick={() => deleteTask(task.id)}
                      className="w-10 h-10 rounded-xl bg-white/50 dark:bg-slate-800/50 hover:bg-red-100 dark:hover:bg-red-900/30 flex items-center justify-center transition-all ripple"
                    >
                      <Trash2 className="w-5 h-5 text-slate-400 hover:text-red-500" />
                    </button>
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