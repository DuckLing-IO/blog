// ============================================================
//  文章配置 — 在数组尾部添加新文章，页面自动按最新在前显示
//  文章内容由 post/文章名/ 下的 HTML 文件全权渲染
// ============================================================

const articles = [
  {
    id: 'SpringBoot-注解-Transactional',
    title: '[SpringBoot]注解@Transactional',
    date: '2026-01-27 14:19'
  },
  {
    id: 'SpringBoot-注解-Options',
    title: '[SpringBoot]注解@Options',
    date: '2026-01-27 12:24'
  },
  {
    id: 'SpringBoot-学习杂记260128',
    title: '[SpringBoot]学习杂记260128',
    date: '2026-01-29 23:30'
  },
  {
    id: 'SpringBoot-前端请求参数的接收方式',
    title: '[SpringBoot]前端请求参数的接收方式',
    date: '2026-01-27 10:44'
  },
  {
    id: 'SpringBoot-分层解耦',
    title: '[SpringBoot]三层框架的分层解耦',
    date: '2026-01-24 14:39'
  },
  {
    id: 'SpringBoot-PageHelper插件',
    title: '[SpringBoot]PageHelper插件',
    date: '2026-01-27 14:19'
  },
  {
    id: 'SpringBoot-AOP',
    title: '[SpringBoot]AOP',
    date: '2026-01-30 16:16'
  },
  {
    id: 'MySQL-锁',
    title: '[MySQL]锁',
    date: '2026-01-24 11:21'
  },
  {
    id: 'MySQL-索引',
    title: '[MySQL]索引',
    date: '2026-01-24 11:21'
  },
  {
    id: 'MySQL-视图-触发器',
    title: '[MySQL]视图&触发器',
    date: '2026-01-24 11:21'
  },
  {
    id: 'HTTP常见响应状态码',
    title: 'HTTP常见响应状态码',
    date: '2026-01-24 11:21'
  },
  {
    id: '26.5.5',
    title: '【每日算法】修复公路',
    date: '2026-05-05 22:49'
  },
  {
    id: '26.5.8-1',
    title: '【每日算法】P3958奶酪',
    date: '2026-05-08 19:34'
  },
  {
    id: '26.5.8-2',
    title: '【每日算法】P1525关押罪犯',
    date: '2026-05-08 19:35'
  },
  {
    id: '26.5.9',
    title: '[每日算法] P1048 [NOIP 2005 普及组] 采药',
    date: '2026-05-09 20:34'
  },
  {
    id: '26.5.10_1',
    title: '[每日算法]P1776 宝物筛选',
    date: '2026-05-10 10:34'
  },
  {
    id: '26.5.10_2',
    title: '[每日算法]P2347 [NOIP 1996 提高组] 砝码称重',
    date: '2026-05-10 11:23'
  },
  {
    id: '26.5.10_3',
    title: '[每日算法]P12210 [蓝桥杯 2023 国 Python B] 背包问题',
    date: '2026-05-10 15:41'
  },
  {
    id: '26.5.10_4',
    title: '[每日算法]P12208 [蓝桥杯 2023 国 Python B] 偶串',
    date: '2026-05-10 15:58'
  },
  {
    id: '26.5.12_1',
    title: '[每日算法]P1918 保龄球',
    date: '2026-05-12 11:55'
  },
  {
    id: '26.5.12_2',
    title: '[每日算法]P5266 【深基17.例6】学籍管理',
    date: '2026-05-12 21:12'
  },
  {
    id: '26.5.12_3',
    title: '[每日算法]P5250 【深基17.例5】木材仓库',
    date: '2026-05-12 21:12'
  },
  {
    id: '26.5.12_4',
    title: '[每日算法]U535982 C-小梦的AB交换',
    date: '2026-05-12 21:13'
  },
  {
    id: '26.5.12_5',
    title: '[每日算法]B3612 【深进1.例1】求区间和',
    date: '2026-05-12 21:14'
  },
  {
    id: 'P1101_单词方阵',
    title: '[每日算法]P1101 单词方阵',
    date: '2026-05-15 21:24'
  },
  {
    id: 'P2036_[COCI_20082009_#2]_PERKET',
    title: '[每日算法]P2036 [COCI 2008/2009 #2] PERKET',
    date: '2026-05-15 21:24'
  },
  {
    id: 'P1464_[PacNW_1999]_Function',
    title: '[每日算法]P1464 [PacNW 1999] Function',
    date: '2026-05-15 21:24'
  },
  {
    id: 'P8649_[蓝桥杯_2017_省_B]_k_倍区间',
    title: '[每日算法]P8649 [蓝桥杯 2017 省 B] k 倍区间',
    date: '2026-05-15 21:24'
  },
  {
    id: 'P3131_[USACO16JAN]_Subsequences_Summing_to_Sevens_S',
    title: '[每日算法]P3131 [USACO16JAN] Subsequences Summing to Sevens S',
    date: '2026-05-15 21:24'
  },
  {
    id: 'CF816B_Karen_and_Coffee',
    title: '[每日算法]CF816B Karen and Coffee',
    date: '2026-05-15 21:23'
  },
  {
    id: 'B3693_数列前缀和_4',
    title: '[每日算法]B3693 数列前缀和 4',
    date: '2026-05-15 21:23'
  },
  {
    id: 'P1135_奇怪的电梯',
    title: '[每日算法]P1135 奇怪的电梯',
    date: '2026-05-15 21:22'
  }
]
