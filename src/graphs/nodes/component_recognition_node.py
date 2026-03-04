"""
组件识别节点

识别设计稿中的UI组件并建立层次结构
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
    ComponentRecognitionInput,
    ComponentRecognitionOutput
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


def component_recognition_node(
    state: ComponentRecognitionInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> ComponentRecognitionOutput:
    """
    title: 组件识别
    desc: 识别设计稿中的UI组件，建立组件层次结构，并提供设计建议
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    logger.info("=" * 80)
    logger.info("开始组件识别")
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
    components_str = json.dumps(state.components, ensure_ascii=False, indent=2)
    layout_str = json.dumps(state.layout, ensure_ascii=False, indent=2)
    assets_str = json.dumps(state.processed_assets, ensure_ascii=False, indent=2)
    
    # 渲染用户提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "components": components_str,
        "layout": layout_str,
        "processed_assets": assets_str
    })
    
    logger.info(f"输入组件数量: {len(state.components)}")
    logger.info(f"输入资源数量: {len(state.processed_assets)}")
    
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
            identified_components = result.get("identified_components", [])
            component_hierarchy = result.get("component_hierarchy", {})
            design_summary = result.get("design_summary", "")
            suggestions = result.get("suggestions", [])
        except json.JSONDecodeError:
            # 如果解析失败，使用默认值
            identified_components = state.components
            component_hierarchy = {"root": state.components}
            design_summary = "组件识别完成"
            suggestions = []
        
        logger.info(f"识别组件数量: {len(identified_components)}")
        logger.info(f"设计建议数量: {len(suggestions)}")
        
        # 生成摘要
        summary = f"""
组件识别摘要:
- 原始组件数量: {len(state.components)}
- 识别组件数量: {len(identified_components)}
- 设计建议: {len(suggestions)} 条
- 设计摘要: {design_summary[:100]}...
"""
        
        logger.info(summary)
        logger.info("=" * 80)
        logger.info("组件识别完成")
        logger.info("=" * 80)
        
        return ComponentRecognitionOutput(
            identified_components=identified_components,
            component_hierarchy=component_hierarchy,
            design_summary=design_summary,
            suggestions=suggestions
        )
        
    except Exception as e:
        logger.error(f"组件识别失败: {e}")
        import traceback
        traceback.print_exc()
        
        # 返回默认值
        return ComponentRecognitionOutput(
            identified_components=state.components,
            component_hierarchy={"root": state.components},
            design_summary=f"组件识别失败: {str(e)}",
            suggestions=[]
        )
