# 在线点餐平台

单商家自营到店取餐在线点餐平台，参考瑞幸咖啡、喜茶GO等主流小程序业务模式，实现从浏览菜单到取餐的完整业务闭环。

---

## 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 前端框架 | Vue.js | 3.x |
| 前端UI | Vant | 4.x |
| 构建工具 | Vite | 8.x |
| 状态管理 | Pinia | 3.x |
| HTTP客户端 | Axios | 1.x |
| 后端框架 | Django | 4.2 |
| REST API | Django REST Framework | 3.x |
| 认证 | SimpleJWT | 5.x |
| 数据库 | MySQL | 8.0+ |
| 图片处理 | Pillow | 12.x |

---

## 环境配置

### 前置要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- npm 9+

### 1. 数据库初始化

```bash
mysql -u root -p -e "CREATE DATABASE onlineOrder CHARACTER SET utf8mb4;"
```

### 2. 配置文件

创建 `backend/config.json`（敏感信息，已加入 .gitignore）：

```json
{
    "SECRET_KEY": "django-insecure-...(替换为你的密钥)",
    "DB_PASSWORD": "你的MySQL密码"
}
```

### 3. 后端启动

```bash
# 安装依赖
pip install -r backend/requirements.txt

# 数据库迁移
python manage.py migrate

# 启动服务
python manage.py runserver
# → http://localhost:8000
```

### 4. 前端启动

```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
# 按F12 → 切换手机模拟模式
```

---

## 演示账号

| 角色 | 账号 | 密码 |
|------|------|------|
| 普通用户 | 13800000000 | 123456 |
| 商家 | 13900000000 | 123456 |

> 演示账号需通过 `python manage.py shell` 手动创建，或使用注册页面自行注册。

---

## 核心功能

### 用户端
- 注册登录（支持角色选择：我要点餐 / 我是商家）
- 浏览菜单（按分类筛选、查看菜品详情）
- 购物车管理（增减数量、删除、清空、实时总价）
- 下单支付（模拟微信/支付宝）
- 订单查看（按状态筛选、订单详情）

### 商家端
- 菜品管理（新增、编辑、删除、上架/下架）
- 订单处理（出餐、输入取餐码确认取餐）
- 经营看板（今日订单数、今日收入）

---

## 项目结构

```
onlineOrderingApp/
├── backend/                    # Django 后端
│   ├── apps/                   # 5个功能模块
│   │   ├── users/              # 用户注册登录、个人信息
│   │   ├── dishes/             # 菜品CRUD、图片上传、上下架
│   │   ├── cart/               # 购物车增删改、自动合并
│   │   ├── orders/             # 订单管理、状态流转、每日统计
│   │   └── payments/           # 模拟支付
│   ├── media/dishes/           # 菜品图片持久化目录
│   ├── config.json             # 敏感配置（SECRET_KEY、DB密码）
│   └── settings.py             # Django配置
│
├── frontend/                   # Vue 3 前端
│   ├── src/
│   │   ├── api/                # 5个API模块
│   │   ├── pages/              # 10个页面组件
│   │   ├── router/             # 路由守卫
│   │   ├── stores/             # 状态管理（user + cart）
│   │   ├── App.vue             # 根组件（统一导航栏）
│   │   └── style.css           # 全局样式
│   └── package.json
│
├── docs/                       # 项目文档
│   ├── 项目说明文档.md          # 项目概述与功能清单
│   ├── 业务说明文档.md          # 业务流程与角色职责
│   ├── 设计与开发文档.md        # 数据模型与API设计
│   ├── 编码实验报告.md          # 编码实现报告
│   ├── 测试文档.md              # 测试用例与验收标准
│   ├── 配置.md                  # 环境配置说明
│   └── 数据库设计.md            # 数据库表结构
│
├── .gitignore                  # Git忽略配置
├── backend/config.json         # 敏感配置（不入仓）
└── manage.py                   # Django管理脚本
```

---

## 已知问题

| 问题 | 影响 | 说明 |
|------|------|------|
| 密码明文存储 | 安全性低 | 当前注册和登录使用明文比较，未使用 Django 的 `set_password`/`check_password`。后续应改为密码哈希存储。 |
| 支付超时未实现 | 业务不完整 | 模型中存在 `pay_deadline` 字段，但未实现15分钟未支付自动取消逻辑。需配合 Celery 定时任务或定期轮询实现。 |
| 无分页 | 数据量大时性能下降 | 菜品列表和订单列表未实现分页，数据量增多后会影响加载速度。 |
| 图片文件名冲突 | 同名文件上传会覆盖 | 当前使用 `get_valid_filename` 处理文件名，未添加 UUID 前缀。多个用户上传同名的 `photo.jpg` 会导致覆盖。 |
| 取餐码仅数字 | 与文档描述不一致 | 业务文档要求"6位随机码（数字+字母）"，当前实现为纯数字6位随机码。 |
| 无演示账号种子脚本 | 首次部署需手动建账号 | 未提供自动创建演示账号的 management command 或 seed 脚本。 |

---

## 数据库

- 数据库名：`onlineOrder`
- 表数量：8张（user、dish、cart、cart_item、order、order_item、payment、daily_stats）
- 迁移文件已就绪，首次运行 `python manage.py migrate` 自动建表
- 图片持久化到 `media/dishes/` 目录
