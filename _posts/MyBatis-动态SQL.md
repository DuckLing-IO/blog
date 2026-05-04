---
title: '[MyBatis]动态SQL'
top_img: /img/home.jpg
date: 2026-01-26 17:49:44
tags:
  - 后端
  - MyBatis
  - 数据库
  - 实用资料
categories:
  - [后端, MyBatis]
  - [资料, MyBatis]
cover: /img/post_MyBatis.png
---

# 简介

> 动态SQL，指的就是随着用户的输入或外部的条件的变化而变化的SQL语句。

比如说现在根据这个员工查询系统设计后端逻辑

![员工查询系统](MyBatis-动态SQL/image-20260126175645753.png)

前端会请求姓名 | 性别 | 入职开始日期 | 入职结束日期 但是不是每次请求都返回完完整整的四个参数

如果只根据姓名查询 或者只根据性别查询，则最普通的`WHERE ... AND ...`SQL语句查询不了这种情况

所以MyBatis提供了一中拼接and语句的SQL注入方式

该操作需要在定义在xml文件中的SQL语句进行修改

# &lt;if test="..."&gt;

```xml
<if test="判断条件">
    待拼接语句
</if>
```

当`test`后的判断条件成立时才会拼接包围的SQL语句

但是这样做仍有一个弊端 比如需要执行 `WHERE a = ? AND b = ?`

当我a的判断条件不成立而b的判断条件成立时 只会进行b的拼接 就变成了``WHERE AND b = ?`

这显然是语法错误了

所以需要引入`where`这个标签

# &lt;where&gt;

被`where`包围的所有`if test`标签会自动选择是否拼接`AND`

```xml
<!--定义 Mapper 映射文件的约束和基本结构-->
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.duckling.mapper.EmpMapper">
    <select id="list" resultType="com.duckling.pojo.Emp">
        select e.*, d.name deptName from emp as e left join dept as d on e.dept_id = d.id
        <where>
            <if test="name != null and name != ''">
                e.name like concat('%',#{name},'%')
            </if>
            <if test="gender != null">
                and e.gender = #{gender}
            </if>
            <if test="begin != null and end != null">
                and e.entry_date between #{begin} and #{end}
            </if>
        </where>
        order by e.update_time desc
    </select>
</mapper>
```

在这个`xml`文件中

`where`标签包围了三个`if test`标签 但是当`name`不生效时，后边的某一个生效时会自动去掉`AND`使得SQL语法合法

# &lt;foreach&gt;

**作用**：遍历集合（List, Set, Array, Map），通常用于构建 `IN` 查询或批量插入。 

**场景**：查询 ID 在某个列表里的所有用户 (`WHERE id IN (1, 2, 3)`)。

**关键属性**：

- `collection`: 参数类型 (list, array, 或 @Param 指定的名字)。
- `item`: 当前遍历到的元素变量名。
- `open`: 循环开始前的符号。
- `close`: 循环结束后的符号。
- `separator`: 每次循环之间的分隔符。

```XML
<select id="findByIds" resultType="User">
    SELECT * FROM user
    WHERE id IN
    <foreach collection="ids" item="id" open="(" close=")" separator=",">
        #{id}
    </foreach>
</select>
```

# &lt;set&gt;

**作用**：

1. 自动插入 `SET` 关键字。
2. **智能去除**内容末尾多余的逗号 `,`。 **场景**：更新操作。只更新传入了值的字段，没传值的字段保持原样。

XML

```
<update id="updateUser">
    UPDATE user
    <set>
        <if test="userName != null"> user_name = #{userName}, </if>
        <if test="password != null"> password = #{password}, </if>
        <if test="email != null"> email = #{email}, </if>
    </set>
    WHERE id = #{id}
</update>
```

*注意：如果所有 if 都不成立，`<set>` 标签内为空，SQL 会报错。业务层需保证至少更新一个字段。*

# &lt;choose&gt;, &lt;when&gt;, &lt;otherwise&gt;

**作用**：类似于 Java 的 `switch...case...default`。只会执行**其中一个**分支。 **场景**：优先按 ID 查，没 ID 按名字查，都没传就查全部活跃用户。

```XML
<select id="selectUserByChoice" resultType="User">
    SELECT * FROM user
    <where>
        <choose>
            <when test="id != null">
                AND id = #{id}
            </when>
            <when test="userName != null">
                AND user_name = #{userName}
            </when>
            <otherwise>
                AND state = 'ACTIVE'
            </otherwise>
        </choose>
    </where>
</select>
```

# &lt;trim&gt;

`<trim>` 标签是所有动态 SQL 标签的**底层父类**（`<where>` 和 `<set>` 其实就是 `<trim>` 的预设模式）。

**作用**：自定义前缀、后缀以及要被覆盖（去掉）的字符。

**场景**：非常规的 SQL 拼接，或者你需要去掉后缀的 `AND` 而不是前缀。

```xml
<trim prefix="SET" suffixOverrides=",">
    <if test="name != null">name = #{name},</if>
</trim>

<trim prefix="WHERE" prefixOverrides="AND |OR ">
    <if test="name != null">AND name = #{name}</if>
</trim>
```

### 属性表

| **属性名**            | **作用方向** | **含义**                                       | **典型值**          |
| --------------------- | ------------ | ---------------------------------------------- | ------------------- |
| **`prefix`**          | **加**在开头 | 如果标签内有内容，就在**最前面**补上这个字符串 | `WHERE`, `SET`, `(` |
| **`suffix`**          | **加**在结尾 | 如果标签内有内容，就在**最后面**补上这个字符串 | `)`, `END`          |
| **`prefixOverrides`** | **删**掉开头 | 如果标签内的内容以这些字符**开头**，就把它删掉 | `AND`, `OR`         |
| **`suffixOverrides`** | **删**掉结尾 | 如果标签内的内容以这些字符**结尾**，就把它删掉 | `,`                 |

### 2. 逻辑执行流程

MyBatis 处理 `<trim>` 的顺序是这样的：

1. **先生成内部 SQL**：先把 `<trim>` 标签里面的 `<if>` 跑一遍，拼出一个原始字符串。
2. **判断空**：如果拼出来的字符串是空的，`<trim>` 啥也不干，直接消失。
3. **去多余（Overrides）**：如果字符串不为空，检查开头有没有命中 `prefixOverrides`，结尾有没有命中 `suffixOverrides`，有则**删掉**。
4. **补前缀后缀（Prefix/Suffix）**：删干净后，再在最前加 `prefix`，最后加 `suffix`。

------

### 3. 实战演示

#### 场景一：手写一个 `<where>` 标签

如果不使用 `<where>` 标签，用 `<trim>` 实现完全一样的功能：

XML

```
<trim prefix="WHERE" prefixOverrides="AND |OR ">
    <if test="state != null">
        AND state = #{state}
    </if> 
    <if test="title != null">
        AND title like #{title}
    </if>
</trim>
```

- **假设 `state` 有值**：内部生成 `AND state = 1`。
- **`prefixOverrides` 工作**：发现开头是 `AND`，删掉！变成 `state = 1`。
- **`prefix` 工作**：在前面加上 `WHERE`。
- **最终结果**：`WHERE state = 1`。
- *注意：`prefixOverrides` 如果有多个，用管道符 `|` 隔开，注意空格（如 `AND |OR`）。*