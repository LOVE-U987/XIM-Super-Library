import os
import shutil
from pathlib import Path

TRAE_SKILLS_DIR = r'c:\Users\97128\.trae-cn\skills'
TARGET_DIR = r'c:\Users\97128\Documents\GitHub\XIM-Super-Library'

CATEGORY_MAP = {
    'minecraft': [
        'neoforge-item-modify-workflow',
        'attribute-modify',
        'legendarymage-trail-system',
        'irons-spells-neoforge-1-21-1',
        'tacz-recipe',
        'neoforge-1.21.1-config-screen',
        'kubejs-neoforge-1.21.1',
        'kubejs-forge-1.20.1',
        'pasterdream-dimension-api',
        'mc-config-ui',
        'modern-ui',
        'api-split-multi-module',
    ],
    'web': [
        'frontend-design',
        'frontend-skill',
        'shadcn',
        'gsap',
        'animejs',
        'interaction-design',
        'theme-factory',
        'web-design-guidelines',
    ],
    'tools': [
        'redis-development',
        'agent-browser',
        'webapp-testing',
        'screenshot',
        'writing-plans',
        'brainstorming',
        'code-reviewer',
        'gh-cli',
        'git-commit',
        'algorithmic-art',
    ],
}

def copy_skill(skill_name, category):
    src_path = Path(TRAE_SKILLS_DIR) / skill_name
    if not src_path.exists():
        print(f"❌ 未找到Skill: {skill_name}")
        return False
    
    dest_path = Path(TARGET_DIR) / category / skill_name
    dest_path.mkdir(parents=True, exist_ok=True)
    
    for item in src_path.rglob('*'):
        if item.is_file():
            rel_path = item.relative_to(src_path)
            dest_file = dest_path / rel_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest_file)
            print(f"📄 复制: {item} -> {dest_file}")
    
    print(f"✅ 成功导入: {skill_name} -> {category}/")
    return True

def create_category_readme(category):
    category_path = Path(TARGET_DIR) / category
    category_path.mkdir(parents=True, exist_ok=True)
    readme_path = category_path / 'README.md'
    
    skills_in_category = CATEGORY_MAP.get(category, [])
    
    content = f"""# {category.capitalize()} Skills

## 📋 目录

"""
    
    for skill in skills_in_category:
        content += f"- [{skill}]({skill}/SKILL.md)\n"
    
    content += f"""
---

**🚀 选择上面的Skill开始学习！**
"""
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"📝 创建目录索引: {readme_path}")

def main():
    print("🚀 开始导入TRAE Skill到XIM超级图书馆...\n")
    
    total_imported = 0
    total_skipped = 0
    
    for category, skills in CATEGORY_MAP.items():
        print(f"\n📂 正在导入 {category} 类别...")
        create_category_readme(category)
        
        for skill in skills:
            if copy_skill(skill, category):
                total_imported += 1
            else:
                total_skipped += 1
    
    print(f"\n🎉 导入完成！")
    print(f"✅ 成功导入: {total_imported} 个Skill")
    print(f"❌ 未找到: {total_skipped} 个Skill")

if __name__ == '__main__':
    main()
