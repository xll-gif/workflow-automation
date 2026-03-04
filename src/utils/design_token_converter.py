"""
设计令牌工具类 - 用于将统一的设计令牌转换为各平台的特定格式
"""
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

# 设置日志
import logging
logger = logging.getLogger(__name__)


class DesignTokenConverter:
    """设计令牌转换器"""

    def __init__(self, tokens_file: Optional[str] = None):
        """
        初始化设计令牌转换器

        Args:
            tokens_file: 设计令牌配置文件路径（默认：config/design_tokens.json）
        """
        if tokens_file is None:
            # 默认路径
            project_root = os.getenv("COZE_WORKSPACE_PATH")
            tokens_file = os.path.join(project_root, "config/design_tokens.json")

        self.tokens_file = tokens_file
        self.tokens = self._load_tokens()

        logger.info(f"DesignTokenConverter initialized with tokens from: {tokens_file}")

    def _load_tokens(self) -> Dict[str, Any]:
        """加载设计令牌配置"""
        try:
            with open(self.tokens_file, 'r', encoding='utf-8') as f:
                tokens = json.load(f)
            logger.info(f"Design tokens loaded successfully")
            return tokens
        except Exception as e:
            logger.error(f"Failed to load design tokens: {e}")
            return {}

    def get_color(self, color_path: str, platform: str) -> str:
        """
        获取指定平台的颜色值

        Args:
            color_path: 颜色路径（如 "primary.default", "text.primary"）
            platform: 平台名称（ios, android, harmonyos, h5, miniprogram）

        Returns:
            平台特定的颜色值
        """
        # 解析路径
        parts = color_path.split(".")
        value = self.tokens.get("tokens", {}).get("colors", {})

        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return color_path  # 返回原始值

        if not value or not isinstance(value, str):
            return color_path

        # 根据平台转换
        return self._convert_color(value, platform)

    def _convert_color(self, hex_color: str, platform: str) -> str:
        """
        转换颜色为平台特定格式

        Args:
            hex_color: 十六进制颜色（如 #1890ff）
            platform: 平台名称

        Returns:
            平台特定的颜色值
        """
        # 移除 # 前缀
        hex_value = hex_color.lstrip("#")

        if len(hex_value) == 6:
            r = hex_value[0:2]
            g = hex_value[2:4]
            b = hex_value[4:6]

            if platform == "ios":
                # iOS: Color(hex: "#1890ff")
                return f'Color(hex: "#{hex_value}")'
            elif platform == "android":
                # Android: Color(0xFF1890FF)
                return f"Color(0xFF{r.upper()}{g.upper()}{b.upper()})"
            elif platform == "harmonyos":
                # 鸿蒙: "#1890ff"
                return f'"#{hex_value}"'
            elif platform == "h5" or platform == "miniprogram":
                # H5/小程序: #1890ff
                return f"#{hex_value}"
            else:
                return hex_color

        elif len(hex_value) == 8:
            # ARGB 格式
            a = hex_value[0:2]
            r = hex_value[2:4]
            g = hex_value[4:6]
            b = hex_value[6:8]

            if platform == "ios":
                # iOS: Color(hex: "#FF1890ff")
                return f'Color(hex: "#{hex_value}")'
            elif platform == "android":
                # Android: Color(0xFF1890FF) - 不使用 alpha
                return f"Color(0xFF{r.upper()}{g.upper()}{b.upper()})"
            elif platform == "harmonyos":
                # 鸿蒙: "#1890ff" - 不使用 alpha
                return f'"#{r}{g}{b}"'
            elif platform == "h5" or platform == "miniprogram":
                # H5/小程序: #1890ff - 不使用 alpha
                return f"#{r}{g}{b}"
            else:
                return hex_color

        return hex_color

    def get_spacing(self, spacing_name: str, platform: str) -> str:
        """
        获取指定平台的间距值

        Args:
            spacing_name: 间距名称（如 "sm", "md", "lg"）
            platform: 平台名称

        Returns:
            平台特定的间距值（带单位）
        """
        spacing_value = self.tokens.get("tokens", {}).get("spacing", {}).get(spacing_name)

        if spacing_value is None:
            return f"{spacing_name}"  # 返回原始名称

        # 根据平台添加单位
        unit_map = {
            "ios": "pt",
            "android": "dp",
            "harmonyos": "vp",
            "h5": "px",
            "miniprogram": "rpx"
        }

        unit = unit_map.get(platform, "px")
        return f"{spacing_value}{unit}"

    def get_font_size(self, size_name: str, platform: str) -> str:
        """
        获取指定平台的字体大小值

        Args:
            size_name: 字体大小名称（如 "sm", "md", "lg"）
            platform: 平台名称

        Returns:
            平台特定的字体大小值（带单位）
        """
        font_size_value = self.tokens.get("tokens", {}).get("fontSize", {}).get(size_name)

        if font_size_value is None:
            return f"{size_name}"  # 返回原始名称

        # 根据平台添加单位
        unit_map = {
            "ios": "pt",
            "android": "sp",
            "harmonyos": "vp",
            "h5": "px",
            "miniprogram": "rpx"
        }

        unit = unit_map.get(platform, "px")
        return f"{font_size_value}{unit}"

    def get_border_radius(self, radius_name: str, platform: str) -> str:
        """
        获取指定平台的圆角值

        Args:
            radius_name: 圆角名称（如 "sm", "md", "lg"）
            platform: 平台名称

        Returns:
            平台特定的圆角值（带单位）
        """
        radius_value = self.tokens.get("tokens", {}).get("borderRadius", {}).get(radius_name)

        if radius_value is None:
            return f"{radius_name}"  # 返回原始名称

        # 根据平台添加单位
        unit_map = {
            "ios": "pt",
            "android": "dp",
            "harmonyos": "vp",
            "h5": "px",
            "miniprogram": "rpx"
        }

        unit = unit_map.get(platform, "px")

        if radius_value >= 1000:
            # 圆角
            if platform == "ios":
                return "CornerSize.infinity"
            elif platform == "android":
                return "9999dp"
            elif platform == "harmonyos":
                return "9999vp"
            elif platform == "h5" or platform == "miniprogram":
                return "9999rpx"
            else:
                return "9999px"

        return f"{radius_value}{unit}"

    def get_component_token(self, component: str, token_path: str, platform: str) -> Any:
        """
        获取组件特定的令牌值

        Args:
            component: 组件名称（如 "button", "input"）
            token_path: 令牌路径（如 "height.md", "padding.horizontal"）
            platform: 平台名称

        Returns:
            组件令牌值
        """
        parts = token_path.split(".")
        value = self.tokens.get("components", {}).get(component, {})

        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return None

        if value is None:
            return None

        # 根据类型处理
        if isinstance(value, str):
            if value in ["sm", "md", "lg", "xl", "xs", "xxl", "xxxl"]:
                # 引用其他令牌
                return self.get_spacing(value, platform)
            return value
        elif isinstance(value, (int, float)):
            # 添加单位
            unit_map = {
                "ios": "pt",
                "android": "dp",
                "harmonyos": "vp",
                "h5": "px",
                "miniprogram": "rpx"
            }
            unit = unit_map.get(platform, "px")
            return f"{value}{unit}"
        else:
            return value

    def get_all_tokens(self, platform: str) -> Dict[str, Any]:
        """
        获取指定平台的所有令牌

        Args:
            platform: 平台名称

        Returns:
            平台特定的所有令牌
        """
        result = {}

        # 转换所有颜色
        colors = self.tokens.get("tokens", {}).get("colors", {})
        result["colors"] = self._convert_color_dict(colors, platform)

        # 转换所有间距
        spacings = self.tokens.get("tokens", {}).get("spacing", {})
        result["spacing"] = {k: self.get_spacing(k, platform) for k in spacings.keys()}

        # 转换所有字体大小
        font_sizes = self.tokens.get("tokens", {}).get("fontSize", {})
        result["fontSize"] = {k: self.get_font_size(k, platform) for k in font_sizes.keys()}

        # 转换所有圆角
        border_radiuses = self.tokens.get("tokens", {}).get("borderRadius", {})
        result["borderRadius"] = {k: self.get_border_radius(k, platform) for k in border_radiuses.keys()}

        return result

    def _convert_color_dict(self, color_dict: Dict[str, Any], platform: str) -> Dict[str, Any]:
        """递归转换颜色字典"""
        result = {}
        for key, value in color_dict.items():
            if isinstance(value, dict):
                result[key] = self._convert_color_dict(value, platform)
            elif isinstance(value, str):
                result[key] = self._convert_color(value, platform)
            else:
                result[key] = value
        return result

    def generate_token_file(self, platform: str, output_file: str) -> None:
        """
        生成平台的令牌文件

        Args:
            platform: 平台名称
            output_file: 输出文件路径
        """
        tokens = self.get_all_tokens(platform)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tokens, f, indent=2, ensure_ascii=False)

        logger.info(f"Generated token file: {output_file}")


# 全局实例
_converter = None


def get_converter() -> DesignTokenConverter:
    """获取全局转换器实例"""
    global _converter
    if _converter is None:
        _converter = DesignTokenConverter()
    return _converter
