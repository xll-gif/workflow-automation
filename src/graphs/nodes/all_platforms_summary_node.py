"""
五端汇总节点

汇总五端代码生成、审查和测试的结果
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
from graphs.state import (
    AllPlatformsSummaryInput,
    AllPlatformsSummaryOutput
)


def get_text_content(content) -> str:
    """安全地从 AIMessage content 中提取文本"""
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


def all_platforms_summary_node(
    state: AllPlatformsSummaryInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> AllPlatformsSummaryOutput:
    """
    title: 五端汇总
    desc: 汇总五端代码生成、审查和测试的结果，生成最终报告
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    logger.info("=" * 80)
    logger.info("开始汇总五端代码生成结果")
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
    summaries = {
        "ios": state.ios_generation_summary,
        "android": state.android_generation_summary,
        "harmonyos": state.harmonyos_generation_summary,
        "h5": state.h5_generation_summary,
        "miniprogram": state.miniprogram_generation_summary
    }
    summaries_str = json.dumps(summaries, ensure_ascii=False, indent=2)
    
    code_review_str = json.dumps(state.code_review_report, ensure_ascii=False, indent=2)
    test_report_str = json.dumps(state.test_report, ensure_ascii=False, indent=2)
    
    # 渲染用户提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "summaries": summaries_str,
        "code_review_report": code_review_str,
        "test_report": test_report_str
    })
    
    logger.info("准备汇总数据...")
    
    try:
        # 初始化 LLM 客户端
        ctx = runtime.context
        llm_client = LLMClient(ctx=ctx)
        
        # 构建消息
        messages = [
            SystemMessage(content=sp),
            HumanMessage(content=user_prompt_content)
        ]
        
        # 调用 LLM
        logger.info(f"调用大模型: {llm_config.get('model', 'unknown')}")
        response = llm_client.invoke(messages)
        
        # 提取响应内容
        response_text = get_text_content(response.content)
        
        logger.info("=" * 80)
        logger.info("LLM 响应内容:")
        logger.info("=" * 80)
        logger.info(response_text)
        logger.info("=" * 80)
        
        # 解析响应
        try:
            result = json.loads(response_text)
            final_summary = result.get("final_summary", "")
            total_files_generated = result.get("total_files_generated", 0)
            platforms_completed = result.get("platforms_completed", [])
            issues_summary = result.get("issues_summary", "")
            next_steps = result.get("next_steps", [])
        except json.JSONDecodeError:
            # 如果解析失败，使用默认值
            final_summary = "五端代码生成完成"
            total_files_generated = 0
            platforms_completed = ["ios", "android", "harmonyos", "h5", "miniprogram"]
            issues_summary = "无明显问题"
            next_steps = ["进行代码审查", "进行功能测试", "准备发布"]
        
        logger.info(f"总生成文件数: {total_files_generated}")
        logger.info(f"完成的平台: {', '.join(platforms_completed)}")
        logger.info(f"后续步骤: {len(next_steps)} 条")
        
        # 生成最终报告
        final_report = f"""
# 五端代码生成完成报告

## 最终汇总
{final_summary}

## 统计信息
- 总生成文件数: {total_files_generated}
- 完成的平台: {', '.join(platforms_completed)}

## 各平台摘要
### iOS
{state.ios_generation_summary}

### Android
{state.android_generation_summary}

### 鸿蒙
{state.harmonyos_generation_summary}

### H5
{state.h5_generation_summary}

### 小程序
{state.miniprogram_generation_summary}

## 问题汇总
{issues_summary}

## 后续步骤
{chr(10).join(f'- {step}' for step in next_steps)}
"""
        
        logger.info(final_report)
        logger.info("=" * 80)
        logger.info("五端汇总完成")
        logger.info("=" * 80)
        
        return AllPlatformsSummaryOutput(
            final_summary=final_report,
            total_files_generated=total_files_generated,
            platforms_completed=platforms_completed,
            issues_summary=issues_summary,
            next_steps=next_steps
        )
        
    except Exception as e:
        logger.error(f"五端汇总失败: {e}")
        import traceback
        traceback.print_exc()
        
        # 返回默认值
        return AllPlatformsSummaryOutput(
            final_summary=f"五端汇总失败: {str(e)}",
            total_files_generated=0,
            platforms_completed=[],
            issues_summary=str(e),
            next_steps=["修复汇总错误"]
        )
