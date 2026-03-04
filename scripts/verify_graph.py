#!/usr/bin/env python3
"""
验证 graph.py 是否正确加载和编译
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("=" * 80)
print("验证 graph.py 加载状态")
print("=" * 80)

try:
    # 1. 检查文件是否存在
    graph_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'graphs', 'graph.py')
    print(f"\n1. 检查文件: {graph_file}")
    print(f"   文件存在: {os.path.exists(graph_file)}")
    print(f"   文件大小: {os.path.getsize(graph_file)} bytes")

    # 2. 读取文件内容
    with open(graph_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"\n2. 文件内容分析:")
        print(f"   文件行数: {len(content.splitlines())}")
        print(f"   是否包含'登录页面': {'登录页面' in content}")
        print(f"   是否包含'五端': {'五端' in content}")

    # 3. 检查节点导入
    print(f"\n3. 检查节点导入:")
    nodes_to_check = [
        'design_parse_node',
        'component_recognition_node',
        'ios_code_generation_node',
        'android_code_generation_node',
        'harmonyos_code_generation_node',
        'h5_code_generation_node',
        'miniprogram_code_generation_node',
        'integration_test_node',
        'integration_fix_node',
        'all_platforms_summary_node'
    ]
    for node in nodes_to_check:
        found = f'from graphs.nodes.{node.replace("_node", "_node")}' in content
        print(f"   {node}: {'✓' if found else '✗'}")

    # 4. 检查 add_node 调用
    print(f"\n4. 检查 add_node 调用:")
    add_node_count = content.count('builder.add_node')
    print(f"   add_node 调用次数: {add_node_count}")

    # 5. 尝试加载图
    print(f"\n5. 尝试加载图:")
    from graphs.graph import main_graph

    print(f"   图加载成功: ✓")
    print(f"   图类型: {type(main_graph).__name__}")

    # 6. 统计节点
    nodes = list(main_graph.nodes)
    print(f"\n6. 节点统计:")
    print(f"   节点总数: {len(nodes)}")

    # 排除内部节点
    user_nodes = [n for n in nodes if not n.startswith('__')]
    print(f"   用户节点数: {len(user_nodes)}")

    # 7. 显示前20个节点
    print(f"\n7. 前20个节点:")
    for i, node in enumerate(user_nodes[:20], 1):
        print(f"   {i:2}. {node}")

    # 8. 检查关键节点是否存在
    print(f"\n8. 检查关键节点:")
    key_nodes = [
        'design_parse',
        'component_recognition',
        'ios_code_generation',
        'android_code_generation',
        'harmonyos_code_generation',
        'h5_code_generation',
        'miniprogram_code_generation',
        'ios_git_push',
        'android_git_push',
        'all_platforms_summary'
    ]
    for node in key_nodes:
        exists = node in nodes
        print(f"   {node}: {'✓' if exists else '✗'}")

    # 9. 结论
    print(f"\n{'=' * 80}")
    print("验证结论:")
    print(f"{'=' * 80}")

    if len(user_nodes) >= 30:
        print("✅ graph.py 加载成功，包含完整的五端工作流（{0}个节点）".format(len(user_nodes)))
    elif len(user_nodes) >= 10:
        print("⚠️  graph.py 加载成功，但节点数量较少（{0}个节点），可能不是完整版本".format(len(user_nodes)))
    else:
        print("❌ graph.py 加载失败或节点数量异常（{0}个节点）".format(len(user_nodes)))

    print("\n如果平台显示的工作流与本地验证结果不一致，")
    print("请参考 docs/CACHE_ISSUE_SOLUTION.md 解决缓存问题。")

except Exception as e:
    print(f"\n❌ 验证失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
