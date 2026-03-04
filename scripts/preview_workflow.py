#!/usr/bin/env python3
"""
工作流预览脚本

显示当前工作流的节点列表、连接关系和执行流程
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from graphs.graph import main_graph
from graphs.state import GlobalState

def print_header(title):
    """打印标题"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def print_nodes():
    """打印所有节点"""
    print_header("📋 工作流节点列表")

    # 获取所有节点（排除内部节点）
    nodes = []
    for node in main_graph.nodes:
        if not node.startswith("__"):
            nodes.append(node)

    print(f"节点总数: {len(nodes)}\n")

    for i, node_name in enumerate(nodes, 1):
        print(f"{i:2}. {node_name}")

    print()

def print_workflow_flow():
    """打印工作流流程"""
    print_header("🚀 工作流执行流程")

    # 打印主要流程
    print("主要执行流程:")
    print("-" * 80)

    workflow_steps = [
        "1. 设计稿解析 (design_parse)",
        "2. 资源处理 (asset_processing)",
        "3. 组件识别 (component_recognition)",
        "4. 五端并行拉取现有代码 (pull_*_code)",
        "   ├─ iOS 代码拉取",
        "   ├─ Android 代码拉取",
        "   ├─ 鸿蒙代码拉取",
        "   ├─ H5 代码拉取",
        "   └─ 小程序代码拉取",
        "5. 五端并行代码生成 (*_code_generation)",
        "   ├─ iOS 代码生成 (SwiftUI)",
        "   ├─ Android 代码生成 (Jetpack Compose)",
        "   ├─ 鸿蒙代码生成 (ArkUI)",
        "   ├─ H5 代码生成 (React + TypeScript)",
        "   └─ 小程序代码生成 (原生小程序)",
        "6. 五端并行测试验证 (*_testing)",
        "7. 五端并行联调测试 (*_integration_test)",
        "8. 五端并行自动修复 (*_integration_fix)",
        "9. 五端并行推送到 GitHub (*_git_push)",
        "10. 五端汇总 (all_platforms_summary)"
    ]

    for step in workflow_steps:
        print(step)

    print("-" * 80 + "\n")

def print_parallel_branches():
    """打印并行分支"""
    print_header("⚡ 并行执行分支")

    parallel_branches = {
        "iOS 分支": [
            "pull_ios_code",
            "ios_code_generation",
            "ios_testing",
            "ios_integration_test",
            "ios_integration_fix",
            "ios_git_push"
        ],
        "Android 分支": [
            "pull_android_code",
            "android_code_generation",
            "android_testing",
            "android_integration_test",
            "android_integration_fix",
            "android_git_push"
        ],
        "鸿蒙分支": [
            "pull_harmonyos_code",
            "harmonyos_code_generation",
            "harmonyos_testing",
            "harmonyos_integration_test",
            "harmonyos_integration_fix",
            "harmonyos_git_push"
        ],
        "H5 分支": [
            "pull_h5_code",
            "h5_code_generation",
            "h5_testing",
            "h5_integration_test",
            "h5_integration_fix",
            "h5_git_push"
        ],
        "小程序分支": [
            "pull_miniprogram_code",
            "miniprogram_code_generation",
            "miniprogram_testing",
            "miniprogram_integration_test",
            "miniprogram_integration_fix",
            "miniprogram_git_push"
        ]
    }

    for branch_name, nodes in parallel_branches.items():
        print(f"{branch_name}:")
        for i, node in enumerate(nodes, 1):
            print(f"  {i}. {node}")
        print()

def print_input_output():
    """打印输入输出"""
    print_header("📥📤 工作流输入输出")

    # 打印输入
    print("工作流输入 (GraphInput):")
    print("-" * 40)
    input_fields = [
        ("repo_owner", "GitHub 仓库所有者"),
        ("ios_repo_name", "iOS 仓库名称"),
        ("android_repo_name", "Android 仓库名称"),
        ("harmonyos_repo_name", "鸿蒙仓库名称"),
        ("h5_repo_name", "H5 仓库名称"),
        ("miniprogram_repo_name", "小程序仓库名称"),
        ("mastergo_url", "MasterGo 设计稿 URL")
    ]

    for field, description in input_fields:
        print(f"  • {field}: {description}")

    print()

    # 打印输出
    print("工作流输出 (GraphOutput):")
    print("-" * 40)
    output_fields = [
        ("ios_generated_files", "iOS 生成的文件列表"),
        ("android_generated_files", "Android 生成的文件列表"),
        ("harmonyos_generated_files", "鸿蒙生成的文件列表"),
        ("h5_generated_files", "H5 生成的文件列表"),
        ("miniprogram_generated_files", "小程序生成的文件列表"),
        ("ios_commit_url", "iOS 提交 URL"),
        ("android_commit_url", "Android 提交 URL"),
        ("harmonyos_commit_url", "鸿蒙提交 URL"),
        ("h5_commit_url", "H5 提交 URL"),
        ("miniprogram_commit_url", "小程序提交 URL"),
        ("summary", "五端汇总结果")
    ]

    for field, description in output_fields:
        print(f"  • {field}: {description}")

    print()

def print_mermaid():
    """打印 Mermaid 格式（用于在 Markdown 中渲染流程图）"""
    print_header("🎨 Mermaid 格式（用于在 Markdown 中渲染流程图）")

    print("```mermaid")
    print("graph TD")
    print("    Start((开始)) --> design_parse[设计稿解析]")
    print("    design_parse --> asset_processing[资源处理]")
    print("    asset_processing --> component_recognition{组件识别}")
    print()
    print("    %% 五端并行拉取代码")
    print("    component_recognition --> |iOS| pull_ios[拉取 iOS 代码]")
    print("    component_recognition --> |Android| pull_android[拉取 Android 代码]")
    print("    component_recognition --> |鸿蒙| pull_harmonyos[拉取鸿蒙代码]")
    print("    component_recognition --> |H5| pull_h5[拉取 H5 代码]")
    print("    component_recognition --> |小程序| pull_miniprogram[拉取小程序代码]")
    print()
    print("    %% 五端并行生成代码")
    print("    pull_ios --> ios_gen[iOS 代码生成]")
    print("    pull_android --> android_gen[Android 代码生成]")
    print("    pull_harmonyos --> harmonyos_gen[鸿蒙代码生成]")
    print("    pull_h5 --> h5_gen[H5 代码生成]")
    print("    pull_miniprogram --> miniprogram_gen[小程序代码生成]")
    print()
    print("    %% 五端并行测试")
    print("    ios_gen --> ios_test[iOS 测试验证]")
    print("    android_gen --> android_test[Android 测试验证]")
    print("    harmonyos_gen --> harmonyos_test[鸿蒙测试验证]")
    print("    h5_gen --> h5_test[H5 测试验证]")
    print("    miniprogram_gen --> miniprogram_test[小程序测试验证]")
    print()
    print("    %% 五端并行联调测试")
    print("    ios_test --> ios_itest[iOS 联调测试]")
    print("    android_test --> android_itest[Android 联调测试]")
    print("    harmonyos_test --> harmonyos_itest[鸿蒙联调测试]")
    print("    h5_test --> h5_itest[H5 联调测试]")
    print("    miniprogram_test --> miniprogram_itest[小程序联调测试]")
    print()
    print("    %% 五端并行自动修复")
    print("    ios_itest --> ios_fix[iOS 自动修复]")
    print("    android_itest --> android_fix[Android 自动修复]")
    print("    harmonyos_itest --> harmonyos_fix[鸿蒙自动修复]")
    print("    h5_itest --> h5_fix[H5 自动修复]")
    print("    miniprogram_itest --> miniprogram_fix[小程序自动修复]")
    print()
    print("    %% 五端并行推送")
    print("    ios_fix --> ios_push[iOS Git 推送]")
    print("    android_fix --> android_push[Android Git 推送]")
    print("    harmonyos_fix --> harmonyos_push[鸿蒙 Git 推送]")
    print("    h5_fix --> h5_push[H5 Git 推送]")
    print("    miniprogram_fix --> miniprogram_push[小程序 Git 推送]")
    print()
    print("    %% 汇总结果")
    print("    ios_push --> summary[五端汇总]")
    print("    android_push --> summary")
    print("    harmonyos_push --> summary")
    print("    h5_push --> summary")
    print("    miniprogram_push --> summary")
    print("    summary --> End((结束))")
    print()
    print("    %% 样式定义")
    print("    classDef primaryNode fill:#e1f5ff,stroke:#0288d1,stroke-width:2px;")
    print("    classDef parallelNode fill:#fff3e0,stroke:#f57c00,stroke-width:2px;")
    print("    classDef agentNode fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;")
    print("    classDef taskNode fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;")
    print("    classDef startEnd fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px,stroke-dasharray: 5 5;")
    print()
    print("    class design_parse,asset_processing,component_recognition primaryNode;")
    print("    class pull_ios,pull_android,pull_harmonyos,pull_h5,pull_miniprogram parallelNode;")
    print("    class ios_gen,android_gen,harmonyos_gen,h5_gen,miniprogram_gen agentNode;")
    print("    class ios_test,android_test,harmonyos_test,h5_test,miniprogram_test taskNode;")
    print("    class ios_itest,android_itest,harmonyos_itest,h5_itest,miniprogram_itest taskNode;")
    print("    class ios_fix,android_fix,harmonyos_fix,h5_fix,miniprogram_fix taskNode;")
    print("    class ios_push,android_push,harmonyos_push,h5_push,miniprogram_push taskNode;")
    print("    class summary primaryNode;")
    print("    class Start,End startEnd;")
    print("```")
    print()
    print("提示: 您可以将上述代码复制到 Markdown 文件中，在 GitHub、GitLab 等平台会自动渲染成流程图。")
    print()

def main():
    """主函数"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "🔍 工作流预览工具" + " " * 30 + "║")
    print("║" + " " * 10 + "登录页面完整开发工作流 - 五端代码自动化生成" + " " * 10 + "║")
    print("╚" + "=" * 78 + "╝")

    try:
        # 打印各个部分
        print_nodes()
        print_workflow_flow()
        print_parallel_branches()
        print_input_output()
        print_mermaid()

        print_header("✅ 预览完成")

        print("其他预览方式：")
        print("  1. 查看文档: AGENTS.md")
        print("  2. 查看文档: README.md")
        print("  3. 启动 HTTP 服务并访问 /graph_parameter 端点")
        print()

    except Exception as e:
        print(f"\n❌ 预览失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
