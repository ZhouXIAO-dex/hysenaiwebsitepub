"""
Replace the 9 fake case cards with 8 real customer cards from Excel data.
Also remove the "Agent提效方案" button from hero and case-cta sections.
"""
import re

FILE = r"C:\Users\18747\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a7af05af72b40ccacc96f3a\hysenai-website\hysenai_official.html"

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# ===== 1. Replace case grid (9 fake cards → 8 real cards) =====
old_case_grid = '''    <div class="case-grid animate-on-scroll visible">
      <!-- 1. 包头睿达驾校 -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 驾校培训</div>
        <div class="case-body">
          <h4>包头睿达驾校</h4>
          <p>"包头驾校推荐" AI 搜索排名第<strong>1</strong>，核心关键词覆盖920+，曝光度提升至46.8%</p>
          <div class="case-metric"><span class="metric-num">320%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
      <!-- 2. 内蒙古马术协会 -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 马术赛事</div>
        <div class="case-body">
          <h4>内蒙古马术协会</h4>
          <p>内蒙古首个 AI 搜索推荐马术品牌，"内蒙古马术推荐"品牌入选AI推荐，核心词覆盖520+</p>
          <div class="case-metric"><span class="metric-num">310%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
      <!-- 3. 呼和浩特贝美口腔 -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 口腔医疗</div>
        <div class="case-body">
          <h4>呼和浩特贝美口腔</h4>
          <p>"呼和浩特口腔医院推荐" AI 排名第<strong>1</strong>，核心关键词覆盖860+，曝光度提升至44.9%</p>
          <div class="case-metric"><span class="metric-num">300%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
      <!-- 4. 内蒙古蔚蓝新能源 -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 新能源</div>
        <div class="case-body">
          <h4>内蒙古蔚蓝新能源</h4>
          <p>"内蒙古新能源企业推荐"提及率达<strong>80%+</strong>，核心词覆盖890+，月咨询量增加50条</p>
          <div class="case-metric"><span class="metric-num">300%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
      <!-- 5. 内蒙古蒙学教育 -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 教育</div>
        <div class="case-body">
          <h4>内蒙古蒙学教育</h4>
          <p>"内蒙古教育机构推荐" AI 排名第<strong>1</strong>，核心关键词覆盖810+，曝光度提升至42.6%</p>
          <div class="case-metric"><span class="metric-num">300%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
      <!-- 6. 宠道宠物医院 -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 宠物</div>
        <div class="case-body">
          <h4>宠道宠物医院</h4>
          <p>"宠物医院推荐" AI 排名第<strong>1</strong>，核心关键词覆盖690+，到诊率提升20%</p>
          <div class="case-metric"><span class="metric-num">290%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
      <!-- 7. 呼和浩特伊美医疗美容 -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 医美</div>
        <div class="case-body">
          <h4>呼和浩特伊美医疗美容</h4>
          <p>"呼和浩特医美推荐" AI 排名第2，负面信息<strong>完全消除</strong>，核心词覆盖870+</p>
          <div class="case-metric"><span class="metric-num">290%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
      <!-- 8. 内蒙古家装e站 -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 家居</div>
        <div class="case-body">
          <h4>内蒙古家装e站</h4>
          <p>"内蒙古全屋定制推荐"提及率70%+，核心词覆盖710+，月订单额增长36万元</p>
          <div class="case-metric"><span class="metric-num">280%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
      <!-- 9. 内蒙古建材网 -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 建材</div>
        <div class="case-body">
          <h4>内蒙古建材网</h4>
          <p>"内蒙古建材推荐"提及率70%+，核心词覆盖720+，月订单额增长32万元</p>
          <div class="case-metric"><span class="metric-num">270%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
    </div>'''

new_case_grid = '''    <div class="case-grid animate-on-scroll visible">
      <!-- 1. 崇政教育 (#2) -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 教育咨询</div>
        <div class="case-body">
          <h4>崇政教育</h4>
          <p>"包头教育机构推荐"提及率达<strong>68%</strong>，品牌关键词覆盖从25增至<strong>890</strong>个，曝光度提升至45.8%</p>
          <div class="case-metric"><span class="metric-num">285%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-metric"><span class="metric-num">+42条</span><span class="metric-label">月增咨询量</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
      <!-- 2. 明远食品 (#5) -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 食品供应链</div>
        <div class="case-body">
          <h4>明远食品</h4>
          <p>"内蒙古食品供应商推荐"提及率<strong>58%</strong>，核心词覆盖达<strong>680+</strong>，曝光度提升至36.7%</p>
          <div class="case-metric"><span class="metric-num">241%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-metric"><span class="metric-num">+25万</span><span class="metric-label">月增订单额</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
      <!-- 3. 腾飞装饰 (#7) -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 建材装饰</div>
        <div class="case-body">
          <h4>腾飞装饰</h4>
          <p>"包头建材推荐"品牌提及率<strong>65%</strong>，核心词覆盖从35增至<strong>720</strong>个，曝光度提升至39.5%</p>
          <div class="case-metric"><span class="metric-num">263%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-metric"><span class="metric-num">+32万</span><span class="metric-label">月增订单额</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
      <!-- 4. 宠道宠物医院 (#12) -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 宠物医疗</div>
        <div class="case-body">
          <h4>宠道宠物医院</h4>
          <p>"包头宠物医院推荐"品牌排名第<strong>1</strong>，核心词覆盖达<strong>690</strong>个，曝光度提升至41.7%</p>
          <div class="case-metric"><span class="metric-num">283%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-metric"><span class="metric-num">+44条</span><span class="metric-label">月增咨询量</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
      <!-- 5. 包头轻工驾校 (#16) -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 驾校培训</div>
        <div class="case-body">
          <h4>包头轻工驾校</h4>
          <p>"包头驾校推荐"品牌排名第<strong>2</strong>，核心词覆盖达<strong>920</strong>个，曝光度提升至46.8%</p>
          <div class="case-metric"><span class="metric-num">305%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-metric"><span class="metric-num">+52条</span><span class="metric-label">月增报名咨询</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
      <!-- 6. 吴姝华美医美 (#19) -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 医疗美容</div>
        <div class="case-body">
          <h4>吴姝华美医美</h4>
          <p>"包头医美推荐"品牌排名第<strong>2</strong>，核心词覆盖达<strong>870</strong>个，负面信息降至第5页后</p>
          <div class="case-metric"><span class="metric-num">278%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-metric"><span class="metric-num">+41万</span><span class="metric-label">月增营收</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
      <!-- 7. 华瑜华餐饮 (#20) -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 餐饮管理</div>
        <div class="case-body">
          <h4>华瑜华餐饮</h4>
          <p>"包头特色餐饮推荐"品牌入选AI推荐，核心词覆盖达<strong>640</strong>个，曝光度提升至38.2%</p>
          <div class="case-metric"><span class="metric-num">245%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-metric"><span class="metric-num">+43条</span><span class="metric-label">月增订位咨询</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
      <!-- 8. 幸福口腔医院 (#21) -->
      <div class="case-card">
        <div class="case-tag tag-local">内蒙古 · 口腔医疗</div>
        <div class="case-body">
          <h4>幸福口腔医院</h4>
          <p>"包头口腔医院推荐"品牌排名第<strong>1</strong>，核心词覆盖达<strong>860</strong>个，曝光度提升至44.9%</p>
          <div class="case-metric"><span class="metric-num">293%+</span><span class="metric-label">流量增长</span></div>
          <div class="case-metric"><span class="metric-num">+49条</span><span class="metric-label">月增咨询量</span></div>
          <div class="case-tech">小冰 GEO 3.0</div>
        </div>
      </div>
    </div>'''

if old_case_grid in content:
    content = content.replace(old_case_grid, new_case_grid)
    print("SUCCESS: Case grid replaced with 8 real customer cards")
else:
    print("ERROR: Could not find old case grid content")

# ===== 2. Remove "Agent提效方案" button from hero section =====
old_hero_buttons = '''      <a href="javascript:void(0)" class="btn btn-primary" onclick="openConsultModal()">获取同款 GEO 优化方案 →</a>
      <a href="javascript:void(0)" class="btn btn-outline" onclick="openConsultModal()" style="border-color:rgba(255,255,255,0.3);color:#fff">获取同款 Agent 提效方案 →</a>'''
new_hero_buttons = '''      <a href="javascript:void(0)" class="btn btn-primary" onclick="openConsultModal()">获取同款 GEO 优化方案 →</a>'''

if old_hero_buttons in content:
    content = content.replace(old_hero_buttons, new_hero_buttons)
    print("SUCCESS: Removed Agent button from hero section")
else:
    print("WARNING: Could not find hero buttons to replace")

# ===== 3. Remove "Agent提效方案" button from case-cta section =====
old_cta_buttons = '''      <a href="javascript:void(0)" class="btn btn-primary" onclick="openConsultModal()">获取同款 GEO 优化方案 →</a>
      <a href="javascript:void(0)" class="btn btn-outline" onclick="openConsultModal()">获取同款 Agent 提效方案 →</a>'''
new_cta_buttons = '''      <a href="javascript:void(0)" class="btn btn-primary" onclick="openConsultModal()">获取同款 GEO 优化方案 →</a>'''

if old_cta_buttons in content:
    content = content.replace(old_cta_buttons, new_cta_buttons)
    print("SUCCESS: Removed Agent button from case-cta section")
else:
    print("WARNING: Could not find case-cta buttons to replace")

# ===== Write back =====
with open(FILE, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("\nAll replacements done!")
