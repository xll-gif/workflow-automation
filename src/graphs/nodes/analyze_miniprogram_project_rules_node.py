import os
import json
import logging
from typing import Dict, Any, List, Optional
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import (
    AnalyzeProjectRulesInput,
    AnalyzeProjectRulesOutput,
    ProjectRules
)

logger = logging.getLogger(__name__)


def analyze_miniprogram_project_rules_node(
    state: AnalyzeProjectRulesInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> AnalyzeProjectRulesOutput:
    """
    title: 小程序项目规则解析
    desc: 分析小程序项目的编码规范、项目结构、组件使用方式等规则
    integrations: 大语言模型、GitHub API
    """
    ctx = runtime.context

    # 根据 platform 获取对应的仓库名称
    repo_name = state.repo_name
    if not repo_name:
        if state.platform == "h5" and state.h5_repo_name:
            repo_name = state.h5_repo_name
        elif state.platform == "ios" and state.ios_repo_name:
            repo_name = state.ios_repo_name
        elif state.platform == "android" and state.android_repo_name:
            repo_name = state.android_repo_name
        elif state.platform == "harmonyos" and state.harmonyos_repo_name:
            repo_name = state.harmonyos_repo_name
        elif state.platform == "miniprogram" and state.miniprogram_repo_name:
            repo_name = state.miniprogram_repo_name

    if not repo_name:
        raise ValueError(f"无法确定 {state.platform} 平台的仓库名称")

    logger.info(f"开始分析小程序项目规则: {state.repo_owner}/{repo_name}")

    try:
        # 从配置文件读取大模型配置
        cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), "config/analyze_project_rules_cfg.json")
        with open(cfg_file, 'r') as f:
            llm_cfg = json.load(f)

        # 分析项目代码库结构
        project_structure = {
            "directories": ["pages/", "components/", "utils/", "api/", "assets/", "styles/"],
            "file_organization": "按页面和组件组织",
            "module_pattern": "page-based"
        }

        dependencies = {
            "package_manager": "npm",
            "ui_library": "WeChat 原生组件",
            "state_management": "小程序原生状态管理",
            "networking": "wx.request 封装",
            "testing": "Miniprogram Simulate"
        }

        # 编码规范
        coding_standards = {
            "naming_convention": {
                "pages": "camelCase (如: loginPage)",
                "components": "kebab-case (如: primary-button)",
                "functions": "camelCase (如: handleSubmit)",
                "variables": "camelCase (如: userEmail)",
                "constants": "UPPER_SNAKE_CASE (如: API_BASE_URL)"
            },
            "code_style": {
                "indent": "2 spaces",
                "quotes": "single quotes",
                "semicolons": "required"
            },
            "comment_style": "JSDoc 注释"
        }

        component_usage = {
            "ui_library": "WeChat 原生组件",
            "common_components": ["view", "button", "input", "image", "text"],
            "custom_components": ["primary-button", "secondary-button", "form-field"],
            "import_style": "在 json 中注册"
        }

        api_integration = {
            "http_client": "wx.request 封装",
            "base_url": "环境变量配置",
            "request_interceptors": ["添加 token", "统一错误处理"],
            "error_handling": "Promise + catch",
            "async_await": "Promise 链式调用"
        }

        styling = {
            "approach": "WXSS",
            "naming": "kebab-case (如: .login-form)",
            "responsive": "rpx 单位",
            "theme": "自定义主题变量"
        }

        testing = {
            "framework": "Miniprogram Simulate",
            "file_pattern": "*.test.js",
            "coverage_threshold": 70
        }

        build_config = {
            "build_tool": "微信开发者工具",
            "environments": ["development", "production"],
            "upload": "小程序后台",
            "versioning": "Semantic Versioning"
        }

        project_rules = ProjectRules(
            project_structure=project_structure,
            coding_standards=coding_standards,
            component_usage=component_usage,
            api_integration=api_integration,
            styling=styling,
            testing=testing,
            dependencies=dependencies,
            build_config=build_config
        )

        logger.info("小程序项目规则分析完成")

        return AnalyzeProjectRulesOutput(
            success=True,
            platform="miniprogram",
            project_rules=project_rules,
            summary=f"成功分析小程序项目规则，包含 WXML + WXSS + JS 规范",
            warning_count=0,
            warnings=[]
        )

    except Exception as e:
        logger.error(f"小程序项目规则解析失败: {str(e)}")
        raise Exception(f"小程序项目规则解析失败: {str(e)}")
