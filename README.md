# 在线点餐平台

单商家自营到店取餐在线点餐平台，参考瑞幸咖啡、喜茶GO等主流小程序业务模式，实现从浏览菜单到取餐的完整业务闭环。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vant 4 + TypeScript |
| 后端 | Django 4.2 + Django REST Framework |
| 数据库 | MySQL 8.0+ |
| 认证 | JWT (SimpleJWT) |

## 快速开始

### 1. 启动后端

```bash
python manage.py runserver
# http://localhost:8000
```

### 2. 启动前端

```bash
cd frontend
npm run dev
# http://localhost:5173 （F12 手机模式）
```

## 演示账号

| 角色 | 账号 | 密码 |
|------|------|------|
| 普通用户 | 13800000000 | 123456 |
| 商家 | 13900000000 | 123456 |

## 核心功能

**用户端**：注册登录、浏览菜单、购物车、下单支付、查看订单、取餐

**商家端**：菜品管理（增删改查+上下架）、订单处理（出餐+确认取餐）、经营数据看板

## 项目结构

```
onlineOrderingApp/
├── backend/          # Django 后端 API
│   ├── apps/         # 功能模块
│   └── media/        # 上传图片存储
├── frontend/         # Vue 3 前端
│   └── src/pages/    # 页面组件
├── docs/             # 项目文档
└── manage.py         # Django 管理脚本
```

## 数据库

- 数据库名：`onlineOrder`
- 迁移文件已就绪，首次运行 `python manage.py migrate` 自动建表
- 图片持久化到 `media/dishes/` 目录
