---
title: "[MySQL]基础操作"  # 文章标题
date: 2026-01-15 10:00:00  # 创建时间 (自动生成的)
categories:
  - [数据库, MySQL]
  - [学习笔记, 数据库, MySQL]
tags:
  - 学习笔记
  - MySQL
  - 数据库
cover: /img/MySQL-Logo.png
top_img: /img/home.jpg
comments: true
---

# DDL基本操作



## 1.数据库操作

### 查询

**查询所有数据库**

```mysql
SHOW DATABASES;
```

**查询当前的数据库**

```mysql
SELECT DATABASE();
```

**创建数据库**

```mysql
CREATE DATABASE [IF NOT EXISTS] 数据库名 [DEFAULT CHARSET 字符集] [COLLATE 排列顺序];
```

*注：[ ]内可不写*

**删除数据库**

```mysql
DROP DATABASE [IF EXISTS] 数据库名;
```

**使用数据库**

```mysql
USE 数据库名;
```

**查询当前数据库中所有的表**

```mysql
SHOW TABLES;
```

**查询表结构**

```mysql
DESC 表名;
```

**查询指定表的建表语句**

```mysql
SHOW CREATE TABLE 表名;
```

###创建
**创建表**

```mysql
CREATE TABLE 表名(
	字段1 字段1类型[COMMENT 字段1注释],
	字段1 字段1类型[COMMENT 字段1注释],
	字段1 字段1类型[COMMENT 字段1注释],
......
	字段1 字段1类型[COMMENT 字段1注释]
)[COMMENT 表注释]
```

*注：[...]内为可选项   最后一个字段后没有逗号
在MySQL中字符串数据类型varchar(...)为变长字符串括号内为字符最大容量*

**示例**

```mysql
create table tb_test1(
    id int comment'编号',
    name varchar(50) comment '姓名',
    age int comment '年龄',
    gender varchar(1) comment '性别'
    ) comment '测试表01';
```

**经过`DESC 表名;`语句的显示效果**

```mysql
+--------+-------------+------+-----+---------+-------+
| Field  | Type        | Null | Key | Default | Extra |
+--------+-------------+------+-----+---------+-------+
| id     | int         | YES  |     | NULL    |       |
| name   | varchar(50) | YES  |     | NULL    |       |
| age    | int         | YES  |     | NULL    |       |
| gender | varchar(1)  | YES  |     | NULL    |       |
+--------+-------------+------+-----+---------+-------+
```

**经过`SHOW CREATE TABLE 表名;`语句的显示效果**

```mysql
+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table    | Create Table                                                                                                                                                                                                                                                                                         |
+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tb_test1 | CREATE TABLE `tb_test1` (
  `id` int DEFAULT NULL COMMENT '编号',
  `name` varchar(50) DEFAULT NULL COMMENT '姓名',
  `age` int DEFAULT NULL COMMENT '年龄',
  `gender` varchar(1) DEFAULT NULL COMMENT '性别'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='测试表01' |
+----------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

### 修改

**添加字段**

```mysql
ALTER TABLE 表名 ADD 字段名 类型(长度) [COMMENT 注释] [约束];
```

**修改原有字段数据类型**

```mysql
ALTER TABLE 表名 MODIFY 字段名 新数据类型(长度);
```

**查询表结构**

```mysql
ALTER TABLE 表名 CHANGE 旧字段名 新字段名 类型(长度) [COMMENT 注释] [约束];
```

**删除字段**

```mysql
ALTER TABLE 表名 DROP 字段名;
```

**修改表名**

```mysql
ALTER TABLE 表名 RENAME TO 新表名;
```

### 删除

**删除表**

```mysql
DROP TABLE [IF EXISTS] 表名;
```

**删除指定表，并重新创建该表**

```mysql
TRUNCATE TABLE 表名;
```

### 1. 数值类型 (Numeric Types)

这里有一个重点：**Java 的 `long` 对应 MySQL 的 `BIGINT`**，**钱（货币）一定要用 `DECIMAL`**。

| **数据类型**      | **大小 (存储空间)** | **描述与应用场景**                                           | **对应 Java 类型** |
| ----------------- | ------------------- | ------------------------------------------------------------ | ------------------ |
| `TINYINT`         | 1 byte              | 非常小的整数。常用 `TINYINT(1)` 来表示 **布尔值 (Boolean)** (0为假, 1为真)。 | `Byte` / `Boolean` |
| `SMALLINT`        | 2 bytes             | 小整数。范围约 $\pm 3$ 万。                                  | `Short`            |
| `MEDIUMINT`       | 3 bytes             | 中等大小整数。范围约 $\pm 800$ 万 (很少用)。                 | `Integer`          |
| `INT` / `INTEGER` | 4 bytes             | **最常用的整数**。范围约 $\pm 21$ 亿。                       | `Integer`          |
| `BIGINT`          | 8 bytes             | 极大整数。通常用于 **主键 ID** 或像推特点击量这种大数。      | `Long`             |
| `FLOAT`           | 4 bytes             | 单精度浮点数。**不精确**，存在精度丢失问题。                 | `Float`            |
| `DOUBLE`          | 8 bytes             | 双精度浮点数。精度比 Float 高，但仍 **不精确**。             | `Double`           |
| `DECIMAL(M, D)`   | 变长 (取决于M)      | **定点数** (精确值)。M是总位数，D是小数位。**涉及金额/财务必用此类型**。 | `BigDecimal`       |

------

### 2. 字符串与二进制类型 (String & Binary Types)

重点区分：**`CHAR` 是定长（死板），`VARCHAR` 是变长（灵活）。**

| **数据类型** | **大小 (存储空间)** | **描述与应用场景**                                           | **对应 Java 类型** |
| ------------ | ------------------- | ------------------------------------------------------------ | ------------------ |
| `CHAR(M)`    | M bytes (0-255)     | **定长字符串**。如果你存 "A"，它也会占满 M 个空间。适合存固定长度数据 (如身份证、手机号、性别)。速度快但费空间。 | `String`           |
| `VARCHAR(M)` | 变长 (0-65535)      | **变长字符串**。存多少占多少+长度标识位。**开发中最常用的字符串类型** (如用户名、地址)。 | `String`           |
| `TINYTEXT`   | 0-255 bytes         | 短文本。                                                     | `String`           |
| `TEXT`       | 0-64 KB             | 长文本。适合存文章内容、评论、简介。                         | `String`           |
| `MEDIUMTEXT` | 0-16 MB             | 中长文本。适合存书的内容。                                   | `String`           |
| `LONGTEXT`   | 0-4 GB              | 极长文本。甚至可以把一整本百科全书存进去。                   | `String`           |
| `BLOB` 系列  | 变长                | 二进制大对象。用于存图片、音频等 (通常**不建议**直接存数据库，建议存文件路径)。 | `byte[]`           |
| `JSON`       | 变长                | **JSON 文档**。MySQL 5.7+ 支持。适合存非结构化数据，能直接解析 Key-Value。 | `String` / Object  |

------

### 3. 日期与时间类型 (Date & Time Types)

重点区分：**`TIMESTAMP` 会随时区变化，`DATETIME` 不会。**

| **数据类型** | **大小 (存储空间)** | **描述与应用场景**                                           | **对应 Java 类型**            |
| ------------ | ------------------- | ------------------------------------------------------------ | ----------------------------- |
| `DATE`       | 3 bytes             | 仅日期。格式：`YYYY-MM-DD`。如：生日 `1990-01-01`。          | `java.sql.Date` / `LocalDate` |
| `TIME`       | 3 bytes             | 仅时间。格式：`HH:MM:SS`。如：时长 `12:30:00`。              | `java.sql.Time` / `LocalTime` |
| `YEAR`       | 1 byte              | 年份。格式：`YYYY` (1901-2155)。                             | `Integer` / `Year`            |
| `DATETIME`   | 8 bytes             | **日期+时间**。范围：1000年到9999年。**绝对时间**，存进去是什么，取出来就是什么，不理会时区。 | `LocalDateTime`               |
| `TIMESTAMP`  | 4 bytes             | **时间戳**。范围：1970年到2038年。**涉及时区转换** (存进去会转成UTC，取出来转回当前时区)。适合记录“创建时间/修改时间”。 | `Timestamp` / `Instant`       |

---

# DML基础操作

### 增

**给指定字段添加数据**

```mysql
INSERT INTO 表名 (字段名1,字段名2,字段名3,...) VALUES (值1,值2,值3,...);
```

**给全部字段添加数据**

```mysql
INSERT INTO 表名 VALUES (值1,值2,值3,...);
```

**批量添加数据**

```mysql
INSERT INTO 表名 (字段名1,字段名2,字段名3,...) VALUES (值1,值2,值3,...),(值1,值2,值3,...),...;
```

```mysql
INSERT INTO 表名 VALUES (值1,值2,值3,...),(值1,值2,值3,...),(值1,值2,值3,...),...;
```



### 删

```mysql
DELETE FROM 表名 WHERE 条件
```

*注：*

*1.若不写where语句则是删除整张表的所有数据*

*2.delete不能删除某一个字段的值 可以用updata设置成null*

### 改

```mysql
UPDATA 表名 SET 字段名1 = 值1, 字段名2 = 值2, ... WHERE 条件;
```

*注：要是不写where语句则是修改整张表的字段的值*

---

# DQL基本操作

### 1.基本查询

**查询多个字段**

```mysql
SELECT 字段1 AS '别名',字段2 '别名',字段3,...FROM 表名;
-- 别名可以不写 如若想写别名显示 可以写AS也可不写
```

**去除重复记录**

```mysql
SELECT DISTINCT 字段列表 FROM 表名;
```

### 2.条件查询

**语法**

```mysql
SELECT 字段列表 FROM 表名 WHERE 条件列表;
```

**条件**

|        比较运算符         |                      功能                       |
| :-----------------------: | :---------------------------------------------: |
|             >             |                      大于                       |
|            >=             |                    大于等于                     |
|             <             |                      小于                       |
|            <=             |                    小于等于                     |
|             =             |                      等于                       |
|         <> 或 !=          |                     不等于                      |
| BETWEEN 最小值 AND 最大值 |          在某个范围之内(含最大最小值)           |
|          IN(...)          |           至少符合IN列表中一项的数据            |
|        LIKE 占位符        | 模糊匹配：'_'  : 任意一个字符  '%' : 任意个字符 |
|          IS NULL          |                     是NULL                      |

-----

| 逻辑运算符 | 功能 |
| :--------: | :--: |
| AND 或 &&  |  与  |
| OR 或 \|\| |  或  |
|  NOT 或！  |  非  |



### 3.聚合函数

`将一列数据作为一个整体 进行纵向计算`

| 函数  |   功能   |
| :---: | :------: |
| count | 统计数量 |
|  max  |  最大值  |
|  min  |  最小值  |
|  avg  |  平均值  |
|  sum  |   求和   |

**语法**

```mysql
SELECT 聚合函数(字符列表) FROM 表名;
```

*注：null值不参与聚合函数的运算！*

### 4.分组查询

**语法**

```mysql
SELECT 字段列表 FROM 表名 [WHERE 条件] GROUP BY 分组字段名 [HAVING 分组后的过滤条件];
```

**WHERE与HAVING的区别**

where是在分组之前进行的过滤 满足where条件的才可进行分组

having是分组之后进行的过滤



**执行顺序**

`where > 聚合函数 > having`

### 5.排序查询

**1.语法**

```mysql
SELECT 字段列表 FROM 表名 ORDER BY 字段1 排序方式1, 字段2 排序方式2...;
```

**2.排序方式**

1.升序：ASC（默认值）

2.降序：DESC

### 6.分页查询

**1.语法**

```mysql
SELECT 字段列表 FROM 表名 LIMIT 起始索引, 查询录数;
```

**2.示例**

若查询的数据每一页有十个数据，那么我查询第一页的代码是

`SELECT 字段列表 FROM 表名 LIMIT 0, 10;`

如果是第一页则`起始索引`可以省略：

`SELECT 字段列表 FROM 表名 LIMIT 10;`

查询第二页的代码为：

`SELECT 字段列表 FROM 表名 LIMIT 10, 10;`

查询第n页的`起始索引`可以通过`（页数 - 1）* 查询录数`计算得出

*注：索引是从0开始的！*

### 7.DQL的编写顺序

```mysql
SELECT
FROM
WHERE
GROUP BY
HAVING
ORDER BY
LIMIT
```

### 8.DQL的执行顺序

```mysql
FROM
WHERE
GROUP BY
HAVING
SELECT
ORDER BY
LIMIT
```



---

# 函数

### 1.字符串函数

```mysql
-- 字符串拼接
select concat('1','23'); -- 123

-- 转换为小写
select lower('Hello!'); -- hello!

-- 转换为大写
select upper('Hello!'); -- HELLO!

-- 左填充
select lpad('1',5,'0'); -- 00001

-- 右填充
select rpad('1',5,'0'); -- 10000

-- 去掉字符串头和尾的空格
select trim(' 1 2 3 '); -- 123

-- 截取字符串
select substr('123456',1,3); -- 123
```

### 2.数值函数

```mysql
-- 向上取整
select ceil(1.1); -- 2

-- 向下取整
select floor(1.9); -- 1

-- x/y的模
select mod(7,3); -- 1

-- 返回0~1内的随机数
select rand(); -- 0.05256707784958843

-- 把x四舍五入，保留y位小数
select round(1.578, 2); -- 1.58
```

### 3.日期函数

```mysql
-- 返回当前日期
select curdate(); -- 2026-01-13

-- 返回当前时间
select curtime(); -- 16:23:15

-- 返回当前日期和时间
select now(); -- 2026-01-13 16:24:00

-- 获取传入date的年份
select year(now()); -- 2026

-- 获取传入date的月份
select month(now()); -- 1

-- 获取传入date的日份
select day(now()); -- 13

-- 返回传入的日期加上传入的时间间隔之后的时间值 INTERVAL是固定值
select date_add(now(), INTERVAL 30 year); -- 2056-01-13 16:26:51

-- 返回两个时间之间的间隔
select datediff(now(), '2007-6-4'); -- 6798
```

### 4.流程函数

|                        函数                         |                       功能                       |
| :-------------------------------------------------: | :----------------------------------------------: |
|                   if(value, t, f)                   |        如果value为true，返回t，否则返回f         |
|              ifnull(value 1, value 2)               | 如果value 1不为空则返回value 1，否则返回value 2  |
|  case when [val1] then [res1]...else[default] end   | 如果val1为true,返回res1,...否则返回default默认值 |
| case [expr] when [val1] then [res1]...else[def] end |   如果expr的值等于val1,返回res1,...否则返回def   |

---

# 多表查询例题

```mysql
-- ------------------------------------> 多表查询 <--------------------------------------------
-- 准备数据
create table dept(
                     id   int auto_increment comment 'ID' primary key,
                     name varchar(50) not null comment '部门名称'
)comment '部门表';

create table emp(
                    id  int auto_increment comment 'ID' primary key,
                    name varchar(50) not null comment '姓名',
                    age  int comment '年龄',
                    job varchar(20) comment '职位',
                    salary int comment '薪资',
                    entrydate date comment '入职时间',
                    managerid int comment '直属领导ID',
                    dept_id int comment '部门ID'
)comment '员工表';

-- 添加外键
alter table emp add constraint fk_emp_dept_id foreign key (dept_id) references dept(id);

INSERT INTO dept (id, name) VALUES (1, '研发部'), (2, '市场部'),(3, '财务部'), (4, '销售部'), (5, '总经办'), (6, '人事部');
INSERT INTO emp (id, name, age, job,salary, entrydate, managerid, dept_id) VALUES
                                                                               (1, '金庸', 66, '总裁',20000, '2000-01-01', null,5),

                                                                               (2, '张无忌', 20, '项目经理',12500, '2005-12-05', 1,1),
                                                                               (3, '杨逍', 33, '开发', 8400,'2000-11-03', 2,1),
                                                                               (4, '韦一笑', 48, '开发',11000, '2002-02-05', 2,1),
                                                                               (5, '常遇春', 43, '开发',10500, '2004-09-07', 3,1),
                                                                               (6, '小昭', 19, '程序员鼓励师',6600, '2004-10-12', 2,1),

                                                                               (7, '灭绝', 60, '财务总监',8500, '2002-09-12', 1,3),
                                                                               (8, '周芷若', 19, '会计',48000, '2006-06-02', 7,3),
                                                                               (9, '丁敏君', 23, '出纳',5250, '2009-05-13', 7,3),

                                                                               (10, '赵敏', 20, '市场部总监',12500, '2004-10-12', 1,2),
                                                                               (11, '鹿杖客', 56, '职员',3750, '2006-10-03', 10,2),
                                                                               (12, '鹤笔翁', 19, '职员',3750, '2007-05-09', 10,2),
                                                                               (13, '方东白', 19, '职员',5500, '2009-02-12', 10,2),

                                                                               (14, '张三丰', 88, '销售总监',14000, '2004-10-12', 1,4),
                                                                               (15, '俞莲舟', 38, '销售',4600, '2004-10-12', 14,4),
                                                                               (16, '宋远桥', 40, '销售',4600, '2004-10-12', 14,4),
                                                                               (17, '陈友谅', 42, null,2000, '2011-10-12', 1,null);
-- ---------------------------------------> 多表查询案例 <----------------------------------
create table salgrade(
                         grade int,
                         losal int,
                         hisal int
) comment '薪资等级表';

insert into salgrade values (1,0,3000);
insert into salgrade values (2,3001,5000);
insert into salgrade values (3,5001,8000);
insert into salgrade values (4,8001,10000);
insert into salgrade values (5,10001,15000);
insert into salgrade values (6,15001,20000);
insert into salgrade values (7,20001,25000);
insert into salgrade values (8,25001,30000);

-- 1. 查询员工的姓名、年龄、职位、部门信息 （隐式内连接）
select e.name,e.age,e.job,d.name from emp e left join dept d on e.dept_id = d.id;

select e.name,e.age,e.job,d.name from emp e , dept d where e.dept_id = d.id;


-- 2. 查询年龄小于30岁的员工的姓名、年龄、职位、部门信息（显式内连接）
select e.name,e.age,e.job,d.name from (select * from emp where emp.age < 30) e left join dept d on e.dept_id = d.id;
select e.name,e.age,e.job,d.name from emp e join dept d on e.dept_id = d.id where e.age < 30;

-- 3. 查询拥有员工的部门ID、部门名称
select distinct d.id,d.name from emp e , dept d where e.dept_id = d.id;

-- 4. 查询所有年龄大于40岁的员工, 及其归属的部门名称; 如果员工没有分配部门, 也需要展示出来
select e.*,d.name from emp e left join dept d on e.dept_id = d.id where e.age > 40;

-- 5. 查询所有员工的工资等级
select e.*,s.grade from emp e,salgrade s where e.salary >= s.losal and e.salary <= s.hisal;
select e.*,s.grade from emp e,salgrade s where e.salary between s.losal and s.hisal;

-- 6. 查询 "研发部" 所有员工的信息及 工资等级
select e.*,d.name,s.grade
from
    emp e, dept d, salgrade s
where
    e.dept_id = d.id and e.salary between s.losal and s.hisal and d.name = '研发部';

-- 7. 查询 "研发部" 员工的平均工资
select
    avg(e.salary)
from
    emp e, dept d
where
    e.dept_id = d.id and
    d.name = '研发部';

-- 8. 查询工资比 "灭绝" 高的员工信息。
select
    *
from
    emp e
where
    e.salary > (select e.salary from emp e where e.name = '灭绝');

-- 9. 查询比平均薪资高的员工信息
select
    *
from
    emp
where
    salary > (select avg(salary) from emp);

-- 10. 查询低于本部门平均工资的员工信息
select *
from emp e1
where
    e1.salary < (select avg(e.salary) from emp e where e.dept_id = e1.dept_id);

-- 11. 查询所有的部门信息, 并统计部门的员工人数
select d.*, (select count(*) from emp e where e.dept_id = d.id) '人数' from dept d;

select d.id,d.name,count(e.id) from dept d left join emp e on d.id = e.dept_id group by d.id,d.name;
```

---

