import { defineConfig } from 'vite';

export default defineConfig({
  // Base public path
  base: './',
  
  // Development server configuration
  server: {
    port: 4000,
    open: true, // Automatically open browser
    host: true, // Allow external connections
  },
  
  // Build configuration
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: true,
    rollupOptions: {
      input: {
        main: './index.html'
      }
    }
  },
  
  // Assets handling
  assetsInclude: ['**/*.svg', '**/*.png', '**/*.jpg', '**/*.ico'],
  
  // CSS configuration
  css: {
    devSourcemap: true
  }
});
