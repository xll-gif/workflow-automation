"""
仓库约束加载器

用于加载和管理各平台仓库的约束配置，确保代码生成节点生成的代码符合仓库规范。
"""

import os
import json
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field


class NamingConventions(BaseModel):
    """命名规范约束"""
    class_field: Optional[str] = Field(None, alias="class", description="类名命名规范")
    class_name: Optional[str] = Field(None, description="类名命名规范（备用）")
    method: str = Field(..., description="方法命名规范")
    variable: str = Field(..., description="变量命名规范")
    constant: str = Field(..., description="常量命名规范")
    file: str = Field(..., description="文件命名规范")
    enum_case: Optional[str] = Field(None, description="枚举命名规范")
    protocol: Optional[str] = Field(None, description="协议命名规范")
    composable: Optional[str] = Field(None, description="组件命名规范")
    viewmodel: Optional[str] = Field(None, description="ViewModel命名规范")
    interface: Optional[str] = Field(None, description="接口命名规范")

    model_config = {"populate_by_name": True}  # 允许使用别名填充字段


class ProjectStructure(BaseModel):
    """项目结构约束"""
    root_dirs: List[str] = Field(default_factory=list, description="根目录列表")
    source_dir: Optional[str] = Field(None, description="源代码目录")
    test_dir: Optional[str] = Field(None, description="测试目录")
    resource_dir: Optional[str] = Field(None, description="资源目录")
    public_dir: Optional[str] = Field(None, description="公共目录")
    pages_dir: Optional[str] = Field(None, description="页面目录")
    components_dir: Optional[str] = Field(None, description="组件目录")
    utils_dir: Optional[str] = Field(None, description="工具目录")
    api_dir: Optional[str] = Field(None, description="API目录")
    file_patterns: Dict[str, str] = Field(default_factory=dict, description="文件命名模式")


class CodeStyle(BaseModel):
    """代码风格约束"""
    indentation: str = Field(..., description="缩进方式")
    line_length: int = Field(..., description="单行最大长度")
    trailing_comma: Optional[Union[bool, str]] = Field(None, description="是否使用尾随逗号")
    sort_imports: Optional[bool] = Field(None, description="是否排序导入")
    max_blank_lines: Optional[int] = Field(None, description="最大空行数")
    import_ordering: Optional[str] = Field(None, description="导入排序方式")
    ktlint: Optional[bool] = Field(None, description="是否使用 ktlint")
    print_width: Optional[int] = Field(None, description="打印宽度")
    quotes: Optional[str] = Field(None, description="引号类型")
    semi: Optional[bool] = Field(None, description="是否使用分号")
    strict_type: Optional[bool] = Field(None, description="是否使用严格类型")
    eslint: Optional[bool] = Field(None, description="是否使用 eslint")
    access_control: Optional[str] = Field(None, description="访问控制")


class TechStack(BaseModel):
    """技术栈约束"""
    language: str = Field(..., description="编程语言")
    language_version: Optional[str] = Field(None, description="语言版本")
    framework: str = Field(..., description="主要框架")
    ui_library: Optional[str] = Field(None, description="UI库")
    build_tool: Optional[str] = Field(None, description="构建工具")
    minimum_version: Optional[str] = Field(None, description="最低版本要求")
    minimum_sdk: Optional[int] = Field(None, description="最低SDK版本")
    target_sdk: Optional[int] = Field(None, description="目标SDK版本")
    min_sdk: Optional[int] = Field(None, description="最低SDK（Android）")
    target_version: Optional[str] = Field(None, description="目标版本")
    dependencies: List[str] = Field(default_factory=list, description="依赖列表")
    dev_dependencies: Optional[List[str]] = Field(None, description="开发依赖列表")
    build_system: Optional[str] = Field(None, description="构建系统")
    package_manager: Optional[str] = Field(None, description="包管理器")


class StyleGuide(BaseModel):
    """样式指南约束"""
    colors: Dict[str, str] = Field(default_factory=dict, description="颜色配置")
    fonts: Dict[str, str] = Field(default_factory=dict, description="字体配置")
    spacing: Dict[str, Any] = Field(default_factory=dict, description="间距配置")
    border_radius: Dict[str, Any] = Field(default_factory=dict, description="圆角配置")


class APIIntegration(BaseModel):
    """API 集成约束"""
    base_url: str = Field(..., description="API 基础地址")
    timeout: int = Field(..., description="超时时间（秒）")
    retry_policy: Dict[str, Any] = Field(default_factory=dict, description="重试策略")
    error_handling: str = Field(..., description="错误处理方式")
    response_format: str = Field(..., description="响应格式")
    token_storage: str = Field(..., description="令牌存储方式")


class Testing(BaseModel):
    """测试约束"""
    framework: Optional[str] = Field(None, description="测试框架")
    unit_framework: Optional[str] = Field(None, description="单元测试框架")
    ui_framework: Optional[str] = Field(None, description="UI测试框架")
    async_framework: Optional[str] = Field(None, description="异步测试框架")
    e2e_framework: Optional[str] = Field(None, description="端到端测试框架")
    test_dir: Optional[str] = Field(None, description="测试目录")
    ui_test_dir: Optional[str] = Field(None, description="UI测试目录")
    naming_pattern: Optional[str] = Field(None, description="测试文件命名模式")
    min_coverage: int = Field(default=80, description="最小代码覆盖率")
    mock_framework: Optional[str] = Field(None, description="Mock框架")
    assertion_library: Optional[str] = Field(None, description="断言库")


class RepositoryConstraints(BaseModel):
    """仓库约束配置"""
    platform: str = Field(..., description="平台标识")
    name: str = Field(..., description="仓库名称")
    repository: str = Field(..., description="仓库标识")
    version: str = Field(..., description="版本号")
    project_structure: ProjectStructure = Field(..., description="项目结构")
    naming_conventions: NamingConventions = Field(..., description="命名规范")
    code_style: CodeStyle = Field(..., description="代码风格")
    tech_stack: TechStack = Field(..., description="技术栈")
    component_mapping: Dict[str, str] = Field(default_factory=dict, description="组件映射")
    style_guide: StyleGuide = Field(..., description="样式指南")
    api_integration: APIIntegration = Field(..., description="API 集成")
    testing: Testing = Field(default_factory=Testing, description="测试配置")
    best_practices: Union[List[str], Dict[str, Any]] = Field(default_factory=list, description="最佳实践")
    forbidden_patterns: List[str] = Field(default_factory=list, description="禁止模式")
    browser_support: Optional[Dict[str, str]] = Field(None, description="浏览器支持")
    platform_specific: Optional[Dict[str, Any]] = Field(None, description="平台特定配置")
    compatibility: Optional[Dict[str, Any]] = Field(None, description="兼容性配置")
    performance: Optional[Dict[str, Any]] = Field(None, description="性能配置")


class ConstraintLoader:
    """约束加载器"""

    SUPPORTED_PLATFORMS = ["ios", "android", "harmonyos", "h5", "miniprogram"]
    CONSTRAINTS_DIR = "config/constraints"

    def __init__(self, workspace_path: Optional[str] = None):
        """
        初始化约束加载器

        Args:
            workspace_path: 工作区路径，默认使用环境变量 COZE_WORKSPACE_PATH
        """
        self.workspace_path = workspace_path or os.getenv("COZE_WORKSPACE_PATH", "")
        self._cache: Dict[str, RepositoryConstraints] = {}

    def _get_constraint_path(self, platform: str) -> str:
        """
        获取约束配置文件路径

        Args:
            platform: 平台标识

        Returns:
            约束配置文件的绝对路径

        Raises:
            ValueError: 平台不支持时抛出
        """
        if platform not in self.SUPPORTED_PLATFORMS:
            raise ValueError(
                f"不支持的平台: {platform}. 支持的平台: {', '.join(self.SUPPORTED_PLATFORMS)}"
            )

        return os.path.join(
            self.workspace_path,
            self.CONSTRAINTS_DIR,
            f"{platform}.json"
        )

    def load(self, platform: str, use_cache: bool = True) -> RepositoryConstraints:
        """
        加载平台仓库约束配置

        Args:
            platform: 平台标识
            use_cache: 是否使用缓存

        Returns:
            RepositoryConstraints 实例

        Raises:
            FileNotFoundError: 配置文件不存在时抛出
            ValueError: 配置文件格式错误时抛出
        """
        # 检查缓存
        if use_cache and platform in self._cache:
            return self._cache[platform]

        # 获取配置文件路径
        constraint_path = self._get_constraint_path(platform)

        # 检查文件是否存在
        if not os.path.exists(constraint_path):
            raise FileNotFoundError(
                f"约束配置文件不存在: {constraint_path}"
            )

        # 读取配置文件
        try:
            with open(constraint_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"约束配置文件格式错误: {e}")
        except Exception as e:
            raise RuntimeError(f"读取约束配置文件失败: {e}")

        # 解析配置
        try:
            constraints = RepositoryConstraints(**config_data)
        except Exception as e:
            raise ValueError(f"约束配置解析失败: {e}")

        # 缓存结果
        if use_cache:
            self._cache[platform] = constraints

        return constraints

    def load_all(self) -> Dict[str, RepositoryConstraints]:
        """
        加载所有平台的约束配置

        Returns:
            平台标识到 RepositoryConstraints 的映射字典
        """
        all_constraints = {}
        for platform in self.SUPPORTED_PLATFORMS:
            try:
                all_constraints[platform] = self.load(platform)
            except Exception as e:
                # 记录错误但继续加载其他平台
                print(f"加载 {platform} 约束失败: {e}")

        return all_constraints

    def apply_naming_convention(
        self,
        name: str,
        convention_type: str,
        platform: str
    ) -> str:
        """
        应用命名规范

        Args:
            name: 原始名称
            convention_type: 命名类型 (class, method, variable, constant, file)
            platform: 平台标识

        Returns:
            符合命名规范的名称
        """
        constraints = self.load(platform)
        convention = constraints.naming_conventions

        # 获取命名规范（尝试多种字段名）
        naming_rule = None
        if hasattr(convention, convention_type):
            naming_rule = getattr(convention, convention_type)
        elif convention_type == "class":
            # 优先使用 class_field，然后使用 class_name
            naming_rule = convention.class_field or convention.class_name
        elif convention_type == "constant":
            naming_rule = getattr(convention, "constant", None)

        if not naming_rule:
            return name

        # 应用命名规范（简化版，实际可以使用命名转换库）
        if naming_rule == "PascalCase":
            return self._to_pascal_case(name)
        elif naming_rule == "camelCase":
            return self._to_camel_case(name)
        elif naming_rule == "UPPER_SNAKE_CASE":
            return self._to_upper_snake_case(name)
        elif naming_rule == "lowercase with hyphens":
            return self._to_kebab_case(name)
        else:
            return name

    def _to_pascal_case(self, name: str) -> str:
        """转换为 PascalCase"""
        components = name.replace("-", " ").replace("_", " ").split()
        return "".join(word.capitalize() for word in components)

    def _to_camel_case(self, name: str) -> str:
        """转换为 camelCase"""
        pascal = self._to_pascal_case(name)
        return pascal[0].lower() + pascal[1:] if pascal else ""

    def _to_upper_snake_case(self, name: str) -> str:
        """转换为 UPPER_SNAKE_CASE"""
        return name.replace("-", "_").replace(" ", "_").upper()

    def _to_kebab_case(self, name: str) -> str:
        """转换为 kebab-case"""
        # 首先将驼峰命名转换为下划线命名
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1)
        # 然后将下划线替换为连字符，并转换为小写
        return s2.replace("_", "-").lower()

    def generate_file_path(
        self,
        platform: str,
        file_type: str,
        feature_name: str
    ) -> str:
        """
        生成文件路径

        Args:
            platform: 平台标识
            file_type: 文件类型 (view, view_model, api 等)
            feature_name: 功能名称

        Returns:
            文件路径
        """
        constraints = self.load(platform)
        structure = constraints.project_structure

        # 获取文件命名模式
        pattern = structure.file_patterns.get(file_type, "{feature_name}.{ext}")

        # 生成文件名
        filename = pattern.replace("{FeatureName}", self._to_pascal_case(feature_name))
        filename = filename.replace("{featureName}", self._to_camel_case(feature_name))

        # 处理扩展名
        if "{ext}" in filename:
            # 根据平台确定扩展名
            ext_map = {
                "ios": "swift",
                "android": "kt",
                "harmonyos": "ets",
                "h5": "vue",
                "miniprogram": "js"
            }
            ext = ext_map.get(platform, "js")
            filename = filename.replace("{ext}", ext)

        # 生成完整路径
        source_dir = structure.source_dir or ""
        if source_dir:
            return os.path.join(source_dir, filename)
        else:
            return filename

    def get_component_mapping(
        self,
        platform: str,
        component_name: str
    ) -> Optional[str]:
        """
        获取组件映射

        Args:
            platform: 平台标识
            component_name: 组件名称

        Returns:
            映射后的组件路径，如果不支持则返回 None
        """
        constraints = self.load(platform)
        return constraints.component_mapping.get(component_name)

    def get_style_value(
        self,
        platform: str,
        style_type: str,
        key: str
    ) -> Optional[Any]:
        """
        获取样式值

        Args:
            platform: 平台标识
            style_type: 样式类型 (colors, fonts, spacing, border_radius)
            key: 样式键

        Returns:
            样式值，如果不存在则返回 None
        """
        constraints = self.load(platform)
        style_guide = constraints.style_guide

        style_dict = getattr(style_guide, style_type, None)
        if not style_dict:
            return None

        return style_dict.get(key)

    def validate_code_style(
        self,
        platform: str,
        code: str
    ) -> Dict[str, Any]:
        """
        验证代码风格（简化版）

        Args:
            platform: 平台标识
            code: 代码内容

        Returns:
            验证结果字典，包含 errors 和 warnings
        """
        constraints = self.load(platform)
        style = constraints.code_style

        errors = []
        warnings = []

        # 检查行长度
        lines = code.split("\n")
        for i, line in enumerate(lines, 1):
            if len(line) > style.line_length:
                warnings.append(
                    f"Line {i}: 超过最大行长度 {style.line_length} (当前: {len(line)})"
                )

        # 检查缩进（简化）
        if style.indentation == "4 spaces":
            for i, line in enumerate(lines, 1):
                if line.startswith(" ") and not line.startswith("    "):
                    errors.append(f"Line {i}: 缩进应为 4 个空格")
        elif style.indentation == "2 spaces":
            for i, line in enumerate(lines, 1):
                if line.startswith("  ") and not line.startswith("  "):
                    errors.append(f"Line {i}: 缩进应为 2 个空格")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }


# 全局单例
_loader_instance: Optional[ConstraintLoader] = None


def get_constraint_loader(workspace_path: Optional[str] = None) -> ConstraintLoader:
    """
    获取约束加载器单例

    Args:
        workspace_path: 工作区路径

    Returns:
        ConstraintLoader 实例
    """
    global _loader_instance

    if _loader_instance is None:
        _loader_instance = ConstraintLoader(workspace_path)

    return _loader_instance
