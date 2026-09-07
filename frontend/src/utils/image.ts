/**
 * 根据文章标题和分类生成默认封面图
 * 使用渐变色背景 + 文字叠加的方式
 */

// 预定义的渐变配色方案
const gradients = [
  'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
  'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
  'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
  'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
  'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
  'linear-gradient(135deg, #667eea 0%, #f093fb 100%)',
]

// Emoji 图标池（根据分类名称哈希自动分配）
const iconPool = [
  '🤖', '🎬', '📊', '💻', '⚙️', '🎨', '📈', '🚀', 
  '💡', '🔧', '📱', '🌐', '🎯', '📚', '🎮', '🔬',
  '💼', '🛠️', '📝', '🎪', '🌟', '🔥', '💎', '🎵',
  '🏆', '🎲', '📦', '🔔', '💬', '🎁', '🌈', '⭐'
]

/**
 * 根据字符串生成哈希值
 */
function hashCode(str: string): number {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash = hash & hash // Convert to 32bit integer
  }
  return Math.abs(hash)
}

/**
 * 生成默认封面图的CSS样式
 */
export function getDefaultCoverStyle(title: string, category?: string): {
  background: string
  icon: string
  textColor: string
} {
  const hash = hashCode(title)
  const gradientIndex = hash % gradients.length
  
  // 根据分类名称哈希自动分配图标（同一分类始终获得相同图标）
  const icon = category 
    ? iconPool[hashCode(category) % iconPool.length]
    : '📰'
  
  return {
    background: gradients[gradientIndex],
    icon,
    textColor: '#ffffff',
  }
}

/**
 * 解析渐变色字符串获取起止颜色
 */
function parseGradientColors(gradient: string): { start: string; end: string } {
  // 从渐变字符串中提取颜色值
  const colorMatches = gradient.match(/#[0-9a-fA-F]{6}/g) || []
  return {
    start: colorMatches[0] || '#667eea',
    end: colorMatches[1] || '#764ba2'
  }
}

/**
 * 生成默认封面图的SVG（仅emoji + 渐变背景，无文字）
 * SVG尺寸与容器完全匹配(使用aspect-ratio 2:1)，避免任何缩放导致的裁剪
 */
export function generateCoverSVG(title: string, category?: string): string {
  const style = getDefaultCoverStyle(title, category)
  const colors = parseGradientColors(style.background)
  
  // SVG使用2:1比例，宽度自适应（PC端320x160，移动端会自动缩放到容器宽度x120）
  const svgWidth = 320
  const svgHeight = 160
  
  // Emoji位置（居中）
  const emojiY = svgHeight / 2 + 12  // 92
  const emojiSize = 64
  
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="${svgWidth}" height="${svgHeight}" viewBox="0 0 ${svgWidth} ${svgHeight}">
      <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:${colors.start};stop-opacity:1" />
          <stop offset="100%" style="stop-color:${colors.end};stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect width="${svgWidth}" height="${svgHeight}" fill="url(#grad)" />
      <text x="${svgWidth / 2}" y="${emojiY}" font-family="Arial, sans-serif" font-size="${emojiSize}" fill="white" text-anchor="middle">${style.icon}</text>
    </svg>
  `
  
  return `data:image/svg+xml;base64,${btoa(unescape(encodeURIComponent(svg)))}`
}

/**
 * 转义XML特殊字符
 */
function escapeXml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;')
}
