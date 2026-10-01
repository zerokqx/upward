import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'
import { devtools } from '@tanstack/devtools-vite'
import { TanStackRouterVite } from '@tanstack/router-plugin/vite'
import viteReact, { reactCompilerPreset } from '@vitejs/plugin-react'
import babel from '@rolldown/plugin-babel'
import tailwindcss from '@tailwindcss/vite'

const config = defineConfig({
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '#': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },

  plugins: [
    devtools(),
    TanStackRouterVite({
      target: 'react',
      autoCodeSplitting: true,
    }),
    tailwindcss(),
    viteReact(),
    babel({ presets: [reactCompilerPreset()] }),
  ],
})

export default config
