"""
拉取远程代码节点
从 GitHub 仓库拉取代码到本地，并分析项目规则
"""
import os
import json
import logging
import subprocess
from typing import Dict, Any, List, Optional
from pathlib import Path
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import (
    PullRemoteCodeInput,
    PullRemoteCodeOutput,
    ProjectRules
)

logger = logging.getLogger(__name__)


def pull_remote_code_node(
    state: PullRemoteCodeInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> PullRemoteCodeOutput:
    """
    title: 拉取远程代码
    desc: 从 GitHub 仓库拉取远程代码到本地临时目录，并分析项目规则
    integrations: GitHub API、Git
    """
    ctx = runtime.context

    logger.info(f"开始拉取远程代码: {state.repo_owner}/{state.repo_name}")
    logger.info(f"平台: {state.platform}")
    logger.info(f"分支: {state.repo_branch or 'main'}")

    try:
        # 获取 GitHub Token
        github_token = state.github_token or os.getenv("GITHUB_TOKEN")

        if not github_token:
            raise ValueError("未提供 GitHub Token，请设置环境变量 GITHUB_TOKEN 或传入参数")

        # 创建临时目录用于存储拉取的代码
        workspace_root = os.getenv("COZE_WORKSPACE_PATH", ".")
        repo_local_path = os.path.join(workspace_root, "temp_repos", f"{state.platform}_repo")

        # 如果目录已存在，先删除
        if os.path.exists(repo_local_path):
            import shutil
            shutil.rmtree(repo_local_path)

        os.makedirs(os.path.dirname(repo_local_path), exist_ok=True)

        # 克隆仓库
        logger.info(f"克隆仓库到: {repo_local_path}")

        # 构造带 Token 的 clone URL
        clone_url = f"https://{github_token}@github.com/{state.repo_owner}/{state.repo_name}.git"

        # 执行 git clone
        try:
            subprocess.run(
                ["git", "clone", clone_url, repo_local_path],
                check=True,
                capture_output=True,
                text=True
            )
            logger.info("✅ 仓库克隆成功")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ 仓库克隆失败: {e.stderr}")
            raise Exception(f"仓库克隆失败: {e.stderr}")

        # 切换到指定分支
        if state.repo_branch and state.repo_branch != "main":
            try:
                subprocess.run(
                    ["git", "checkout", state.repo_branch],
                    check=True,
                    capture_output=True,
                    text=True,
                    cwd=repo_local_path
                )
                logger.info(f"✅ 切换到分支: {state.repo_branch}")
            except subprocess.CalledProcessError as e:
                logger.warning(f"⚠️ 切换分支失败: {e.stderr}，使用默认分支")

        # 分析项目结构
        project_structure = analyze_project_structure(repo_local_path, state.platform)

        # 提取项目规则
        project_rules = extract_project_rules(repo_local_path, state.platform)

        # 获取代码文件列表
        code_files = get_code_files(repo_local_path, state.platform)

        logger.info(f"✅ 项目规则分析完成")
        logger.info(f"  - 项目结构: {len(project_structure)} 个目录")
        logger.info(f"  - 代码文件: {len(code_files)} 个")

        return PullRemoteCodeOutput(
            success=True,
            platform=state.platform,
            repo_local_path=repo_local_path,
            project_rules=project_rules,
            project_structure=project_structure,
            code_files=code_files,
            summary=f"成功拉取并分析 {state.platform} 代码，包含 {len(code_files)} 个文件"
        )

    except Exception as e:
        logger.error(f"拉取远程代码失败: {str(e)}")
        raise Exception(f"拉取远程代码失败: {str(e)}")


def analyze_project_structure(repo_path: str, platform: str) -> Dict[str, Any]:
    """
    分析项目结构
    """
    structure = {}

    if not os.path.exists(repo_path):
        return structure

    # 常见目录
    directories = []

    for root, dirs, files in os.walk(repo_path):
        # 跳过隐藏目录和 node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != 'dist' and d != 'build']

        rel_path = os.path.relpath(root, repo_path)
        if rel_path == '.':
            continue

        directories.append({
            "name": os.path.basename(root),
            "path": rel_path,
            "file_count": len(files)
        })

    structure["directories"] = directories
    structure["total_files"] = sum(d["file_count"] for d in directories)

    return structure


def extract_project_rules(repo_path: str, platform: str) -> ProjectRules:
    """
    从项目代码中提取规则
    """
    rules = ProjectRules()

    if not os.path.exists(repo_path):
        return rules

    # 1. 分析 package.json（H5 平台）
    if platform == "h5":
        package_json_path = os.path.join(repo_path, "package.json")
        if os.path.exists(package_json_path):
            try:
                with open(package_json_path, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)

                # 依赖管理
                rules.dependencies = {
                    "package_manager": "npm",
                    "framework": "Unknown",
                    "ui_library": "Unknown",
                    "build_tool": "Unknown",
                    "test_framework": "Unknown",
                    "styling": "Unknown",
                    "common_dependencies": list(package_data.get("dependencies", {}).keys())
                }

                # 识别框架
                deps = set(rules.dependencies["common_dependencies"])
                if "react" in deps:
                    rules.dependencies["framework"] = "React"
                if "vue" in deps:
                    rules.dependencies["framework"] = "Vue"
                if "antd" in deps:
                    rules.dependencies["ui_library"] = "Ant Design"
                if "element-plus" in deps:
                    rules.dependencies["ui_library"] = "Element Plus"
                if "vite" in deps:
                    rules.dependencies["build_tool"] = "Vite"
                if "vitest" in deps or "jest" in deps:
                    rules.dependencies["test_framework"] = "Vitest" if "vitest" in deps else "Jest"
                if "tailwindcss" in deps:
                    rules.dependencies["styling"] = "Tailwind CSS"
            except Exception as e:
                logger.warning(f"解析 package.json 失败: {e}")

        # 2. 分析 tsconfig.json（TypeScript 配置）
        tsconfig_path = os.path.join(repo_path, "tsconfig.json")
        if os.path.exists(tsconfig_path):
            try:
                with open(tsconfig_path, 'r', encoding='utf-8') as f:
                    tsconfig = json.load(f)
                rules.coding_standards["typescript_strict"] = tsconfig.get("compilerOptions", {}).get("strict", False)
            except Exception as e:
                logger.warning(f"解析 tsconfig.json 失败: {e}")

        # 3. 分析 eslint 配置
        eslint_files = [".eslintrc.json", ".eslintrc.js", ".eslintrc.cjs"]
        for eslint_file in eslint_files:
            eslint_path = os.path.join(repo_path, eslint_file)
            if os.path.exists(eslint_path):
                rules.coding_standards["linter"] = "ESLint"
                break

        # 4. 分析 prettier 配置
        prettier_files = [".prettierrc", ".prettierrc.json", ".prettierrc.js"]
        for prettier_file in prettier_files:
            prettier_path = os.path.join(repo_path, prettier_file)
            if os.path.exists(prettier_path):
                rules.coding_standards["formatter"] = "Prettier"
                break

    # 2. 分析 iOS 项目
    elif platform == "ios":
        project_files = [f for f in os.listdir(repo_path) if f.endswith(".xcodeproj")]
        if project_files:
            rules.project_structure["build_system"] = "Xcode"
            rules.dependencies["ui_framework"] = "SwiftUI"

        # 查找 Package.swift (Swift Package Manager)
        if os.path.exists(os.path.join(repo_path, "Package.swift")):
            rules.dependencies["package_manager"] = "Swift Package Manager"

    # 3. 分析 Android 项目
    elif platform == "android":
        build_gradle_files = ["build.gradle", "build.gradle.kts", "app/build.gradle", "app/build.gradle.kts"]
        for gradle_file in build_gradle_files:
            if os.path.exists(os.path.join(repo_path, gradle_file)):
                rules.dependencies["build_tool"] = "Gradle"
                if gradle_file.endswith(".kts"):
                    rules.dependencies["build_tool"] = "Gradle (Kotlin DSL)"
                break

        # 查找 build.gradle 中的依赖
        settings_gradle_path = os.path.join(repo_path, "settings.gradle.kts")
        if os.path.exists(settings_gradle_path):
            with open(settings_gradle_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "com.google.dagger" in content:
                    rules.dependencies["dependency_injection"] = "Hilt"
                if "org.koin" in content:
                    rules.dependencies["dependency_injection"] = "Koin"

    # 4. 分析鸿蒙项目
    elif platform == "harmonyos":
        if os.path.exists(os.path.join(repo_path, "oh-package.json5")):
            rules.dependencies["package_manager"] = "ohpm"

        # 查找 hvigor 配置
        hvigor_files = ["hvigorw", "hvigorw.bat"]
        for hvigor_file in hvigor_files:
            if os.path.exists(os.path.join(repo_path, hvigor_file)):
                rules.build_config["build_tool"] = "hvigor"
                break

    # 5. 分析小程序项目
    elif platform == "miniprogram":
        if os.path.exists(os.path.join(repo_path, "app.json")):
            try:
                with open(os.path.join(repo_path, "app.json"), 'r', encoding='utf-8') as f:
                    app_config = json.load(f)
                rules.dependencies["framework"] = "微信小程序"
            except Exception as e:
                logger.warning(f"解析 app.json 失败: {e}")

    return rules


def get_code_files(repo_path: str, platform: str) -> List[Dict[str, Any]]:
    """
    获取代码文件列表
    """
    code_files = []

    if not os.path.exists(repo_path):
        return code_files

    # 根据平台定义文件扩展名
    if platform == "h5":
        extensions = [".ts", ".tsx", ".js", ".jsx", ".css", ".scss", ".json"]
    elif platform == "ios":
        extensions = [".swift", ".m", ".h"]
    elif platform == "android":
        extensions = [".kt", ".java", ".xml", ".gradle", ".gradle.kts"]
    elif platform == "harmonyos":
        extensions = [".ets", ".ts", ".json"]
    elif platform == "miniprogram":
        extensions = [".wxml", ".wxss", ".js", ".json"]
    else:
        extensions = [".ts", ".js", ".json"]

    for root, dirs, files in os.walk(repo_path):
        # 跳过隐藏目录和构建产物
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != 'dist' and d != 'build' and d != '.git']

        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, repo_path)

            # 检查文件扩展名
            if any(file.endswith(ext) for ext in extensions):
                code_files.append({
                    "path": rel_path,
                    "name": file,
                    "size": os.path.getsize(file_path)
                })

    return code_files
