---
title: '[SpringBoot]注解@Options'
top_img: /img/home.jpg
date: 2026-01-27 11:22:58
tags:
  - 学习笔记
  - 后端
  - SpringBoot
  - 实用资料
categories:
  - [后端, SpringBoot]
  - [学习笔记, 后端, SpringBoot]
  - [资料, SpringBoot, 注解]
cover: /img/post_springboot_260124.jpg
---

# 常用功能

## 主键返回

假设你的数据库里 `user` 表的主键 `id` 是 **自增 (Auto Increment)** 的。 当你执行一个 `insert` 操作时：

```java
@Insert("INSERT INTO user (username, password) VALUES (#{username}, #{password})")
int insert(User user);
```

**默认情况**：这个方法返回的 `int` 是 **“受影响的行数”**（成功插入 1 行，就返回 1）。 **你的痛点**：刚刚插入的那个用户，ID 到底是多少？Java 对象里的 `user.getId()` 此时还是 `null`。

#### 解决方案：使用 `@Options`

你需要告诉 MyBatis：“插入完之后，帮我去数据库问问刚才生成的 ID 是多少，然后填回到我的 User 对象里。”

```java
// 1. 插入语句
@Insert("INSERT INTO user (username, password) VALUES (#{username}, #{password})")
// 2. 开启高级配置
@Options(useGeneratedKeys = true, keyProperty = "id") 
int insert(User user);
```

- **`useGeneratedKeys = true`**：主键返回开关。将主键用 JDBC 的 `getGeneratedKeys` 方法取回来
- **`keyProperty = "id"`**：目标填空。将取回的主键返回到参数对象（User）的 **`id` 属性**（Java 属性名）里

**执行后的效果**：

```java
User user = new User("zhangsan", "123456");
System.out.println(user.getId()); // 输出 null

mapper.insert(user); // 执行插入

System.out.println(user.getId()); // 输出 101 (MyBatis 已经悄悄把 ID 填进去了！)
```

# 其他用法

- **`flushCache`** (默认为 true):
  - `flushCache = Options.FlushCachePolicy.TRUE`
  - 意思是：只要执行这句 SQL，就清空本地缓存。通常用于 `Insert/Update/Delete`，防止查到脏数据。
- **`timeout`**:
  - `timeout = 1000`
  - 意思是：如果这句 SQL 执行超过 1000 秒还没反应，就直接报错（抛出异常），别卡死程序。

# XML中配置

**XML 里的对应写法（等价于上面的注解）：**

```XML
<insert id="insertUser" useGeneratedKeys="true" keyProperty="id">
    INSERT INTO user (username, password) VALUES (#{username}, #{password})
</insert>
```