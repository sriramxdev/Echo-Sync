// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://sriramxdev.github.io',
  base: '/Echo-Sync',
  integrations: [
    starlight({
      title: 'Echo-Sync',
      customCss: ['./src/styles/global.css'],
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/sriramxdev/Echo-Sync' }
      ],
      sidebar: [
        {
          label: 'Overview',
          items: [{ autogenerate: { directory: 'overview' } }],
        },
        {
          label: 'Pipeline & Core',
          items: [{ autogenerate: { directory: 'pipeline' } }],
        },
        {
          label: 'Models',
          items: [{ autogenerate: { directory: 'models' } }],
        },
        {
          label: 'Edge & Engine',
          items: [{ autogenerate: { directory: 'edge' } }],
        },
      ],
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});