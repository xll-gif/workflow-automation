"""
iOS Git 推送节点 - 将 iOS 生成的代码推送到 GitHub 仓库
"""
import os
import logging
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import IOSGitPushInput, IOSGitPushOutput
from tools.git_pusher import GitPusher, generate_commit_message

# 设置日志
logger = logging.getLogger(__name__)


def ios_git_push_node(state: IOSGitPushInput, config: RunnableConfig, runtime: Runtime[Context]) -> IOSGitPushOutput:
    """
    title: iOS 代码推送
    desc: 将 iOS 生成的代码推送到 GitHub 仓库
    integrations: GitHub
    """
    ctx = runtime.context

    logger.info("=" * 80)
    logger.info("开始 iOS 代码推送")
    logger.info("=" * 80)

    try:
        # 检查是否有文件需要推送
        if not state.ios_generated_files:
            logger.warning("没有 iOS 生成的文件，跳过推送")
            return IOSGitPushOutput(
                ios_push_result={
                    "success": False,
                    "error": "No files to push",
                    "repo_url": f"https://github.com/{state.repo_owner}/{state.ios_repo_name}.git",
                    "files_pushed": 0
                }
            )

        logger.info(f"推送目标仓库: {state.repo_owner}/{state.ios_repo_name}")
        logger.info(f"待推送文件数: {len(state.ios_generated_files)}")

        # 创建 Git 推送工具
        pusher = GitPusher()

        # 生成提交信息
        commit_message = generate_commit_message(
            issue_title=state.issue_title,
            feature_list=state.feature_list
        )
        logger.info(f"提交信息: {commit_message[:100]}...")

        # 推送文件到仓库
        result = pusher.push_to_repo(
            owner=state.repo_owner,
            repo_name=state.ios_repo_name,
            files=state.ios_generated_files,
            commit_message=commit_message,
            branch="main"
        )

        logger.info("=" * 80)
        logger.info(f"iOS 代码推送{'成功' if result.get('success') else '失败'}")
        logger.info("=" * 80)

        if result.get('success'):
            logger.info(f"推送成功: {result.get('repo_url')}")
            logger.info(f"提交哈希: {result.get('commit_hash')}")
            logger.info(f"推送文件数: {result.get('files_pushed')}")
        else:
            logger.error(f"推送失败: {result.get('error')}")

        return IOSGitPushOutput(ios_push_result=result)

    except Exception as e:
        logger.error(f"iOS 代码推送异常: {e}")
        import traceback
        traceback.print_exc()

        return IOSGitPushOutput(
            ios_push_result={
                "success": False,
                "error": str(e),
                "repo_url": f"https://github.com/{state.repo_owner}/{state.ios_repo_name}.git",
                "files_pushed": 0
            }
        )
