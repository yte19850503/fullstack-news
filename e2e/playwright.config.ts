import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './specs',
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: false,
  retries: 1,
  reporter: [['html', { open: 'never' }], ['list']],
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'admin',
      use: { baseURL: 'http://localhost:5173' },
      testMatch: /admin\.spec\.ts/,
    },
    {
      name: 'frontend',
      use: { baseURL: 'http://localhost:5178' },
      testMatch: /frontend\.spec\.ts/,
    },
  ],
})
