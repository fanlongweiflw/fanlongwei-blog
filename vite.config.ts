import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  css: { transformer: 'postcss' },
  build: { cssMinify: 'esbuild' },
  test: { environment: 'jsdom', globals: true, setupFiles: './src/test/setup.ts' },
});
