import re

path = r'C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website\hysenai_official.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'<h1 id="heroTitle">.*?</h1>'
replacement = '<h1 id="heroTitle">\u8ba9AI\u4e3a\u5185\u8499\u53e4\u4f01\u4e1a\u6ce8\u5165<span class="highlight">\u589e\u957f\u5f15\u64ce</span></h1>'

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

if new_content == content:
    print('ERROR: No replacement made')
else:
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(new_content)
    print('SUCCESS: heroTitle fixed')

with open(path, 'r', encoding='utf-8') as f:
    verify = f.read()
if '<h1 id="heroTitle">\u8ba9AI' in verify:
    print('VERIFIED: OK')
else:
    print('FAILED: still wrong')
