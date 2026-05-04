# Hello, Blog

这是一篇**测试文章**，用来验证 Markdown → HTML 转换器的工作情况。

## 图片测试

下面是一张示例图片：

![示例图片](https://picsum.photos/800/400)

## 代码高亮测试

Python 代码块：

```python
def fibonacci(n: int) -> list[int]:
    """Generate the first n Fibonacci numbers."""
    seq = [0, 1]
    for _ in range(n - 2):
        seq.append(seq[-1] + seq[-2])
    return seq[:n]

# 前 10 个斐波那契数
print(fibonacci(10))
```

JavaScript 代码：

```javascript
const greeting = (name) => {
    console.log(`Hello, ${name}!`);
};

greeting("World");
```

一段行内代码 `const x = 42` 看起来应该和正文不一样。

## 表格

| 特性 | 状态 | 备注 |
|------|------|------|
| 图片渲染 | ✅ | 支持远程 URL |
| 代码高亮 | ✅ | Pygments + monokai |
| 中文字体 | ✅ | Noto Sans/Serif SC 回退 |

## 引用

> 好的代码本身就是最好的文档。
> —— *Steve McConnell*

## 列表

- 第一项
- 第二项
  - 嵌套项 A
  - 嵌套项 B
- 第三项

---

转换完毕。
