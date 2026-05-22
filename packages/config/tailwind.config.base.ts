import type { Config } from "tailwindcss";

export const baseConfig: Partial<Config> = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#fff7ed",
          500: "#f97316",
          600: "#ea580c",
          900: "#7c2d12",
        },
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
    },
  },
};
