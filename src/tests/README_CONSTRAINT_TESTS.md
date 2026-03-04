# 仓库约束配置系统测试说明

## 测试概述

本目录包含仓库约束配置系统的测试用例，用于验证约束加载器的各项功能。

## 测试文件

- `test_constraint_loader.py` - 约束加载器测试用例

## 运行测试

### 方法 1: 使用 Python unittest

```bash
cd workflow-automation
python -m pytest src/tests/test_constraint_loader.py -v
```

或者使用 unittest：

```bash
cd workflow-automation
python -m unittest src.tests.test_constraint_loader -v
```

### 方法 2: 使用 pytest（推荐）

```bash
cd workflow-automation
pytest src/tests/test_constraint_loader.py -v
```

## 测试覆盖率

运行测试并生成覆盖率报告：

```bash
cd workflow-automation
pytest src/tests/test_constraint_loader.py --cov=src/utils/constraint_loader --cov-report=html
```

覆盖率报告将生成在 `htmlcov/` 目录中，使用浏览器打开 `htmlcov/index.html` 查看详细报告。

## 测试用例说明

### TestConstraintLoader 类

主要测试约束加载器的功能：

1. **加载约束配置测试**
   - `test_load_ios_constraints` - 测试加载 iOS 约束
   - `test_load_android_constraints` - 测试加载 Android 约束
   - `test_load_harmonyos_constraints` - 测试加载鸿蒙约束
   - `test_load_h5_constraints` - 测试加载 H5 约束
   - `test_load_miniprogram_constraints` - 测试加载小程序约束
   - `test_load_unsupported_platform` - 测试加载不支持的平台

2. **缓存功能测试**
   - `test_load_cache` - 测试缓存功能
   - `test_load_without_cache` - 测试不使用缓存

3. **命名规范测试**
   - `test_apply_naming_convention_pascal_case` - 测试 PascalCase 转换
   - `test_apply_naming_convention_camel_case` - 测试 camelCase 转换
   - `test_apply_naming_convention_upper_snake_case` - 测试 UPPER_SNAKE_CASE 转换
   - `test_apply_naming_convention_kebab_case` - 测试 kebab-case 转换

4. **文件路径生成测试**
   - `test_generate_file_path_ios_view` - 测试生成 iOS View 文件路径
   - `test_generate_file_path_android_view_model` - 测试生成 Android ViewModel 文件路径
   - `test_generate_file_path_h5_page` - 测试生成 H5 Page 文件路径

5. **组件映射测试**
   - `test_get_component_mapping` - 测试获取组件映射

6. **样式值测试**
   - `test_get_style_value_colors` - 测试获取颜色值
   - `test_get_style_value_spacing` - 测试获取间距值

7. **代码风格验证测试**
   - `test_validate_code_style_valid_code` - 测试验证有效代码
   - `test_validate_code_style_invalid_code` - 测试验证无效代码

8. **批量加载测试**
   - `test_load_all_platforms` - 测试加载所有平台

9. **单例模式测试**
   - `test_get_constraint_loader_singleton` - 测试获取约束加载器单例

### TestNamingConversions 类

测试命名转换功能：

1. `test_to_pascal_case` - 测试 PascalCase 转换
2. `test_to_camel_case` - 测试 camelCase 转换
3. `test_to_upper_snake_case` - 测试 UPPER_SNAKE_CASE 转换
4. `test_to_kebab_case` - 测试 kebab-case 转换

## 测试数据

测试数据使用项目中的实际配置文件：

- `config/constraints/ios.json`
- `config/constraints/android.json`
- `config/constraints/harmonyos.json`
- `config/constraints/h5.json`
- `config/constraints/miniprogram.json`

## 预期结果

所有测试用例应该通过，预期结果如下：

```
test_load_android_constraints ... ok
test_load_h5_constraints ... ok
test_load_harmonyos_constraints ... ok
test_load_ios_constraints ... ok
test_load_miniprogram_constraints ... ok
test_load_unsupported_platform ... ok
test_load_cache ... ok
test_load_without_cache ... ok
test_apply_naming_convention_camel_case ... ok
test_apply_naming_convention_kebab_case ... ok
test_apply_naming_convention_pascal_case ... ok
test_apply_naming_convention_upper_snake_case ... ok
test_generate_file_path_android_view_model ... ok
test_generate_file_path_h5_page ... ok
test_generate_file_path_ios_view ... ok
test_get_component_mapping ... ok
test_get_style_value_colors ... ok
test_get_style_value_spacing ... ok
test_load_all_platforms ... ok
test_get_constraint_loader_singleton ... ok
test_to_camel_case ... ok
test_to_kebab_case ... ok
test_to_pascal_case ... ok
test_to_upper_snake_case ... ok

----------------------------------------------------------------------
Ran 24 tests in 0.XXXs

OK
```

## 故障排除

### 问题 1: ModuleNotFoundError

**错误信息**：
```
ModuleNotFoundError: No module named 'utils.constraint_loader'
```

**解决方案**：
确保在 `workflow-automation` 目录下运行测试，并且 Python 路径设置正确。

### 问题 2: FileNotFoundError

**错误信息**：
```
FileNotFoundError: 约束配置文件不存在: config/constraints/ios.json
```

**解决方案**：
确保配置文件存在于正确的路径，并且文件格式正确。

### 问题 3: JSONDecodeError

**错误信息**：
```
ValueError: 约束配置文件格式错误
```

**解决方案**：
检查配置文件的 JSON 格式是否正确，可以使用在线 JSON 验证工具验证。

## 持续集成

测试应该在 CI/CD 流程中自动运行。以下是 GitHub Actions 配置示例：

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          pytest src/tests/test_constraint_loader.py --cov=src/utils/constraint_loader --cov-report=xml
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v2
        with:
          file: ./coverage.xml
```

## 贡献

添加新的测试用例时，请遵循以下规范：

1. 测试方法以 `test_` 开头
2. 使用清晰的测试方法名称
3. 添加必要的文档字符串
4. 使用 `assertEqual`、`assertTrue` 等断言方法
5. 测试失败时提供清晰的错误信息

## 相关文档

- [仓库约束配置系统](../docs/REPOSITORY_CONSTRAINTS.md)
- [代码生成节点使用约束指南](../docs/CODE_GENERATOR_CONSTRAINTS_GUIDE.md)
- [约束配置文件](../config/constraints/)
