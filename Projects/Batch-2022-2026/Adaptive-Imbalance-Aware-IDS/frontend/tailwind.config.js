/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        soc: {
          bg: '#0d1117',
          panel: '#161b22',
          border: '#30363d',
          green: '#3fb950',
          red: '#f85149',
          amber: '#d29922',
          blue: '#58a6ff',
        },
      },
      fontFamily: { mono: ['ui-monospace', 'Cascadia Code', 'Monaco', 'monospace'] },
    },
  },
  plugins: [],
};
