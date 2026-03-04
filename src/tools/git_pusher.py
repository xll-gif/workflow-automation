"""
Git 推送工具 - 用于将生成的代码推送到 GitHub 仓库
"""
import os
import shutil
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

# 导入 GitPython
try:
    import git
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False

# 设置日志
logger = logging.getLogger(__name__)


class GitPusher:
    """Git 推送工具类"""

    def __init__(
        self,
        token: Optional[str] = None,
        workspace_dir: str = "/tmp/git_pusher"
    ):
        """
        初始化 Git 推送工具

        Args:
            token: GitHub Token（如果不提供，将从环境变量读取）
            workspace_dir: 工作目录（用于克隆仓库）
        """
        if not GIT_AVAILABLE:
            raise ImportError("GitPython not available. Please install with: pip install gitpython")

        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GitHub Token not found. Please set GITHUB_TOKEN environment variable.")

        self.workspace_dir = workspace_dir
        self.temp_repos: List[str] = []

        # 创建工作目录
        os.makedirs(self.workspace_dir, exist_ok=True)

        logger.info(f"GitPusher initialized. Workspace: {self.workspace_dir}")

    def _get_auth_url(self, repo_url: str) -> str:
        """
        获取带认证的仓库 URL

        Args:
            repo_url: 原始仓库 URL（https://github.com/owner/repo.git）

        Returns:
            带认证的 URL（https://token@github.com/owner/repo.git）
        """
        if repo_url.startswith("https://github.com/"):
            return repo_url.replace("https://github.com/", f"https://{self.token}@github.com/")
        return repo_url

    def clone_repo(
        self,
        owner: str,
        repo_name: str,
        branch: str = "main"
    ) -> str:
        """
        克隆远程仓库

        Args:
            owner: 仓库所有者
            repo_name: 仓库名称
            branch: 分支名称

        Returns:
            本地仓库路径
        """
        repo_url = f"https://github.com/{owner}/{repo_name}.git"
        auth_url = self._get_auth_url(repo_url)
        local_path = os.path.join(self.workspace_dir, repo_name)

        # 如果目录已存在，先删除
        if os.path.exists(local_path):
            shutil.rmtree(local_path)
            logger.info(f"Removed existing directory: {local_path}")

        logger.info(f"Cloning repository: {owner}/{repo_name} (branch: {branch})")

        try:
            repo = git.Repo.clone_from(
                auth_url,
                local_path,
                branch=branch
            )
            self.temp_repos.append(local_path)
            logger.info(f"Repository cloned to: {local_path}")
            return local_path
        except Exception as e:
            logger.error(f"Failed to clone repository: {e}")
            raise

    def write_files(
        self,
        repo_path: str,
        files: List[Dict[str, str]]
    ) -> None:
        """
        将文件写入仓库

        Args:
            repo_path: 仓库本地路径
            files: 文件列表，每个文件包含 path 和 content
        """
        logger.info(f"Writing {len(files)} files to repository: {repo_path}")

        for file_info in files:
            file_path = file_info.get("path", "")
            content = file_info.get("content", "")

            if not file_path:
                logger.warning("File path is empty, skipping")
                continue

            full_path = os.path.join(repo_path, file_path)

            # 创建目录
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            # 写入文件
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info(f"Written file: {file_path}")

    def commit_and_push(
        self,
        repo_path: str,
        commit_message: str,
        branch: str = "main"
    ) -> str:
        """
        提交并推送更改

        Args:
            repo_path: 仓库本地路径
            commit_message: 提交信息
            branch: 分支名称

        Returns:
            提交哈希
        """
        logger.info(f"Committing and pushing changes to branch: {branch}")

        try:
            repo = git.Repo(repo_path)

            # 检查是否有更改
            if repo.is_dirty(untracked_files=True):
                # 添加所有文件
                repo.git.add(A=True)

                # 提交
                commit_hash = repo.index.commit(commit_message)
                logger.info(f"Committed changes: {commit_hash}")

                # 推送
                origin = repo.remote(name="origin")
                origin.push(branch)

                logger.info(f"Pushed changes to remote: {branch}")
                return str(commit_hash)
            else:
                logger.warning("No changes to commit")
                return ""

        except Exception as e:
            logger.error(f"Failed to commit and push: {e}")
            raise

    def push_to_repo(
        self,
        owner: str,
        repo_name: str,
        files: List[Dict[str, str]],
        commit_message: str,
        branch: str = "main"
    ) -> Dict[str, Any]:
        """
        推送文件到仓库（完整流程）

        Args:
            owner: 仓库所有者
            repo_name: 仓库名称
            files: 文件列表
            commit_message: 提交信息
            branch: 分支名称

        Returns:
            推送结果
        """
        logger.info(f"Starting push to repository: {owner}/{repo_name}")

        result = {
            "success": False,
            "repo_url": f"https://github.com/{owner}/{repo_name}.git",
            "branch": branch,
            "commit_hash": "",
            "error": None,
            "files_pushed": len(files)
        }

        try:
            # 1. 克隆仓库
            repo_path = self.clone_repo(owner, repo_name, branch)

            # 2. 写入文件
            self.write_files(repo_path, files)

            # 3. 提交并推送
            commit_hash = self.commit_and_push(repo_path, commit_message, branch)

            result["success"] = True
            result["commit_hash"] = commit_hash

            logger.info(f"Successfully pushed to repository: {owner}/{repo_name}")

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Failed to push to repository: {e}")

        return result

    def cleanup(self) -> None:
        """清理临时仓库"""
        logger.info("Cleaning up temporary repositories")

        for repo_path in self.temp_repos:
            try:
                if os.path.exists(repo_path):
                    shutil.rmtree(repo_path)
                    logger.info(f"Removed: {repo_path}")
            except Exception as e:
                logger.error(f"Failed to remove {repo_path}: {e}")

        self.temp_repos = []


def generate_commit_message(
    issue_number: Optional[int] = None,
    issue_title: str = "",
    feature_list: List[str] = None
) -> str:
    """
    生成提交信息

    Args:
        issue_number: GitHub Issue 编号
        issue_title: Issue 标题
        feature_list: 功能列表

    Returns:
        提交信息
    """
    if feature_list is None:
        feature_list = []

    parts = []

    # Issue 引用
    if issue_number:
        parts.append(f"feat: #{issue_number} {issue_title}")
    else:
        parts.append(f"feat: {issue_title}")

    # 功能列表
    if feature_list:
        feature_desc = "、".join(feature_list[:3])
        if len(feature_list) > 3:
            feature_desc += "等"
        parts.append(f"实现功能：{feature_desc}")

    return "\n\n".join(parts)
