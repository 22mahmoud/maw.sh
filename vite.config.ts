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
    rollupOptions: {
      output: {
        advancedChunks: {
          groups: [{ name: 'vendor', test: /node_modules\/htmx\.org\// }],
        },
      },
      input: {
        app: 'src/resources/js/app.ts',
        admin: 'src/resources/js/admin.ts',
        'contact-recaptcha': 'src/resources/js/contact-recaptcha.ts',
      },
    },
  },
});
