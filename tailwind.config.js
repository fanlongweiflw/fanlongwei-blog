/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: { display: ['Instrument Serif', 'serif'], body: ['Inter', 'sans-serif'] },
      colors: { ink: '#021f2e', paper: '#f7f1e8' },
    },
  },
  plugins: [],
};
