"""
联调测试节点（v7.0 新增）

对五端代码进行 API 联调测试（Mock 数据联调）
支持 MSW 和 Mock.js 两种 Mock 格式
"""
import os
import json
import logging
import tempfile
import re
from typing import List, Dict, Any, Optional
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from jinja2 import Template

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 导入状态定义
from graphs.state import (
    IntegrationTestInput,
    IntegrationTestOutput
)


def get_text_content(content) -> str:
    """
    安全地从 AIMessage content 中提取文本
    """
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        if content and isinstance(content[0], str):
            return " ".join(content)
        else:
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            return " ".join(text_parts)
    else:
        return str(content)


def generate_mock_service(api_definitions: List[Dict[str, Any]], mock_type: str) -> str:
    """
    生成 Mock 服务代码

    Args:
        api_definitions: API 定义列表
        mock_type: Mock 类型（msw/mockjs）

    Returns:
        Mock 服务代码
    """
    logger.info(f"生成 Mock 服务代码（类型：{mock_type}）")

    if mock_type == "msw":
        # 生成 MSW 格式的 Mock 代码
        handlers = []
        for api_def in api_definitions:
            method = api_def.get("method", "GET").upper()
            path = api_def.get("path", "")
            name = api_def.get("name", "unknown")

            handler = f"""
    rest.{method.lower()}('{path}', (req, res, ctx) => {{
        return res(
            ctx.status(200),
            ctx.json({{
                "code": 0,
                "message": "success",
                "data": {json.dumps(generate_mock_response(api_def), ensure_ascii=False)}
            }})
        )
    }}),
"""
            handlers.append(handler)

        mock_code = f"""// MSW Mock 服务
import {{ rest }} from 'msw'
import {{ setupWorker }} from 'msw/browser'

const handlers = [
{"".join(handlers)}
]

export const worker = setupWorker(...handlers)
"""
    else:  # mockjs
        # 生成 Mock.js 格式的 Mock 代码
        mock_rules = []
        for api_def in api_definitions:
            method = api_def.get("method", "GET").upper()
            path = api_def.get("path", "")

            rule = f"""Mock.mock(new RegExp('{path}'), '{method}', (options) => {{
    return {json.dumps({
        "code": 0,
        "message": "success",
        "data": generate_mock_response(api_def)
    }, ensure_ascii=False)}
}})"""
            mock_rules.append(rule)

        mock_code = "\n".join(mock_rules)

    return mock_code


def generate_mock_response(api_def: Dict[str, Any]) -> Any:
    """
    根据定义生成 Mock 响应数据

    Args:
        api_def: API 定义

    Returns:
        Mock 响应数据
    """
    response_schema = api_def.get("response_schema", {})

    # 简单的 Mock 数据生成逻辑
    if "email" in str(response_schema):
        return {"email": "test@example.com"}
    elif "token" in str(response_schema):
        return {"token": "mock_token_12345"}
    elif "user" in str(response_schema):
        return {
            "id": 1,
            "username": "test_user",
            "email": "test@example.com"
        }
    else:
        return {"success": True}


def analyze_api_calls(generated_code: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    分析代码中的 API 调用

    Args:
        generated_code: 生成的代码字典

    Returns:
        API 调用列表
    """
    api_calls = []
    api_patterns = [
        (r'axios\.(get|post|put|delete)\(["\']([^"\']+)["\']', "axios"),
        (r'fetch\(["\']([^"\']+)["\']\s*,\s*{{\s*method:\s*["\'](\w+)["\']', "fetch"),
        (r'Uni\.request\({{\s*url:\s*["\']([^"\']+)["\']\s*,\s*method:\s*["\'](\w+)["\']', "uni.request"),
        (r'request\(["\']([^"\']+)["\']', "微信小程序 request"),
    ]

    for file_path, code in generated_code.items():
        for pattern, source in api_patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                if source == "axios":
                    method = match.group(1)
                    url = match.group(2)
                elif source == "fetch":
                    url = match.group(1)
                    method = match.group(2)
                elif source == "uni.request":
                    url = match.group(1)
                    method = match.group(2)
                else:
                    url = match.group(1)
                    method = "POST"  # 默认

                api_calls.append({
                    "file": file_path,
                    "source": source,
                    "method": method.upper(),
                    "url": url,
                    "line": code[:match.start()].count("\n") + 1
                })

    return api_calls


def detect_issues(
    generated_code: Dict[str, str],
    api_calls: List[Dict[str, Any]],
    api_definitions: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    检测代码中的问题

    Args:
        generated_code: 生成的代码
        api_calls: API 调用列表
        api_definitions: API 定义列表

    Returns:
        问题列表
    """
    issues = []

    # 1. 检查是否有 API 调用
    if not api_calls:
        issues.append({
            "type": "missing_api_call",
            "severity": "warning",
            "message": "代码中未检测到 API 调用",
            "suggestion": "建议添加 API 调用以实现功能"
        })

    # 2. 检查错误处理
    for file_path, code in generated_code.items():
        if "axios" in code or "fetch" in code:
            if "try" not in code and "catch" not in code:
                issues.append({
                    "type": "missing_error_handling",
                    "severity": "error",
                    "file": file_path,
                    "message": "API 调用缺少错误处理",
                    "suggestion": "建议添加 try-catch 块处理 API 调用异常"
                })

    # 3. 检查加载状态
    for file_path, code in generated_code.items():
        if "axios" in code or "fetch" in code:
            if "loading" not in code.lower() and "isLoading" not in code:
                issues.append({
                    "type": "missing_loading_state",
                    "severity": "warning",
                    "file": file_path,
                    "message": "API 调用缺少加载状态",
                    "suggestion": "建议添加 loading 状态以提升用户体验"
                })

    # 4. 检查 Mock 服务集成
    has_msw = any("msw" in code for code in generated_code.values())
    has_mockjs = any("mockjs" in code or "Mock.mock" in code for code in generated_code.values())

    if not has_msw and not has_mockjs:
        issues.append({
            "type": "missing_mock_integration",
            "severity": "error",
            "message": "代码中未集成 Mock 服务",
            "suggestion": "建议集成 MSW 或 Mock.js 以支持 Mock 数据联调"
        })

    return issues


def integration_test_node(
    state: IntegrationTestInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> IntegrationTestOutput:
    """
    title: 联调测试
    desc: 对五端代码进行 API 联调测试（Mock 数据联调），支持 MSW 和 Mock.js
    integrations: 大语言模型
    """
    ctx = runtime.context

    logger.info("=" * 80)
    logger.info("🔗 开始联调测试")
    logger.info("=" * 80)

    # 读取配置文件
    cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
    with open(cfg_file, 'r') as fd:
        _cfg = json.load(fd)

    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")

    logger.info(f"测试平台: {state.platform}")
    logger.info(f"使用 Mock: {state.use_mock}")
    logger.info(f"Mock 类型: {state.mock_type}")
    logger.info(f"API 定义数量: {len(state.api_definitions)}")
    logger.info(f"生成文件数量: {len(state.generated_code)}")

    try:
        # 1. 生成 Mock 服务代码
        logger.info("\n📋 步骤 1: 生成 Mock 服务")
        logger.info("-" * 80)

        if state.api_definitions:
            mock_code = generate_mock_service(state.api_definitions, state.mock_type)
            logger.info(f"✅ Mock 服务代码生成成功（{len(mock_code)} 字符）")
        else:
            logger.warning("⚠️ 未提供 API 定义，跳过 Mock 服务生成")
            mock_code = ""

        # 2. 分析 API 调用
        logger.info("\n📋 步骤 2: 分析 API 调用")
        logger.info("-" * 80)

        api_calls = analyze_api_calls(state.generated_code)
        logger.info(f"✅ 检测到 {len(api_calls)} 个 API 调用")

        for api_call in api_calls[:5]:  # 只显示前 5 个
            logger.info(f"  - {api_call['source']}: {api_call['method']} {api_call['url']} ({api_call['file']})")

        # 3. 检测问题
        logger.info("\n📋 步骤 3: 检测代码问题")
        logger.info("-" * 80)

        issues = detect_issues(state.generated_code, api_calls, state.api_definitions)
        logger.info(f"✅ 检测到 {len(issues)} 个问题")

        error_count = sum(1 for issue in issues if issue.get("severity") == "error")
        warning_count = sum(1 for issue in issues if issue.get("severity") == "warning")

        logger.info(f"  - 错误: {error_count}")
        logger.info(f"  - 警告: {warning_count}")

        for issue in issues[:5]:  # 只显示前 5 个问题
            logger.info(f"  [{issue.get('severity').upper()}] {issue.get('message')}")

        # 4. 生成测试摘要
        logger.info("\n📋 步骤 4: 生成测试摘要")
        logger.info("-" * 80)

        summary = f"""
联调测试摘要:
- 测试平台: {state.platform}
- Mock 服务: {'已启用' if state.use_mock else '未启用'}
- Mock 类型: {state.mock_type}
- API 定义数量: {len(state.api_definitions)}
- 检测到的 API 调用: {len(api_calls)}
- 发现的问题: {len(issues)}
  - 错误: {error_count}
  - 警告: {warning_count}
"""

        # 5. 构建测试结果
        test_results = {
            "platform": state.platform,
            "mock_enabled": state.use_mock,
            "mock_type": state.mock_type,
            "api_definitions_count": len(state.api_definitions),
            "api_calls_count": len(api_calls),
            "issues_count": len(issues),
            "error_count": error_count,
            "warning_count": warning_count,
            "all_tests_passed": error_count == 0,
            "success": error_count == 0
        }

        logger.info(summary)
        logger.info("=" * 80)
        logger.info("🔗 联调测试完成")
        logger.info("=" * 80)

        return IntegrationTestOutput(
            success=test_results.get("all_tests_passed", False),
            platform=state.platform,
            test_results=test_results,
            api_calls=api_calls,
            errors=[issue for issue in issues if issue.get("severity") == "error"],
            issues_found=issues,
            summary=summary
        )

    except Exception as e:
        logger.error(f"❌ 联调测试失败: {e}")
        import traceback
        traceback.print_exc()

        return IntegrationTestOutput(
            success=False,
            platform=state.platform,
            test_results={
                "platform": state.platform,
                "error": str(e),
                "all_tests_passed": False
            },
            api_calls=[],
            errors=[{
                "type": "test_failure",
                "severity": "error",
                "message": f"联调测试失败: {str(e)}",
                "suggestion": "请检查代码和配置"
            }],
            issues_found=[],
            summary=f"❌ 联调测试失败: {str(e)}"
        )
