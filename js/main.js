/* main.js - TG站点通用交互脚本 */

/* FAQ 手风琴 */
document.querySelectorAll('.faq-q').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.parentElement;
    const isOpen = item.classList.contains('open');
    /* 关闭其他 */
    document.querySelectorAll('.faq-item.open').forEach(o => o.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  });
});

/* 平滑滚动 */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior:'smooth', block:'start' }); }
  });
});

/* 下载按钮点击统计（可扩展） */
document.querySelectorAll('.dl-btn, .btn-primary').forEach(btn => {
  btn.addEventListener('click', () => {
    console.log('下载按钮点击:', btn.textContent.trim());
  });
});

/* 页面加载动画已移除，避免白屏问题 */
