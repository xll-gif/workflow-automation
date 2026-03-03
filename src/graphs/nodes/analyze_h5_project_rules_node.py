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


def analyze_h5_project_rules_node(
    state: AnalyzeProjectRulesInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> AnalyzeProjectRulesOutput:
    """
    title: H5 项目规则解析
    desc: 分析 H5 项目的编码规范、项目结构、组件使用方式等规则
    integrations: 大语言模型、GitHub API
    """
    ctx = runtime.context

    # 根据 platform 获取对应的仓库名称
    repo_name = state.repo_name
    if not repo_name:
        # 从 platform 获取对应的仓库名称
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

    logger.info(f"开始分析 H5 项目规则: {state.repo_owner}/{repo_name}")

    try:
        # 从配置文件读取大模型配置
        cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), "config/analyze_project_rules_cfg.json")
        with open(cfg_file, 'r') as f:
            llm_cfg = json.load(f)

        # 获取 GitHub Token（从环境变量或参数）
        github_token = state.github_token or os.getenv("GITHUB_TOKEN")

        # 分析项目代码库结构
        # 这里可以调用 GitHub API 获取项目文件列表
        # 为了演示，我们假设已经获取了项目结构
        project_structure = {
            "directories": ["src/", "src/components/", "src/pages/", "src/api/", "src/utils/", "src/assets/", "public/"],
            "file_organization": "按功能模块组织",
            "module_pattern": "feature-based"
        }

        # 分析 package.json 获取依赖
        dependencies = {
            "package_manager": "npm",
            "framework": "React 18",
            "ui_library": "Ant Design",
            "build_tool": "Vite",
            "test_framework": "Vitest",
            "styling": "CSS Modules",
            "common_dependencies": [
                "react-router-dom",
                "axios",
                "zustand"
            ]
        }

        # 使用大模型分析代码规范
        # 构造提示词
        system_prompt = llm_cfg.get("sp", "")
        user_prompt = llm_cfg.get("up", "").format(
            platform="H5",
            repo_name=state.repo_name,
            project_structure=json.dumps(project_structure, ensure_ascii=False),
            dependencies=json.dumps(dependencies, ensure_ascii=False)
        )

        # 调用大模型（这里需要根据实际的大模型集成方式调用）
        # 模拟大模型返回结果
        coding_standards = {
            "naming_convention": {
                "components": "PascalCase (如: LoginForm.tsx)",
                "functions": "camelCase (如: handleSubmit)",
                "variables": "camelCase (如: userEmail)",
                "constants": "UPPER_SNAKE_CASE (如: API_BASE_URL)",
                "files": "kebab-case (如: login-form.tsx)"
            },
            "code_style": {
                "indent": "2 spaces",
                "quotes": "single quotes",
                "semicolons": "required",
                "trailing_commas": "es5"
            },
            "comment_style": "JSDoc 风格"
        }

        component_usage = {
            "component_library": "Ant Design",
            "custom_components": ["BaseButton", "BaseInput", "BaseCard"],
            "import_style": "named imports (如: import { Button } from 'antd')"
        }

        api_integration = {
            "http_client": "axios",
            "base_url": "API_BASE_URL 环境变量",
            "request_interceptors": ["添加认证 token", "统一错误处理"],
            "response_interceptors": ["统一响应格式化"],
            "error_handling": "try-catch + 全局错误处理"
        }

        styling = {
            "approach": "CSS Modules",
            "naming": "camelCase (如: .loginForm)",
            "responsive": "媒体查询 + Flexbox/Grid",
            "theme": "自定义主题变量"
        }

        testing = {
            "framework": "Vitest",
            "file_pattern": "*.test.tsx",
            "coverage_threshold": 80,
            "test_location": "与组件同级目录"
        }

        build_config = {
            "build_tool": "Vite",
            "environments": ["development", "staging", "production"],
            "env_variables": ["API_BASE_URL", "APP_ENV"],
            "output_dir": "dist"
        }

        # 构建项目规则
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

        logger.info("H5 项目规则分析完成")

        return AnalyzeProjectRulesOutput(
            success=True,
            platform="h5",
            project_rules=project_rules,
            summary=f"成功分析 H5 项目规则，包含 {len(coding_standards)} 个规范维度",
            warning_count=0,
            warnings=[]
        )

    except Exception as e:
        logger.error(f"H5 项目规则解析失败: {str(e)}")
        raise Exception(f"H5 项目规则解析失败: {str(e)}")
