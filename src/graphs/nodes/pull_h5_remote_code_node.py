"""
拉取 H5 远程代码节点
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


def pull_h5_remote_code_node(
    state: PullRemoteCodeInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> PullRemoteCodeOutput:
    """
    title: 拉取 H5 远程代码
    desc: 从 GitHub 仓库拉取 H5 代码到本地，并分析项目规则
    integrations: GitHub API、Git
    """
    ctx = runtime.context
    platform = "h5"

    logger.info(f"开始拉取 H5 远程代码: {state.repo_owner}/{state.repo_name}")

    try:
        github_token = state.github_token or os.getenv("GITHUB_TOKEN")
        workspace_root = os.getenv("COZE_WORKSPACE_PATH", ".")
        repo_local_path = os.path.join(workspace_root, "temp_repos", f"{platform}_repo")

        # 清理旧代码
        if os.path.exists(repo_local_path):
            import shutil
            shutil.rmtree(repo_local_path)

        os.makedirs(os.path.dirname(repo_local_path), exist_ok=True)

        # 克隆仓库
        clone_url = f"https://{github_token}@github.com/{state.repo_owner}/{state.repo_name}.git"
        subprocess.run(
            ["git", "clone", clone_url, repo_local_path],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("✅ H5 仓库克隆成功")

        # 切换分支
        if state.repo_branch and state.repo_branch != "main":
            subprocess.run(
                ["git", "checkout", state.repo_branch],
                check=True,
                capture_output=True,
                text=True,
                cwd=repo_local_path
            )

        # 提取项目规则
        rules = ProjectRules()

        # 分析 package.json
        package_json_path = os.path.join(repo_local_path, "package.json")
        if os.path.exists(package_json_path):
            try:
                with open(package_json_path, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)

                rules.dependencies = {
                    "package_manager": "npm",
                    "framework": "React 18" if "react" in package_data.get("dependencies", {}) else "Unknown",
                    "ui_library": "Ant Design" if "antd" in package_data.get("dependencies", {}) else "Unknown",
                    "build_tool": "Vite" if "vite" in package_data.get("devDependencies", {}) else "Unknown",
                    "test_framework": "Vitest" if "vitest" in package_data.get("devDependencies", {}) else "Unknown"
                }

                rules.coding_standards = {
                    "typescript_strict": True,
                    "linter": "ESLint" if os.path.exists(os.path.join(repo_local_path, ".eslintrc.json")) else "None",
                    "formatter": "Prettier" if os.path.exists(os.path.join(repo_local_path, ".prettierrc")) else "None"
                }

                rules.api_integration = {
                    "http_client": "axios" if "axios" in package_data.get("dependencies", {}) else "fetch",
                    "error_handling": "try-catch"
                }

            except Exception as e:
                logger.warning(f"解析 package.json 失败: {e}")

        # 分析项目结构
        directories = []
        for root, dirs, files in os.walk(repo_local_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != 'dist']
            rel_path = os.path.relpath(root, repo_local_path)
            if rel_path != '.':
                directories.append({"name": os.path.basename(root), "path": rel_path})

        rules.project_structure = {
            "directories": directories,
            "file_organization": "feature-based",
            "module_pattern": "React 组件"
        }

        # 获取代码文件
        code_files = []
        for root, dirs, files in os.walk(repo_local_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != 'dist']
            for file in files:
                if file.endswith(('.ts', '.tsx', '.js', '.jsx', '.css', '.json')):
                    code_files.append({
                        "path": os.path.relpath(os.path.join(root, file), repo_local_path),
                        "name": file
                    })

        return PullRemoteCodeOutput(
            success=True,
            platform=platform,
            repo_local_path=repo_local_path,
            project_rules=rules,
            project_structure={"directories": directories},
            code_files=code_files,
            summary=f"成功拉取 H5 代码，包含 {len(code_files)} 个文件"
        )

    except Exception as e:
        logger.error(f"拉取 H5 代码失败: {str(e)}")
        raise Exception(f"拉取 H5 代码失败: {str(e)}")
