#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TG站点生成脚本 v2.0 - 数据驱动架构
文章数据: articles/*.json
用法: python build.py
"""
import os, json, datetime, glob

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DOMAIN    = "https://shengyi5.com"
SITE_NAME = "TG图片修复站"

META = {
    "title":       "Telegram图片加载转圈解决办法｜TG图片发不出修复教程",
    "description": "专注解决Telegram图片加载卡住、转圈、无法显示、发送失败等问题，分享手机电脑端本地设置排查方案。",
    "keywords":    "telegram图片加载转圈,TG图片发不出,telegram图片卡住",
}

CATEGORIES = [
    {"slug": "image-circle",    "name": "图片转圈修复", "kw": "telegram图片加载转圈修复"},
    {"slug": "image-send-fail", "name": "图片发送失败", "kw": "TG图片发送失败解决"},
    {"slug": "image-not-show",  "name": "图片无法显示", "kw": "telegram图片不显示"},
    {"slug": "album-permission","name": "相册权限设置", "kw": "telegram相册权限"},
    {"slug": "media-optimize",  "name": "媒体加载优化", "kw": "telegram媒体加载优化"},
]

# 分类页专属内容（让每个分类页有独特内容，避免重复）
CATEGORY_CONTENT = {
    "image-circle": {
        "intro": "Telegram图片一直转圈是最常见的问题之一，通常和缓存堆积、网络不稳定、自动下载设置有关。本分类下的教程覆盖了从基础清缓存到高级网络排查的全部方法。",
        "steps": [
            ("清除Telegram媒体缓存", "进入Telegram设置 → 数据和存储 → 存储用量 → 点击「清除全部缓存」。缓存过多是图片转圈的首要原因，很多用户清完缓存就解决了。"),
            ("检查自动下载设置", "进入设置 → 数据和存储 → 自动下载媒体，确认当前网络环境下已开启图片自动下载。如果关了，图片就不会自动加载，需要手动点击。"),
            ("切换网络环境", "Telegram服务器在海外，网络不稳定会导致图片一直转圈。试试从WiFi切到移动数据，或反过来。如果用了代理工具，尝试更换节点。"),
            ("重启Telegram应用", "完全关闭Telegram（包括后台进程），等5秒后重新打开。临时性的加载卡顿通常重启就能解决。"),
            ("重新安装Telegram", "如果以上方法都不行，卸载后重新安装最新版Telegram。聊天记录存在云端不会丢失，但秘密聊天记录会消失。"),
        ],
        "faq": [
            ("Telegram图片转圈多久算异常？", "正常情况下图片应在3-5秒内显示。如果转圈超过30秒仍未加载，基本可以判定是缓存或网络问题，建议按上述步骤排查。"),
            ("清除缓存会删聊天记录吗？", "不会。清缓存只删除本地存的图片、视频文件，聊天记录存在Telegram云端，不受影响。清完后第一次看图片会重新下载。"),
            ("为什么只有图片转圈，文字消息正常？", "文字消息体积很小，对网络要求低。图片文件较大，需要更稳定的连接。网络不稳定时就会出现文字能发但图片转圈的情况。"),
            ("重装Telegram后群还在吗？", "在的。Telegram的群、联系人、聊天记录都存在云端，重新登录后自动同步。但秘密聊天（Secret Chat）的记录会丢失。"),
        ],
    },
    "image-send-fail": {
        "intro": "Telegram图片发送失败通常表现为上传卡住、提示发送失败、或者图片发出去对方看不到。这和文件大小、网络上传速度、存储空间、相册权限都有关系。",
        "steps": [
            ("检查相册权限", "iOS: 设置 → Telegram → 照片 → 选择「所有照片」。Android: 设置 → 应用管理 → Telegram → 权限 → 开启存储/照片权限。权限不足是最常见原因。"),
            ("压缩图片后重试", "如果图片太大（超过10MB），上传容易卡住。可以用手机自带的裁剪/压缩功能把图片缩小后再发送，或者先发截图试试。"),
            ("切换网络环境", "上传图片需要稳定的上行带宽。从WiFi切到移动数据（或反过来），关闭再开启飞行模式，有时候能重置网络连接解决发送卡住的问题。"),
            ("检查存储空间", "手机存储空间不足也会导致发送失败。去设置里看看剩余空间，如果低于1GB建议先清理一下。Telegram缓存在「设置→数据和存储→存储用量」里清。"),
            ("更新或重装Telegram", "旧版本可能有发送相关的bug。去应用商店更新到最新版，或者卸载重装。重装前确认手机号可用以便重新验证。"),
        ],
        "faq": [
            ("Telegram发送图片一直卡在上传中怎么办？", "通常是文件太大或网络上行速度慢。先试试发一张小图片（截图），如果小图能发大图不能发，就是文件大小问题。压缩后再发即可。"),
            ("为什么图片发出去对方看不到？", "可能是你的网络上传不完整，或者对方网络下载有问题。你可以试试删除那条消息重新发送，或者让对方检查TA的网络。"),
            ("Telegram发送图片提示失败但不卡住？", "这通常是相册权限问题。去系统设置里检查Telegram的照片权限是否打开。Android还要检查存储权限。"),
            ("视频发不出去但图片可以？", "视频文件比图片大很多，对网络要求更高。建议在WiFi环境下发送视频，或者把视频压缩后再发。Telegram对单个文件大小限制是2GB。"),
        ],
    },
    "image-not-show": {
        "intro": "Telegram图片无法显示包括图片空白、裂图、只显示缩略图等情况。这和缓存文件损坏、Telegram版本bug、系统兼容性有关，桌面版和手机版的原因可能不同。",
        "steps": [
            ("清除媒体缓存", "进入Telegram设置 → 数据和存储 → 存储用量 → 清除全部缓存。缓存文件损坏会导致图片显示空白或裂图，清除后重新加载通常能解决。"),
            ("退出重新登录", "在Telegram设置里退出账号再重新登录。这会刷新本地数据，解决因本地数据异常导致的图片不显示问题。聊天记录不会丢失。"),
            ("检查Telegram版本", "旧版本可能有图片渲染的bug。去应用商店检查是否有更新，更新到最新版通常能修复已知的显示问题。"),
            ("检查系统WebView", "Android设备上Telegram依赖系统WebView渲染图片。更新Android System WebView到最新版可能解决图片显示问题。"),
            ("尝试桌面版或网页版", "如果手机版一直无法显示图片，试试Telegram Desktop或Telegram Web，看看是否是设备特定的问题。"),
        ],
        "faq": [
            ("为什么Telegram图片显示空白但能点击？", "这说明图片已经下载但渲染失败，通常是缓存文件损坏或版本bug。清除缓存后重新加载，或更新Telegram到最新版。"),
            ("Telegram图片显示裂图怎么修复？", "裂图（灰色方块带个碎图标）表示图片文件不完整。清除缓存让它重新下载，如果还不行就退出重新登录。"),
            ("为什么只有部分图片不显示？", "可能是某些特定格式的图片（如WebP）在你的设备上不兼容。更新Telegram和系统WebView通常能解决格式兼容问题。"),
            ("桌面版Telegram图片不显示怎么办？", "桌面版可能有代理设置、防火墙拦截、缓存路径权限等问题。检查代理配置，或尝试以管理员身份运行Telegram。"),
        ],
    },
    "album-permission": {
        "intro": "Telegram相册权限问题表现为无法选取图片发送、提示没有权限、或者保存图片到相册失败。这在iOS上特别常见，因为iOS的权限管理比较严格。",
        "steps": [
            ("iOS设置照片权限", "打开iPhone「设置」→ 往下翻找到「Telegram」→ 点击「照片」→ 选择「所有照片」。如果选了「选中的照片」可能部分图片无法发送。"),
            ("Android设置存储权限", "打开「设置」→「应用管理」→找到Telegram→「权限」→ 开启「存储」和「照片和视频」权限。不同品牌手机路径可能略有不同。"),
            ("检查「节省空间」模式", "iOS如果开了「低数据模式」可能会限制Telegram的后台数据。去「设置→蜂窝网络→蜂窝数据选项」检查。Android检查「数据节省程序」。"),
            ("重启应用和手机", "修改权限后需要完全关闭Telegram再重新打开。如果还不行，重启手机试试，有时候权限变更需要重启才能生效。"),
            ("重装Telegram并重新授权", "如果以上方法都不行，卸载Telegram重新安装。安装后第一次打开时会重新请求相册权限，这次记得点「允许」。"),
        ],
        "faq": [
            ("iOS上Telegram无法访问相册怎么办？", "去「设置→Telegram→照片」选择「所有照片」。如果找不到Telegram选项，先打开Telegram尝试发送一张图片，系统会弹出权限请求。"),
            ("Android Telegram相册权限在哪里开？", "「设置→应用管理→Telegram→权限→存储」（或「照片和视频」）。部分国产手机还需要在手机管家类应用里单独授权。"),
            ("为什么改了权限还是不能发图片？", "修改权限后需要完全关闭Telegram（从后台划掉）再重新打开。如果还不行，重启手机试试。"),
            ("Telegram保存的图片在相册里找不到？", "iOS检查「设置→Telegram→照片」是否开了权限。Android检查Telegram的存储权限，以及相册是否显示了Telegram文件夹。"),
        ],
    },
    "media-optimize": {
        "intro": "Telegram媒体加载优化涵盖图片、视频、GIF动图、贴纸等各类媒体的加载速度和显示问题。通过调整自动下载设置、清理缓存、优化网络配置，可以显著提升Telegram的媒体加载体验。",
        "steps": [
            ("调整自动下载设置", "进入Telegram设置 → 数据和存储 → 自动下载媒体。建议：移动数据下只自动下载图片，WiFi下下载图片和视频，漫游时关闭自动下载。"),
            ("定期清理缓存", "Telegram缓存会持续增长，建议每月清理一次。在「设置→数据和存储→存储用量」里可以查看缓存大小并清理。深度清理可以参考缓存清理教程。"),
            ("优化网络配置", "如果用了代理，选择延迟更低的节点。Telegram媒体走的是不同的服务器，有时候代理节点能连上但媒体服务器连不上，换个节点可能就好了。"),
            ("关闭后台不必要的同步", "在「设置→数据和存储」里关闭「在漫游时自动下载」，限制后台同步频率。这能减少网络带宽争用，让前台图片加载更快。"),
            ("使用Telegram桌面版辅助", "桌面版Telegram的网络处理和手机版不同，有时候手机版加载慢但桌面版正常。可以对比测试来判断是网络问题还是手机端问题。"),
        ],
        "faq": [
            ("Telegram视频播放卡顿怎么办？", "先检查网络速度，视频需要更稳定的带宽。在WiFi环境下预加载视频，或者降低视频质量。也可以先下载再播放，不用在线看。"),
            ("为什么Telegram GIF动图不自动播放？", "检查自动下载设置里GIF是否开启。如果网络不稳定，Telegram可能会暂停GIF自动播放。清除缓存后重试。"),
            ("Telegram贴纸不显示怎么修复？", "贴纸不显示通常是缓存问题。清除缓存后重新打开聊天，贴纸会重新下载。如果是动画贴纸，可能需要更稳定的网络。"),
            ("怎么让Telegram加载图片更快？", "开启自动下载、定期清缓存、使用稳定网络。如果一直慢，可能是代理节点问题，尝试更换节点或调整代理协议。"),
        ],
    },
}

# ============================================================
# HTML 公共片段
# ============================================================
NAV = """<header>
<div class="container header-inner">
  <a href="index.html" class="logo"><div class="logo-icon">TG</div>TG图片修复站</a>
  <nav>
    <a href="image-circle.html">图片转圈</a>
    <a href="image-send-fail.html">发送失败</a>
    <a href="image-not-show.html">无法显示</a>
    <a href="album-permission.html">相册权限</a>
    <a href="media-optimize.html">加载优化</a>
  </nav>
  <a href="#guide" class="header-btn">立即修复</a>
</div>
</header>"""

DISCLAIMER = """<div class="container"><div class="disclaimer">
本站内容仅为海外合规地区软件功能科普教程，不提供网络访问相关方案，不引导任何违规操作，内容仅供学习参考。
</div></div>"""

DL_SECTION = '''<section class="dl-section">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">立即下载</div>
      <h2>获取 Telegram 最新版客户端</h2>
      <p class="section-sub">官方正版 · 安全无捆绑 · 免费使用 · 多平台同步</p>
      <div class="dl-rating">
        <span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
        <span class="rating-text">4.6 分 / 1200万+ 用户评价</span>
      </div>
    </div>
    <div class="dl-grid">
      <div class="dl-platform-card">
        <div class="dl-badge">推荐</div>
        <div class="dl-platform-icon" style="background:linear-gradient(135deg,#ea580c,#fb923c)">W</div>
        <h3>Windows 版</h3>
        <p class="dl-sub">适用于 Windows 10 / 11</p>
        <div class="dl-platform-meta">
          <span><span class="meta-label">版本</span><span class="meta-val">5.8.2</span></span>
          <span><span class="meta-label">大小</span><span class="meta-val">48.3 MB</span></span>
          <span><span class="meta-label">更新</span><span class="meta-val">06-10</span></span>
        </div>
        <a href="https://telegram.org/dl/desktop/win" target="_blank" class="dl-btn">&#11015; 下载 Windows 版</a>
      </div>
      <div class="dl-platform-card">
        <div class="dl-platform-icon" style="background:linear-gradient(135deg,#d97706,#fbbf24)">A</div>
        <h3>Android 版</h3>
        <p class="dl-sub">适用于 Android 8.0+</p>
        <div class="dl-platform-meta">
          <span><span class="meta-label">版本</span><span class="meta-val">5.8.2</span></span>
          <span><span class="meta-label">大小</span><span class="meta-val">35.7 MB</span></span>
          <span><span class="meta-label">更新</span><span class="meta-val">06-10</span></span>
        </div>
        <a href="https://telegram.org/dl/android" target="_blank" class="dl-btn" style="background:linear-gradient(135deg,#d97706,#b45309)">&#11015; 下载 Android 版</a>
      </div>
      <div class="dl-platform-card">
        <div class="dl-platform-icon" style="background:linear-gradient(135deg,#be185d,#f472b6)">i</div>
        <h3>iOS 版</h3>
        <p class="dl-sub">适用于 iPhone / iPad</p>
        <div class="dl-platform-meta">
          <span><span class="meta-label">版本</span><span class="meta-val">5.8.2</span></span>
          <span><span class="meta-label">大小</span><span class="meta-val">App Store</span></span>
          <span><span class="meta-label">更新</span><span class="meta-val">06-10</span></span>
        </div>
        <a href="https://apps.apple.com/app/telegram-messenger/id686449807" target="_blank" class="dl-btn" style="background:linear-gradient(135deg,#be185d,#9d174d)">&#127818; 前往 App Store</a>
      </div>
    </div>
    <div class="dl-trust">
      <div class="dl-trust-item"><span class="check">&#10003;</span> 官方正版</div>
      <div class="dl-trust-item"><span class="check">&#10003;</span> 安全无捆绑</div>
      <div class="dl-trust-item"><span class="check">&#10003;</span> 免费使用</div>
      <div class="dl-trust-item"><span class="check">&#10003;</span> 聊天云端同步</div>
      <div class="dl-trust-item"><span class="check">&#10003;</span> 多平台同时登录</div>
    </div>
  </div>
</section>'''

ART_CARD = '''<div class="article-dl-card">
  <div class="adl-info">
    <h3>&#128241; 立即下载 Telegram 最新版</h3>
    <p>更新到最新版本可修复大部分图片加载问题，官方正版安全无捆绑。</p>
    <div class="adl-meta">
      <span>&#10003; 版本 5.8.2</span>
      <span>&#10003; 官方正版</span>
      <span>&#10003; 免费下载</span>
    </div>
  </div>
  <a href="download.html" class="adl-btn">&#11015; 立即下载<span class="adl-btn-sub">Windows / Android / iOS</span></a>
</div>'''

FOOTER = """<footer>
<div class="container">
  <div class="footer-grid">
    <div class="footer-brand">
      <h3>TG图片修复站</h3>
      <p>专注Telegram图片加载相关问题解决，提供免费的排查教程与修复方法。</p>
    </div>
    <div class="footer-col">
      <h4>问题分类</h4>
      <ul>
        <li><a href="image-circle.html">图片转圈修复</a></li>
        <li><a href="image-send-fail.html">图片发送失败</a></li>
        <li><a href="image-not-show.html">图片无法显示</a></li>
        <li><a href="album-permission.html">相册权限设置</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Telegram下载</h4>
      <ul>
        <li><a href="download.html">Telegram客户端下载</a></li>
        <li><a href="https://telegram.org/dl/desktop/win" target="_blank">Telegram Windows版</a></li>
        <li><a href="https://telegram.org/dl/android" target="_blank">Telegram Android版</a></li>
        <li><a href="https://apps.apple.com/app/telegram-messenger/id686449807" target="_blank">Telegram iOS版</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>关于</h4>
      <ul>
        <li><a href="about.html">关于我们</a></li>
        <li><a href="privacy.html">隐私政策</a></li>
        <li><a href="contact.html">联系我们</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2026 TG图片修复站 — 内容仅供学习参考</span>
    <span>本站与Telegram官方无关</span>
  </div>
</div>
</footer>
<script>
document.addEventListener('DOMContentLoaded',function(){
  document.querySelectorAll('.faq-q').forEach(function(q){
    q.addEventListener('click',function(){
      this.parentElement.classList.toggle('open');
    });
  });
});
</script>
</body>
</html>"""

# ============================================================
# 读取文章数据
# ============================================================
def load_articles():
    articles = []
    article_dir = os.path.join(BASE_DIR, "articles")
    if not os.path.exists(article_dir):
        return articles
    for filepath in sorted(glob.glob(os.path.join(article_dir, "*.json"))):
        with open(filepath, "r", encoding="utf-8") as f:
            art = json.load(f)
            art["_filename"] = os.path.basename(filepath)
            articles.append(art)
    articles.sort(key=lambda x: x.get("date", ""), reverse=True)
    return articles

# ============================================================
# 文章内容渲染器
# ============================================================
def nl2br(text):
    """将文本中的 \\n\\n 转换为段落分隔，单个 \\n 转换为 <br>"""
    import html as _html
    text = _html.escape(text, quote=False)
    # 先按双换行分段
    paras = text.split("\n\n")
    if len(paras) > 1:
        return "".join(f"<p>{p.strip()}</p>" for p in paras if p.strip())
    # 单换行转 <br>
    return f"<p>{text.replace(chr(10), '<br>')}</p>"


import re as _re

# 所有合法的内部链接目标（文章slug + 分类slug + 功能页）
VALID_LINK_TARGETS = set()
for _cat in CATEGORIES:
    VALID_LINK_TARGETS.add(_cat["slug"])
VALID_LINK_TARGETS.update(["index", "download", "about", "contact", "privacy"])

def process_internal_links(html_text, all_articles):
    """将文章正文中的 [[slug|锚文本]] 占位符转换为 <a> 内链标签。
    用法示例:
      [[telegram-image-circle-fix|Telegram图片转圈的解决方法]]
      [[index|Telegram图片修复首页]]
      [[image-circle|图片转圈修复分类]]
    """
    # 收集所有合法的文章slug
    article_slugs = {a["slug"] for a in all_articles}
    valid = VALID_LINK_TARGETS | article_slugs

    def _replace(m):
        slug = m.group(1).strip()
        anchor = m.group(2).strip()
        if slug in valid:
            return f'<a href="{slug}.html" style="color:var(--primary);text-decoration:underline;">{anchor}</a>'
        return anchor  # 不合法则只显示文字

    return _re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', _replace, html_text)

def render_section(section):
    sec_type = section.get("type", "")
    if sec_type == "heading":
        import html as _html
        return f'<h2>{_html.escape(section["text"], quote=False)}</h2>'
    elif sec_type == "paragraph":
        return nl2br(section["text"])
    elif sec_type == "tip":
        color = section.get("color", "primary")
        bg = "#fff7ed" if color == "primary" else ("#fef2f2" if color == "danger" else "#fef3c7")
        border = "var(--primary)" if color == "primary" else ("#dc2626" if color == "danger" else "#d97706")
        return (f'<div style="background:{bg};border-left:4px solid {border};'
                f'padding:16px 20px;border-radius:0 8px 8px 0;margin:16px 0;">'
                f'<p><strong>{section["title"]}</strong>'
                f'{"：" if section.get("title") else ""}{nl2br(section["content"])}</p></div>')
    elif sec_type == "steps":
        steps_html = ""
        for i, step in enumerate(section["steps"], 1):
            if "text" in step:
                step_title = f"步骤 {i}"
                step_content = step["text"]
            else:
                step_title = step.get("title", f"步骤 {i}")
                step_content = step.get("content", "")
            steps_html += (f'<div class="step"><div class="step-num">{i}</div>'
                           f'<h4>{step_title}</h4><p>{step_content}</p></div>')
        return f'<div class="steps-wrap" style="margin:20px 0;">{steps_html}</div>'
    elif sec_type == "list":
        items_html = "".join(f'<li>{item}</li>' for item in section["items"])
        return f'<ul style="padding-left:20px;margin:16px 0;line-height:2;">{items_html}</ul>'
    elif sec_type == "qa":
        qa_html = '<h2>常见问题</h2><div class="faq-list" style="margin:20px 0;">'
        for item in section.get("qa", []):
            qa_html += (f'<div class="faq-item">'
                        f'<div class="faq-q">{item["q"]}</div>'
                        f'<div class="faq-a">{item["a"]}</div></div>')
        qa_html += '</div>'
        return qa_html
    return ""

def render_article_body(article):
    html = ""
    for section in article.get("sections", []):
        html += render_section(section) + "\n"
    return html

def render_faq(faq_list):
    if not faq_list:
        return ""
    html = '<div class="faq-list" style="margin:20px 0;">'
    for item in faq_list:
        html += (f'<div class="faq-item">'
                 f'<div class="faq-q">{item["q"]}</div>'
                 f'<div class="faq-a">{item["a"]}</div></div>')
    html += '</div>'
    return html

# ============================================================
# Schema 生成
# ============================================================
def schema_software():
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Telegram",
        "operatingSystem": "Android, iOS, Windows, macOS, Web",
        "applicationCategory": "CommunicationApplication",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.6", "ratingCount": "12000000"}
    }, ensure_ascii=False, indent=2)

def schema_article_obj(headline, desc, date_pub=None, date_mod=None):
    obj = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": desc,
        "author": {"@type": "Organization", "name": SITE_NAME},
        "datePublished": date_pub or "2026-06-18",
        "dateModified": date_mod or "2026-06-18"
    }
    return json.dumps(obj, ensure_ascii=False, indent=2)

def schema_breadcrumb(items):
    """生成面包屑导航Schema, items = [(name, url), ...]"""
    elements = []
    for i, (name, url) in enumerate(items, 1):
        elements.append({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": DOMAIN + "/" + url
        })
    obj = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements
    }
    return json.dumps(obj, ensure_ascii=False, indent=2)

def schema_faq(faq_list):
    if not faq_list:
        return ""
    entities = []
    for item in faq_list:
        entities.append({
            "@type": "Question",
            "name": item["q"],
            "acceptedAnswer": {"@type": "Answer", "text": item["a"]}
        })
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }, ensure_ascii=False, indent=2)

# ============================================================
# 页面组装器
# ============================================================
def wrap_page(title, desc, kw, canonical, schema_json, body_html, articles=None):
    schema_tag = ('<script type="application/ld+json">\n' + schema_json + '\n</script>\n') if schema_json else ''
    canon = (DOMAIN + '/' + canonical) if canonical else DOMAIN + '/'
    footer_html = FOOTER
    return (f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{kw}">
<link rel="canonical" href="{canon}">
<link rel="stylesheet" href="css/style.css?v=20260619">
{schema_tag}</head>
<body>
{NAV}
{body_html}
{DISCLAIMER}
{footer_html}''')

# ============================================================
# 首页 - 文章列表自动生成
# ============================================================
def build_index(articles):
    # 首页文章列表固定3行3列=9篇，按日期降序（最新文章排第一行第一列）
    homepage_articles = articles[:9]
    article_cards = ""
    for art in homepage_articles:
        icon = art.get("icon", "&#128196;")
        desc_short = art.get("description", "")[:70]
        article_cards += f'''      <a href="{art["slug"]}.html" style="text-decoration:none;color:inherit;">
        <div class="card">
          <div class="card-icon red" style="font-size:22px;">{icon}</div>
          <span style="font-size:12px;color:var(--primary);font-weight:600;">{art.get("category_name","")}</span>
          <h3 style="margin-top:6px;">{art["title"]}</h3>
          <p>{desc_short}...</p>
          <span class="card-link">阅读全文 &rarr;</span>
        </div>
      </a>
'''

    body = f'''
<section class="hero">
  <div class="container hero-inner">
    <div>
      <div class="hero-badge">免费修复教程</div>
      <h1>Telegram 图片<span>加载转圈</span>？这里有完整解决方案</h1>
      <p>专注解决Telegram图片加载转圈、Telegram图片发送失败、Telegram图片不显示、Telegram相册权限等全部场景，逐步引导你快速恢复Telegram正常使用。</p>
      <div class="hero-btns">
        <a href="image-circle.html" class="btn-primary">Telegram图片转圈修复</a>
        <a href="#articles" class="btn-secondary">浏览全部文章</a>
      </div>
      <div class="hero-stats">
        <div class="stat"><div class="stat-num">{len(CATEGORIES)}+</div><div class="stat-label">问题分类</div></div>
        <div class="stat"><div class="stat-num">{len(articles)}</div><div class="stat-label">教程文章</div></div>
        <div class="stat"><div class="stat-num">100%</div><div class="stat-label">免费使用</div></div>
      </div>
    </div>
    <div class="hero-img">
      <div style="background:rgba(255,255,255,.15);border-radius:20px;padding:40px;text-align:center;backdrop-filter:blur(10px);">
        <div style="font-size:64px;margin-bottom:16px;">&#128196;</div>
        <div style="font-size:18px;font-weight:700;">Telegram图片加载异常</div>
        <div style="font-size:14px;opacity:.8;margin-top:8px;">已帮助百万Telegram用户修复</div>
      </div>
    </div>
  </div>
</section>

''' + DL_SECTION + f'''

<section class="section" id="problems">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">问题分类</div>
      <h2>你遇到的是哪种Telegram图片问题？</h2>
      <p class="section-sub">选择对应的Telegram图片问题类型，获取精准解决方案</p>
    </div>
    <div class="cards-grid">
      <a href="image-circle.html" style="text-decoration:none;color:inherit;">
        <div class="card">
          <div class="card-icon red">&#8634;</div>
          <h3>Telegram图片加载转圈</h3>
          <p>Telegram聊天中图片一直转圈无法显示，常见于网络或缓存问题。</p>
          <span class="card-link">查看修复方法</span>
        </div>
      </a>
      <a href="image-send-fail.html" style="text-decoration:none;color:inherit;">
        <div class="card">
          <div class="card-icon yellow">!</div>
          <h3>Telegram图片发送失败</h3>
          <p>Telegram发送图片时一直卡在上传阶段，或提示发送失败。</p>
          <span class="card-link">查看解决方案</span>
        </div>
      </a>
      <a href="image-not-show.html" style="text-decoration:none;color:inherit;">
        <div class="card">
          <div class="card-icon blue">&#9889;</div>
          <h3>Telegram图片无法显示</h3>
          <p>Telegram聊天图片显示空白、裂图，或只显示部分内容。</p>
          <span class="card-link">查看解决方案</span>
        </div>
      </a>
      <a href="album-permission.html" style="text-decoration:none;color:inherit;">
        <div class="card">
          <div class="card-icon green">&#128247;</div>
          <h3>Telegram相册权限设置</h3>
          <p>Telegram无法访问手机相册，导致无法选取或发送图片。</p>
          <span class="card-link">查看设置步骤</span>
        </div>
      </a>
      <a href="media-optimize.html" style="text-decoration:none;color:inherit;">
        <div class="card">
          <div class="card-icon purple">&#9889;</div>
          <h3>Telegram媒体加载优化</h3>
          <p>Telegram加载图片视频速度慢，通过调整Telegram设置提升加载速度。</p>
          <span class="card-link">查看优化技巧</span>
        </div>
      </a>
    </div>
  </div>
</section>

<section class="section" id="articles" style="background:#fff;">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">最新文章</div>
      <h2>Telegram图片修复教程文章</h2>
      <p class="section-sub">Telegram图片问题修复教程 · 持续更新</p>
    </div>
    <div class="articles-grid">
{article_cards}    </div>
{'    <div style="text-align:center;margin-top:30px;"><a href="articles.html" class="btn-secondary">查看全部文章 (' + str(len(articles)) + ' 篇)</a></div>' if len(articles) > 9 else ''}
  </div>
</section>

<section class="section" id="guide">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">快速排查</div>
      <h2>Telegram图片问题通用排查步骤</h2>
      <p class="section-sub">大多数Telegram图片加载问题按以下步骤即可解决</p>
    </div>
    <div class="steps-wrap">
      <div class="step"><div class="step-num">1</div><h4>检查网络连接</h4><p>确认手机/电脑已连接网络，切换Wi-Fi或移动数据后重新打开Telegram重试</p></div>
      <div class="step"><div class="step-num">2</div><h4>清除Telegram媒体缓存</h4><p>进入Telegram设置 → 数据和存储 → 存储用量 → 清除缓存</p></div>
      <div class="step"><div class="step-num">3</div><h4>重启Telegram应用</h4><p>完全关闭Telegram后重新打开，解决临时性的加载卡顿</p></div>
      <div class="step"><div class="step-num">4</div><h4>检查相册权限</h4><p>确认系统已授予Telegram访问相册的权限，尤其iOS设备</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">常见问答</div>
      <h2>Telegram图片加载 FAQ</h2>
    </div>
    <div class="faq-list" id="faq">
      <div class="faq-item">
        <div class="faq-q">Telegram图片一直转圈是什么原因？</div>
        <div class="faq-a">Telegram图片转圈通常是因为媒体文件未能正常下载。最常见原因是Telegram缓存满了或网络连接不稳定。建议先清除Telegram缓存，再切换网络环境重试。</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">Telegram发送图片一直卡在上传中怎么办？</div>
        <div class="faq-a">Telegram上传卡住通常是因为文件过大或网络上传速度慢。尝试压缩图片后再通过Telegram发送，或切换更稳定的网络环境。</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">为什么Telegram部分图片显示空白？</div>
        <div class="faq-a">Telegram图片显示空白通常是因为缓存文件损坏。进入Telegram设置清除媒体缓存，然后退出重新登录Telegram账号，通常可以解决。</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">iOS上Telegram无法访问相册怎么办？</div>
        <div class="faq-a">进入iOS系统设置 → 找到Telegram → 打开「照片」权限，选择「所有照片」即可让Telegram正常访问相册。</div>
      </div>
    </div>
  </div>
</section>

<section class="cta">
  <div class="container">
    <h2>Telegram问题还没解决？</h2>
    <p>查看我们针对各类Telegram图片问题的详细修复指南</p>
    <div class="cta-btns">
      <a href="image-circle.html" class="btn-white">Telegram图片转圈修复</a>
      <a href="album-permission.html" class="btn-outline-white">Telegram相册权限设置</a>
    </div>
  </div>
</section>'''
    return wrap_page(META["title"], META["description"], META["keywords"],
                    "", schema_article_obj(META["title"], META["description"]), body, articles)

# ============================================================
# 文章归档页 - 列出全部文章
# ============================================================
def build_articles_page(articles):
    article_cards = ""
    for art in articles:
        icon = art.get("icon", "&#128196;")
        desc_short = art.get("description", "")[:70]
        article_cards += f'''      <a href="{art["slug"]}.html" style="text-decoration:none;color:inherit;">
        <div class="card">
          <div class="card-icon red" style="font-size:22px;">{icon}</div>
          <span style="font-size:12px;color:var(--primary);font-weight:600;">{art.get("category_name","")}</span>
          <h3 style="margin-top:6px;">{art["title"]}</h3>
          <p>{desc_short}...</p>
          <span class="card-link">阅读全文 &rarr;</span>
        </div>
      </a>
'''

    body = f'''
<section class="section" id="articles" style="background:#fff;">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">全部文章</div>
      <h2>Telegram图片修复教程 · 全部文章</h2>
      <p class="section-sub">共 {len(articles)} 篇教程 · 按发布时间排序</p>
    </div>
    <div class="cards-grid">
{article_cards}    </div>
  </div>
</section>'''
    return wrap_page(
        "全部Telegram图片修复教程文章 | " + SITE_NAME,
        "浏览全部Telegram图片修复教程文章，涵盖图片转圈、发送失败、无法显示、相册权限等问题的解决方案。",
        "telegram图片修复教程,telegram图片问题,全部文章",
        "articles.html",
        schema_breadcrumb([("首页", "index.html"), ("全部文章", "articles.html")]),
        body, articles)

# ============================================================
# 文章详情页（从JSON数据生成）
# ============================================================
def build_article_page(article, all_articles):
    cat_slug = article.get("category", "")
    cat_name = article.get("category_name", "")
    body_html = render_article_body(article)
    body_html = process_internal_links(body_html, all_articles)  # 处理内链占位符
    faq_html = render_faq(article.get("faq", []))

    related = [a for a in all_articles if a["slug"] != article["slug"]][:3]
    related_cards = ""
    color_map = ["#ea580c,#fb923c", "#d97706,#fbbf24", "#be185d,#f472b6"]
    for i, ra in enumerate(related):
        c = color_map[i % len(color_map)]
        related_cards += f'''        <a href="{ra["slug"]}.html" style="text-decoration:none;color:inherit;display:block;">
        <div style="background:var(--card);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);border:1px solid var(--border);transition:.2s;">
          <div style="height:140px;background:linear-gradient(135deg,{c.split(',')[0]},{c.split(',')[1]});display:flex;align-items:center;justify-content:center;font-size:48px;color:#fff;">{ra.get("icon","&#128196;")}</div>
          <div style="padding:16px;">
            <span style="font-size:12px;color:var(--primary);font-weight:600;">{ra.get("category_name","")}</span>
            <h4 style="font-size:15px;font-weight:700;margin:8px 0;">{ra["title"]}</h4>
            <span style="font-size:12px;color:var(--text-sub);">{ra.get("date","")}</span>
          </div>
        </div>
        </a>
'''

    body = f'''
<div class="container"><div class="breadcrumb"><a href="index.html">首页</a> &gt; <a href="{cat_slug}.html">{cat_name}</a> &gt; {article["title"]}</div></div>

<section class="hero" style="padding:40px 0;">
  <div class="container">
    <div class="hero-badge">{cat_name}教程</div>
    <h1>{article["title"]}<br>{article.get("subtitle","")}</h1>
  </div>
</section>

<div class="container" style="display:grid;grid-template-columns:1fr 280px;gap:32px;padding:40px 20px;">
  <div class="article-main">
    <div class="article-meta" style="display:flex;gap:16px;font-size:13px;color:var(--text-sub);margin-bottom:24px;">
      <span>作者：{article.get("author",SITE_NAME)}</span>
      <span>发布时间：{article.get("date","")}</span>
      <span>阅读时间：约{article.get("read_time","5分钟")}</span>
    </div>

    <div class="article-body">
      {body_html}

{ART_CARD}
    </div>

    <div style="margin-top:40px;">
      <div class="section-header"><div class="section-tag">相关文章</div><h2>更多图片问题教程</h2></div>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;">
{related_cards}      </div>
    </div>
  </div>

  <div class="article-sidebar">
    <div style="position:sticky;top:84px;">
    <div style="background:var(--card);border-radius:var(--radius);padding:20px;box-shadow:var(--shadow);border:1px solid var(--border);margin-bottom:20px;">
      <h4 style="font-size:15px;font-weight:700;margin-bottom:12px;">文章目录</h4>
      <ul style="list-style:none;font-size:13px;line-height:2;">
        {''.join(f'<li><a href="#" style="color:var(--text-sub);">{s["text"]}</a></li>' for s in article.get("sections",[]) if s.get("type")=="heading")}
      </ul>
    </div>
    <div style="background:linear-gradient(135deg,var(--primary),var(--primary-light));border-radius:var(--radius);padding:24px;color:#fff;text-align:center;">
      <div style="font-size:40px;margin-bottom:12px;">&#128241;</div>
      <h4 style="font-size:16px;font-weight:700;margin-bottom:8px;">立即下载Telegram</h4>
      <p style="font-size:13px;opacity:.9;margin-bottom:16px;">最新版Telegram客户端，修复已知问题</p>
      <a href="download.html" style="display:inline-block;padding:10px 24px;background:#fff;color:var(--primary);border-radius:8px;font-weight:700;font-size:14px;">免费下载</a>
    </div>
    </div>
  </div>
</div>

''' + DL_SECTION + '''

<section class="cta">
  <div class="container">
    <h2>问题解决了吗？</h2>
    <p>如果以上方法仍无法解决，查看其他相关教程</p>
    <div class="cta-btns">
      <a href="image-send-fail.html" class="btn-white">图片发送失败</a>
      <a href="download.html" class="btn-outline-white">下载TG客户端</a>
    </div>
  </div>
</section>'''

    meta_title = article.get("meta_title", article["title"] + " | " + SITE_NAME)
    desc = article.get("description", "")
    kw = article.get("keywords", "")
    art_date = article.get("date", "2026-06-18")
    faq_schema = schema_faq(article.get("faq", []))
    breadcrumb_schema = schema_breadcrumb([
        ("首页", ""),
        (cat_name, cat_slug + ".html"),
        (article["title"], article["slug"] + ".html")
    ])
    combined_schema = schema_article_obj(meta_title, desc, art_date, art_date)
    combined_schema = combined_schema + ',\n' + breadcrumb_schema
    if faq_schema:
        combined_schema = combined_schema + ',\n' + faq_schema
    return wrap_page(meta_title, desc, kw, article["slug"] + ".html", combined_schema, body, all_articles)

# ============================================================
# 分类页
# ============================================================
def build_category(slug, name, kw, articles):
    cat_articles = [a for a in articles if a.get("category") == slug]
    cat_data = CATEGORY_CONTENT.get(slug, {})

    cat_article_list = ""
    if cat_articles:
        cat_article_list = f'''
<section class="section" style="background:#fff;">
  <div class="container">
    <div class="section-header"><div class="section-tag">相关文章</div><h2>{name}教程文章</h2></div>
    <div class="cards-grid">'''
        for art in cat_articles:
            cat_article_list += f'''
      <a href="{art["slug"]}.html" style="text-decoration:none;color:inherit;">
        <div class="card">
          <div class="card-icon red" style="font-size:22px;">{art.get("icon","&#128196;")}</div>
          <h3>{art["title"]}</h3>
          <p>{art.get("description","")[:60]}...</p>
          <span class="card-link">阅读全文 &rarr;</span>
        </div>
      </a>'''
        cat_article_list += '\n    </div>\n  </div>\n</section>\n'

    # 生成分类专属的修复步骤
    steps_data = cat_data.get("steps", [
        ("清除媒体缓存", "进入Telegram设置 → 数据和存储 → 存储用量 → 点击「清除全部缓存」。缓存过多是图片问题的常见原因。"),
        ("切换网络环境", "图片加载需要稳定的网络连接。切换Wi-Fi或移动数据后重新打开Telegram。"),
        ("重启Telegram应用", "完全关闭Telegram后台进程，等待5秒后重新启动。"),
        ("检查自动下载设置", "进入设置 → 数据和存储 → 自动下载媒体，确认当前网络环境下已开启图片自动下载。"),
        ("重新安装Telegram", "如果以上步骤均无效，卸载Telegram后重新安装最新版本。"),
    ])
    steps_html = ""
    for i, (step_title, step_desc) in enumerate(steps_data, 1):
        steps_html += f'<div class="gs"><div class="gs-num">{i}</div><div class="gs-text"><h4>{step_title}</h4><p>{step_desc}</p></div></div>\n        '

    # 生成分类专属的FAQ
    faq_data = cat_data.get("faq", [
        ("Telegram图片加载转圈多久算异常？", "正常情况下图片应在5秒内显示。如果转圈超过30秒，建议先清除缓存，再排查网络问题。"),
        ("清除缓存后图片还需要重新下载吗？", "是的，清除缓存后图片需要重新下载。但聊天记录不会丢失。"),
        ("为什么只在Wi-Fi下图片加载慢？", "部分Wi-Fi网络对媒体文件下载有限速。可尝试切换到移动数据再试。"),
    ])
    faq_html = ""
    for q, a in faq_data:
        faq_html += f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>\n      '

    # 分类专属介绍文字
    intro_text = cat_data.get("intro", f"本文提供{name}的详细排查步骤与修复方法，覆盖Android、iOS、Windows各平台。")

    body = f'''
<div class="container"><div class="breadcrumb"><a href="index.html">首页</a> &gt; {name}</div></div>
<section class="hero" style="padding:40px 0;">
  <div class="container">
    <div class="hero-badge">{name}</div>
    <h1>Telegram <span>{name}</span>完整解决方案</h1>
    <p>{intro_text}</p>
    <div class="hero-btns">
      <a href="#guide" class="btn-primary">查看修复步骤</a>
      <a href="#faq" class="btn-secondary">常见问答</a>
    </div>
  </div>
</section>

<section class="section" id="guide" style="background:#fff;">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">修复步骤</div>
      <h2>{name}完整修复流程</h2>
      <p class="section-sub">按顺序尝试以下方法，大多数情况可在前两步解决</p>
    </div>
    <div class="guide-grid">
      <div class="guide-steps">
        {steps_html}
      </div>
      <div class="guide-box">
        <h3>注意事项</h3>
        <ul>
          <li>清除缓存不会删除聊天记录，仅删除本地临时媒体文件</li>
          <li>重新安装前请确认账号绑定的手机号码可用</li>
          <li>自动下载设置中可分别配置移动数据、Wi-Fi、漫游时的行为</li>
          <li>图片加载转圈超过30秒基本可判定为网络问题</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section" id="faq">
  <div class="container">
    <div class="section-header"><div class="section-tag">FAQ</div><h2>{name}常见问答</h2></div>
    <div class="faq-list">
      {faq_html}
    </div>
  </div>
</section>
{cat_article_list}
<section class="cta">
  <div class="container">
    <h2>问题还没解决？</h2>
    <p>查看其他图片问题的详细教程</p>
    <div class="cta-btns">
      <a href="download.html" class="btn-white">下载TG客户端</a>
      <a href="index.html#articles" class="btn-outline-white">查看全部文章</a>
    </div>
  </div>
</section>'''
    title = f"Telegram{name}解决方法 - TG图片问题修复教程 | TG图片修复站"
    desc  = f"{intro_text[:120]}"
    # 分类页FAQ也加入schema
    faq_schema = schema_faq([{"q": q, "a": a} for q, a in faq_data])
    breadcrumb_schema = schema_breadcrumb([("首页", ""), (name, slug + ".html")])
    combined_schema = schema_article_obj(title, desc) + ',\n' + breadcrumb_schema
    if faq_schema:
        combined_schema = combined_schema + ',\n' + faq_schema
    return wrap_page(title, desc, kw, slug + ".html", combined_schema, body, articles)

# ============================================================
# 下载页
# ============================================================
def build_download():
    body = '''
<section class="hero" style="padding:40px 0;">
  <div class="container">
    <div class="hero-badge">官方版本下载</div>
    <h1>Telegram <span>最新版</span>免费下载</h1>
    <p>提供Telegram各平台官方正版客户端下载，安全无捆绑，覆盖Android、iOS、Windows、macOS。</p>
  </div>
</section>

<div class="container" style="display:grid;grid-template-columns:1fr 320px;gap:32px;padding:40px 20px;">
  <div>
    <div style="background:var(--card);border-radius:var(--radius);padding:28px;box-shadow:var(--shadow);border:1px solid var(--border);margin-bottom:24px;">
      <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;">
        <div style="width:48px;height:48px;background:#fff7ed;color:var(--primary);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:800;">W</div>
        <div>
          <h3 style="font-size:18px;font-weight:700;">Telegram Windows 客户端</h3>
          <p style="font-size:13px;color:var(--text-sub);">适用于 Windows 10 / 11</p>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px;font-size:13px;">
        <div><span style="color:var(--text-sub);">版本：</span>5.8.2</div>
        <div><span style="color:var(--text-sub);">大小：</span>48.3 MB</div>
        <div><span style="color:var(--text-sub);">更新：</span>2026-06-10</div>
      </div>
      <div style="background:#fff7ed;border:1px solid #fed7aa;border-radius:8px;padding:12px 16px;font-size:13px;color:#9a3412;margin-bottom:20px;">
        &#10003; 官方正版 &nbsp;|&nbsp; &#10003; 安全无捆绑 &nbsp;|&nbsp; &#10003; 免费使用
      </div>
      <a href="https://telegram.org/dl/desktop/win" target="_blank" style="display:inline-flex;align-items:center;gap:10px;padding:16px 40px;background:linear-gradient(135deg,var(--primary),var(--primary-dark));color:#fff;border-radius:10px;font-weight:700;font-size:16px;box-shadow:0 4px 16px rgba(234,88,12,.3);">&#11015; 立即下载 Windows 版</a>
    </div>

    <div style="background:var(--card);border-radius:var(--radius);padding:28px;box-shadow:var(--shadow);border:1px solid var(--border);margin-bottom:24px;">
      <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;">
        <div style="width:48px;height:48px;background:#fef3c7;color:#d97706;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:800;">A</div>
        <div>
          <h3 style="font-size:18px;font-weight:700;">Telegram Android 客户端</h3>
          <p style="font-size:13px;color:var(--text-sub);">适用于 Android 8.0 及以上</p>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px;font-size:13px;">
        <div><span style="color:var(--text-sub);">版本：</span>5.8.2</div>
        <div><span style="color:var(--text-sub);">大小：</span>35.7 MB</div>
        <div><span style="color:var(--text-sub);">更新：</span>2026-06-10</div>
      </div>
      <div style="background:#fff7ed;border:1px solid #fed7aa;border-radius:8px;padding:12px 16px;font-size:13px;color:#9a3412;margin-bottom:20px;">
        &#10003; 官方正版 &nbsp;|&nbsp; &#10003; 安全无捆绑 &nbsp;|&nbsp; &#10003; 免费使用
      </div>
      <a href="https://telegram.org/dl/android" target="_blank" style="display:inline-flex;align-items:center;gap:10px;padding:16px 40px;background:linear-gradient(135deg,var(--primary),var(--primary-dark));color:#fff;border-radius:10px;font-weight:700;font-size:16px;box-shadow:0 4px 16px rgba(234,88,12,.3);">&#11015; 立即下载 Android 版</a>
    </div>

    <div style="background:var(--card);border-radius:var(--radius);padding:28px;box-shadow:var(--shadow);border:1px solid var(--border);">
      <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;">
        <div style="width:48px;height:48px;background:#fce7f3;color:#be185d;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:800;">i</div>
        <div>
          <h3 style="font-size:18px;font-weight:700;">Telegram iOS 客户端</h3>
          <p style="font-size:13px;color:var(--text-sub);">适用于 iPhone / iPad，iOS 13.0 及以上</p>
        </div>
      </div>
      <div style="background:#fff7ed;border:1px solid #fed7aa;border-radius:8px;padding:12px 16px;font-size:13px;color:#9a3412;margin-bottom:20px;">
        &#10003; 前往 App Store 下载官方正版 &nbsp;|&nbsp; &#10003; 免费使用
      </div>
      <a href="https://apps.apple.com/app/telegram-messenger/id686449807" target="_blank" style="display:inline-flex;align-items:center;gap:10px;padding:16px 40px;background:linear-gradient(135deg,var(--primary),var(--primary-dark));color:#fff;border-radius:10px;font-weight:700;font-size:16px;box-shadow:0 4px 16px rgba(234,88,12,.3);">&#127818; 前往 App Store 下载</a>
    </div>
  </div>

  <div>
    <div style="background:var(--card);border-radius:var(--radius);padding:24px;box-shadow:var(--shadow);border:1px solid var(--border);margin-bottom:20px;position:sticky;top:84px;">
      <h4 style="font-size:16px;font-weight:700;margin-bottom:16px;">下载说明</h4>
      <ul style="list-style:none;font-size:14px;line-height:2.2;color:var(--text-sub);">
        <li>&#10003; 所有版本均为官方正版</li>
        <li>&#10003; 免费下载，无捆绑软件</li>
        <li>&#10003; 支持多平台同时使用</li>
        <li>&#10003; 聊天记录云端同步</li>
      </ul>
    </div>
    <div style="background:linear-gradient(135deg,var(--primary),var(--primary-light));border-radius:var(--radius);padding:24px;color:#fff;text-align:center;">
      <h4 style="font-size:16px;font-weight:700;margin-bottom:8px;">安装遇到问题？</h4>
      <p style="font-size:13px;opacity:.9;margin-bottom:16px;">查看我们的安装教程文章</p>
      <a href="index.html#articles" style="display:inline-block;padding:10px 24px;background:#fff;color:var(--primary);border-radius:8px;font-weight:700;font-size:14px;">查看教程</a>
    </div>
  </div>
</div>'''
    return wrap_page(
        "Telegram最新版免费下载 - Windows/Android/iOS官方客户端 | TG图片修复站",
        "提供Telegram各平台最新版官方客户端免费下载，覆盖Windows、Android、iOS，安全无捆绑，附安装教程。",
        "telegram下载,telegram最新版,TG客户端下载",
        "download.html", schema_software(), body
    )

# ============================================================
# 合规页面
# ============================================================
def build_privacy():
    body = '''
<section class="hero" style="padding:40px 0;"><div class="container"><div class="hero-badge">隐私政策</div><h1>隐私政策</h1><p>最后更新：2026年6月18日</p></div></section>
<section class="section" style="background:#fff;">
<div class="container" style="max-width:800px;line-height:1.9;font-size:14px;">
  <h2 style="font-size:20px;font-weight:700;margin:28px 0 12px;">信息收集</h2>
  <p>本站不收集任何个人身份信息。访问本站的日志数据（如IP地址、浏览器类型）仅用于技术分析，不会与第三方共享。</p>
  <h2 style="font-size:20px;font-weight:700;margin:28px 0 12px;">Cookie使用</h2>
  <p>本站使用必要Cookie以确保基本功能正常运行。您可以随时通过浏览器设置拒绝Cookie，但这可能会影响部分功能的使用。</p>
  <h2 style="font-size:20px;font-weight:700;margin:28px 0 12px;">外部链接</h2>
  <p>本站包含指向外部网站的链接（如官方下载地址）。这些网站有独立的隐私政策，本站对其内容或隐私实践不承担责任。</p>
  <h2 style="font-size:20px;font-weight:700;margin:28px 0 12px;">政策更新</h2>
  <p>我们可能会不时更新本隐私政策。任何变更将在本页面发布，并注明最后更新日期。建议您定期查阅本页面以了解最新隐私实践。</p>
  <h2 style="font-size:20px;font-weight:700;margin:28px 0 12px;">联系我们</h2>
  <p>如果您对本隐私政策有任何疑问，请通过邮箱 contact@shengyi5.com 联系我们。</p>
</div>
</section>'''
    return wrap_page("隐私政策 - TG图片修复站", "TG图片修复站隐私政策说明。", "隐私政策", "privacy.html", None, body)

def build_about():
    body = '''
<section class="hero" style="padding:40px 0;"><div class="container"><div class="hero-badge">关于我们</div><h1>关于 TG图片修复站</h1><p>专注Telegram图片相关问题解决</p></div></section>
<section class="section" style="background:#fff;">
<div class="container" style="max-width:800px;line-height:1.9;font-size:15px;">
  <h2 style="font-size:22px;font-weight:700;margin-bottom:16px;">站点简介</h2>
  <p>TG图片修复站是一个专注于Telegram图片加载相关问题解决的教程站点。我们提供免费的、详细的排查与修复指南，帮助用户解决使用过程中遇到的各类图片相关问题。</p>
  <h2 style="font-size:22px;font-weight:700;margin:24px 0 16px;">我们的内容</h2>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px;">
    <div style="background:var(--bg);border-radius:var(--radius);padding:20px;"><h4 style="font-weight:700;margin-bottom:8px;">&#128214; 教程文章</h4><p style="font-size:14px;color:var(--text-sub);">详细的步骤教程，覆盖各类图片问题场景</p></div>
    <div style="background:var(--bg);border-radius:var(--radius);padding:20px;"><h4 style="font-weight:700;margin-bottom:8px;">&#128295; 修复指南</h4><p style="font-size:14px;color:var(--text-sub);">按问题分类的修复方法，快速定位解决方案</p></div>
    <div style="background:var(--bg);border-radius:var(--radius);padding:20px;"><h4 style="font-weight:700;margin-bottom:8px;">&#128241; 下载资源</h4><p style="font-size:14px;color:var(--text-sub);">提供各平台Telegram官方客户端下载</p></div>
    <div style="background:var(--bg);border-radius:var(--radius);padding:20px;"><h4 style="font-weight:700;margin-bottom:8px;">&#10067; 常见问题</h4><p style="font-size:14px;color:var(--text-sub);">整理高频问题，快速查阅答案</p></div>
  </div>
  <h2 style="font-size:22px;font-weight:700;margin-bottom:16px;">免责声明</h2>
  <div style="background:var(--primary-soft);border:1px solid #fed7aa;border-radius:var(--radius);padding:16px 20px;font-size:14px;color:#9a3412;line-height:1.8;">
    本站内容仅为海外合规地区软件功能科普教程，不提供网络访问相关方案，不引导任何违规操作，内容仅供学习参考。本站与Telegram官方无关。
  </div>
</div>
</section>'''
    return wrap_page("关于我们 - TG图片修复站", "了解TG图片修复站，专注Telegram图片加载相关问题解决。", "关于我们", "about.html", None, body)

def build_contact():
    body = '''
<section class="hero" style="padding:40px 0;"><div class="container"><div class="hero-badge">联系我们</div><h1>联系我们</h1><p>如有疑问，请通过以下方式联系</p></div></section>
<section class="section" style="background:#fff;">
<div class="container" style="max-width:600px;text-align:center;font-size:15px;line-height:2;">
  <p>邮箱：contact@shengyi5.com</p>
  <p>我们会在3个工作日内回复您的邮件。</p>
</div>
</section>'''
    return wrap_page("联系我们 - TG图片修复站", "联系TG图片修复站。", "联系我们", "contact.html", None, body)

# ============================================================
# sitemap + robots（自动包含文章）
# ============================================================
def build_sitemap(articles):
    today = datetime.date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    urls = [
        ("/",            "1.0",  "daily"),
        ("/articles.html",     "0.9",  "weekly"),
        ("/download.html",     "0.95", "weekly"),
    ]
    for art in articles:
        urls.append((f"/{art['slug']}.html", "0.9", "weekly"))
    for cat in CATEGORIES:
        urls.append((f"/{cat['slug']}.html", "0.8", "monthly"))
    urls.append(("/privacy.html",   "0.3",  "yearly"))
    urls.append(("/about.html",      "0.3",  "yearly"))
    urls.append(("/contact.html",    "0.3",  "yearly"))
    for path, pri, freq in urls:
        lines.append(f'  <url><loc>{DOMAIN}{path}</loc><priority>{pri}</priority><changefreq>{freq}</changefreq><lastmod>{today}</lastmod></url>')
    lines.append('</urlset>')
    return '\n'.join(lines)

def build_robots():
    return f'''User-agent: *
Allow: /

Disallow: /admin/
Disallow: /private/

Sitemap: {DOMAIN}/sitemap.xml'''

# ============================================================
# 主函数
# ============================================================
def main():
    print("=" * 50)
    print("TG站点生成器 v2.0 - 数据驱动架构")
    print("=" * 50)

    os.chdir(BASE_DIR)

    # 1. 读取文章数据
    articles = load_articles()
    print(f"\n[数据] 读取到 {len(articles)} 篇文章:")
    for art in articles:
        print(f"  - {art['slug']}.json  ({art.get('category_name','')})")

    total_pages = 1 + 1 + len(CATEGORIES) + len(articles) + 1 + 3  # 首页+归档+分类+文章+下载+合规
    print(f"\n将生成 {total_pages} 个页面 + sitemap + robots\n")

    page_num = 0

    # 1. 首页
    page_num += 1
    print(f"  [{page_num}/{total_pages}] index.html")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(build_index(articles))

    # 1b. 文章归档页
    page_num += 1
    print(f"  [{page_num}/{total_pages}] articles.html")
    with open("articles.html", "w", encoding="utf-8") as f:
        f.write(build_articles_page(articles))

    # 2. 分类页
    for cat in CATEGORIES:
        page_num += 1
        fname = cat["slug"] + ".html"
        print(f"  [{page_num}/{total_pages}] {fname}")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(build_category(cat["slug"], cat["name"], cat["kw"], articles))

    # 3. 文章页（从JSON数据自动生成）
    for art in articles:
        page_num += 1
        fname = art["slug"] + ".html"
        print(f"  [{page_num}/{total_pages}] {fname}  <- {art['_filename']}")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(build_article_page(art, articles))

    # 4. 下载页
    page_num += 1
    print(f"  [{page_num}/{total_pages}] download.html")
    with open("download.html", "w", encoding="utf-8") as f:
        f.write(build_download())

    # 5. 合规页
    page_num += 1
    print(f"  [{page_num}/{total_pages}] privacy.html / about.html / contact.html")
    with open("privacy.html", "w", encoding="utf-8") as f:
        f.write(build_privacy())
    with open("about.html", "w", encoding="utf-8") as f:
        f.write(build_about())
    with open("contact.html", "w", encoding="utf-8") as f:
        f.write(build_contact())

    # 6. sitemap + robots
    print(f"  [sitemap] sitemap.xml ({len(articles)} 篇文章自动包含)")
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(build_sitemap(articles))
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(build_robots())

    print(f"\n{'=' * 50}")
    print(f"完成！共生成 {total_pages + 2} 个文件")
    print(f"文章数据: articles/ 目录下 {len(articles)} 个 JSON 文件")
    print(f"加新文章: 在 articles/ 放入 JSON 文件，重新运行 build.py")
    print(f"{'=' * 50}")

if __name__ == "__main__":
    main()
