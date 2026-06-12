# API 接口文档

基础URL：`http://127.0.0.1:8000/api/v1`
认证方式：请求头 `Authorization: Bearer {token}`
统一响应格式：`{ "code": 200, "message": "success", "data": {} }`

---

## 用户模块

### 注册

```
POST /users/register
Content-Type: application/json

{
    "username": "昵称",
    "phone": "13800138000",
    "password": "123456",
    "role": "user"        // "user" 或 "merchant"
}

Response 200:
{
    "code": 200,
    "data": {
        "user": { "user_id": "...", "username": "...", "phone": "...", "role": "user" },
        "tokens": { "access": "jwt_token..." }
    }
}
```

### 登录

```
POST /users/login
Content-Type: application/json

{
    "username": "昵称",
    "password": "123456"
}

Response 200: 同上
Response 400: { "code": 400, "message": "密码错误" }
Response 400: { "code": 400, "message": "用户名不存在" }
```

### 获取个人信息

```
GET /users/profile
Authorization: Bearer {token}

Response 200:
{ "user_id": "...", "username": "...", "phone": "...", "role": "user", "avatar": null, "create_time": "..." }
```

### 修改个人信息

```
PUT /users/profile
Authorization: Bearer {token}
Content-Type: application/json

{ "username": "新昵称" }
```

---

## 菜品模块

### 获取上架菜品列表

```
GET /dishes/?category=drinks
(可选参数 category: drinks/snacks/recommended/signature)

Response 200:
{
    "data": [
        {
            "dish_id": "...",
            "dish_name": "经典拿铁",
            "price": "28.00",
            "category": "drinks",
            "image": "http://.../media/dishes/xxx.jpg",
            "images": ["http://..."],
            "month_sales": 328,
            "status": true
        }
    ]
}
```

### 获取菜品详情

```
GET /dishes/{dishId}
```

### 获取所有菜品（含下架，商家用）

```
GET /dishes/all
Authorization: Bearer {token}  // 商家token
```

### 新增菜品（商家）

```
POST /dishes/create
Authorization: Bearer {token}
Content-Type: multipart/form-data

dish_name: 菜品名称
price: 28.00
category: drinks
image: (图片文件)
```

### 更新菜品（商家）

```
PUT /dishes/{dishId}/update
Authorization: Bearer {token}
Content-Type: multipart/form-data

dish_name: 新名称
price: 30.00
category: snacks
image: (新图片文件，可选)
remove_image: true  // 删除图片标记
```

### 上下架菜品（商家）

```
PUT /dishes/{dishId}/status
Authorization: Bearer {token}
Content-Type: application/json

{ "status": false }  // true上架 false下架
```

### 删除菜品（商家）

```
DELETE /dishes/{dishId}/delete
Authorization: Bearer {token}
```

---

## 购物车模块

### 查看购物车

```
GET /cart/
Authorization: Bearer {token}

Response:
{
    "data": {
        "cart_id": "...",
        "items": [
            {
                "item_id": "...",
                "dish": { "dish_id": "...", "dish_name": "...", "price": "28.00", "image": "..." },
                "quantity": 2
            }
        ],
        "itemCount": 2,
        "total": "56.00"
    }
}
```

### 添加菜品

```
POST /cart/add
Authorization: Bearer {token}
Content-Type: application/json

{ "dish_id": "...", "quantity": 1 }
```

### 修改数量

```
PUT /cart/item/{itemId}
Authorization: Bearer {token}
Content-Type: application/json

{ "quantity": 3 }
```

### 删除菜品

```
DELETE /cart/item/{itemId}
Authorization: Bearer {token}
```

### 清空购物车

```
DELETE /cart/clear
Authorization: Bearer {token}
```

---

## 订单模块

### 提交订单（从购物车）

```
POST /orders/create
Authorization: Bearer {token}

Response:
{
    "data": {
        "order": { "order_id": "26061112345678", "total_money": "56.00", "order_status": "pending_payment", ... },
        "pay_id": "..."
    }
}
```

### 获取用户订单列表

```
GET /orders/?status=pending_payment
Authorization: Bearer {token}
(可选参数 status: pending_payment/preparing/waiting_pickup/completed/cancelled)
```

### 获取订单详情

```
GET /orders/{orderId}
Authorization: Bearer {token}
```

### 获取用户订单数量统计

```
GET /orders/count
Authorization: Bearer {token}

Response:
{ "data": { "pending_payment": 2, "preparing": 1, "waiting_pickup": 0, "completed": 5 } }
```

### 商家获取所有订单

```
GET /orders/merchant?status=preparing
Authorization: Bearer {token}  // 商家token
```

### 商家获取经营统计

```
GET /orders/merchant/stats
Authorization: Bearer {token}  // 商家token

Response:
{
    "data": {
        "today_orders": 12,
        "today_revenue": 356.00,
        "preparing": 3,
        "waiting_pickup": 2,
        "completed": 5,
        "cancelled": 0
    }
}
```

### 商家更新订单状态（出餐）

```
PUT /orders/{orderId}/status
Authorization: Bearer {token}  // 商家token
Content-Type: application/json

{ "order_status": "waiting_pickup" }
```

### 商家确认取餐（验证取餐码）

```
PUT /orders/merchant/confirm-pickup/{orderId}
Authorization: Bearer {token}  // 商家token
Content-Type: application/json

{ "pick_up_code": "123456" }

Response 200: { "code": 200, "message": "取餐确认成功" }
Response 400: { "code": 400, "message": "取餐码错误" }
```

---

## 支付模块

### 发起支付

```
POST /payments/pay
Authorization: Bearer {token}
Content-Type: application/json

{ "order_id": "260611...", "pay_type": "wechat" }

Response 200:
{ "data": { "pay_id": "...", "pay_status": "success", "pay_time": "..." } }
```

### 查询支付状态

```
GET /payments/status/{payId}
Authorization: Bearer {token}
```
