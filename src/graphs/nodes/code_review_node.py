"""
代码审查节点
使用大模型审查生成的代码质量、规范性和潜在问题
"""
import os
import json
import logging
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
from graphs.state import CodeReviewInput, CodeReviewOutput


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


def code_review_node(
    state: CodeReviewInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> CodeReviewOutput:
    """
    title: 代码审查
    desc: 使用大模型审查生成的代码质量、规范性和潜在问题
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    logger.info("=" * 80)
    logger.info("🔍 开始代码审查")
    logger.info("=" * 80)
    
    # 读取配置文件
    cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
    with open(cfg_file, 'r') as fd:
        _cfg = json.load(fd)
    
    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")
    
    logger.info(f"使用的模型: {llm_config.get('model', 'unknown')}")
    
    # 准备输入数据
    all_files_str = json.dumps(state.all_generated_files, ensure_ascii=False, indent=2)
    platform_files_str = json.dumps(state.platform_files, ensure_ascii=False, indent=2)
    
    # 渲染用户提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "all_generated_files": all_files_str,
        "platform_files": platform_files_str,
        "platform": state.platform
    })
    
    logger.info(f"审查平台: {state.platform}")
    logger.info(f"待审查文件数: {len(state.all_generated_files)}")
    
    try:
        # 初始化 LLM 客户端
        llm_client = LLMClient(llm_config)
        
        # 构建消息
        messages = [
            SystemMessage(content=sp),
            HumanMessage(content=user_prompt_content)
        ]
        
        # 调用 LLM
        logger.info("正在调用大语言模型进行代码审查...")
        response = llm_client.invoke(messages)
        
        # 提取响应内容
        response_text = get_text_content(response.content)
        
        logger.info("=" * 80)
        logger.info("代码审查结果:")
        logger.info("=" * 80)
        logger.info(response_text)
        logger.info("=" * 80)
        
        # 解析审查结果
        try:
            review_result = json.loads(response_text)
        except json.JSONDecodeError:
            # 如果不是 JSON，使用默认结构
            review_result = {
                "overall_score": 7.0,
                "issues": [],
                "suggestions": [],
                "summary": response_text
            }
        
        logger.info(f"整体评分: {review_result.get('overall_score', 'N/A')}/10")
        logger.info(f"发现问题: {len(review_result.get('issues', []))}")
        logger.info(f"改进建议: {len(review_result.get('suggestions', []))}")
        
        # 生成摘要
        summary = f"""
代码审查摘要:
- 审查平台: {state.platform}
- 审查文件数: {len(state.all_generated_files)}
- 整体评分: {review_result.get('overall_score', 'N/A')}/10
- 发现问题: {len(review_result.get('issues', []))}
- 改进建议: {len(review_result.get('suggestions', []))}
"""
        
        logger.info(summary)
        logger.info("=" * 80)
        logger.info("代码审查完成")
        logger.info("=" * 80)
        
        return CodeReviewOutput(
            overall_score=review_result.get("overall_score", 7.0),
            issues=review_result.get("issues", []),
            suggestions=review_result.get("suggestions", []),
            summary=review_result.get("summary", summary)
        )
        
    except Exception as e:
        logger.error(f"代码审查失败: {e}")
        import traceback
        traceback.print_exc()
        
        return CodeReviewOutput(
            overall_score=0.0,
            issues=[{"severity": "error", "message": f"审查失败: {str(e)}"}],
            suggestions=[],
            summary=f"代码审查失败: {str(e)}"
        )
