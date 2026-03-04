"""
生成各平台的设计令牌文件（修复版）
"""
import os
import sys
import json

# 获取项目根目录
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# 添加项目根目录到 Python 路径
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

# 设置工作空间环境变量
os.environ['COZE_WORKSPACE_PATH'] = project_root

from src.utils.design_token_converter import DesignTokenConverter

print("=" * 80)
print("生成各平台设计令牌文件")
print("=" * 80)
print(f"项目根目录: {project_root}")
print(f"设计令牌文件: {project_root}/config/design_tokens.json")

# 创建转换器
converter = DesignTokenConverter()

# 定义各平台
platforms = ["ios", "android", "harmonyos", "h5", "miniprogram"]

# 生成令牌文件
for platform in platforms:
    print(f"\n生成 {platform} 平台令牌文件...")

    # 输出文件路径
    output_file = os.path.join(project_root, "config", "tokens", f"{platform}_tokens.json")

    # 确保目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # 生成文件
    converter.generate_token_file(platform, output_file)

    print(f"   ✅ 已生成: {output_file}")

print("\n" + "=" * 80)
print("所有平台令牌文件生成完成！")
print("=" * 80)

# 展示示例
print("\n📊 颜色转换示例：")
print("-" * 40)
for platform in platforms:  # 展示所有平台
    print(f"\n{platform}:")
    print(f"  primary.default: {converter.get_color('primary.default', platform)}")
    print(f"  text.primary:    {converter.get_color('text.primary', platform)}")
    print(f"  error.default:   {converter.get_color('error.default', platform)}")

print("\n📊 间距转换示例：")
print("-" * 40)
for platform in platforms:
    print(f"\n{platform}:")
    print(f"  sm: {converter.get_spacing('sm', platform)}")
    print(f"  md: {converter.get_spacing('md', platform)}")
    print(f"  lg: {converter.get_spacing('lg', platform)}")

print("\n📊 字体大小示例：")
print("-" * 40)
for platform in platforms:
    print(f"\n{platform}:")
    print(f"  sm: {converter.get_font_size('sm', platform)}")
    print(f"  md: {converter.get_font_size('md', platform)}")
    print(f"  lg: {converter.get_font_size('lg', platform)}")

print("\n📊 圆角示例：")
print("-" * 40)
for platform in platforms:
    print(f"\n{platform}:")
    print(f"  sm: {converter.get_border_radius('sm', platform)}")
    print(f"  md: {converter.get_border_radius('md', platform)}")
    print(f"  lg: {converter.get_border_radius('lg', platform)}")

print("\n📊 组件令牌示例：")
print("-" * 40)
for platform in platforms:
    print(f"\n{platform}:")
    print(f"  button.height.md: {converter.get_component_token('button', 'height.md', platform)}")
    print(f"  input.height.md:  {converter.get_component_token('input', 'height.md', platform)}")
    print(f"  logo.width:       {converter.get_component_token('logo', 'width', platform)}")
