---
name: test-driven-development
description: 测试驱动开发（TDD）方法论。在实现任何功能或修复 bug 之前，先写测试代码。触发词：TDD、测试驱动、先写测试、Red-Green-Refactor。
---

# 测试驱动开发（TDD）

## 概述

先写测试。看它失败。写最少代码让它通过。

**核心原则**：如果你没有看到测试失败，你就不知道它是否测试了正确的东西。

**违反规则的字面意思就是违反规则的精神。**

## 何时使用

**始终**：
- 新功能
- Bug 修复
- 重构
- 行为变更

**例外（需询问你的人类伙伴）**：
- 一次性原型
- 生成的代码
- 配置文件

想着"就这一次跳过 TDD"？停下。那是合理化。

---

## 铁律

```
没有先失败的测试，就没有生产代码
```

在测试前写了代码？删除它。重新开始。

**无例外**：
- 不要保留它作为"参考"
- 不要在写测试时"调整"它
- 不要看它
- 删除就是删除

从测试开始全新实现。句号。

---

## Red-Green-Refactor 循环

```
RED（写失败测试）→ 验证正确失败 → GREEN（最少代码）→ 验证通过 → REFACTOR（清理）→ 下一个
```

### RED - 写失败测试

写一个最小测试，展示应该发生什么。

**好例子**：
```typescript
test('失败操作重试3次', async () => {
    let attempts = 0;
    const operation = () => {
        attempts++;
        if (attempts < 3) throw new Error('fail');
        return 'success';
    };

    const result = await retryOperation(operation);

    expect(result).toBe('success');
    expect(attempts).toBe(3);
});
```
清晰名称，测试真实行为，一件事

**坏例子**：
```typescript
test('retry works', async () => {
    const mock = jest.fn()
        .mockRejectedValueOnce(new Error())
        .mockResolvedValueOnce('success');
    await retryOperation(mock);
    expect(mock).toHaveBeenCalledTimes(2);
});
```
名称模糊，测试 mock 而非代码

**要求**：
- 一个行为
- 清晰名称
- 真实代码（除非不可避免才用 mock）

### 验证 RED - 看它失败

**强制。绝不跳过。**

```bash
npm test path/to/test.test.ts
# 或
pytest path/to/test.py
```

确认：
- 测试失败（不是错误）
- 失败消息符合预期
- 因为功能缺失而失败（不是拼写错误）

**测试通过？** 你在测试现有行为。修复测试。

**测试报错？** 修复错误，重新运行直到它正确失败。

### GREEN - 最少代码

写最简单的代码让测试通过。

**好例子**：
```typescript
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
    for (let i = 0; i < 3; i++) {
        try {
            return await fn();
        } catch (e) {
            if (i === 2) throw e;
        }
    }
    throw new Error('unreachable');
}
```
刚好够通过

**坏例子**：
```typescript
async function retryOperation<T>(
    fn: () => Promise<T>,
    options?: {
        maxRetries?: number;
        backoff?: 'linear' | 'exponential';
        onRetry?: (attempt: number) => void;
    }
): Promise<T> {
    // YAGNI - 你不需要它
}
```
过度工程

不要添加功能、重构其他代码或超出测试"改进"。

### 验证 GREEN - 看它通过

**强制。**

```bash
npm test path/to/test.test.ts
```

确认：
- 测试通过
- 其他测试仍然通过
- 输出干净（无错误、警告）

**测试失败？** 修复代码，不是测试。

**其他测试失败？** 现在修复。

### REFACTOR - 清理

仅在 GREEN 之后：
- 消除重复
- 改进命名
- 提取辅助函数

保持测试绿色。不添加行为。

---

## 好测试的特征

| 质量 | 好 | 坏 |
|------|----|----|
| **最小** | 一件事。名称中有"和"？拆分它。 | `test('验证邮箱和域名和空白')` |
| **清晰** | 名称描述行为 | `test('test1')` |
| **显示意图** | 演示期望的 API | 掩盖代码应该做什么 |

---

## 为什么顺序重要

**"我会在之后写测试来验证它工作"**

之后写的测试立即通过。立即通过什么都不证明：
- 可能测试错误的东西
- 可能测试实现而非行为
- 可能遗漏你忘记的边缘情况
- 你从未看到它捕获 bug

测试优先迫使你看到测试失败，证明它确实测试了某些东西。

**"我已经手动测试了所有边缘情况"**

手动测试是临时的。你以为测试了所有但：
- 没有测试记录
- 代码变化时无法重新运行
- 压力下容易忘记情况
- "我试的时候它工作了" ≠ 全面

自动化测试是系统性的。每次以相同方式运行。

**"删除 X 小时工作是浪费"**

沉没成本谬误。时间已经过去。你现在的选择：
- 删除并用 TDD 重写（多 X 小时，高信心）
- 保留它并之后添加测试（30分钟，低信心，可能有 bug）

"浪费"是保留你无法信任的代码。没有真正测试的工作代码是技术债务。

---

## 常见借口

| 借口 | 现实 |
|------|------|
| "太简单不需要测试" | 简单代码也会出错。测试只需30秒。 |
| "我会之后测试" | 立即通过的测试什么都不证明。 |
| "之后测试实现相同目标" | 之后测试 = "这做了什么？" 先测试 = "这应该做什么？" |
| "已经手动测试了" | 临时 ≠ 系统性。无记录，无法重新运行。 |
| "删除 X 小时是浪费" | 沉没成本谬误。保留未验证代码是技术债务。 |
| "保留作为参考，先写测试" | 你会调整它。那是之后测试。删除就是删除。 |
| "需要先探索" | 可以。丢弃探索，从 TDD 开始。 |
| "测试难 = 设计不清晰" | 听测试的话。难测试 = 难使用。 |
| "TDD 会拖慢我" | TDD 比调试快。务实 = 先测试。 |

---

## 红旗 - 停下并重新开始

- 测试前写代码
- 实现后写测试
- 测试立即通过
- 无法解释为什么测试失败
- "之后"添加测试
- 合理化"就这一次"
- "我已经手动测试了"
- "之后测试实现相同目的"
- "重要的是精神而非形式"
- "保留作为参考"或"调整现有代码"
- "已经花了 X 小时，删除是浪费"
- "TDD 是教条的，我在务实"
- "这个不一样因为..."

**所有这些意味着：删除代码。从 TDD 重新开始。**

---

## 示例：Bug 修复

**Bug**：空邮箱被接受

**RED**
```python
def test_rejects_empty_email():
    result = submit_form({"email": ""})
    assert result.error == "Email required"
```

**验证 RED**
```bash
$ pytest test_form.py
FAIL: expected 'Email required', got None
```

**GREEN**
```python
def submit_form(data):
    if not data.get("email", "").strip():
        return Result(error="Email required")
    # ...
```

**验证 GREEN**
```bash
$ pytest test_form.py
PASS
```

**REFACTOR**
如需要，提取验证逻辑用于多个字段。

---

## 验证清单

标记工作完成前：

- [ ] 每个新函数/方法都有测试
- [ ] 实现前看到每个测试失败
- [ ] 每个测试因预期原因失败（功能缺失，不是拼写错误）
- [ ] 写最少代码通过每个测试
- [ ] 所有测试通过
- [ ] 输出干净（无错误、警告）
- [ ] 测试使用真实代码（仅不可避免时用 mock）
- [ ] 覆盖边缘情况和错误

无法勾选所有框？你跳过了 TDD。重新开始。

---

## 卡住时怎么办

| 问题 | 解决方案 |
|------|----------|
| 不知道如何测试 | 写期望的 API。先写断言。问你的人类伙伴。 |
| 测试太复杂 | 设计太复杂。简化接口。 |
| 必须 mock 所有东西 | 代码耦合太紧。使用依赖注入。 |
| 测试设置太大 | 提取辅助函数。仍然复杂？简化设计。 |

---

## 最终规则

```
生产代码 → 测试存在且先失败
否则 → 不是 TDD
```

没有你人类伙伴的许可，无例外。
