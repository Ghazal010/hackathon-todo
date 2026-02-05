/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./frontend/src/app/**/*.{js,ts,jsx,tsx}",
    "./frontend/src/pages/**/*.{js,ts,jsx,tsx}",
    "./frontend/src/components/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Enable dark mode with class strategy
  theme: {
    extend: {
      colors: {
        'rose-mist': '#EAC8CA',
        'lavender-dream': '#F2D5F8',
        'orchid-whisper': '#E6C0E9',
        'purple-haze': '#BFABCB',
        'slate-purple': '#8D89A6',
      },
    },
  },
  plugins: [],
}