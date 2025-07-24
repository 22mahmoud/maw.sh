import path from 'node:path';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [tailwindcss()],
  base: '/static',
  resolve: {
    alias: {
      '@': path.resolve('src/resources'),
    },
  },
  build: {
    manifest: 'manifest.json',
    outDir: path.resolve('./static'),
    emptyOutDir: true,
    minify: 'terser',
    cssMinify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (/node_modules\/(htmx\.org|alpinejs)\//.test(id)) {
            return 'vendor';
          }
        },
      },
      input: {
        app: 'src/resources/js/app.ts',
        admin: 'src/resources/js/admin.ts',
      },
    },
  },
});
