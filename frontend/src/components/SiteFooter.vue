<template>
  <footer class="site-footer">
    <div class="footer-container">
      <div class="footer-content">
        <div class="footer-links">
          <a href="#" class="footer-link">关于我们</a>
          <a href="#" class="footer-link">联系方式</a>
          <a href="#" class="footer-link">隐私政策</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 FullStack News. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  background: var(--color-bg-card);
  border-top: 1px solid var(--color-border-light);
  margin-top: auto;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.03);
}

.footer-container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: var(--space-4) var(--space-6);
}

.footer-content {
  text-align: center;
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: var(--space-6);
  flex-wrap: wrap;
}

.footer-link {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  transition: color var(--transition-fast);
}

.footer-link:hover {
  color: var(--color-primary);
}

.footer-bottom {
  text-align: center;
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border-light);
}

.footer-bottom p {
  color: var(--color-text-muted);
  font-size: var(--text-xs);
}

/* 移动端响应式 */
@media (max-width: 768px) {
  .footer-container {
    padding: var(--space-6) var(--space-4);
  }
  
  .footer-links {
    gap: var(--space-4);
  }
}

@media (max-width: 480px) {
  .footer-container {
    padding: var(--space-5) var(--space-3);
  }
  
  .footer-title {
    font-size: var(--text-lg);
  }
  
  .footer-description {
    font-size: var(--text-xs);
  }
  
  .footer-link {
    font-size: var(--text-xs);
  }
}
</style>
