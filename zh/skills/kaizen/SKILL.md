---
name: kaizen
description: 持续改进方法论。用于代码实现和重构、架构或系统设计、流程和工作流改进、错误处理和验证。提供避免过度工程和应用迭代改进的技术。触发词：持续改进、Kaizen、YAGNI、Poka-Yoke、防错设计。
---

# Kaizen：持续改进

应用持续改进思维 - 建议小的迭代改进、防错设计、遵循已建立的模式、避免过度工程。

## 概述

小改进，持续进行。设计时防错。遵循有效的做法。只构建需要的。

**核心原则**：许多小改进胜过一个大变化。在设计时预防错误，而非用修复。

---

## 四大支柱

### 1. 持续改进（Kaizen）

小的、频繁的改进复利成主要收益。

#### 原则

**增量优于革命**：
- 做能提高质量的最小可行更改
- 一次一个改进
- 每次更改后验证再进行下一个
- 通过小胜利建立动力

**始终让代码变得更好**：
- 遇到小问题时修复它们
- 工作时重构（在范围内）
- 更新过时的注释
- 看到死代码时删除它

**迭代精炼**：
- 第一版：让它工作
- 第二遍：让它清晰
- 第三遍：让它高效
- 不要试图一次做完三件事

#### 示例

```python
# 迭代 1：让它工作
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total

# 迭代 2：让它清晰
def calculate_total(items):
    return sum(item.price * item.quantity for item in items)

# 迭代 3：让它健壮（添加验证）
def calculate_total(items):
    if not items:
        return 0
    
    for item in items:
        if item.price < 0 or item.quantity < 0:
            raise ValueError("价格和数量必须非负")
    
    return sum(item.price * item.quantity for item in items)
```

每一步都是完整的、经过测试的、可工作的。

---

### 2. Poka-Yoke（防错）

设计在编译/设计时预防错误的系统，而非运行时。

#### 原则

**使错误不可能**：
- 类型系统捕获错误
- 编译器强制契约
- 无效状态不可表示
- 错误早期捕获（在生产之前）

**为安全设计**：
- 快速且大声地失败
- 提供有帮助的错误消息
- 使正确路径明显
- 使错误路径困难

#### 类型系统防错

```typescript
// 坏：string 状态可以是任何值
type OrderBad = {
    status: string;
};

// 好：只有有效状态可能
type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered';
type Order = {
    status: OrderStatus;
};

// 更好：状态带关联数据
type Order =
    | { status: 'pending'; createdAt: Date }
    | { status: 'shipped'; trackingNumber: string; shippedAt: Date }
    | { status: 'delivered'; deliveredAt: Date };

// 现在不可能有 shipped 没有 trackingNumber
```

#### 验证防错

```python
# 坏：使用后验证
def process_payment(amount):
    fee = amount * 0.03  # 验证前使用！
    if amount <= 0:
        raise ValueError("无效金额")

# 好：立即验证
def process_payment(amount):
    if amount <= 0:
        raise ValueError("支付金额必须为正")
    if amount > 10000:
        raise ValueError("支付超过允许的最大值")
    
    fee = amount * 0.03
    # ... 现在可以安全使用
```

#### 守卫和前置条件

```python
# 早期返回防止深度嵌套代码
def process_user(user):
    if not user:
        logger.error("用户不存在")
        return
    
    if not user.email:
        logger.error("用户邮箱缺失")
        return
    
    if not user.is_active:
        logger.info("用户未激活，跳过")
        return
    
    # 主逻辑在这里，保证用户有效且激活
    send_email(user.email, "欢迎！")
```

#### 配置防错

```python
# 坏：可选配置带不安全默认值
config = {"timeout": 5000}  # api_key 缺失！

# 好：必需配置，早期失败
def load_config():
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY 环境变量必需")
    
    return {"api_key": api_key, "timeout": 5000}

# 应用在启动时如果配置无效则失败，而非在请求期间
config = load_config()
```

---

### 3. 标准化工作

遵循已建立的模式。记录有效的做法。使好实践易于遵循。

#### 原则

**一致性优于聪明**：
- 遵循现有代码库模式
- 不要重新发明已解决的问题
- 只有显著更好时才引入新模式
- 新模式需要团队同意

**文档与代码同在**：
- README 用于设置和架构
- CLAUDE.md 用于 AI 编码规范
- 注释解释"为什么"，而非"什么"
- 复杂模式提供示例

**自动化标准**：
- Linter 强制风格
- 类型检查强制契约
- 测试验证行为
- CI/CD 强制质量门

#### 遵循模式

```python
# 现有代码库模式用于 API 客户端
class UserAPIClient:
    async def get_user(self, id: str) -> User:
        return await self.fetch(f"/users/{id}")

# 新代码遵循相同模式 ✓
class OrderAPIClient:
    async def get_order(self, id: str) -> Order:
        return await self.fetch(f"/orders/{id}")

# 不要因为"我更喜欢函数"而引入不同模式 ✗
async def get_order(id: str) -> Order:
    # 破坏一致性
    pass
```

---

### 4. Just-In-Time（JIT）

构建现在需要的。不多不少。避免过早优化和过度工程。

#### 原则

**YAGNI（你不需要它）**：
- 只实现当前需求
- 没有"以防万一"功能
- 没有"我们以后可能需要这个"代码
- 删除推测

**最简单可行的方案**：
- 从直接的解决方案开始
- 只在需要时添加复杂性
- 需求变化时重构
- 不要预测未来需求

**测量后优化**：
- 不要过早优化
- 优化前先分析
- 测量更改的影响
- 接受"足够好"的性能

#### YAGNI 实践

```python
# 当前需求：将错误记录到控制台
def log_error(error):
    print(f"ERROR: {error}")
# 简单，满足当前需求 ✓

# 过度工程用于"未来需求" ✗
class LogTransport(ABC):
    @abstractmethod
    async def write(self, level, message): pass

class ConsoleTransport(LogTransport): ...
class FileTransport(LogTransport): ...
class RemoteTransport(LogTransport): ...

class Logger:
    def __init__(self):
        self.transports = []
        self.queue = []
        # 200行代码用于"也许我们会需要"
```

#### 何时添加复杂性

- 当前需求要求它
- 通过使用识别出痛点
- 测量到性能问题
- 出现多个使用案例

```python
# 随需求演进添加复杂性
# 版本 1：简单
def format_currency(amount):
    return f"${amount:.2f}"

# 版本 2：需求演进 - 支持多种货币
def format_currency(amount, currency):
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    return f"{symbols[currency]}{amount:.2f}"

# 版本 3：需求演进 - 支持本地化
def format_currency(amount, locale):
    # 使用 locale 库...
```

复杂性只在需要时添加。

#### 过早抽象

```python
# 坏：一个用例，但构建通用框架
class BaseCRUDService(ABC):
    @abstractmethod
    def get_all(self): pass
    @abstractmethod
    def get_by_id(self, id): pass
    # 为单个表构建整个 ORM...

# 好：当前需求的简单函数
async def get_users():
    return await db.query("SELECT * FROM users")

# 三次法则：当模式在 3+ 个实体中出现时再抽象
```

#### 性能优化

```python
# 当前：简单方法
def filter_active_users(users):
    return [u for u in users if u.is_active]

# 基准测试显示：1000 用户 50ms（可接受）
# ✓ 发布它，无需优化

# 之后：分析显示这是瓶颈后
# 然后用索引查找或缓存优化
```

基于测量优化，而非假设。

---

## 红旗

**违反持续改进**：
- "我之后会重构它"（永远不会发生）
- 让代码比你发现时更差
- 大爆炸重写而非增量改进

**违反 Poka-Yoke**：
- "用户应该小心"
- 使用后验证而非使用前
- 可选配置无验证

**违反标准化工作**：
- "我更喜欢按我的方式做"
- 不检查现有模式
- 忽略项目规范

**违反 Just-In-Time**：
- "我们某天可能需要这个"
- 在使用之前构建框架
- 不测量就优化

---

## 记住

**Kaizen 关于**：
- 小改进持续进行
- 通过设计预防错误
- 遵循经过验证的模式
- 只构建需要的

**不关于**：
- 第一次就完美
- 大规模重构项目
- 聪明的抽象
- 过早优化

**心态**：今天足够好，明天更好。重复。
