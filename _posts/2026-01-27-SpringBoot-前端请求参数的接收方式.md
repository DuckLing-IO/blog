---
title: '[SpringBoot]前端请求参数的接收方式'
date: 2026-01-27 10:44:00 +0800
slug: SpringBoot-前端请求参数的接收方式
permalink: /post/SpringBoot-前端请求参数的接收方式.html
---

### 核心速查表

| **数据来源位置** | **数据格式/类型** | **典型请求方式** | **关键注解** | **Content-Type** |
| --- | --- | --- | --- | --- |
| **URL 路径** | `/users/{id}` | GET / DELETE | **`@PathVariable`** | - |
| **URL 参数** | `?id=1&name=so` | GET (主要) | **`@RequestParam`** | - |
| **Body (请求体)** | JSON 字符串 | POST / PUT | **`@RequestBody`** | `application/json` |
| **Body (请求体)** | 表单 (k=v&k=v) | POST | **无注解** (直接用对象接) | `application/x-www-form-urlencoded` |
| **Body (请求体)** | 文件上传 | POST | **`@RequestPart`** | `multipart/form-data` |
| **Header (请求头)** | Token / 自定义头 | 任意 | **`@RequestHeader`** | - |

---

### 详细代码示例

#### 1. URL 路径参数 (`@PathVariable`)

**场景**：RESTful 风格接口，参数是 URL 的一部分。

- 请求：`GET /users/101`

Java

```text-only
@GetMapping("/users/{id}")
public String getUser(@PathVariable("id") Long id) {
    return "获取ID为 " + id + " 的用户";
}
```

#### 2. URL 查询参数 (`@RequestParam`)

**场景**：传统的问号传参，用于筛选、分页等。

- 请求：`GET /users?name=gemini&age=18`

Java

```text-only
@GetMapping("/users")
public String searchUser(@RequestParam("name") String name, 
                         @RequestParam(value = "age", required = false) Integer age) {
    return "搜索名字: " + name + ", 年龄: " + age;
}
```

> **注意**：如果参数名和变量名一致，且参数必传，其实可以省略 `@RequestParam`，但为了代码可读性，建议加上。

#### 3. JSON 数据 (`@RequestBody`) —— **最常用**

**场景**：前后端分离，前端发 JSON 对象。

- 请求头：`Content-Type: application/json`
- 请求体：`{"name": "Gemini", "age": 18}`

Java

```text-only
@PostMapping("/json")
public String saveJson(@RequestBody User user) {
    return "接收 JSON: " + user.getName();
}
```

#### 4. 普通表单数据 (Form Data)

**场景**：传统 `<form>` 提交，或者 Postman 中选 `x-www-form-urlencoded`。

- 请求头：`Content-Type: application/x-www-form-urlencoded`
- 请求体：`name=Gemini&age=18`

Java

```text-only
@PostMapping("/form")
// ❌ 千万不要加 @RequestBody
// ✅ Spring 会自动将 name 和 age 映射到 User 对象的同名属性上
public String saveForm(User user) {
    return "接收表单: " + user.getName();
}
```

#### 5. 文件上传 (`@RequestPart` 或 `MultipartFile`)

**场景**：上传图片、文档。

- 请求头：`Content-Type: multipart/form-data`

Java

```text-only
@PostMapping("/upload")
public String upload(@RequestPart("file") MultipartFile file,
                     @RequestParam("description") String description) {
    return "文件名: " + file.getOriginalFilename() + ", 描述: " + description;
}
```

#### 6. 获取请求头 (`@RequestHeader`)

**场景**：需要获取 Token 或客户端信息。

Java

```text-only
@GetMapping("/header")
public String getHeader(@RequestHeader("Authorization") String token) {
    return "Token is: " + token;
}
```

---

### 一个容易混淆的特例：Map 接收

有时候你不想定义一个 Java Bean (User 类)，想偷懒直接用 `Map` 接数据：

1. **接 JSON**：必须加 `@RequestBody`。

`public void test(@RequestBody Map<String, Object> map)`

1. **接普通表单**：必须加 `@RequestParam`。

`public void test(@RequestParam Map<String, String> map)`

*(如果你这里不加注解，Spring 无法判断你要把表单数据放入 Map，可能会得到空 Map)*
