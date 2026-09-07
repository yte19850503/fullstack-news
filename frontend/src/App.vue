<template>
  <router-view />
</template>

<style>
:root {
  --color-primary: #1890ff;
  --color-primary-hover: #40a9ff;
  --color-success: #52c41a;
  --color-warning: #faad14;
  --color-danger: #ff4d4f;
  --color-text: #333;
  --color-text-secondary: #666;
  --color-text-muted: #999;
  --color-bg: #f5f7fa;
  --color-bg-white: #fff;
  --color-border: #e8e8e8;
  --max-width: 1200px;
  --sidebar-width: 300px;
  --header-height: 60px;
  --radius: 8px;
  --shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  --shadow-hover: 0 4px 16px rgba(0, 0, 0, 0.12);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans SC', sans-serif;
  color: var(--color-text);
  background: var(--color-bg);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

a {
  color: var(--color-primary);
  text-decoration: none;
}

a:hover {
  color: var(--color-primary-hover);
}

img {
  max-width: 100%;
  height: auto;
}
</style>
