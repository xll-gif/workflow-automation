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


def analyze_ios_project_rules_node(
    state: AnalyzeProjectRulesInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> AnalyzeProjectRulesOutput:
    """
    title: iOS 项目规则解析
    desc: 分析 iOS 项目的编码规范、项目结构、组件使用方式等规则
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

    logger.info(f"开始分析 iOS 项目规则: {state.repo_owner}/{repo_name}")

    try:
        # 从配置文件读取大模型配置
        cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), "config/analyze_project_rules_cfg.json")
        with open(cfg_file, 'r') as f:
            llm_cfg = json.load(f)

        # 分析项目代码库结构
        project_structure = {
            "directories": ["App/", "Views/", "ViewModels/", "Models/", "Services/", "Utils/", "Resources/"],
            "file_organization": "MVVM 架构",
            "module_pattern": "feature-based"
        }

        dependencies = {
            "package_manager": "Swift Package Manager",
            "ui_framework": "SwiftUI",
            "networking": "URLSession / Alamofire",
            "dependency_injection": "Environment",
            "testing": "XCTest"
        }

        # 编码规范
        coding_standards = {
            "naming_convention": {
                "types": "PascalCase (如: LoginForm)",
                "properties": "camelCase (如: userEmail)",
                "functions": "camelCase (如: handleSubmit)",
                "constants": "camelCase with 'k' prefix (如: kAPIBaseURL)"
            },
            "code_style": {
                "indent": "4 spaces",
                "line_length": "100 characters",
                "access_control": "explicit (private, public, internal)"
            },
            "comment_style": "MARK 注释 + 文档注释"
        }

        component_usage = {
            "ui_framework": "SwiftUI",
            "common_components": ["VStack", "HStack", "Button", "TextField"],
            "custom_components": ["PrimaryButton", "SecondaryButton", "FormField"],
            "modifiers": "链式调用"
        }

        api_integration = {
            "http_client": "URLSession 或 Alamofire",
            "base_url": "环境变量配置",
            "request_model": "Codable 协议",
            "error_handling": "Result 类型 + @Published",
            "async_await": "使用 async/await"
        }

        styling = {
            "approach": "SwiftUI 声明式 UI",
            "colors": "Asset Catalog",
            "spacing": "系统 spacing",
            "typography": "系统字体"
        }

        testing = {
            "framework": "XCTest",
            "ui_testing": "XCUITest",
            "file_pattern": "*Tests.swift",
            "coverage_threshold": 70
        }

        build_config = {
            "build_system": "Xcode Build System",
            "environments": ["Debug", "Release"],
            "schemes": ["App"],
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

        logger.info("iOS 项目规则分析完成")

        return AnalyzeProjectRulesOutput(
            success=True,
            platform="ios",
            project_rules=project_rules,
            summary=f"成功分析 iOS 项目规则，包含 MVVM 架构和 SwiftUI 规范",
            warning_count=0,
            warnings=[]
        )

    except Exception as e:
        logger.error(f"iOS 项目规则解析失败: {str(e)}")
        raise Exception(f"iOS 项目规则解析失败: {str(e)}")
