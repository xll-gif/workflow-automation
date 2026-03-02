from langgraph.graph import StateGraph, END
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)
from graphs.nodes.hello_world_node import hello_world_node
from graphs.nodes.requirement_analysis_node import requirement_analysis_node
from graphs.nodes.analyze_codebase_node import analyze_codebase_node
from graphs.nodes.code_gen_and_push_node import code_gen_and_push_node
from graphs.nodes.design_parse_node import design_parse_node
from graphs.nodes.mastergo_asset_upload_node import mastergo_asset_upload_node
from graphs.nodes.component_identify_node import component_identify_node
from graphs.nodes.h5_code_generation_node import h5_code_generation_node
from graphs.nodes.ios_code_generation_node import ios_code_generation_node
from graphs.nodes.android_code_generation_node import android_code_generation_node
from graphs.nodes.harmonyos_code_generation_node import harmonyos_code_generation_node
from graphs.nodes.miniprogram_code_generation_node import miniprogram_code_generation_node
from graphs.nodes.fetch_generated_code_node import fetch_generated_code_node

# 创建状态图，指定图的入参和出参
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("hello_world", hello_world_node)
builder.add_node("requirement_analysis", requirement_analysis_node)
builder.add_node("analyze_codebase", analyze_codebase_node)
builder.add_node("code_gen_and_push", code_gen_and_push_node)
builder.add_node("design_parse", design_parse_node)
builder.add_node("mastergo_asset_upload", mastergo_asset_upload_node)
builder.add_node("component_identify", component_identify_node, metadata={"type": "agent", "llm_cfg": "config/component_identify_cfg.json"})

# 添加五端代码生成节点（并行执行）
builder.add_node("h5_code_generation", h5_code_generation_node, metadata={"type": "agent", "llm_cfg": "config/h5_code_generation_cfg.json"})
builder.add_node("ios_code_generation", ios_code_generation_node, metadata={"type": "agent", "llm_cfg": "config/ios_code_generation_cfg.json"})
builder.add_node("android_code_generation", android_code_generation_node, metadata={"type": "agent", "llm_cfg": "config/android_code_generation_cfg.json"})
builder.add_node("harmonyos_code_generation", harmonyos_code_generation_node, metadata={"type": "agent", "llm_cfg": "config/harmonyos_code_generation_cfg.json"})
builder.add_node("miniprogram_code_generation", miniprogram_code_generation_node, metadata={"type": "agent", "llm_cfg": "config/miniprogram_code_generation_cfg.json"})

# 设置入口点 - 从需求分析开始
builder.set_entry_point("requirement_analysis")

# 添加边：从 requirement_analysis 到 design_parse
builder.add_edge("requirement_analysis", "design_parse")

# 添加边：从 design_parse 到 mastergo_asset_upload
builder.add_edge("design_parse", "mastergo_asset_upload")

# 添加边：从 mastergo_asset_upload 到 component_identify
builder.add_edge("mastergo_asset_upload", "component_identify")

# 添加边：从 component_identify 到五端代码生成节点（并行执行）
builder.add_edge("component_identify", "h5_code_generation")
builder.add_edge("component_identify", "ios_code_generation")
builder.add_edge("component_identify", "android_code_generation")
builder.add_edge("component_identify", "harmonyos_code_generation")
builder.add_edge("component_identify", "miniprogram_code_generation")

# 添加边：从五端代码生成节点到 fetch_generated_code（所有并行分支完成后）
builder.add_edge(["h5_code_generation", "ios_code_generation", "android_code_generation", "harmonyos_code_generation", "miniprogram_code_generation"], "fetch_generated_code")

# 添加边：从 fetch_generated_code 到 code_gen_and_push
builder.add_edge("fetch_generated_code", "code_gen_and_push")

# 添加边：从 code_gen_and_push 到 END
builder.add_edge("code_gen_and_push", END)

# 编译图
main_graph = builder.compile()

if __name__ == "__main__":
    # 测试运行
    print("开始测试完整工作流（包含 MasterGo 集成）...")
    print("=" * 80)

    # 创建测试输入 - 使用包含 MasterGo 设计稿的 GitHub Issue
    test_input = {
        "github_issue_url": "https://github.com/xll-gif/workflowDemo/issues/2"
    }

    print(f"输入参数: {test_input}")
    print("\n开始执行工作流...\n")

    # 运行工作流
    try:
        result = main_graph.invoke(test_input)

        # 打印结果
        print("\n" + "="*80)
        print("工作流执行结果:")
        print("="*80)
        print(f"功能列表: {result.get('feature_list', [])}")
        print(f"API 定义: {result.get('api_definitions', [])}")
        print(f"MasterGo URL: {result.get('mastergo_url', 'N/A')}")
        print(f"组件数量: {len(result.get('components', []))}")
        print(f"静态资源数量: {len(result.get('static_assets', []))}")
        print(f"\n需求摘要:\n{result.get('summary', '')}")
        print(f"\n设计稿摘要:\n{result.get('mastergo_summary', '')}")
        
        print("\n" + "="*80)
        print("五端代码生成结果:")
        print("="*80)
        print(f"H5 生成文件数: {len(result.get('h5_generated_files', []))}")
        print(f"iOS 生成文件数: {len(result.get('ios_generated_files', []))}")
        print(f"Android 生成文件数: {len(result.get('android_generated_files', []))}")
        print(f"鸿蒙生成文件数: {len(result.get('harmonyos_generated_files', []))}")
        print(f"小程序生成文件数: {len(result.get('miniprogram_generated_files', []))}")
        
        print(f"\nH5 摘要: {result.get('h5_generation_summary', 'N/A')}")
        print(f"iOS 摘要: {result.get('ios_generation_summary', 'N/A')}")
        print(f"Android 摘要: {result.get('android_generation_summary', 'N/A')}")
        print(f"鸿蒙摘要: {result.get('harmonyos_generation_summary', 'N/A')}")
        print(f"小程序摘要: {result.get('miniprogram_generation_summary', 'N/A')}")
        print("="*80)

    except Exception as e:
        print(f"\n❌ 工作流执行失败: {e}")
        import traceback
        traceback.print_exc()
