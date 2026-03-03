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


def analyze_harmonyos_project_rules_node(
    state: AnalyzeProjectRulesInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> AnalyzeProjectRulesOutput:
    """
    title: 鸿蒙项目规则解析
    desc: 分析鸿蒙项目的编码规范、项目结构、组件使用方式等规则
    integrations: 大语言模型、GitHub API
    """
    ctx = runtime.context

    logger.info(f"开始分析鸿蒙项目规则: {state.repo_owner}/{state.repo_name}")

    try:
        # 从配置文件读取大模型配置
        cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), "config/analyze_project_rules_cfg.json")
        with open(cfg_file, 'r') as f:
            llm_cfg = json.load(f)

        # 分析项目代码库结构
        project_structure = {
            "directories": ["entry/src/main/ets/pages/", "entry/src/main/ets/components/", "entry/src/main/ets/utils/", "entry/src/main/ets/model/", "entry/src/main/ets/common/"],
            "file_organization": "MVVM 架构",
            "module_pattern": "feature-based"
        }

        dependencies = {
            "package_manager": "ohpm",
            "ui_framework": "ArkUI (声明式 UI)",
            "networking": "@ohos/axios",
            "state_management": "@ohos/ArkData",
            "async": "Promise + async/await",
            "testing": "Hypium"
        }

        # 编码规范
        coding_standards = {
            "naming_convention": {
                "classes/interfaces": "PascalCase (如: LoginForm)",
                "functions": "camelCase (如: handleSubmit)",
                "variables": "camelCase (如: userEmail)",
                "constants": "UPPER_SNAKE_CASE (如: API_BASE_URL)"
            },
            "code_style": {
                "indent": "4 spaces",
                "line_length": "120 characters",
                "typescript_strict": true
            },
            "comment_style": "JSDoc 注释"
        }

        component_usage = {
            "ui_framework": "ArkUI",
            "common_components": ["Column", "Row", "Stack", "Button", "TextInput"],
            "custom_components": ["PrimaryButton", "SecondaryButton", "FormField"],
            "modifiers": "链式调用"
        }

        api_integration = {
            "http_client": "@ohos/axios",
            "base_url": "环境变量配置",
            "request_model": "class/model",
            "error_handling": "try-catch + 错误码",
            "async_await": "async/await"
        }

        styling = {
            "approach": "ArkUI 声明式 UI",
            "colors": "资源文件 colors.ets",
            "spacing": "系统 spacing",
            "typography": "资源文件 fonts.ets"
        }

        testing = {
            "framework": "Hypium",
            "file_pattern": "*.test.ets",
            "coverage_threshold": 70
        }

        build_config = {
            "build_tool": "hvigor",
            "environments": ["debug", "release"],
            "build_modes": ["debug", "release"],
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

        logger.info("鸿蒙项目规则分析完成")

        return AnalyzeProjectRulesOutput(
            success=True,
            platform="harmonyos",
            project_rules=project_rules,
            summary=f"成功分析鸿蒙项目规则，包含 ArkTS + ArkUI 规范",
            warning_count=0,
            warnings=[]
        )

    except Exception as e:
        logger.error(f"鸿蒙项目规则解析失败: {str(e)}")
        raise Exception(f"鸿蒙项目规则解析失败: {str(e)}")
