/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'gr-red': '#eb0a1e',
        'gr-black': '#1a1a1a',
      }
    },
  },
  plugins: [],
}
