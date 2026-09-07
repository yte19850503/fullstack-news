import { test, expect } from '@playwright/test'

const ADMIN_EMAIL = 'admin@test.com'
const ADMIN_PASS = '123456'

async function adminLogin(page: any) {
  await page.goto('/login')
  await page.waitForLoadState('domcontentloaded')
  await page.getByPlaceholder('邮箱').fill(ADMIN_EMAIL)
  await page.getByPlaceholder('密码').fill(ADMIN_PASS)
  await page.getByRole('button', { name: '登录' }).click()
  await page.waitForURL('**/dashboard', { timeout: 15000 })
}

test.describe('登录', () => {
  test('正确凭据登录成功并跳转到仪表盘', async ({ page }) => {
    await page.goto('/login')
    await page.getByPlaceholder('邮箱').fill(ADMIN_EMAIL)
    await page.getByPlaceholder('密码').fill(ADMIN_PASS)
    await page.getByRole('button', { name: '登录' }).click()
    await page.waitForURL('**/dashboard')
    await expect(page).toHaveURL(/\/dashboard/)
  })

  test('错误凭据登录失败后停留在登录页', async ({ page }) => {
    await page.goto('/login')
    await page.getByPlaceholder('邮箱').fill('wrong@test.com')
    await page.getByPlaceholder('密码').fill('wrongpass')
    await page.getByRole('button', { name: '登录' }).click()
    await page.waitForTimeout(2000)
    await expect(page).toHaveURL(/\/login/)
  })

  test('未登录访问受保护页面跳转到登录页', async ({ page }) => {
    await page.goto('/dashboard')
    await expect(page).toHaveURL(/\/login/)
  })

  test('空表单提交显示验证错误', async ({ page }) => {
    await page.goto('/login')
    await page.getByRole('button', { name: '登录' }).click()
    await expect(page.locator('.el-form-item__error')).toHaveCount(2, { timeout: 3000 })
  })
})

test.describe('仪表盘', () => {
  test.beforeEach(async ({ page }) => {
    await adminLogin(page)
  })

  test('显示统计卡片', async ({ page }) => {
    await expect(page.locator('.stat-label').filter({ hasText: '用户总数' })).toBeVisible()
    await expect(page.locator('.stat-label').filter({ hasText: '文章总数' })).toBeVisible()
    await expect(page.locator('.stat-label').filter({ hasText: '评论总数' })).toBeVisible()
    await expect(page.locator('.stat-label').filter({ hasText: '分类 / 标签' })).toBeVisible()
  })

  test('显示 ECharts 图表容器', async ({ page }) => {
    await expect(page.locator('.chart')).toHaveCount(2)
  })
})

test.describe('文章管理', () => {
  test.beforeEach(async ({ page }) => {
    await adminLogin(page)
    await page.goto('/articles')
    await page.waitForLoadState('networkidle')
  })

  test('文章列表页加载并显示表格', async ({ page }) => {
    await expect(page.locator('.el-table')).toBeVisible()
    await expect(page.getByRole('button', { name: '新增文章' })).toBeVisible()
  })

  test('搜索文章', async ({ page }) => {
    const searchInput = page.locator('.filter-bar .el-input').filter({ hasText: '' }).locator('input')
    await searchInput.fill('AI')
    await page.getByRole('button', { name: '查询' }).click()
    await page.waitForLoadState('networkidle')
    await expect(page.locator('.el-table')).toBeVisible()
  })

  test('新增文章表单', async ({ page }) => {
    await page.getByRole('button', { name: '新增文章' }).click()
    await page.waitForURL('**/articles/new')

    await page.getByLabel('标题').fill('E2E 测试文章')
    await page.locator('.el-form-item').filter({ hasText: '分类' }).locator('.el-select').click()
    await page.locator('.el-select-dropdown__item').first().click()
    await page.getByLabel('正文').fill('<p>E2E 测试正文内容</p>')

    await page.getByRole('button', { name: '创建文章' }).click()
    await page.waitForURL('**/articles')
    await expect(page).toHaveURL(/\/articles/)
  })

  test('查看文章详情', async ({ page }) => {
    await page.locator('.el-table').getByRole('button', { name: '查看' }).first().click()
    await page.waitForURL(/\/articles\/\d+/)
    await expect(page.locator('.el-page-header')).toBeVisible()
  })

  test('编辑文章', async ({ page }) => {
    await page.locator('.el-table').getByRole('button', { name: '编辑' }).first().click()
    await page.waitForURL(/\/articles\/\d+\/edit/)
    await expect(page.getByLabel('标题')).toHaveValue(/.+/)
  })

  test('删除文章', async ({ page }) => {
    const rowCount = await page.locator('.el-table__body-wrapper .el-table__row').count()
    if (rowCount === 0) return

    await page.locator('.el-table').getByRole('button', { name: '删除' }).first().click()
    await expect(page.locator('.el-popconfirm')).toBeVisible({ timeout: 3000 })
    await page.locator('.el-popconfirm').locator('.el-button--primary').click()
    await page.waitForLoadState('networkidle')
    await page.waitForTimeout(1000)

    const newCount = await page.locator('.el-table__body-wrapper .el-table__row').count()
    expect(newCount).toBeLessThan(rowCount)
  })
})

test.describe('侧边栏导航', () => {
  test.beforeEach(async ({ page }) => {
    await adminLogin(page)
  })

  const menuItems = [
    { name: '仪表盘', url: /\/dashboard/ },
    { name: '文章管理', url: /\/articles/ },
    { name: '分类管理', url: /\/categories/ },
    { name: '标签管理', url: /\/tags/ },
    { name: '评论管理', url: /\/comments/ },
    { name: '用户管理', url: /\/users/ },
    { name: '操作日志', url: /\/logs/ },
  ]

  for (const item of menuItems) {
    test(`导航到${item.name}`, async ({ page }) => {
      await page.locator('.el-menu-item').filter({ hasText: item.name }).click()
      await page.waitForURL(item.url)
      await expect(page).toHaveURL(item.url)
    })
  }
})
