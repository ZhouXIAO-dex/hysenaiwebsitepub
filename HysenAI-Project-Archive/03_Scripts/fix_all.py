import re

path = r'C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website\hysenai_official.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ===== 1. Remove hero paragraph (slogan) =====
old_p = '<p>\u6d77\u68ee\u667a\u6e90 \u2014\u2014 \u706b\u5c71\u5f15\u64ce\u5b98\u65b9\u6388\u6743\u670d\u52a1\u5546 \u00b7 \u5c0f\u51b0 GEO \u5185\u8499\u53e4\u72ec\u5bb6\u4ee3\u7406\uff0c\u57fa\u4e8e\u706b\u5c71\u5f15\u64ce\u5927\u6a21\u578b\u5e95\u5ea7\u4e0e XiaoIce \u667a\u80fd\u4ea4\u4e92\u6846\u67b6\uff0c\u4e3a\u4f01\u4e1a\u63d0\u4f9b\u4ece AI \u6a21\u578b\u5e95\u5ea7\u5230\u641c\u7d22\u4f18\u5316\u7684\u5168\u94fe\u8def\u667a\u80fd\u89e3\u51b3\u65b9\u6848\u3002</p>'
if old_p in content:
    content = content.replace(old_p, '')
    print("1. Removed hero paragraph (slogan)")
else:
    print("1. WARNING: hero paragraph not found")

# ===== 2. Remove corrupted hero-stats section =====
# Match from <div class="hero-stats"> to the closing </div> that ends the stats section
# The section is corrupted, so use regex
pattern_stats = r'\s*<div class="hero-stats">.*?</div>\s*'
# This is tricky because of nested divs. Let me match more specifically.
# The corrupted section looks like:
# <div class="hero-stats">50+</div><div class="label">内蒙古企业</div></div>
#   <div class="hero-stat">...</div>
#   <div class="hero-stat">...</div>
# Let me match from hero-stats opening to the scroll-indicator

old_stats = '''    <div class="hero-stats">50+</div><div class="label">\u5185\u8499\u53e4\u4f01\u4e1a</div></div>
      <div class="hero-stat"><div class="num" data-count="17" data-animated="true">50+</div><div class="label">GEO\u5b9e\u6218\u6848\u4f8b</div></div>
      <div class="hero-stat"><div class="num" data-count="2" data-animated="true">2\u5927</div><div class="label">\u6743\u5a01\u8ba4\u8bc1</div></div>
    '''

if old_stats in content:
    content = content.replace(old_stats, '')
    print("2. Removed corrupted hero-stats section")
else:
    # Try a regex approach
    pattern = r'<div class="hero-stats">.*?<div class="scroll-indicator">'
    replacement = '<div class="scroll-indicator">'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    if new_content != content:
        content = new_content
        print("2. Removed hero-stats section (regex)")
    else:
        print("2. WARNING: hero-stats not found")

# ===== 3. Remove case-cta section (获取 GEO 优化方案 button) =====
old_cta = '''    <div class="case-cta">
      <a href="javascript:void(0)" class="btn btn-primary" onclick="openConsultModal()">\u83b7\u53d6\u540c\u6b3e GEO \u4f18\u5316\u65b9\u6848 \u2192</a>
    </div>'''
if old_cta in content:
    content = content.replace(old_cta, '')
    print("3. Removed case-cta section")
else:
    # Try without the arrow character
    pattern = r'\s*<div class="case-cta">.*?</div>\s*\n'
    new_content = re.sub(pattern, '\n', content, flags=re.DOTALL)
    if new_content != content:
        content = new_content
        print("3. Removed case-cta section (regex)")
    else:
        print("3. WARNING: case-cta not found")

# ===== 4. Re-add JavaScript guard check =====
old_js = '''(function initHeroTitle(){
  const title = document.getElementById('heroTitle');
  const text = title.innerHTML;'''

new_js = '''(function initHeroTitle(){
  const title = document.getElementById('heroTitle');
  if(!title || title.querySelector('.hero-title-char')) return;
  const text = title.innerHTML;'''

if old_js in content:
    content = content.replace(old_js, new_js)
    print("4. Added JavaScript guard check")
else:
    print("4. WARNING: JavaScript function not found")

# ===== Write back =====
with open(path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("\nAll fixes applied!")

# ===== Verify =====
with open(path, 'r', encoding='utf-8') as f:
    verify = f.read()

checks = [
    ('heroTitle correct', '<h1 id="heroTitle">\u8ba9AI\u4e3a\u5185\u8499\u53e4\u4f01\u4e1a\u6ce8\u5165<span class="highlight">\u589e\u957f\u5f15\u64ce</span></h1>' in verify),
    ('No hero paragraph', '\u6d77\u68ee\u667a\u6e90 \u2014\u2014 \u706b\u5c71\u5f15\u64ce\u5b98\u65b9\u6388\u6743' not in verify),
    ('No hero-stats', 'hero-stats' not in verify),
    ('No case-cta', 'case-cta' not in verify),
    ('JS guard check', "querySelector('.hero-title-char')) return" in verify),
]
for name, result in checks:
    print(f"  {'OK' if result else 'FAIL'}: {name}")
