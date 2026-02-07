'use client';

import React, { useState, useEffect } from 'react';
import { Plus, Check, Trash2, Calendar, Search, Filter, Star, Moon, Sun, Circle, CheckCircle2, Clock } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useRouter } from 'next/navigation';

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
  user_id: number;
}

interface Subtask {
  id: string;
  title: string;
  completed: boolean;
}

export default function TodoApp() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  // State for form inputs
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
    } else {
      // Load tasks for authenticated user
      fetchTasks();
    }
  }, [isAuthenticated, router]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('access_token');

      if (!token) {
        router.push('/login');
        return;
      }

      const response = await fetch('https://ghazakshaikh1-to-do-app.hf.space/api/tasks', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          router.push('/login');
          return;
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setTasks(data.data.tasks || []);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      // Set to empty array on error but continue to show UI
      setTasks([]);
    } finally {
      setLoading(false);
    }
  };

  // Only render if authenticated
  if (!isAuthenticated) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-center">
          <p>Redirecting to login...</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-center">
          <p>Loading your tasks...</p>
        </div>
      </div>
    );
  }

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
        notifyBefore: newTaskNotifyBefore
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
                    onClick={() => setFilter(f as 'all' | 'active' | 'completed')}
                    className={`px-6 py-3 rounded-2xl font-medium transition-all ripple capitalize ${
                      f === filter
                        ? 'button-gradient text-white shadow-lg'
                        : 'bg-white/50 dark:bg-slate-800/50 hover:bg-white/80 dark:hover:bg-slate-700/50'
                    }`}
                    style={f !== filter ? {color: '#8D89A6'} : {}}
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
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="col-span-2">
                  <input
                    type="text"
                    placeholder="What's on your mind?"
                    value={newTask}
                    onChange={(e) => setNewTask(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && addTask()}
                    autoFocus
                    className="w-full px-4 py-3 rounded-2xl border-2 bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow dark:text-white"
                    style={{borderColor: '#E6C0E9'}}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2" style={{color: '#8D89A6'}}>Category</label>
                  <select
                    value={newTaskCategory}
                    onChange={(e) => setNewTaskCategory(e.target.value)}
                    className="w-full px-4 py-3 rounded-2xl border-2 bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow dark:text-white"
                    style={{borderColor: '#E6C0E9'}}
                  >
                    <option value="personal">Personal</option>
                    <option value="work">Work</option>
                    <option value="office">Office</option>
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
                    className="w-full px-4 py-3 rounded-2xl border-2 bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow dark:text-white"
                    style={{borderColor: '#E6C0E9'}}
                  >
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2" style={{color: '#8D89A6'}}>Due Date</label>
                  <input
                    type="date"
                    value={newTaskDueDate}
                    onChange={(e) => setNewTaskDueDate(e.target.value)}
                    className="w-full px-4 py-3 rounded-2xl border-2 bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow dark:text-white"
                    style={{borderColor: '#E6C0E9'}}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2" style={{color: '#8D89A6'}}>Recurring</label>
                  <select
                    value={newTaskRecurring || ''}
                    onChange={(e) => setNewTaskRecurring(e.target.value || null)}
                    className="w-full px-4 py-3 rounded-2xl border-2 bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow dark:text-white"
                    style={{borderColor: '#E6C0E9'}}
                  >
                    <option value="">None</option>
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                  </select>
                </div>

                <div className="col-span-2">
                  <label className="block text-sm font-medium mb-2" style={{color: '#8D89A6'}}>Tags (comma separated)</label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      placeholder="Enter tags separated by commas"
                      value={newTaskTagInput}
                      onChange={(e) => setNewTaskTagInput(e.target.value)}
                      onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          const tags = newTaskTagInput.split(',').map(tag => tag.trim()).filter(tag => tag);
                          setNewTaskTags(prev => [...prev, ...tags]);
                          setNewTaskTagInput('');
                        }
                      }}
                      className="flex-1 px-4 py-3 rounded-2xl border-2 bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow dark:text-white"
                      style={{borderColor: '#E6C0E9'}}
                    />
                    <button
                      type="button"
                      onClick={() => {
                        const tags = newTaskTagInput.split(',').map(tag => tag.trim()).filter(tag => tag);
                        setNewTaskTags(prev => [...prev, ...tags]);
                        setNewTaskTagInput('');
                      }}
                      className="px-4 py-3 rounded-2xl bg-white/50 dark:bg-slate-800/50 hover:bg-white/80 dark:hover:bg-slate-700/50 ripple"
                      style={{color: '#8D89A6'}}
                    >
                      Add
                    </button>
                  </div>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {newTaskTags.map((tag, index) => (
                      <span key={index} className="tag-pill flex items-center gap-1">
                        {tag}
                        <button
                          type="button"
                          onClick={() => setNewTaskTags(prev => prev.filter((_, i) => i !== index))}
                          className="ml-1 text-red-500 hover:text-red-700"
                        >
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2" style={{color: '#8D89A6'}}>Progress (%)</label>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={newTaskProgress}
                    onChange={(e) => setNewTaskProgress(parseInt(e.target.value))}
                    className="w-full"
                  />
                  <div className="text-center text-sm" style={{color: '#8D89A6'}}>{newTaskProgress}%</div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2" style={{color: '#8D89A6'}}>Notification Before (minutes)</label>
                  <select
                    value={newTaskNotifyBefore || ''}
                    onChange={(e) => setNewTaskNotifyBefore(e.target.value ? parseInt(e.target.value) : null)}
                    className="w-full px-4 py-3 rounded-2xl border-2 bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow dark:text-white"
                    style={{borderColor: '#E6C0E9'}}
                  >
                    <option value="">None</option>
                    <option value="5">5 minutes</option>
                    <option value="15">15 minutes</option>
                    <option value="30">30 minutes</option>
                    <option value="60">1 hour</option>
                    <option value="120">2 hours</option>
                    <option value="1440">1 day</option>
                  </select>
                </div>

                <div className="col-span-2">
                  <label className="block text-sm font-medium mb-2" style={{color: '#8D89A6'}}>Subtasks</label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      placeholder="Add a subtask"
                      value={newSubtaskTitle}
                      onChange={(e) => setNewSubtaskTitle(e.target.value)}
                      onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          if (newSubtaskTitle.trim()) {
                            setNewTaskSubtasks(prev => [...prev, {id: Date.now().toString(), title: newSubtaskTitle, completed: false}]);
                            setNewSubtaskTitle('');
                          }
                        }
                      }}
                      className="flex-1 px-4 py-3 rounded-2xl border-2 bg-white/50 dark:bg-slate-800/50 focus:outline-none search-glow dark:text-white"
                      style={{borderColor: '#E6C0E9'}}
                    />
                    <button
                      type="button"
                      onClick={() => {
                        if (newSubtaskTitle.trim()) {
                          setNewTaskSubtasks(prev => [...prev, {id: Date.now().toString(), title: newSubtaskTitle, completed: false}]);
                          setNewSubtaskTitle('');
                        }
                      }}
                      className="px-4 py-3 rounded-2xl bg-white/50 dark:bg-slate-800/50 hover:bg-white/80 dark:hover:bg-slate-700/50 ripple"
                      style={{color: '#8D89A6'}}
                    >
                      Add
                    </button>
                  </div>
                  <div className="mt-2">
                    {newTaskSubtasks.map((subtask, index) => (
                      <div key={subtask.id} className="flex items-center gap-2 mb-1">
                        <input
                          type="checkbox"
                          checked={subtask.completed}
                          onChange={() => {
                            const updatedSubtasks = [...newTaskSubtasks];
                            updatedSubtasks[index] = {...subtask, completed: !subtask.completed};
                            setNewTaskSubtasks(updatedSubtasks);
                          }}
                          className="w-4 h-4"
                        />
                        <span className={subtask.completed ? 'line-through opacity-50' : ''} style={{color: '#8D89A6'}}>
                          {subtask.title}
                        </span>
                        <button
                          type="button"
                          onClick={() => setNewTaskSubtasks(prev => prev.filter((_, i) => i !== index))}
                          className="text-red-500 hover:text-red-700 ml-2"
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="col-span-2 flex gap-3 justify-end">
                  <button
                    onClick={addTask}
                    className="px-8 py-3 rounded-2xl button-gradient text-white font-semibold hover-lift shadow-lg ripple"
                  >
                    Add Task
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
                      <div className="flex items-center gap-3 mb-1">
                        <span className="text-xs px-2 py-1 rounded-full text-white font-medium"
                          style={{
                            backgroundColor: task.category === 'work' ? '#BFABCB' :
                                            task.category === 'personal' ? '#E6C0E9' :
                                            task.category === 'office' ? '#EAC8CA' :
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
                            {tag}
                          </span>
                        ))}
                        {task.dueDate && (
                          <div className="flex items-center gap-1 text-sm" style={{color: '#BFABCB'}}>
                            <Calendar className="w-4 h-4" />
                            <span>{new Date(task.dueDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</span>
                          </div>
                        )}
                        {task.createdAt && (
                          <div className="flex items-center gap-1 text-sm" style={{color: '#BFABCB'}}>
                            <Calendar className="w-4 h-4" />
                            <span>Added: {new Date(task.createdAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</span>
                          </div>
                        )}
                        {task.notifyBefore && (
                          <div className="flex items-center gap-1 text-sm" style={{color: '#BFABCB'}}>
                            <Clock className="w-4 h-4" />
                            <span>Notify: {task.notifyBefore} min before</span>
                          </div>
                        )}
                        {task.recurring && (
                          <div className="flex items-center gap-1 text-sm" style={{color: '#BFABCB'}}>
                            <Star className="w-4 h-4" />
                            <span>{task.recurring}</span>
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