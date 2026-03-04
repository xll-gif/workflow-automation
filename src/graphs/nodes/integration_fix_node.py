"""
联调问题自动修复节点（v7.0 新增）

根据联调测试结果自动修复代码中的问题
支持常见问题的自动修复：错误处理、加载状态、Mock 集成等
"""
import os
import json
import logging
import re
from typing import List, Dict, Any
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
    IntegrationFixInput,
    IntegrationFixOutput
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


def apply_error_handling_fix(code: str, file_path: str) -> Dict[str, Any]:
    """
    应用错误处理修复

    Args:
        code: 原始代码
        file_path: 文件路径

    Returns:
        修复结果
    """
    # 检查是否已经有错误处理
    if "try {" in code or "try:" in code:
        return {"applied": False, "reason": "已存在错误处理"}

    # 简单的修复策略：在 API 调用周围添加 try-catch
    if "axios" in code:
        # 查找 axios 调用
        pattern = r'(await\s+)?axios\.(get|post|put|delete)\([^)]+\)'

        def add_try_catch(match):
            api_call = match.group(0)
            indent = "    " * code[:match.start()].count("\n")
            return f"""{indent}try {{
                {indent}    {api_call}
                {indent}}} catch (error) {{
                {indent}    console.error('API调用失败:', error)
                {indent}    // 处理错误
                {indent}}}
"""

        fixed_code = re.sub(pattern, add_try_catch, code)
        return {"applied": True, "fixed_code": fixed_code}
    elif "fetch" in code:
        # 查找 fetch 调用
        pattern = r'(await\s+)?fetch\([^)]+\)'

        def add_try_catch(match):
            api_call = match.group(0)
            indent = "    " * code[:match.start()].count("\n")
            return f"""{indent}try {{
                {indent}    {api_call}
                {indent}}} catch (error) {{
                {indent}    console.error('API调用失败:', error)
                {indent}    // 处理错误
                {indent}}}
"""

        fixed_code = re.sub(pattern, add_try_catch, code)
        return {"applied": True, "fixed_code": fixed_code}

    return {"applied": False, "reason": "未找到需要修复的 API 调用"}


def apply_loading_state_fix(code: str, file_path: str) -> Dict[str, Any]:
    """
    应用加载状态修复

    Args:
        code: 原始代码
        file_path: 文件路径

    Returns:
        修复结果
    """
    # 检查是否已经有加载状态
    if "loading" in code.lower() or "isLoading" in code or "loadingState" in code:
        return {"applied": False, "reason": "已存在加载状态"}

    # 简单的修复策略：在文件开头添加 loading 状态
    if "axios" in code or "fetch" in code:
        # 查找变量声明部分
        if "const " in code:
            # 在第一个 const 声明后添加 loading 状态
            first_const = code.find("const ")
            after_first_const = code.find("\n", first_const)
            insert_pos = after_first_const + 1

            indent = "    " * code[:insert_pos].count("\n")
            loading_state = f"{indent}const [loading, setLoading] = useState(false)\n{indent}const [error, setError] = useState(null)\n\n"

            fixed_code = code[:insert_pos] + loading_state + code[insert_pos:]
            return {"applied": True, "fixed_code": fixed_code}

    return {"applied": False, "reason": "未找到合适的位置添加加载状态"}


def apply_mock_integration_fix(code: str, file_path: str, mock_type: str) -> Dict[str, Any]:
    """
    应用 Mock 集成修复

    Args:
        code: 原始代码
        file_path: 文件路径
        mock_type: Mock 类型（msw/mockjs）

    Returns:
        修复结果
    """
    # 检查是否已经集成 Mock
    if "msw" in code or "Mock.mock" in code:
        return {"applied": False, "reason": "已集成 Mock 服务"}

    # 简单的修复策略：在文件末尾添加 Mock 服务初始化代码
    if mock_type == "msw":
        mock_code = """
// 初始化 MSW Mock 服务
if (import.meta.env.DEV) {
  const { worker } = await import('./mocks/handlers')
  await worker.start()
}
"""
    else:  # mockjs
        mock_code = """
// 初始化 Mock.js
import Mock from 'mockjs'
// Mock 请求会在 mocks 目录中配置
"""

    fixed_code = code + "\n" + mock_code
    return {"applied": True, "fixed_code": fixed_code}


def integration_fix_node(
    state: IntegrationFixInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> IntegrationFixOutput:
    """
    title: 联调问题自动修复
    desc: 根据联调测试结果自动修复代码中的问题
    integrations: 大语言模型
    """
    ctx = runtime.context

    logger.info("=" * 80)
    logger.info("🔧 开始自动修复联调问题")
    logger.info("=" * 80)

    logger.info(f"修复平台: {state.platform}")
    logger.info(f"待修复问题数: {len(state.issues_to_fix)}")
    logger.info(f"生成文件数量: {len(state.generated_code)}")

    try:
        # 读取配置文件
        cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
        with open(cfg_file, 'r') as fd:
            _cfg = json.load(fd)

        llm_config = _cfg.get("config", {})
        sp = _cfg.get("sp", "")
        up = _cfg.get("up", "")

        # 初始化 LLM 客户端
        llm_client = LLMClient(llm_config)

        fixed_code = state.generated_code.copy()
        fixes_applied = []
        remaining_issues = []

        # 按问题类型进行修复
        for issue in state.issues_to_fix:
            issue_type = issue.get("type")
            file_path = issue.get("file", "")
            severity = issue.get("severity")

            # 只修复错误级别的问题
            if severity != "error":
                remaining_issues.append(issue)
                continue

            if file_path not in fixed_code:
                remaining_issues.append(issue)
                continue

            original_code = fixed_code[file_path]
            fix_result = None

            # 根据问题类型应用不同的修复策略
            if issue_type == "missing_error_handling":
                fix_result = apply_error_handling_fix(original_code, file_path)
            elif issue_type == "missing_loading_state":
                fix_result = apply_loading_state_fix(original_code, file_path)
            elif issue_type == "missing_mock_integration":
                fix_result = apply_mock_integration_fix(original_code, file_path, "msw")

            if fix_result and fix_result.get("applied"):
                fixed_code[file_path] = fix_result["fixed_code"]
                fixes_applied.append({
                    "issue_type": issue_type,
                    "file": file_path,
                    "reason": fix_result.get("reason", ""),
                    "suggestion": issue.get("suggestion", "")
                })
                logger.info(f"✅ 已修复问题: {issue_type} ({file_path})")
            else:
                remaining_issues.append(issue)
                logger.warning(f"⚠️ 无法自动修复: {issue_type} - {fix_result.get('reason', '未知原因') if fix_result else '未知原因'}")

        # 如果还有复杂问题，使用 LLM 辅助修复
        if remaining_issues:
            logger.info("\n📋 使用 LLM 辅助修复复杂问题")
            logger.info("-" * 80)

            complex_issues = [issue for issue in remaining_issues if issue.get("severity") == "error"]
            if complex_issues:
                issues_str = json.dumps(complex_issues, ensure_ascii=False, indent=2)
                code_str = json.dumps(fixed_code, ensure_ascii=False)

                up_tpl = Template(up)
                user_prompt_content = up_tpl.render({
                    "issues": issues_str,
                    "code": code_str,
                    "platform": state.platform
                })

                messages = [
                    SystemMessage(content=sp),
                    HumanMessage(content=user_prompt_content)
                ]

                response = llm_client.invoke(messages)
                response_text = get_text_content(response.content)

                try:
                    # 尝试解析 LLM 返回的修复方案
                    llm_fixes = json.loads(response_text)
                    for fix in llm_fixes.get("fixes", []):
                        file_path = fix.get("file")
                        if file_path in fixed_code:
                            fixed_code[file_path] = fix.get("fixed_code", fixed_code[file_path])
                            fixes_applied.append(fix)

                    # 更新剩余问题列表
                    remaining_issues = [issue for issue in remaining_issues if issue not in llm_fixes.get("fixed_issues", [])]

                except json.JSONDecodeError:
                    logger.warning("⚠️ 无法解析 LLM 返回的修复方案")

        # 生成摘要
        summary = f"""
自动修复摘要:
- 修复平台: {state.platform}
- 原始问题数: {len(state.issues_to_fix)}
- 已修复问题数: {len(fixes_applied)}
- 剩余问题数: {len(remaining_issues)}

已应用的修复:
"""
        for fix in fixes_applied[:5]:  # 只显示前 5 个
            summary += f"  - {fix.get('issue_type', 'unknown')}: {fix.get('file', 'unknown')}\n"

        if len(fixes_applied) > 5:
            summary += f"  ... 还有 {len(fixes_applied) - 5} 个修复\n"

        logger.info(summary)
        logger.info("=" * 80)
        logger.info("🔧 自动修复完成")
        logger.info("=" * 80)

        return IntegrationFixOutput(
            success=len(remaining_issues) == 0,
            platform=state.platform,
            fixed_code=fixed_code,
            fixes_applied=fixes_applied,
            remaining_issues=remaining_issues,
            summary=summary
        )

    except Exception as e:
        logger.error(f"❌ 自动修复失败: {e}")
        import traceback
        traceback.print_exc()

        return IntegrationFixOutput(
            success=False,
            platform=state.platform,
            fixed_code=state.generated_code,
            fixes_applied=[],
            remaining_issues=state.issues_to_fix,
            summary=f"❌ 自动修复失败: {str(e)}"
        )
