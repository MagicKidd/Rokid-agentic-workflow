---
name: software-architecture
description: 软件架构设计指南。当用户想要编写代码、设计架构、分析代码时使用，适用于任何与软件开发相关的场景。基于 Clean Architecture 和 DDD 原则。触发词：架构设计、代码规范、重构、Clean Architecture、DDD。
---

# 软件架构开发技能

提供以质量为中心的软件开发和架构指导，基于 Clean Architecture 和领域驱动设计（DDD）原则。

## 代码风格规则

### 通用原则

- **早期返回模式**：始终使用早期返回而非嵌套条件，提高可读性
- 通过创建可复用函数和模块避免代码重复
- 将长组件和函数（超过 80 行）分解为多个较小的组件和函数
- 如果文件超过 200 行代码，应拆分为多个文件
- 尽可能使用箭头函数而非函数声明

---

## 最佳实践

### 库优先方法

**在写自定义代码前始终搜索现有解决方案**

- 检查 npm/pip 是否有现成库解决问题
- 评估现有服务/SaaS 解决方案
- 考虑第三方 API 用于常见功能
- 使用库而非自己写 utils 或 helpers

**示例**：使用 `cockatiel`（JS）或 `tenacity`（Python）而非自己写重试逻辑

**何时自定义代码合理**：
- 特定于领域的独特业务逻辑
- 有特殊需求的性能关键路径
- 外部依赖会过度复杂化
- 需要完全控制的安全敏感代码
- 现有解决方案经过彻底评估后不满足需求

### 架构和设计

**Clean Architecture & DDD 原则**：

- 遵循领域驱动设计和统一语言
- 将领域实体与基础设施关注点分离
- 保持业务逻辑独立于框架
- 清晰定义用例并保持隔离

**命名规范**：

| 避免 | 使用 |
|------|------|
| `utils`, `helpers`, `common`, `shared` | 领域特定名称 |
| `processData()` | `OrderCalculator`, `UserAuthenticator` |
| `misc.py` | `invoice_generator.py` |

- 遵循限界上下文命名模式
- 每个模块应有单一、清晰的用途

**关注点分离**：

- 不要将业务逻辑与 UI 组件混合
- 保持数据库查询不在控制器中
- 维护上下文之间的清晰边界
- 确保职责的适当分离

---

## 反模式清单

### NIH（非此处发明）综合症

| 不要 | 使用 |
|------|------|
| 构建自定义认证 | Auth0/Supabase/Firebase |
| 编写自定义状态管理 | Redux/Zustand/Pinia |
| 创建自定义表单验证 | 成熟的验证库 |

### 糟糕的架构选择

- 将业务逻辑与 UI 组件混合
- 直接在控制器中查询数据库
- 缺乏清晰的关注点分离

### 通用命名反模式

- `utils.js` 包含 50 个不相关函数
- `helpers/misc.js` 作为垃圾场
- `common/shared.js` 用途不清晰

**记住**：每行自定义代码都是需要维护、测试和文档的负债

---

## 代码质量

### 错误处理

```python
# 好：带类型的 catch 块
try:
    result = process_data(data)
except ValidationError as e:
    logger.error(f"验证失败: {e}")
    return Result(error=str(e))
except DatabaseError as e:
    logger.error(f"数据库错误: {e}")
    raise
```

### 函数设计

- 将复杂逻辑分解为更小、可复用的函数
- 避免深度嵌套（最多3层）
- 尽可能保持函数在 50 行以内
- 尽可能保持文件在 200 行代码以内

### 早期返回示例

```python
# 坏：深度嵌套
def process_user(user):
    if user:
        if user.is_active:
            if user.has_permission:
                # 实际逻辑在这里
                do_something()
            else:
                return "无权限"
        else:
            return "用户未激活"
    else:
        return "用户不存在"

# 好：早期返回
def process_user(user):
    if not user:
        return "用户不存在"
    
    if not user.is_active:
        return "用户未激活"
    
    if not user.has_permission:
        return "无权限"
    
    # 主逻辑在这里，保证用户有效且有权限
    do_something()
```

---

## 类型系统防错

### 使字符串类型更安全

```typescript
// 坏：string 状态可以是任何值
type OrderBad = {
    status: string;  // 可以是 "pending", "PENDING", "pnding", 任何东西！
};

// 好：只有有效状态可能
type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered';
type Order = {
    status: OrderStatus;
};

// 更好：状态带关联数据
type Order =
    | { status: 'pending'; createdAt: Date }
    | { status: 'processing'; startedAt: Date; estimatedCompletion: Date }
    | { status: 'shipped'; trackingNumber: string; shippedAt: Date }
    | { status: 'delivered'; deliveredAt: Date; signature: string };

// 现在不可能有 shipped 没有 trackingNumber
```

### 在边界验证

```python
# 好：在系统边界验证一次
def handle_payment_request(request):
    amount = validate_positive(request.body.amount)  # 验证一次
    process_payment(amount)  # 到处安全使用

def validate_positive(n: float) -> float:
    if n <= 0:
        raise ValueError("必须为正数")
    return n

def process_payment(amount: float):
    # amount 保证为正，无需检查
    fee = amount * 0.03
```

---

## 配置防错

```python
# 坏：可选配置带不安全默认值
config = {
    "api_key": os.getenv("API_KEY"),  # 可能是 None！
    "timeout": 5000,
}

# 好：必需配置，早期失败
def load_config():
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY 环境变量必需")
    
    return {
        "api_key": api_key,
        "timeout": 5000,
    }

# 应用在启动时如果配置无效则失败，而非在请求期间
config = load_config()
```

---

## 标准化工作

### 遵循模式

```python
# 现有代码库模式用于 API 客户端
class UserAPIClient:
    async def get_user(self, id: str) -> User:
        return await self.fetch(f"/users/{id}")

# 新代码遵循相同模式
class OrderAPIClient:
    async def get_order(self, id: str) -> Order:
        return await self.fetch(f"/orders/{id}")
```

一致性使代码库可预测。

### 文档标准

```python
"""
用指数退避重试异步操作。

为什么：网络请求临时失败；重试提高可靠性
何时使用：外部 API 调用、数据库操作
何时不用：用户输入验证、内部函数调用

示例:
    result = await retry(
        lambda: fetch('https://api.example.com/data'),
        max_attempts=3, base_delay=1.0
    )
"""
```

记录为什么、何时和如何。

---

## YAGNI（你不需要它）

### 好例子

```python
# 当前需求：将错误记录到控制台
def log_error(error):
    print(f"ERROR: {error}")
```

简单，满足当前需求。

### 坏例子

```python
# 为"未来需求"过度工程
class LogTransport(ABC):
    @abstractmethod
    async def write(self, level, message, meta=None): pass

class ConsoleTransport(LogTransport): ...
class FileTransport(LogTransport): ...
class RemoteTransport(LogTransport): ...

class Logger:
    def __init__(self):
        self.transports = []
        self.queue = []
        self.rate_limiter = RateLimiter()
        # 200行代码用于"也许我们会需要"
```

为想象的未来需求构建。

### 何时添加复杂性

- 当前需求要求它
- 通过使用识别出痛点
- 测量到性能问题
- 出现多个使用案例

---

## 过早抽象

```python
# 坏：一个用例，但构建通用框架
class BaseCRUDService(ABC):
    @abstractmethod
    def get_all(self): pass
    @abstractmethod
    def get_by_id(self, id): pass
    @abstractmethod
    def create(self, data): pass
    # ... 为单个表构建整个 ORM

# 好：当前需求的简单函数
async def get_users():
    return await db.query("SELECT * FROM users")

async def get_user_by_id(id: str):
    return await db.query("SELECT * FROM users WHERE id = $1", [id])

# 当模式在 3+ 个实体中出现时再抽象
```

**三次法则**：仅当模式在 3+ 个相似情况中被证明后才抽象。

---

## 性能优化

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

## 记住

**关于**：
- 小步持续改进
- 通过设计预防错误
- 遵循经过验证的模式
- 只构建需要的

**不关于**：
- 第一次就完美
- 大规模重构项目
- 聪明的抽象
- 过早优化

**心态**：今天足够好，明天更好。重复。
