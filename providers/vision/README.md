# Vision Provider 插件

Provider 模式视觉能力，第一个 Provider 为 MiMo。

## 目录

- base.py：VisionProvider 抽象接口
- registry.py：Provider 注册表
- mimo.py：MiMo Vision Provider
- analyzer.py：图片 / PDF 页面截图统一入口

## 调用示例

```python
from providers.vision import MimoVisionProvider, VisionProviderRegistry, analyze_media

config = {
    "enabled": True,
    "base_url": "https://your-mimo-endpoint",
    "api_key_env": "MIMO_API_KEY",
    "model": "mimo-vision",
}
provider = MimoVisionProvider(config)
reg = VisionProviderRegistry()
reg.register("mimo", provider)

result = analyze_media("案例图.png", "请分析该图片并输出结构化JSON", provider)
print(result)
```

PDF 页面：

```python
result = analyze_media("课件.pdf", "请分析第3页版式", provider, page_index=2)
```

API Key 只从环境变量 MIMO_API_KEY 读取，默认 disabled。