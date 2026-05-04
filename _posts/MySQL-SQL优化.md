---
title: "[MySQL]优化"  # 文章标题
date: 2026-01-15 23:18:15  # 创建时间 (自动生成的)
# updated: 2026-01-16 10:00:00 # 更新时间 (可选)

# 👇 分类 (支持多级，比如：后端 -> Java)
categories:
  - [数据库, MySQL]
  - [学习笔记, 数据库, MySQL]

# 👇 标签 (扁平化，随便写)
tags:
  - 学习笔记
  - MySQL
  - 数据库

# 👇 封面图设置 (这就是你要的“文章标题图片”)
# cover: 首页卡片上显示的缩略图
cover: /img/MySQL-Logo.png
# top_img: 点进文章后，顶部那个巨大的背景图 (通常和cover用同一张)
top_img: /img/home.jpg

# 👇 评论开关 (默认是开启的，想关闭就写 false)
comments: true
---

### 1. 插入数据优化 (Insert Optimization)

**核心目标：** 减少磁盘I/O交互次数，降低日志刷新频率。

- 批量插入 (Batch Insert):

  不要使用多条 INSERT INTO 语句，合并为一条。

  ```
  -- 推荐
  INSERT INTO tb_test VALUES (1,'a'), (2,'b'), (3,'c');
  ```

- 手动事务控制 (Manual Transaction):

  如果插入数据量大（例如几千条），不要让数据库自动提交事务。手动开启事务，执行完后一次提交。

  ```
  START TRANSACTION;
  INSERT ...;
  INSERT ...;
  COMMIT;
  ```

- 主键顺序插入:

  数据按照主键顺序插入效率最高，减少由于页分裂 (Page Split) 带来的性能损耗。

- 大批量导入 (Load Data):

  对于百万级以上数据，使用 LOAD DATA INFILE 指令，性能远超 INSERT。

  ```
  LOAD DATA LOCAL INFILE '/path/to/data.sql' INTO TABLE tb_user ...;
  ```

  示例：

  ```mysql
  load data local infile '/root/load_user_100w_sort.sql' into table tb_user fields terminated by ',' lines terminated by '\n';
  -- fields terminated by ','是每个数据以','进行分割
  -- lines terminated by '\n'是每行数据以换行符进行分割
  -- 具体分割方式依照要导入的数据排列方式而定
  ```

  

------

### 2. 主键优化 (Primary Key Optimization)

**核心目标：** 维护B+树结构的稳定，减少空间浪费。

- **主键长度:** 越短越好。二级索引的叶子节点存储的是主键值，主键越长，二级索引占用空间越大，IO效率越低。
- **自增主键 (Auto-increment):** 强烈建议使用自增ID。
  - **优势:** 顺序写入，数据直接追加到当前页，写满申请新页。
  - **避免:** 尽量避免使用 UUID 做主键。UUID 无序且长，会导致频繁的**页分裂**（Page Split）和**页合并**，造成大量的磁盘随机IO和碎片。
- **避免修改主键:** 修改主键相当于删除旧记录+插入新记录，代价极高。

------

### 3. Order By 优化

**核心目标:** 使用 `Using index` (索引排序)，避免 `Using filesort` (文件排序)。

- **全值匹配/最左前缀:** 排序字段必须符合索引的最左前缀法则。
- **覆盖索引:** `SELECT` 的字段和 `ORDER BY` 的字段最好都能包含在索引中，避免回表查询。
- **升降序一致性:**
  - 索引默认为 ASC。如果查询 `ORDER BY a ASC, b DESC`，在 MySQL 8.0 之前会导致 Filesort。
  - **优化:** 创建联合索引时直接指定排序规则: `CREATE INDEX idx_a_b ON table(a ASC, b DESC);`
- **Filesort 兜底:** 如果不得不发生 Filesort，且数据量大，尝试增加 `sort_buffer_size` 参数，避免使用磁盘临时文件进行排序。

------

### 4. Group By 优化

**核心目标:** 利用索引结构直接分组，避免创建临时表。

- **索引法则:** 与 Order By 一致，严格遵循最左前缀法则。
- **Where 优于 Having:** 能在分组前通过 `WHERE` 过滤掉的数据，尽量不要留到 `HAVING` 中过滤。减少参与分组计算的数据量是第一原则。

------

### 5. Limit 优化 (分页优化)

**核心目标:** 解决深度分页（Deep Pagination）时的全表扫描问题。

**问题场景:** `LIMIT 2000000, 10`。MySQL 需要排序并读取前 2,000,010 条记录，丢弃前 200万条，仅返回最后 10 条。

- 方案一：覆盖索引 + 子查询 (推荐)

  先在索引中快速找到对应的 ID（避免回表），然后再通过 ID 关联主表获取详情。

  ```
  -- 优化前
  SELECT * FROM tb_sku LIMIT 2000000, 10;
  
  -- 优化后
  SELECT t.* FROM tb_sku t,
  (SELECT id FROM tb_sku ORDER BY id LIMIT 2000000, 10) a
  WHERE t.id = a.id;
  ```

- 方案二：锚点定位 (适用连续ID)

  如果ID是连续的且可以推断，直接用 Where 过滤。

  ```
  SELECT * FROM tb_sku WHERE id > 2000000 LIMIT 10;
  ```

------

### 6. Count 优化

**核心目标:** 了解不同 Count 写法的性能差异 (InnoDB 引擎)。

- **性能排序:** `count(*) ≈ count(1) > count(主键) > count(字段)`
- **原理区别:**
  - **count(字段):** 会遍历全表，**不计算 NULL 值**。如果字段没有 `NOT NULL` 约束，还要一行行判断是否为 NULL，最慢。
  - **count(主键):** 遍历全表，取出主键，累加。
  - **count(\*):** MySQL 做了专门优化，不取值，直接按行累加。InnoDB 会自动选择最小的二级索引进行遍历（成本最低）。
- **建议:** 总是使用 `count(*)`。
- **超大数据量:** 如果需要频繁查询千万级数据的总数且允许微小误差，使用 `EXPLAIN` 的 `rows` 值估算；要求精确则需自己在 Redis 或计数表中维护计数。

------

### 7. Update 优化

**核心目标:** 避免**行锁 (Row Lock)** 升级为 **表锁 (Table Lock)**。

- **索引是关键:** InnoDB 的行锁是加在**索引**上的，而不是加在记录上的。

- **必须走索引:**

  - 如果 `UPDATE` 语句的 `WHERE` 条件字段**建立了索引**，InnoDB 会锁定对应的行（行锁），并发性能好。
  - 如果 `WHERE` 条件字段**没有索引**（或索引失效），InnoDB 将被迫锁住整张表（表锁），导致其他事务无法操作该表，严重阻塞业务。

  ```
  -- 假设 name 字段没有索引
  -- 这条语句会锁住整张表！
  UPDATE student SET name = 'NewName' WHERE name = 'OldName';
  ```

------

