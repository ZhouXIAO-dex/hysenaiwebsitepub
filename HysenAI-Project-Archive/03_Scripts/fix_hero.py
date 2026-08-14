import re

path = r'C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website\hysenai_official.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ===== 1. Fix heroTitle: replace processed spans with simple HTML =====
pattern = r'<h1 id="heroTitle">.*?</h1>'
replacement = '<h1 id="heroTitle">\u8ba9AI\u4e3a\u5185\u8499\u53e4\u4f01\u4e1a\u6ce8\u5165<span class="highlight">\u589e\u957f\u5f15\u64ce</span></h1>'
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
if new_content != content:
    content = new_content
    print("1. heroTitle restored to simple HTML")
else:
    print("1. WARNING: heroTitle pattern not found")

# ===== 2. Restore the paragraph below heroTitle =====
# The paragraph was deleted, leaving an empty line between </h1> and <div class="hero-actions">
# Current: </h1>\n    \n    <div class="hero-actions">
# Target:  </h1>\n    <p>海森智源 —— ...</p>\n    <div class="hero-actions">

old_empty = '</h1>\n    \n    <div class="hero-actions">'
new_with_p = '</h1>\n    <p>\u6d77\u68ee\u667a\u6e90 \u2014\u2014 \u706b\u5c71\u5f15\u64ce\u5b98\u65b9\u6388\u6743\u670d\u52a1\u5546 \u00b7 \u5c0f\u51b0 GEO \u5185\u8499\u53e4\u72ec\u5bb6\u4ee3\u7406\uff0c\u57fa\u4e8e\u706b\u5c71\u5f15\u64ce\u5927\u6a21\u578b\u5e95\u5ea7\u4e0e XiaoIce \u667a\u80fd\u4ea4\u4e92\u6846\u67b6\uff0c\u4e3a\u4f01\u4e1a\u63d0\u4f9b\u4ece AI \u6a21\u578b\u5e95\u5ea7\u5230\u641c\u7d22\u4f18\u5316\u7684\u5168\u94fe\u8def\u667a\u80fd\u89e3\u51b3\u65b9\u6848\u3002</p>\n    <div class="hero-actions">'

if old_empty in content:
    content = content.replace(old_empty, new_with_p)
    print("2. Restored hero paragraph (slogan description)")
else:
    # Try with different whitespace
    pattern2 = r'(</h1>)\s*(<div class="hero-actions">)'
    replacement2 = r'\1\n    <p>\u6d77\u68ee\u667a\u6e90 \u2014\u2014 \u706b\u5c71\u5f15\u64ce\u5b98\u65b9\u6388\u6743\u670d\u52a1\u5546 \u00b7 \u5c0f\u51b0 GEO \u5185\u8499\u53e4\u72ec\u5bb6\u4ee3\u7406\uff0c\u57fa\u4e8e\u706b\u5c71\u5f15\u64ce\u5927\u6a21\u578b\u5e95\u5ea7\u4e0e XiaoIce \u667a\u80fd\u4ea4\u4e92\u6846\u67b6\uff0c\u4e3a\u4f01\u4e1a\u63d0\u4f9b\u4ece AI \u6a21\u578b\u5e95\u5ea7\u5230\u641c\u7d22\u4f18\u5316\u7684\u5168\u94fe\u8def\u667a\u80fd\u89e3\u51b3\u65b9\u6848\u3002</p>\n    \2'
    new_content = re.sub(pattern2, replacement2, content)
    if new_content != content:
        content = new_content
        print("2. Restored hero paragraph (regex)")
    else:
        print("2. WARNING: Could not find insertion point")

# ===== Write back =====
with open(path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("\nDone!")

# ===== Verify =====
with open(path, 'r', encoding='utf-8') as f:
    verify = f.read()

checks = [
    ('heroTitle simple', '<h1 id="heroTitle">\u8ba9AI\u4e3a\u5185\u8499\u53e4\u4f01\u4e1a\u6ce8\u5165<span class="highlight">\u589e\u957f\u5f15\u64ce</span></h1>' in verify),
    ('heroTitle no spans', 'hero-title-char visible' not in verify),
    ('paragraph restored', '\u6d77\u68ee\u667a\u6e90 \u2014\u2014 \u706b\u5c71\u5f15\u64ce\u5b98\u65b9\u6388\u6743' in verify),
    ('JS guard check', "querySelector('.hero-title-char')) return" in verify),
    ('no hero-stats HTML', '<div class="hero-stats">' not in verify),
]
for name, result in checks:
    print(f"  {'OK' if result else 'FAIL'}: {name}")
