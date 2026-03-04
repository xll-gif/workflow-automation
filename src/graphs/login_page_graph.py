"""
登录页面完整开发工作流 - 主图编排

实现从设计稿解析到五端代码生成的完整流程
"""
import os
from typing import Literal
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig

# 导入状态定义
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput,
    PullRemoteCodeInput,
    PullRemoteCodeOutput,
    IntegrationTestInput,
    IntegrationTestOutput,
    IntegrationFixInput,
    IntegrationFixOutput
)

# 导入节点函数
from graphs.nodes.design_parse_node import design_parse_node
from graphs.nodes.mastergo_asset_upload_node import mastergo_asset_upload_node
from graphs.nodes.component_recognition_node import component_recognition_node
from graphs.nodes.ios_code_generation_node import ios_code_generation_node
from graphs.nodes.android_code_generation_node import android_code_generation_node
from graphs.nodes.harmonyos_code_generation_node import harmonyos_code_generation_node
from graphs.nodes.h5_code_generation_node import h5_code_generation_node
from graphs.nodes.miniprogram_code_generation_node import miniprogram_code_generation_node
from graphs.nodes.testing_node import testing_node
from graphs.nodes.all_platforms_summary_node import all_platforms_summary_node

# 导入 Git 推送节点（v5.0 新增）
from graphs.nodes.h5_git_push_node import h5_git_push_node
from graphs.nodes.ios_git_push_node import ios_git_push_node
from graphs.nodes.android_git_push_node import android_git_push_node
from graphs.nodes.harmonyos_git_push_node import harmonyos_git_push_node
from graphs.nodes.miniprogram_git_push_node import miniprogram_git_push_node

# 导入拉取代码节点（v6.0 新增）
from graphs.nodes.pull_remote_code_node import pull_remote_code_node

# 导入联调测试和修复节点（v7.0 新增）
from graphs.nodes.integration_test_node import integration_test_node
from graphs.nodes.integration_fix_node import integration_fix_node


def should_generate_code(state: GlobalState) -> str:
    """
    判断是否需要继续生成代码

    Returns:
        "generate" - 继续生成代码
        "complete" - 跳过代码生成，直接汇总
    """
    if state.mastergo_url and len(state.components) > 0:
        return "generate"
    else:
        return "complete"


# ==================== 拉取代码节点包装函数（v6.0 新增）====================

def pull_ios_code_wrapper(state: GlobalState, config: RunnableConfig) -> PullRemoteCodeOutput:
    """iOS 代码拉取包装函数"""
    pull_input = PullRemoteCodeInput(
        platform="ios",
        repo_owner=state.repo_owner,
        repo_name=state.ios_repo_name,
        repo_branch="main"
    )
    return pull_remote_code_node(pull_input, config, None)


def pull_android_code_wrapper(state: GlobalState, config: RunnableConfig) -> PullRemoteCodeOutput:
    """Android 代码拉取包装函数"""
    pull_input = PullRemoteCodeInput(
        platform="android",
        repo_owner=state.repo_owner,
        repo_name=state.android_repo_name,
        repo_branch="main"
    )
    return pull_remote_code_node(pull_input, config, None)


def pull_harmonyos_code_wrapper(state: GlobalState, config: RunnableConfig) -> PullRemoteCodeOutput:
    """鸿蒙代码拉取包装函数"""
    pull_input = PullRemoteCodeInput(
        platform="harmonyos",
        repo_owner=state.repo_owner,
        repo_name=state.harmonyos_repo_name,
        repo_branch="main"
    )
    return pull_remote_code_node(pull_input, config, None)


def pull_h5_code_wrapper(state: GlobalState, config: RunnableConfig) -> PullRemoteCodeOutput:
    """H5 代码拉取包装函数"""
    pull_input = PullRemoteCodeInput(
        platform="h5",
        repo_owner=state.repo_owner,
        repo_name=state.h5_repo_name,
        repo_branch="main"
    )
    return pull_remote_code_node(pull_input, config, None)


def pull_miniprogram_code_wrapper(state: GlobalState, config: RunnableConfig) -> PullRemoteCodeOutput:
    """小程序代码拉取包装函数"""
    pull_input = PullRemoteCodeInput(
        platform="miniprogram",
        repo_owner=state.repo_owner,
        repo_name=state.miniprogram_repo_name,
        repo_branch="main"
    )
    return pull_remote_code_node(pull_input, config, None)


# ==================== 联调测试节点包装函数（v7.0 新增）====================

def ios_integration_test_wrapper(state: GlobalState, config: RunnableConfig) -> IntegrationTestOutput:
    """iOS 联调测试包装函数"""
    # 将文件列表转换为代码字典
    ios_code_dict = {}
    for file_info in state.ios_generated_files:
        ios_code_dict[file_info.get("path", "")] = file_info.get("content", "")

    test_input = IntegrationTestInput(
        platform="ios",
        generated_code=ios_code_dict,
        api_definitions=state.api_definitions,
        use_mock=True,
        mock_type="msw"
    )
    return integration_test_node(test_input, config, None)


def android_integration_test_wrapper(state: GlobalState, config: RunnableConfig) -> IntegrationTestOutput:
    """Android 联调测试包装函数"""
    android_code_dict = {}
    for file_info in state.android_generated_files:
        android_code_dict[file_info.get("path", "")] = file_info.get("content", "")

    test_input = IntegrationTestInput(
        platform="android",
        generated_code=android_code_dict,
        api_definitions=state.api_definitions,
        use_mock=True,
        mock_type="msw"
    )
    return integration_test_node(test_input, config, None)


def harmonyos_integration_test_wrapper(state: GlobalState, config: RunnableConfig) -> IntegrationTestOutput:
    """鸿蒙联调测试包装函数"""
    harmonyos_code_dict = {}
    for file_info in state.harmonyos_generated_files:
        harmonyos_code_dict[file_info.get("path", "")] = file_info.get("content", "")

    test_input = IntegrationTestInput(
        platform="harmonyos",
        generated_code=harmonyos_code_dict,
        api_definitions=state.api_definitions,
        use_mock=True,
        mock_type="msw"
    )
    return integration_test_node(test_input, config, None)


def h5_integration_test_wrapper(state: GlobalState, config: RunnableConfig) -> IntegrationTestOutput:
    """H5 联调测试包装函数"""
    h5_code_dict = {}
    for file_info in state.h5_generated_files:
        h5_code_dict[file_info.get("path", "")] = file_info.get("content", "")

    test_input = IntegrationTestInput(
        platform="h5",
        generated_code=h5_code_dict,
        api_definitions=state.api_definitions,
        use_mock=True,
        mock_type="msw"
    )
    return integration_test_node(test_input, config, None)


def miniprogram_integration_test_wrapper(state: GlobalState, config: RunnableConfig) -> IntegrationTestOutput:
    """小程序联调测试包装函数"""
    miniprogram_code_dict = {}
    for file_info in state.miniprogram_generated_files:
        miniprogram_code_dict[file_info.get("path", "")] = file_info.get("content", "")

    test_input = IntegrationTestInput(
        platform="miniprogram",
        generated_code=miniprogram_code_dict,
        api_definitions=state.api_definitions,
        use_mock=True,
        mock_type="msw"
    )
    return integration_test_node(test_input, config, None)


# ==================== 联调修复节点包装函数（v7.0 新增）====================

def ios_integration_fix_wrapper(state: GlobalState, config: RunnableConfig) -> IntegrationFixOutput:
    """iOS 联调修复包装函数"""
    # 从状态中获取测试结果（这里简化处理，实际应该存储在 GlobalState 中）
    ios_code_dict = {}
    for file_info in state.ios_generated_files:
        ios_code_dict[file_info.get("path", "")] = file_info.get("content", "")

    # 这里简化处理，实际应该从测试结果中获取问题列表
    test_result = state.get("ios_integration_test_result", {})
    issues = test_result.get("issues_found", [])

    fix_input = IntegrationFixInput(
        platform="ios",
        generated_code=ios_code_dict,
        integration_test_result=test_result,
        issues_to_fix=issues
    )
    return integration_fix_node(fix_input, config, None)


def android_integration_fix_wrapper(state: GlobalState, config: RunnableConfig) -> IntegrationFixOutput:
    """Android 联调修复包装函数"""
    android_code_dict = {}
    for file_info in state.android_generated_files:
        android_code_dict[file_info.get("path", "")] = file_info.get("content", "")

    test_result = state.get("android_integration_test_result", {})
    issues = test_result.get("issues_found", [])

    fix_input = IntegrationFixInput(
        platform="android",
        generated_code=android_code_dict,
        integration_test_result=test_result,
        issues_to_fix=issues
    )
    return integration_fix_node(fix_input, config, None)


def harmonyos_integration_fix_wrapper(state: GlobalState, config: RunnableConfig) -> IntegrationFixOutput:
    """鸿蒙联调修复包装函数"""
    harmonyos_code_dict = {}
    for file_info in state.harmonyos_generated_files:
        harmonyos_code_dict[file_info.get("path", "")] = file_info.get("content", "")

    test_result = state.get("harmonyos_integration_test_result", {})
    issues = test_result.get("issues_found", [])

    fix_input = IntegrationFixInput(
        platform="harmonyos",
        generated_code=harmonyos_code_dict,
        integration_test_result=test_result,
        issues_to_fix=issues
    )
    return integration_fix_node(fix_input, config, None)


def h5_integration_fix_wrapper(state: GlobalState, config: RunnableConfig) -> IntegrationFixOutput:
    """H5 联调修复包装函数"""
    h5_code_dict = {}
    for file_info in state.h5_generated_files:
        h5_code_dict[file_info.get("path", "")] = file_info.get("content", "")

    test_result = state.get("h5_integration_test_result", {})
    issues = test_result.get("issues_found", [])

    fix_input = IntegrationFixInput(
        platform="h5",
        generated_code=h5_code_dict,
        integration_test_result=test_result,
        issues_to_fix=issues
    )
    return integration_fix_node(fix_input, config, None)


def miniprogram_integration_fix_wrapper(state: GlobalState, config: RunnableConfig) -> IntegrationFixOutput:
    """小程序联调修复包装函数"""
    miniprogram_code_dict = {}
    for file_info in state.miniprogram_generated_files:
        miniprogram_code_dict[file_info.get("path", "")] = file_info.get("content", "")

    test_result = state.get("miniprogram_integration_test_result", {})
    issues = test_result.get("issues_found", [])

    fix_input = IntegrationFixInput(
        platform="miniprogram",
        generated_code=miniprogram_code_dict,
        integration_test_result=test_result,
        issues_to_fix=issues
    )
    return integration_fix_node(fix_input, config, None)


# 创建状态图
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("design_parse", design_parse_node, metadata={"type": "agent", "llm_cfg": "config/design_parse_cfg.json"})
builder.add_node("asset_processing", mastergo_asset_upload_node)
builder.add_node("component_recognition", component_recognition_node, metadata={"type": "agent", "llm_cfg": "config/component_recognition_cfg.json"})

# 添加拉取代码节点（v6.0 新增）
builder.add_node("pull_ios_code", pull_ios_code_wrapper)
builder.add_node("pull_android_code", pull_android_code_wrapper)
builder.add_node("pull_harmonyos_code", pull_harmonyos_code_wrapper)
builder.add_node("pull_h5_code", pull_h5_code_wrapper)
builder.add_node("pull_miniprogram_code", pull_miniprogram_code_wrapper)

# 添加五端代码生成节点
builder.add_node("ios_code_generation", ios_code_generation_node, metadata={"type": "agent", "llm_cfg": "config/ios_code_generation_cfg.json"})
builder.add_node("android_code_generation", android_code_generation_node, metadata={"type": "agent", "llm_cfg": "config/android_code_generation_cfg.json"})
builder.add_node("harmonyos_code_generation", harmonyos_code_generation_node, metadata={"type": "agent", "llm_cfg": "config/harmonyos_code_generation_cfg.json"})
builder.add_node("h5_code_generation", h5_code_generation_node, metadata={"type": "agent", "llm_cfg": "config/h5_code_generation_cfg.json"})
builder.add_node("miniprogram_code_generation", miniprogram_code_generation_node, metadata={"type": "agent", "llm_cfg": "config/miniprogram_code_generation_cfg.json"})

# 添加测试节点
builder.add_node("ios_testing", testing_node, metadata={"type": "agent", "llm_cfg": "config/testing_cfg.json"})
builder.add_node("android_testing", testing_node, metadata={"type": "agent", "llm_cfg": "config/testing_cfg.json"})
builder.add_node("harmonyos_testing", testing_node, metadata={"type": "agent", "llm_cfg": "config/testing_cfg.json"})
builder.add_node("h5_testing", testing_node, metadata={"type": "agent", "llm_cfg": "config/testing_cfg.json"})
builder.add_node("miniprogram_testing", testing_node, metadata={"type": "agent", "llm_cfg": "config/testing_cfg.json"})

# 添加联调测试节点（v7.0 新增）
builder.add_node("ios_integration_test", ios_integration_test_wrapper, metadata={"type": "agent", "llm_cfg": "config/integration_test_cfg.json"})
builder.add_node("android_integration_test", android_integration_test_wrapper, metadata={"type": "agent", "llm_cfg": "config/integration_test_cfg.json"})
builder.add_node("harmonyos_integration_test", harmonyos_integration_test_wrapper, metadata={"type": "agent", "llm_cfg": "config/integration_test_cfg.json"})
builder.add_node("h5_integration_test", h5_integration_test_wrapper, metadata={"type": "agent", "llm_cfg": "config/integration_test_cfg.json"})
builder.add_node("miniprogram_integration_test", miniprogram_integration_test_wrapper, metadata={"type": "agent", "llm_cfg": "config/integration_test_cfg.json"})

# 添加联调修复节点（v7.0 新增）
builder.add_node("ios_integration_fix", ios_integration_fix_wrapper, metadata={"type": "agent", "llm_cfg": "config/integration_fix_cfg.json"})
builder.add_node("android_integration_fix", android_integration_fix_wrapper, metadata={"type": "agent", "llm_cfg": "config/integration_fix_cfg.json"})
builder.add_node("harmonyos_integration_fix", harmonyos_integration_fix_wrapper, metadata={"type": "agent", "llm_cfg": "config/integration_fix_cfg.json"})
builder.add_node("h5_integration_fix", h5_integration_fix_wrapper, metadata={"type": "agent", "llm_cfg": "config/integration_fix_cfg.json"})
builder.add_node("miniprogram_integration_fix", miniprogram_integration_fix_wrapper, metadata={"type": "agent", "llm_cfg": "config/integration_fix_cfg.json"})

# 添加 Git 推送节点（v5.0 新增）
builder.add_node("h5_git_push", h5_git_push_node)
builder.add_node("ios_git_push", ios_git_push_node)
builder.add_node("android_git_push", android_git_push_node)
builder.add_node("harmonyos_git_push", harmonyos_git_push_node)
builder.add_node("miniprogram_git_push", miniprogram_git_push_node)

# 添加汇总节点
builder.add_node("all_platforms_summary", all_platforms_summary_node, metadata={"type": "agent", "llm_cfg": "config/all_platforms_summary_cfg.json"})

# 设置入口点
builder.set_entry_point("design_parse")

# 添加边
builder.add_edge("design_parse", "asset_processing")
builder.add_edge("asset_processing", "component_recognition")

# 添加条件分支
builder.add_conditional_edges(
    source="component_recognition",
    path=should_generate_code,
    path_map={
        "generate": "ios_code_generation",
        "complete": "all_platforms_summary"
    }
)

# 五端并行拉取代码（v6.0 新增）
builder.add_edge("component_recognition", "pull_ios_code")
builder.add_edge("component_recognition", "pull_android_code")
builder.add_edge("component_recognition", "pull_harmonyos_code")
builder.add_edge("component_recognition", "pull_h5_code")
builder.add_edge("component_recognition", "pull_miniprogram_code")

# 五端并行代码生成
builder.add_edge("pull_ios_code", "ios_code_generation")
builder.add_edge("pull_android_code", "android_code_generation")
builder.add_edge("pull_harmonyos_code", "harmonyos_code_generation")
builder.add_edge("pull_h5_code", "h5_code_generation")
builder.add_edge("pull_miniprogram_code", "miniprogram_code_generation")

# 代码生成后并行测试
builder.add_edge("ios_code_generation", "ios_testing")
builder.add_edge("android_code_generation", "android_testing")
builder.add_edge("harmonyos_code_generation", "harmonyos_testing")
builder.add_edge("h5_code_generation", "h5_testing")
builder.add_edge("miniprogram_code_generation", "miniprogram_testing")

# 测试后进行联调测试（v7.0 新增）
builder.add_edge("ios_testing", "ios_integration_test")
builder.add_edge("android_testing", "android_integration_test")
builder.add_edge("harmonyos_testing", "harmonyos_integration_test")
builder.add_edge("h5_testing", "h5_integration_test")
builder.add_edge("miniprogram_testing", "miniprogram_integration_test")

# 联调测试后自动修复问题（v7.0 新增）
builder.add_edge("ios_integration_test", "ios_integration_fix")
builder.add_edge("android_integration_test", "android_integration_fix")
builder.add_edge("harmonyos_integration_test", "harmonyos_integration_fix")
builder.add_edge("h5_integration_test", "h5_integration_fix")
builder.add_edge("miniprogram_integration_test", "miniprogram_integration_fix")

# 修复后推送到 GitHub（v5.0 新增）
builder.add_edge("ios_integration_fix", "ios_git_push")
builder.add_edge("android_integration_fix", "android_git_push")
builder.add_edge("harmonyos_integration_fix", "harmonyos_git_push")
builder.add_edge("h5_integration_fix", "h5_git_push")
builder.add_edge("miniprogram_integration_fix", "miniprogram_git_push")

# 推送后汇总
builder.add_edge(["ios_git_push", "android_git_push", "harmonyos_git_push", "h5_git_push", "miniprogram_git_push"], "all_platforms_summary")

# 汇总后结束
builder.add_edge("all_platforms_summary", END)

# 编译图
main_graph = builder.compile()


if __name__ == "__main__":
    print("登录页面完整开发工作流已编译成功！")
    print("\n工作流流程（v7.0）：")
    print("1. 设计稿解析")
    print("2. 资源处理")
    print("3. 组件识别")
    print("4. 五端并行拉取现有代码（v6.0 新增）")
    print("5. 五端并行代码生成（基于现有项目规则）")
    print("6. 五端并行测试")
    print("7. 五端并行联调测试（v7.0 新增）")
    print("8. 五端并行自动修复（v7.0 新增）")
    print("9. 五端并行推送到 GitHub（v5.0 新增）")
    print("10. 五端汇总")
    print("\n支持的平台：iOS、Android、鸿蒙、H5、小程序")
    print("\n推送目标仓库：")
    print("  - H5:   https://github.com/{owner}/{h5_repo}")
    print("  - iOS:  https://github.com/{owner}/{ios_repo}")
    print("  - Android: https://github.com/{owner}/{android_repo}")
    print("  - 鸿蒙: https://github.com/{owner}/{harmonyos_repo}")
    print("  - 小程序: https://github.com/{owner}/{miniprogram_repo}")
    print("\nv6.0 新增功能：")
    print("  - 在代码生成前拉取各平台现有代码")
    print("  - 分析各平台项目规则（结构、规范、组件、API、样式、测试、依赖、构建）")
    print("  - 确保生成的代码符合现有项目规范")
    print("\nv7.0 新增功能：")
    print("  - 五端并行联调测试（Mock 数据联调）")
    print("  - 自动检测代码问题（错误处理、加载状态、Mock 集成等）")
    print("  - 自动修复常见问题")
    print("  - 使用 LLM 辅助修复复杂问题")
    print("  - 生成详细的测试和修复报告")
