"""
 * XIM超级图书馆 - 加速部署工具
 * 
 * 功能：多线程加速下载开发环境和Skill文件
 * 特点：
 * - 自动检测aria2c进行16线程并发下载
 * - Python自带多线程保底下载（8线程）
 * - 自动使用ghproxy国内镜像加速
 * - 实时显示下载速度、进度和ETA
 * - 下载完成后自动解压
 * 
 * 作者: XIM Super Library
 * 版本: 1.0.0
 * 日期: 2026-07-05
"""

import os
import sys
import json
import shutil
import subprocess
import time
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# ==================== 配置 ====================

GITHUB_REPO = "LOVE-U987/XIM-Super-Library"
GHPROXY_URL = "https://ghproxy.com/"

# 环境配置：框架 -> (分支名, 可用的Minecraft版本列表)
ENVIRONMENTS = {
    "Forge": {
        "branch": "Forge",
        "versions": ["1.20.1", "1.20.2", "1.20.3", "1.20.4"]
    },
    "Fabric": {
        "branch": "Fabric",
        "versions": ["1.21.1", "1.21.2", "1.21.3", "1.21.4", "1.21.5", "1.21.6", "1.21.7", "1.21.8", "1.21.9", "1.21.10", "1.21.11"]
    },
    "NeoForge": {
        "branch": "NeoForge",
        "versions": ["1.21.1", "1.21.2", "1.21.3", "1.21.4", "1.21.5", "1.21.6", "1.21.7", "1.21.8", "1.21.9", "1.21.10", "1.21.11"]
    }
}

# Skill分类配置
SKILL_CATEGORIES = {
    "minecraft": {
        "name": "Minecraft模组开发",
        "skills": [
            "neoforge-item-modify-workflow", "attribute-modify",
            "legendarymage-trail-system", "irons-spells-neoforge-1-21-1",
            "tacz-recipe", "neoforge-1.21.1-config-screen",
            "kubejs-neoforge-1.21.1", "kubejs-forge-1.20.1",
            "pasterdream-dimension-api", "mc-config-ui",
            "modern-ui", "api-split-multi-module"
        ]
    },
    "web": {
        "name": "Web开发",
        "skills": [
            "frontend-design", "frontend-skill", "shadcn", "gsap",
            "animejs", "interaction-design", "theme-factory", "web-design-guidelines"
        ]
    },
    "tools": {
        "name": "工具使用",
        "skills": [
            "redis-development", "agent-browser", "webapp-testing",
            "screenshot", "writing-plans", "brainstorming",
            "code-reviewer", "gh-cli", "git-commit", "algorithmic-art"
        ]
    }
}

# ==================== 工具函数 ====================

def print_banner():
    """打印启动横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════════════╗
║          🚀 XIM超级图书馆 - 极速部署工具 v2.0                        ║
║                                                                      ║
║   🎯 ghproxy镜像加速 + git clone秒级下载 + aria2多线程并发           ║
╚══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_aria2c():
    """
    检查系统是否安装了aria2c
    
    @return: True表示已安装，False表示未安装
    """
    try:
        result = subprocess.run(["aria2c", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.split("\n")[0] if result.stdout else "unknown"
            print(f"  ✅ 发现 aria2c: {version}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return False

def download_with_aria2c(url, file_path):
    """
    使用aria2c进行16线程并发下载
    
    @param url: 下载URL
    @param file_path: 保存路径
    @return: 下载成功返回True
    """
    print(f"  🚀 使用 aria2c 16线程并发下载...")
    cmd = [
        "aria2c",
        "-x", "16",       # 最多16个连接
        "-s", "16",       # 拆分16个分段
        "-k", "1M",       # 每段1MB
        "--summary-interval", "1",  # 每秒显示进度
        "--console-log-level", "notice",
        "-d", str(file_path.parent),
        "-o", file_path.name,
        url
    ]
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            line = line.strip()
            if "DIR" in line or "CUID" in line or "SEED" in line:
                continue
            if line:
                print(f"     {line}")
        process.wait()
        return process.returncode == 0
    except Exception as e:
        print(f"  ⚠️  aria2c下载失败: {e}")
        return False

def download_with_python(url, file_path, num_threads=8):
    """
    使用Python多线程下载（含进度条）
    
    @param url: 下载URL
    @param file_path: 保存路径
    @param num_threads: 线程数，默认8
    @return: 下载成功返回True
    """
    print(f"  🐍 使用 Python {num_threads}线程并发下载...")
    
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # 获取文件大小
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=30) as resp:
            total_size = int(resp.headers.get("Content-Length", 0))
        
        if total_size == 0:
            # 无法获取大小，直接单线程下载
            print("  ⚠️  无法获取文件大小，降级为单线程下载...")
            urllib.request.urlretrieve(url, str(file_path))
            return True
        
        # 分段下载
        chunk_size = total_size // num_threads + 1
        ranges = []
        for i in range(num_threads):
            start = i * chunk_size
            end = min((i + 1) * chunk_size - 1, total_size - 1)
            if start <= end:
                ranges.append((start, end))
        
        # 进度追踪
        progress_lock = Lock()
        downloaded = [0]
        start_time = time.time()
        
        def download_chunk(range_start, range_end, chunk_idx):
            """下载单个分段"""
            headers = {"Range": f"bytes={range_start}-{range_end}"}
            req = urllib.request.Request(url, headers=headers)
            
            part_path = file_path.with_suffix(f"{file_path.suffix}.part{chunk_idx}")
            
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    with open(part_path, "wb") as f:
                        while True:
                            chunk = resp.read(8192)
                            if not chunk:
                                break
                            f.write(chunk)
                            with progress_lock:
                                downloaded[0] += len(chunk)
                                
                                # 每秒更新一次进度
                                elapsed = time.time() - start_time
                                if elapsed > 0:
                                    speed = downloaded[0] / elapsed / 1024 / 1024
                                    pct = downloaded[0] / total_size * 100
                                    eta = (total_size - downloaded[0]) / (downloaded[0] / elapsed) if downloaded[0] > 0 else 0
                                    if eta > 0:
                                        print(f"\r     📥 进度: {pct:.1f}% | 速度: {speed:.2f} MB/s | ETA: {eta:.0f}s", end="", flush=True)
                return True, chunk_idx
            except Exception as e:
                return False, f"分段{chunk_idx}错误: {e}"
        
        print(f"  📦 文件大小: {total_size / 1024 / 1024:.1f} MB, 分成 {len(ranges)} 段")
        print(f"  🔗 开始下载...\n")
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = {
                executor.submit(download_chunk, start, end, i): i
                for i, (start, end) in enumerate(ranges)
            }
            
            results = []
            for future in as_completed(futures):
                success, info = future.result()
                results.append((success, info))
        
        print(f"\n")
        
        # 检查所有分段是否成功
        failed = [info for success, info in results if not success]
        if failed:
            print(f"  ❌ 下载失败: {failed}")
            return False
        
        # 合并分段
        print(f"  🔗 正在合并分段文件...")
        with open(file_path, "wb") as outfile:
            for i in range(len(ranges)):
                part_path = file_path.with_suffix(f"{file_path.suffix}.part{i}")
                if part_path.exists():
                    with open(part_path, "rb") as infile:
                        shutil.copyfileobj(infile, outfile)
                    part_path.unlink()
        
        elapsed = time.time() - start_time
        speed = total_size / elapsed / 1024 / 1024
        print(f"  ✅ 下载完成！耗时: {elapsed:.1f}s, 平均速度: {speed:.1f} MB/s")
        return True
        
    except Exception as e:
        print(f"  ❌ 下载失败: {e}")
        return False

def get_github_files(branch):
    """
    通过GitHub API获取指定分支的文件列表
    
    @param branch: 分支名
    @return: 文件列表
    """
    url = f"https://api.github.com/repos/{GITHUB_REPO}/git/trees/{branch}?recursive=1"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "XIM-Super-Library"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            tree = json.loads(resp.read().decode())
            return tree.get("tree", [])
    except Exception as e:
        print(f"  ⚠️  无法获取分支 {branch} 文件列表: {e}")
        return []

def find_env_file(env_name, version):
    """
    查找指定环境和版本的环境包文件
    
    @param env_name: 框架名称
    @param version: Minecraft版本
    @return: (文件名, 分支名) 或 None
    """
    env_info = ENVIRONMENTS.get(env_name)
    if not env_info:
        return None
    
    branch = env_info["branch"]
    files = get_github_files(branch)
    
    # 匹配格式: {env_name}-{version}*.7z
    # 例如: Forge-1.20.1-47.4.10.7z
    prefix = f"{env_name}-{version}"
    
    for item in files:
        if item["path"].startswith(prefix) and item["path"].endswith(".7z"):
            return item["path"], branch
    
    return None

def build_url(file_name, branch, use_mirror=True):
    """
    构建下载URL
    
    @param file_name: 文件名
    @param branch: 分支名
    @param use_mirror: 是否使用ghproxy镜像
    @return: 下载URL
    """
    raw_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{branch}/{file_name}"
    if use_mirror:
        return f"{GHPROXY_URL}{raw_url}"
    return raw_url

def extract_7z(file_path, extract_dir):
    """
    解压.7z文件
    
    @param file_path: 压缩文件路径
    @param extract_dir: 解压目标目录
    @return: 解压成功返回True
    """
    print(f"  📦 正在解压到 {extract_dir}...")
    extract_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        import py7zr
        with py7zr.SevenZipFile(file_path, mode='r') as z:
            z.extractall(path=str(extract_dir))
        print(f"  ✅ 解压完成！")
        return True
    except ImportError:
        print(f"  ⚠️  未安装 py7zr，尝试使用 7z 命令行...")
        try:
            subprocess.run(["7z", "x", str(file_path), f"-o{extract_dir}", "-y"], check=True, capture_output=True)
            print(f"  ✅ 解压完成！")
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            print(f"  ❌ 解压失败，请手动解压: {file_path}")
            print(f"     可以使用: pip install py7zr")
            return False

# ==================== 交互与主逻辑 ====================

def select_from_list(options, title):
    """
    交互式选择器
    
    @param options: 选项列表
    @param title: 标题
    @return: 用户选择的选项值
    """
    print(f"\n📋 {title}：")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    while True:
        try:
            choice = int(input("\n请输入序号："))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print("❌ 无效的选择")
        except ValueError:
            print("❌ 请输入数字")

def select_multi_from_list(options, title):
    """
    多选交互式选择器
    
    @param options: 选项字典 {key: display_name}
    @param title: 标题
    @return: 用户选择的键列表
    """
    items = list(options.items())
    print(f"\n🧩 {title}（可多选，用空格分隔）：")
    for i, (key, display) in enumerate(items, 1):
        print(f"  {i}. {display}")
    
    while True:
        try:
            choices = input("请输入序号（如：1 3）：").split()
            choices = [int(c) for c in choices]
            if choices and all(1 <= c <= len(items) for c in choices):
                return [items[c - 1][0] for c in choices]
            print("❌ 无效的选择")
        except ValueError:
            print("❌ 请输入数字")

def deploy_env(env_name, version, deploy_path, use_mirror):
    """
    部署开发环境
    
    @param env_name: 框架名称
    @param version: Minecraft版本
    @param deploy_path: 部署路径
    @param use_mirror: 是否使用镜像
    """
    print(f"\n{'='*60}")
    print(f"📦 步骤：部署 {env_name} {version} 环境")
    print(f"{'='*60}")
    
    # 查找环境包
    print(f"\n🔍 正在查找 {env_name} {version} 环境包...")
    result = find_env_file(env_name, version)
    
    if not result:
        print(f"❌ 未找到 {env_name} {version} 的环境包")
        print(f"💡 请检查版本号是否正确，或稍后重试")
        return False
    
    file_name, branch = result
    print(f"  ✅ 找到: {file_name}")
    
    # 构建下载URL
    url = build_url(file_name, branch, use_mirror)
    source = "ghproxy镜像" if use_mirror else "GitHub原始"
    print(f"  📡 下载源: {source}")
    
    # 选择下载方式
    file_path = deploy_path / "environment" / file_name
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    has_aria2 = check_aria2c()
    
    if has_aria2:
        print(f"\n🚀 使用 aria2c 16线程极速下载...")
        success = download_with_aria2c(url, file_path)
    else:
        print(f"\n🐍 使用 Python 多线程下载（推荐安装 aria2c 以获得更快速度）...")
        success = download_with_python(url, file_path)
    
    if not success:
        # 降级到单线程
        print(f"\n⚠️  多线程下载失败，降级到单线程下载...")
        try:
            urllib.request.urlretrieve(url, str(file_path))
            print(f"  ✅ 下载完成！")
            success = True
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            return False
    
    # 解压
    extract_dir = deploy_path / "environment" / f"{env_name}-{version}"
    success = extract_7z(file_path, extract_dir)
    
    if success:
        print(f"\n🎉 {env_name} {version} 环境部署完成！")
        print(f"📁 路径: {extract_dir}")
        
        # 清理压缩包
        file_path.unlink(missing_ok=True)
        print(f"🧹 已清理临时压缩包")
        
    return success

def deploy_skills(categories, deploy_path):
    """
    部署Skill文件（从当前项目复制）
    
    @param categories: 需要部署的Skill类别列表
    @param deploy_path: 部署路径
    """
    print(f"\n{'='*60}")
    print(f"📚 步骤：部署Skill文件")
    print(f"{'='*60}")
    
    # 查找当前项目的skill目录
    project_skill_dir = Path(__file__).parent
    category_dirs = {
        "minecraft": project_skill_dir / "minecraft",
        "web": project_skill_dir / "web",
        "tools": project_skill_dir / "tools"
    }
    
    skill_deploy_path = deploy_path / "skills"
    skill_deploy_path.mkdir(parents=True, exist_ok=True)
    
    total_copied = 0
    
    for category in categories:
        cat_info = SKILL_CATEGORIES[category]
        src_dir = category_dirs.get(category)
        
        if not src_dir or not src_dir.exists():
            print(f"  ⚠️ 未找到 {cat_info['name']} 的源文件")
            continue
        
        print(f"\n  📂 {cat_info['name']}:")
        
        for skill_name in cat_info["skills"]:
            skill_src = src_dir / skill_name
            skill_dst = skill_deploy_path / category / skill_name
            
            if not skill_src.exists() or not (skill_src / "SKILL.md").exists():
                print(f"     ⚠️ 跳过: {skill_name}")
                continue
            
            if skill_dst.exists():
                shutil.rmtree(skill_dst)
            
            shutil.copytree(skill_src, skill_dst)
            total_copied += 1
            print(f"     ✅ {skill_name}")
    
    print(f"\n✅ Skill部署完成！共 {total_copied} 个Skill")
    return True

def main():
    """主入口函数"""
    print_banner()
    
    print("\n💡 提示：本工具自动使用 ghproxy.com 国内镜像加速下载")
    print("   如遇下载速度慢，将自动降级或切换下载方式\n")
    
    # 是否使用镜像
    use_mirror = True
    
    # 选择框架
    env_names = list(ENVIRONMENTS.keys())
    env_name = select_from_list(env_names, "请选择开发框架")
    
    # 选择版本
    versions = ENVIRONMENTS[env_name]["versions"]
    version = select_from_list(versions, f"请选择 {env_name} 版本")
    
    # 选择Skill类别
    cat_options = {k: v["name"] for k, v in SKILL_CATEGORIES.items()}
    selected_cats = select_multi_from_list(cat_options, "请选择需要的Skill类别")
    
    # 部署路径
    default_path = str(Path.home() / "Documents" / "XIM-Deploy")
    path_input = input(f"\n📂 部署路径（默认: {default_path}）：").strip()
    deploy_path = Path(path_input) if path_input else Path(default_path)
    deploy_path.mkdir(parents=True, exist_ok=True)
    
    # 确认
    print(f"\n{'='*60}")
    print(f"📋 部署确认")
    print(f"{'='*60}")
    print(f"  框架: {env_name} {version}")
    print(f"  Skill: {', '.join([SKILL_CATEGORIES[c]['name'] for c in selected_cats])}")
    print(f"  路径: {deploy_path}")
    print(f"  加速: {'ghproxy镜像' if use_mirror else '原始GitHub'}")
    
    confirm = input("\n开始部署？(y/n): ").strip().lower()
    if confirm != 'y':
        print("🚫 已取消")
        return
    
    # 开始部署
    env_ok = deploy_env(env_name, version, deploy_path, use_mirror)
    skill_ok = deploy_skills(selected_cats, deploy_path)
    
    # 总结
    print(f"\n{'='*60}")
    if env_ok and skill_ok:
        print(f"🎉 全部部署成功！")
    elif env_ok:
        print(f"⚠️  环境部署成功，但部分Skill部署失败")
    else:
        print(f"❌ 部署过程中出现错误")
    print(f"{'='*60}")
    
    if env_ok:
        print(f"\n📁 {env_name} {version}: {deploy_path / 'environment' / f'{env_name}-{version}'}")
    if skill_ok:
        print(f"📁 Skill文件: {deploy_path / 'skills'}")

if __name__ == "__main__":
    main()
