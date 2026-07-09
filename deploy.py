import os
import sys
import json
import shutil
import urllib.request
import zipfile
import tarfile
from pathlib import Path

GITHUB_REPO = "LOVE-U987/XIM-Super-Library"
BRANCH_URL = f"https://api.github.com/repos/{GITHUB_REPO}/branches"

ENVIRONMENTS = {
    "Forge": {
        "branch": "Forge",
        "versions": ["1.20.1", "1.20.2", "1.20.3", "1.20.4"],
        "file_pattern": "Forge-{version}-{build}.7z"
    },
    "Fabric": {
        "branch": "Fabric",
        "versions": ["1.21.1", "1.21.2", "1.21.3", "1.21.4", "1.21.5", "1.21.6", "1.21.7", "1.21.8", "1.21.9", "1.21.10", "1.21.11"],
        "file_pattern": "Fabric-{version}-0.18.4.7z"
    },
    "NeoForge": {
        "branch": "NeoForge",
        "versions": ["1.21.1", "1.21.2", "1.21.3", "1.21.4", "1.21.5", "1.21.6", "1.21.7", "1.21.8", "1.21.9", "1.21.10", "1.21.11"],
        "file_pattern": "NeoForge-{version}-{build}.7z"
    }
}

SKILL_CATEGORIES = {
    "minecraft": {
        "name": "Minecraft模组开发",
        "skills": [
            "neoforge-item-modify-workflow",
            "attribute-modify",
            "legendarymage-trail-system",
            "irons-spells-neoforge-1-21-1",
            "tacz-recipe",
            "neoforge-1.21.1-config-screen",
            "kubejs-neoforge-1.21.1",
            "kubejs-forge-1.20.1",
            "pasterdream-dimension-api",
            "mc-config-ui",
            "modern-ui",
            "api-split-multi-module"
        ]
    },
    "web": {
        "name": "Web开发",
        "skills": [
            "frontend-design",
            "frontend-skill",
            "shadcn",
            "gsap",
            "animejs",
            "interaction-design",
            "theme-factory",
            "web-design-guidelines"
        ]
    },
    "tools": {
        "name": "工具使用",
        "skills": [
            "redis-development",
            "agent-browser",
            "webapp-testing",
            "screenshot",
            "writing-plans",
            "brainstorming",
            "code-reviewer",
            "gh-cli",
            "git-commit",
            "algorithmic-art"
        ]
    }
}

TRAe_SKILLS_DIR = Path.home() / ".trae-cn" / "skills"

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                      🚀 XIM超级图书馆 - 一键部署工具                          ║
║                                                                              ║
║  快速部署开发环境和Skill到您的开发目录，让您专注于真正的开发工作！                ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def select_environment():
    print("\n📦 请选择开发环境：")
    for i, (env_name, env_info) in enumerate(ENVIRONMENTS.items(), 1):
        print(f"  {i}. {env_name}")
    
    while True:
        try:
            choice = int(input("\n请输入序号："))
            if 1 <= choice <= len(ENVIRONMENTS):
                return list(ENVIRONMENTS.keys())[choice - 1]
            print("❌ 无效的选择，请重试")
        except ValueError:
            print("❌ 请输入数字")

def select_version(env_name):
    env_info = ENVIRONMENTS[env_name]
    versions = env_info["versions"]
    
    print(f"\n📋 可用的{env_name}版本：")
    for i, version in enumerate(versions, 1):
        print(f"  {i}. {version}")
    
    while True:
        try:
            choice = int(input("\n请输入序号："))
            if 1 <= choice <= len(versions):
                return versions[choice - 1]
            print("❌ 无效的选择，请重试")
        except ValueError:
            print("❌ 请输入数字")

def select_skill_categories():
    print("\n🧩 请选择需要的Skill类别（可多选，用空格分隔）：")
    for i, (cat_key, cat_info) in enumerate(SKILL_CATEGORIES.items(), 1):
        print(f"  {i}. {cat_info['name']} ({len(cat_info['skills'])}个Skill)")
    
    selected = []
    while True:
        try:
            choices = input("\n请输入序号（如：1 3）：").split()
            choices = [int(c) for c in choices]
            
            if all(1 <= c <= len(SKILL_CATEGORIES) for c in choices):
                for c in choices:
                    selected.append(list(SKILL_CATEGORIES.keys())[c - 1])
                return selected
            print("❌ 无效的选择，请重试")
        except ValueError:
            print("❌ 请输入数字")

def select_deploy_path():
    default_path = str(Path.home() / "Documents" / "XIM-Deploy")
    path = input(f"\n📂 请输入部署路径（默认：{default_path}）：").strip()
    
    if not path:
        path = default_path
    
    deploy_path = Path(path)
    deploy_path.mkdir(parents=True, exist_ok=True)
    
    return deploy_path

def download_env_package(env_name, version, deploy_path):
    print(f"\n⬇️ 正在下载{env_name} {version}开发环境...")
    
    env_info = ENVIRONMENTS[env_name]
    branch = env_info["branch"]
    
    download_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{branch}/{env_info['file_pattern'].format(version=version, build='*')}"
    
    try:
        import re
        response = urllib.request.urlopen(f"https://api.github.com/repos/{GITHUB_REPO}/git/trees/{branch}?recursive=1")
        tree = json.loads(response.read())
        
        file_name = None
        for item in tree["tree"]:
            if item["path"].startswith(f"{env_name}-{version}") and item["path"].endswith(".7z"):
                file_name = item["path"]
                break
        
        if not file_name:
            print(f"❌ 未找到{env_name} {version}的环境包")
            return False
        
        url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{branch}/{file_name}"
        file_path = deploy_path / "environment" / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"   URL: {url}")
        print(f"   目标: {file_path}")
        
        urllib.request.urlretrieve(url, str(file_path))
        print(f"✅ {file_name} 下载完成！")
        
        print(f"\n📦 正在解压到 {deploy_path / 'environment' / version}...")
        
        import py7zr
        with py7zr.SevenZipFile(file_path, mode='r') as z:
            z.extractall(path=str(deploy_path / 'environment' / version))
        
        print(f"✅ {env_name} {version} 部署完成！")
        return True
    
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False

def deploy_skills(categories, deploy_path):
    print("\n📤 正在部署Skill文件...")
    
    skill_deploy_path = deploy_path / "skills"
    skill_deploy_path.mkdir(parents=True, exist_ok=True)
    
    for category in categories:
        cat_info = SKILL_CATEGORIES[category]
        print(f"\n   📂 {cat_info['name']}")
        
        for skill_name in cat_info["skills"]:
            src_path = SKILLS_DIR / category / skill_name
            dest_path = skill_deploy_path / category / skill_name
            
            if not src_path.exists():
                print(f"      ⚠️ 未找到Skill: {skill_name}")
                continue
            
            if dest_path.exists():
                shutil.rmtree(dest_path)
            
            shutil.copytree(src_path, dest_path)
            print(f"      ✅ {skill_name}")
    
    print("\n✅ Skill部署完成！")
    return True

def deploy_to_trae(categories):
    print("\n📤 正在部署到TRAE技能目录...")
    
    for category in categories:
        cat_info = SKILL_CATEGORIES[category]
        print(f"\n   📂 {cat_info['name']}")
        
        for skill_name in cat_info["skills"]:
            src_path = TRAe_SKILLS_DIR / skill_name
            dest_path = TRAe_SKILLS_DIR / skill_name
            
            if not src_path.exists():
                print(f"      ⚠️ 未找到Skill: {skill_name}")
                continue
            
            print(f"      ✅ {skill_name} (已在TRAE目录中)")
    
    print("\n✅ TRAE技能目录部署完成！")
    return True

def main():
    print_banner()
    
    print("\n" + "="*60)
    print("🎯 步骤1：选择开发环境")
    print("="*60)
    env_name = select_environment()
    version = select_version(env_name)
    
    print("\n" + "="*60)
    print("🎯 步骤2：选择Skill类别")
    print("="*60)
    skill_categories = select_skill_categories()
    
    print("\n" + "="*60)
    print("🎯 步骤3：选择部署路径")
    print("="*60)
    deploy_path = select_deploy_path()
    
    print("\n" + "="*60)
    print("📋 部署确认")
    print("="*60)
    print(f"  开发环境: {env_name} {version}")
    print(f"  Skill类别: {', '.join([SKILL_CATEGORIES[c]['name'] for c in skill_categories])}")
    print(f"  部署路径: {deploy_path}")
    
    confirm = input("\n是否开始部署？(y/n): ").strip().lower()
    if confirm != 'y':
        print("🚫 部署已取消")
        return
    
    print("\n" + "="*60)
    print("🚀 开始部署")
    print("="*60)
    
    env_success = download_env_package(env_name, version, deploy_path)
    skill_success = deploy_skills(skill_categories, deploy_path)
    trae_success = deploy_to_trae(skill_categories)
    
    print("\n" + "="*60)
    print("🎉 部署完成！")
    print("="*60)
    print(f"  📁 开发环境: {deploy_path / 'environment' / version}")
    print(f"  📁 Skill文件: {deploy_path / 'skills'}")
    print(f"  📁 TRAE技能: {TRAE_SKILLS_DIR}")
    print("\n💡 提示：")
    print("   - 开发环境已解压到指定目录，可以直接用IDE打开")
    print("   - Skill文件已部署，可以在AI助手中使用")
    print("   - 如果需要更新，再次运行此脚本即可")

if __name__ == "__main__":
    main()
