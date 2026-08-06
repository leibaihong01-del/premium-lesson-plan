# -*- coding: utf-8 -*-
"""视觉分析入口：支持图片与 PDF 页面截图输入。"""
import os
import tempfile

try:
    import pypdfium2 as pdfium
except Exception:  # pragma: no cover
    pdfium = None

MIME_MAP = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "bmp": "image/bmp",
    "webp": "image/webp",
}


def render_pdf_page(pdf_path, page_index=0, scale=2.0, out_path=None):
    """将 PDF 指定页渲染为 PNG 截图，返回截图路径。"""
    if not os.path.exists(pdf_path):
        return None
    if pdfium is None:
        raise RuntimeError("pypdfium2 未安装，无法渲染PDF页面")
    doc = pdfium.PdfDocument(pdf_path)
    try:
        if page_index < 0 or page_index >= len(doc):
            raise IndexError("page_index 超出范围")
        img = doc[page_index].render(scale=scale).to_pil()
        out_path = out_path or tempfile.mktemp(suffix=".png")
        img.save(out_path)
        return out_path
    finally:
        doc.close()


def _guess_mime(lower_path):
    ext = lower_path.rsplit(".", 1)[-1]
    return MIME_MAP.get(ext, "application/octet-stream")


def analyze_media(path, prompt, provider, page_index=0, mime=None, **kwargs):
    """统一视觉分析入口。

    图片直接分析；PDF 渲染指定页为截图后分析。
    任何异常返回结构化 dict，不抛出。
    """
    if provider is None:
        return {"ok": False, "error": "provider 未提供"}
    if not os.path.exists(path):
        return {"ok": False, "error": "文件不存在", "path": path}
    lower = path.lower()
    try:
        if lower.endswith(".pdf"):
            image_path = render_pdf_page(path, page_index=page_index)
            if not image_path:
                return {"ok": False, "error": "PDF 页面渲染失败",
                        "path": path, "page_index": page_index}
            return provider.analyze(image_path, prompt, mime=mime or "image/png", **kwargs)
        return provider.analyze(path, prompt, mime=mime or _guess_mime(lower), **kwargs)
    except Exception as exc:
        return {"ok": False, "error": str(exc),
                "provider": getattr(provider, "name", "unknown")}