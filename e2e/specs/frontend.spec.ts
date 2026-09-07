import { test, expect } from '@playwright/test'

test.describe('首页', () => {
  test('加载文章列表', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')
    await expect(page.locator('.article-card, .article-list').first()).toBeVisible({ timeout: 5000 })
  })

  test('显示头部导航和 Logo', async ({ page }) => {
    await page.goto('/')
    await expect(page.locator('.logo')).toHaveText('AI 资讯站')
    await expect(page.locator('.nav-link').first()).toBeVisible()
  })

  test('侧边栏显示热门标签', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')
    await expect(page.locator('.sidebar-title').filter({ hasText: '热门标签' })).toBeVisible()
  })

  test('分类导航过滤', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')

    const navLinks = page.locator('.nav-link')
    const count = await navLinks.count()
    if (count > 1) {
      await navLinks.nth(1).click()
      await page.waitForURL(/\?category_id=/)
      await expect(page).toHaveURL(/category_id=/)
    }
  })

  test('搜索功能', async ({ page }) => {
    await page.goto('/')
    await page.locator('.search-box input').fill('AI')
    await page.locator('.search-box button').click()
    await page.waitForURL(/\/search/)
    await expect(page.locator('.search-header h2')).toContainText('AI')
  })
})

test.describe('文章详情页', () => {
  test('从首页点击进入文章详情', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')

    const firstLink = page.locator('.article-card a, .article-list a').first()
    if (await firstLink.isVisible()) {
      await firstLink.click()
      await page.waitForURL(/\/article\//)
      await expect(page.locator('.article-title')).toBeVisible({ timeout: 5000 })
    }
  })

  test('不存在的文章显示错误提示', async ({ page }) => {
    await page.goto('/article/non-existent-slug-xyz')
    await page.waitForLoadState('networkidle')
    await expect(page.locator('.error')).toBeVisible({ timeout: 5000 })
  })
})

test.describe('登录', () => {
  test('正确凭据登录成功', async ({ page }) => {
    await page.goto('/login')
    await page.locator('input[type="email"]').fill('admin@test.com')
    await page.locator('input[type="password"]').fill('123456')
    await page.locator('button.btn-submit').click()
    await page.waitForURL('/')
    await expect(page).toHaveURL('/')
  })

  test('错误密码登录后停留在登录页', async ({ page }) => {
    await page.goto('/login')
    await page.locator('input[type="email"]').fill('admin@test.com')
    await page.locator('input[type="password"]').fill('wrongpassword')
    await page.locator('button.btn-submit').click()
    await page.waitForTimeout(2000)
    await expect(page).toHaveURL(/\/login/)
  })

  test('切换到注册表单', async ({ page }) => {
    await page.goto('/login')
    await page.getByText('去注册').click()
    await expect(page.locator('.login-title')).toHaveText('注册账号')
    await expect(page.locator('input[type="text"]')).toBeVisible()
  })

  test('注册新用户', async ({ page }) => {
    await page.goto('/login')
    await page.getByText('去注册').click()

    const timestamp = Date.now()
    await page.locator('input[type="text"]').fill(`e2e_user_${timestamp}`)
    await page.locator('input[type="email"]').fill(`e2e_${timestamp}@test.com`)
    await page.locator('input[type="password"]').fill('123456')
    await page.locator('button.btn-submit').click()
    await page.waitForURL('/')
    await expect(page).toHaveURL('/')
  })
})

test.describe('页面标题', () => {
  test('首页标题正确', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveTitle(/AI 资讯站/)
  })

  test('登录页标题正确', async ({ page }) => {
    await page.goto('/login')
    await expect(page).toHaveTitle(/登录/)
  })
})
