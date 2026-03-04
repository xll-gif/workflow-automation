"""
iOS 代码生成节点

基于需求、设计稿和组件识别结果生成 iOS 代码（SwiftUI）
"""
import os
import json
import logging
from typing import List, Dict, Any
from pathlib import Path
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
from graphs.state import IOSCodeGenerationInput, IOSCodeGenerationOutput


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


def ios_code_generation_node(
    state: IOSCodeGenerationInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> IOSCodeGenerationOutput:
    """
    title: iOS 代码生成
    desc: 生成 iOS 应用的完整代码（SwiftUI）
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    logger.info("=" * 80)
    logger.info("开始 iOS 代码生成")
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
    components_str = json.dumps(state.identified_components, ensure_ascii=False, indent=2)
    api_definitions_str = json.dumps(state.api_definitions, ensure_ascii=False, indent=2)
    static_assets_str = json.dumps(state.static_assets, ensure_ascii=False, indent=2)
    
    # 渲染用户提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "components": components_str,
        "api_definitions": api_definitions_str,
        "static_assets": static_assets_str,
        "feature_list": json.dumps(state.feature_list, ensure_ascii=False)
    })
    
    logger.info(f"输入组件数量: {len(state.identified_components)}")
    logger.info(f"输入 API 数量: {len(state.api_definitions)}")
    logger.info(f"静态资源数量: {len(state.static_assets)}")
    
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
        
        # 解析生成的代码
        try:
            result = json.loads(response_text)

            # 检查返回格式
            if isinstance(result, dict):
                # 如果是 dict，检查是否有 generated_files 字段
                if 'generated_files' in result:
                    generated_files = result['generated_files']
                    summary = result.get('summary', summary)
                else:
                    # 如果没有 generated_files 字段，将整个 dict 作为单个文件
                    generated_files = [{
                        "path": "ios.json",
                        "content": json.dumps(result, ensure_ascii=False, indent=2)
                    }]
            elif isinstance(result, list):
                # 如果是 list，直接使用
                generated_files = result
            else:
                # 其他情况，将结果作为单个文件
                generated_files = [{
                    "path": "ios.json",
                    "content": json.dumps(result, ensure_ascii=False, indent=2)
                }]
        except json.JSONDecodeError:
            # 如果不是 JSON，尝试提取代码块
            import re
            code_blocks = re.findall(r'```swift\n(.*?)\n```', response_text, re.DOTALL)
            if code_blocks:
                generated_files = []
                for i, code in enumerate(code_blocks):
                    generated_files.append({
                        "path": f"Views/Page{i+1}.swift",
                        "content": code
                    })
            else:
                generated_files = [{"path": "GeneratedCode.swift", "content": response_text}]
        
        logger.info(f"生成文件数量: {len(generated_files)}")
        
        # 生成摘要
        summary = f"""
iOS 代码生成摘要:
- 组件数量: {len(state.identified_components)}
- API 数量: {len(state.api_definitions)}
- 生成文件数量: {len(generated_files)}
- 技术栈: SwiftUI
"""
        
        logger.info(summary)
        logger.info("=" * 80)
        logger.info("iOS 代码生成完成")
        logger.info("=" * 80)
        
        return IOSCodeGenerationOutput(
            ios_generated_files=generated_files,
            ios_generation_summary=summary
        )
        
    except Exception as e:
        logger.error(f"iOS 代码生成失败: {e}")
        import traceback
        traceback.print_exc()
        
        return IOSCodeGenerationOutput(
            ios_generated_files=[],
            ios_generation_summary=f"iOS 代码生成失败: {str(e)}"
        )
