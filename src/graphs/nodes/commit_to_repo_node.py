"""
提交到仓库节点

将生成的代码提交到 GitHub 仓库并创建 PR
"""
import os
import json
import logging
from typing import List, Dict, Any
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import GitHubClient

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 导入状态定义
from graphs.state import (
    CommitToRepoInput,
    CommitToRepoOutput
)


def commit_to_repo_node(
    state: CommitToRepoInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> CommitToRepoOutput:
    """
    title: 提交到仓库
    desc: 将生成的代码提交到 GitHub 仓库，并创建 Pull Request（可选）
    integrations: GitHub
    """
    ctx = runtime.context
    
    logger.info("=" * 80)
    logger.info(f"开始提交 {state.platform.upper()} 平台代码到仓库")
    logger.info("=" * 80)
    
    try:
        # 初始化 GitHub 客户端
        github_token = os.getenv("GITHUB_TOKEN", "")
        if not github_token:
            raise ValueError("GITHUB_TOKEN 环境变量未设置")
        
        github_client = GitHubClient(token=github_token)
        
        # 构建仓库路径
        repo_full_name = f"{state.repo_owner}/{state.repo_name}"
        logger.info(f"仓库: {repo_full_name}")
        logger.info(f"分支: {state.branch_name}")
        
        # 1. 检查分支是否存在
        logger.info("检查分支是否存在...")
        try:
            branch = github_client.get_branch(
                owner=state.repo_owner,
                repo=state.repo_name,
                branch=state.branch_name
            )
            logger.info(f"分支 {state.branch_name} 已存在")
            branch_exists = True
        except Exception:
            logger.info(f"分支 {state.branch_name} 不存在，将创建新分支")
            branch_exists = False
        
        # 2. 创建或更新分支
        if not branch_exists:
            logger.info(f"创建新分支 {state.branch_name}...")
            # 获取默认分支的最新提交
            default_branch = "main"
            try:
                default_branch_info = github_client.get_repo(state.repo_owner, state.repo_name)
                default_branch = default_branch_info.get("default_branch", "main")
            except Exception:
                pass
            
            # 创建新分支
            github_client.create_branch(
                owner=state.repo_owner,
                repo=state.repo_name,
                branch=state.branch_name,
                sha=github_client.get_ref(
                    owner=state.repo_owner,
                    repo=state.repo_name,
                    ref=f"heads/{default_branch}"
                ).get("object", {}).get("sha", "")
            )
            logger.info(f"分支 {state.branch_name} 创建成功")
        
        # 3. 创建或更新文件
        logger.info(f"开始提交 {len(state.generated_files)} 个文件...")
        for file_info in state.generated_files:
            file_path = file_info.get("path", "")
            file_content = file_info.get("content", "")
            
            logger.info(f"处理文件: {file_path}")
            
            # 检查文件是否存在
            try:
                existing_file = github_client.get_content(
                    owner=state.repo_owner,
                    repo=state.repo_name,
                    path=file_path,
                    ref=state.branch_name
                )
                sha = existing_file.get("sha", "")
                logger.info(f"文件已存在，将更新")
            except Exception:
                sha = None
                logger.info(f"文件不存在，将创建")
            
            # 创建或更新文件
            github_client.create_or_update_file(
                owner=state.repo_owner,
                repo=state.repo_name,
                path=file_path,
                message=f"{state.commit_message} - {file_path}",
                content=file_content,
                sha=sha,
                branch=state.branch_name
            )
            logger.info(f"文件 {file_path} 提交成功")
        
        # 4. 创建 Pull Request（如果需要）
        pr_url = ""
        if state.create_pr:
            logger.info("创建 Pull Request...")
            pr = github_client.create_pull_request(
                owner=state.repo_owner,
                repo=state.repo_name,
                title=state.pr_title or state.commit_message,
                body=state.commit_message,
                head=state.branch_name,
                base="main"
            )
            pr_url = pr.get("html_url", "")
            logger.info(f"Pull Request 创建成功: {pr_url}")
        
        # 5. 生成分支 URL
        branch_url = f"https://github.com/{repo_full_name}/tree/{state.branch_name}"
        
        # 生成摘要
        summary = f"""
提交摘要 ({state.platform.upper()}):
- 仓库: {repo_full_name}
- 分支: {state.branch_name}
- 提交文件数量: {len(state.generated_files)}
- 分支 URL: {branch_url}
- PR URL: {pr_url if pr_url else '未创建 PR'}
"""
        
        logger.info(summary)
        logger.info("=" * 80)
        logger.info(f"{state.platform.upper()} 平台代码提交完成")
        logger.info("=" * 80)
        
        return CommitToRepoOutput(
            platform=state.platform,
            commit_successful=True,
            branch_url=branch_url,
            pr_url=pr_url,
            error_message="",
            summary=summary
        )
        
    except Exception as e:
        logger.error(f"提交到仓库失败: {e}")
        import traceback
        traceback.print_exc()
        
        # 返回错误信息
        return CommitToRepoOutput(
            platform=state.platform,
            commit_successful=False,
            branch_url="",
            pr_url="",
            error_message=str(e),
            summary=f"{state.platform.upper()} 平台代码提交失败: {str(e)}"
        )
