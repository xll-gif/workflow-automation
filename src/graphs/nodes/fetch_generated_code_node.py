"""
代码获取与准备节点
收集五端生成的代码并准备推送数据
"""
import os
import json
from typing import List, Dict, Any
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from pydantic import BaseModel, Field

# 导入状态定义
from graphs.state import (
    FetchGeneratedCodeInput,
    FetchGeneratedCodeOutput
)


def fetch_generated_code_node(
    state: FetchGeneratedCodeInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> FetchGeneratedCodeOutput:
    """
    title: 获取生成的代码
    desc: 收集五端生成的代码并准备推送数据
    integrations: 无
    """
    ctx = runtime.context
    
    print("="*80)
    print("📦 收集五端生成的代码")
    print("="*80)
    
    # 汇总五端代码生成结果
    all_generated_files = []
    platform_files = {}
    
    # 收集 H5 代码
    if state.h5_generated_files:
        print(f"\n✅ H5 代码生成 ({len(state.h5_generated_files)} 个文件)")
        platform_files["h5"] = state.h5_generated_files
        for file_info in state.h5_generated_files:
            print(f"  📄 {file_info.get('path', 'unknown')}")
            all_generated_files.append({
                "platform": "h5",
                **file_info
            })
    
    # 收集 iOS 代码
    if state.ios_generated_files:
        print(f"\n✅ iOS 代码生成 ({len(state.ios_generated_files)} 个文件)")
        platform_files["ios"] = state.ios_generated_files
        for file_info in state.ios_generated_files:
            print(f"  📄 {file_info.get('path', 'unknown')}")
            all_generated_files.append({
                "platform": "ios",
                **file_info
            })
    
    # 收集 Android 代码
    if state.android_generated_files:
        print(f"\n✅ Android 代码生成 ({len(state.android_generated_files)} 个文件)")
        platform_files["android"] = state.android_generated_files
        for file_info in state.android_generated_files:
            print(f"  📄 {file_info.get('path', 'unknown')}")
            all_generated_files.append({
                "platform": "android",
                **file_info
            })
    
    # 收集鸿蒙代码
    if state.harmonyos_generated_files:
        print(f"\n✅ 鸿蒙代码生成 ({len(state.harmonyos_generated_files)} 个文件)")
        platform_files["harmonyos"] = state.harmonyos_generated_files
        for file_info in state.harmonyos_generated_files:
            print(f"  📄 {file_info.get('path', 'unknown')}")
            all_generated_files.append({
                "platform": "harmonyos",
                **file_info
            })
    
    # 收集小程序代码
    if state.miniprogram_generated_files:
        print(f"\n✅ 小程序代码生成 ({len(state.miniprogram_generated_files)} 个文件)")
        platform_files["miniprogram"] = state.miniprogram_generated_files
        for file_info in state.miniprogram_generated_files:
            print(f"  📄 {file_info.get('path', 'unknown')}")
            all_generated_files.append({
                "platform": "miniprogram",
                **file_info
            })
    
    print(f"\n📊 总计: {len(all_generated_files)} 个文件")
    print(f"📊 平台分布: {len(platform_files)} 个平台")
    print("="*80)
    
    # 生成摘要
    summary = f"""
代码收集摘要:
- H5: {len(platform_files.get('h5', []))} 个文件
- iOS: {len(platform_files.get('ios', []))} 个文件
- Android: {len(platform_files.get('android', []))} 个文件
- 鸿蒙: {len(platform_files.get('harmonyos', []))} 个文件
- 小程序: {len(platform_files.get('miniprogram', []))} 个文件
- 总计: {len(all_generated_files)} 个文件
"""
    
    return FetchGeneratedCodeOutput(
        all_generated_files=all_generated_files,
        platform_files=platform_files,
        summary=summary
    )
