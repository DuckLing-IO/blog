---
title: '[JavaScript]JS入门'
date: 2026-01-19 16:23:34
tags:
  - 学习笔记
  - 前端
  - JavaScript
categories:
  - [前端, JavaScript]
  - [学习笔记, 前端, JavaScript]
top_img: /img/home.jpg
cover: /img/post_js-logo.png
---

# JavaScript 入门

---

## 1.HTML引入方式

### 1.1 内部脚本

将JS代码定义在HTML页面中

- JavaScript代码必须位于&lt;script&gt;&lt;/script&gt;标签之间
- 在HTML文档中，可以在任意地方，放置任意数量的&lt;script&gt;
- 一般会把脚本置于&lt;body&gt;元素的底部，可改善显示速度

例子：

~~~html
<script>
    alert("Hello JavaScript")
</script>
~~~

### 1.2 外部脚本

JS代码定义在外部 JS文件中，然后引入到 HTML页面中

- 外部JS文件中，只包含JS代码，不包含&ltscript&gt;标签
- 引入外部js的&lt;script&gt;标签，必须是双标签

例子：

~~~html
<script src="js/demo.js"></script>
~~~

*注意：demo.js中只有js代码，没有&lt;script&gt;标签*

---

## 2.基本语法

### 2.1 书写语法

- 区分大小写

- 每行结尾的分号可有可无

- 大括号表示代码块

- 注释：

  1. 单行注释：`// 注释内容`

  2. 多行注释：`/* 注释内容 */`

### 2.2 基本输出语句

| api              | 描述             |
| ---------------- | ---------------- |
| window.alert()   | 警告框           |
| document.write() | 在HTML 输出内容  |
| console.log()    | 写入浏览器控制台 |

### 2.3 变量

**JavaScript作为一门弱类型语言，其中的变量与常规编译型语言的变量大有不同<br>**
主要通过以下三个关键字来声明变量：

| 关键字 | 解释                                                         |
| ------ | ------------------------------------------------------------ |
| var    | 早期ECMAScript5中用于变量声明的关键字                        |
| let    | ECMAScript6中新增的用于变量声明的关键字，相比较var，let只在代码块内生效 |
| const  | 声明常量的，常量一旦声明，不能修改                           |

注意如下几点：

- JavaScript 中变量可以存放不同类型的值

- 变量名需要遵循如下规则：

  1. 组成字符可以是任何字母、数字、下划线（_）或美元符号（$）

  - 数字不能开头
  - 建议使用驼峰命名

**JS中 `0` | `null` | `undefined` | `""` | `NaN` 理解成false,反之理解成true**

### 2.4 数据类型

JS中的数据类型主要分为**原始类型**和**引用类型**

#### 2.4.1 原始数据类型

| 数据类型  | 描述                                               |
| --------- | -------------------------------------------------- |
| number    | 数字（整数、小数、NaN(Not a Number)）              |
| string    | 字符串，单双引皆可                                 |
| boolean   | 布尔。true，false                                  |
| null      | 对象为空                                           |
| undefined | 当声明的变量未初始化时，该变量的默认值是 undefined |

Object（对象）：最基础的引用类型，包含普通对象、数组、函数、日期、正则等，具体细分：

- 普通对象：{ name: '张三', age: 20 }
- 数组（Array）：[1, 2, 3]
- 函数（Function）：function() {}、() => {}
- 日期（Date）：new Date()
- 正则（RegExp）：/abc/
- 其他（如 Map、Set、Error 等）

### 2.5 运算符

JS中的运算符大体与JAVA或CPP一致

| 运算规则   | 运算符                                                       |
| ---------- | ------------------------------------------------------------ |
| 算术运算符 | + , - , * , / , % , ++ , --                                  |
| 赋值运算符 | = , += , -= , *= , /= , %=                                   |
| 比较运算符 | &gt; , < , >= , <= , != , == , ===   注意     == 会进行类型转换，=== 不会进行类型转换 |
| 逻辑运算符 | && , \|\| , !                                                |
| 三元运算符 | 条件表达式 ? true_value: false_value                         |

## 3.函数

### 3.1 第一种定义方式

第一种定义格式如下：

~~~js
function 函数名(参数1,参数2..){
    要执行的代码
}
~~~

因为JavaScript是弱数据类型的语言，所以有如下几点需要注意：

- 形式参数不需要声明类型，并且JavaScript中不管什么类型都是let或者var去声明，加上也没有意义。
- 返回值也不需要声明类型，直接return即可

如下示例：

~~~js
function add(a, b){
    return a + b;
}
~~~

### 3.2 第二种定义方式

第二种可以通过var去定义函数的名字，具体格式如下：

~~~js
var functionName = function (参数1,参数2..){   
	//要执行的代码
}
~~~

## 4.JavaScript对象

**JavaScript对象可以大体分页3大类**

### 4.1基本对象

#### 4.1.1 Array对象

##### 语法格式

Array对象时用来定义数组的。常用语法格式有如下2种：

方式1：

~~~js
var 变量名 = new Array(元素列表); 
~~~

例如：

~~~js
var arr = new Array(1,2,3,4); //1,2,3,4 是存储在数组中的数据（元素）
~~~



方式2：

~~~js
var 变量名 = [ 元素列表 ]; 
~~~

例如：

~~~js
var arr = [1,2,3,4]; //1,2,3,4 是存储在数组中的数据（元素）
~~~

数组定义好了，那么我们该如何获取数组中的值呢？和java中一样，需要通过索引来获取数组中的值。语法如下：

~~~js
arr[索引] = 值;
~~~

##### 特点

`JavaScript`数组的长度是可以变化的，而且数组中可以存储任意数据类型的值

##### 属性和方法

Array作为一个对象，那么对象是有属性和方法的，所以接下来我们介绍一下Array对象的属性和方法

官方文档中提供了Array的很多属性和方法，但是我们只学习常用的属性和方法，如下图所示：

属性：

| 属性   | 描述                         |
| :----- | :--------------------------- |
| length | 设置或返回数组中元素的数量。 |

方法：

| 方法方法  | 描述                                             |
| :-------- | :----------------------------------------------- |
| forEach() | 遍历数组中的每个有值得元素，并调用一次传入的函数 |
| push()    | 将新元素添加到数组的末尾，并返回新的长度         |
| splice()  | 从数组中删除元素                                 |

- length属性：

  length属性可以用来获取数组的长度，所以我们可以借助这个属性，来遍历数组中的元素，添加如下代码：

  ~~~js
  var arr = [1,2,3,4];
  arr[10] = 50;
  	for (let i = 0; i < arr.length; i++) {
  	console.log(arr[i]);
  }
  ~~~

  - forEach()函数

    首先我们学习forEach()方法，顾名思义，这是用来遍历的，那么遍历做什么事呢？所以这个方法的参数，需要传递一个函数，而且这个函数接受一个参数，就是遍历时数组的值。修改之前的遍历代码如下：

    ~~~js
    //e是形参，接受的是数组遍历时的值
    arr.forEach(function(e){
         console.log(e);
    })
    ~~~

    在ES6中，引入箭头函数的写法，语法类似java中lambda表达式，修改上述代码如下：

    ~~~js
    arr.forEach((e) => {
         console.log(e);
    }) 
    ~~~

    *没有元素的内容是不会输出的，因为forEach只会遍历有值的元素*

- push()函数

  push()函数是用于向数组的末尾添加元素的，其中函数的参数就是需要添加的元素，编写如下代码：向数组的末尾添加3个元素

  ~~~js
  //push: 添加元素到数组末尾
  arr.push(7,8,9);
  console.log(arr);
  ~~~

  

- splice()函数

  splice()函数用来数组中的元素，函数中填入2个参数。

  参数1：表示从哪个索引位置删除

  参数2：表示删除元素的个数

  如下代码表示：从索引2的位置开始删，删除2个元素

  ~~~js
  //splice: 删除元素
  arr.splice(2,2);
  console.log(arr);
  ~~~

  

#### 4.1.2 String对象

##### 语法格式

String对象的创建方式有2种：

方式1：

~~~js
var 变量名 = new String("…") ; //方式一
~~~

例如：

~~~js
var str = new String("Hello String");
~~~



方式2：

~~~js
var 变量名 = "…" ; //方式二
~~~

例如：

~~~js
var str = 'Hello String';
~~~

##### 性和方法

String对象也提供了一些常用的属性和方法，如下表格所示：

属性：

| 属性   | 描述           |
| ------ | -------------- |
| length | 字符串的长度。 |

方法：

| 方法        | 描述                                     |
| ----------- | ---------------------------------------- |
| charAt()    | 返回在指定位置的字符。                   |
| indexOf()   | 检索字符串。                             |
| trim()      | 去除字符串两边的空格                     |
| substring() | 提取字符串中两个指定的索引号之间的字符。 |

- length属性：

  length属性可以用于返回字符串的长度，添加如下代码：

  ~~~js
  //length
  console.log(str.length);
  ~~~

- charAt()函数：

  charAt()函数用于返回在指定索引位置的字符，函数的参数就是索引。添加如下代码：

  ~~~js
  console.log(str.charAt(4));
  ~~~

- indexOf()函数

  indexOf()函数用于检索指定内容在字符串中的索引位置的，返回值是索引，参数是指定的内容。添加如下代码：

  ~~~js
  console.log(str.indexOf("lo"));
  ~~~

- trim()函数

  trim()函数用于去除字符串两边的空格的。添加如下代码：

  ~~~js
  var s = str.trim();
  console.log(s.length);
  ~~~

- substring()函数

  substring()函数用于截取字符串的，函数有2个参数。

  参数1：表示从那个索引位置开始截取。包含

  参数2：表示到那个索引位置结束。不包含

  ~~~js
  console.log(s.substring(0,5));
  ~~~

#### 4.1.3 JSON对象

##### 自定义对象

在 JavaScript 中自定义对象特别简单，其语法格式如下：

~~~js
var 对象名 = {
    属性名1: 属性值1, 
    属性名2: 属性值2,
    属性名3: 属性值3,
    函数名称: function(形参列表){}
};

~~~

我们可以通过如下语法调用属性：

~~~js
对象名.属性名
~~~

通过如下语法调用函数：

~~~js
对象名.函数名()
~~~

示例：

~~~html
<script>
    //自定义对象
    var user = {
        name: "张三",
        age: 18,
        gender: "male",
        eat: function(){
             console.log("正在吃饭");
         }
    }

    console.log(user.name);
    user.eat();
<script>
~~~



其中上述函数定义的语法可以简化成如下格式：

~~~js
    var user = {
        name: "张三",
        age: 18,
        gender: "male",
        eat(){
            console.log("正在吃饭");
        }
    }
~~~



##### json对象

JSON对象：**J**ava**S**cript **O**bject **N**otation，JavaScript对象标记法。是通过JavaScript标记法书写的文本。其格式如下：

~~~js
{
    "key":value,
    "key":value,
    "key":value
}
~~~

其中，**key必须使用引号并且是双引号标记，value可以是任意数据类型。**

`JSON`经常用来作为前后台交互的数据载体

###### json字符串和json对象的转换

~~~js
var obj = JSON.parse(jsonstr);
alert(obj.name); 
~~~



~~~js
alert(JSON.stringify(obj)); 
~~~

### 4.2 BOM对象

BOM中提供了如下5个对象：

| 对象名称  | 描述           |
| :-------- | :------------- |
| Window    | 浏览器窗口对象 |
| Navigator | 浏览器对象     |
| Screen    | 屏幕对象       |
| History   | 历史记录对象   |
| Location  | 地址栏对象     |

#### 4.2.1 Window对象

window对象指的是浏览器窗口对象，是JavaScript的全部对象，所以对于window对象，我们可以直接使用，并且对于window对象的方法和属性，我们可以省略window.

~~~
window.alert('hello');
~~~

其可以省略window.  所以可以简写成

~~~
alert('hello')
~~~

所以对于window对象的属性和方法，我们都是采用简写的方式。window提供了很多属性和方法，下表列出了常用属性和方法

window对象提供了获取其他BOM对象的属性：

| 属性      | 描述                  |
| --------- | --------------------- |
| history   | 用于获取history对象   |
| location  | 用于获取location对象  |
| Navigator | 用于获取Navigator对象 |
| Screen    | 用于获取Screen对象    |

也就是说我们要使用location对象，只需要通过代码`window.location`或者简写`location`即可使用

window也提供了一些常用的函数，如下表格所示：

| 函数          | 描述                                               |
| ------------- | -------------------------------------------------- |
| alert()       | 显示带有一段消息和一个确认按钮的警告框。           |
| comfirm()     | 显示带有一段消息以及确认按钮和取消按钮的对话框。   |
| setInterval() | 按照指定的周期（以毫秒计）来调用函数或计算表达式。 |
| setTimeout()  | 在指定的毫秒数后调用函数或计算表达式。             |

- alert()函数：弹出警告框，函数的内容就是警告框的内容

  ~~~html
  <script>
      //window对象是全局对象，window对象的属性和方法在调用时可以省略window.
      window.alert("Hello BOM");
      alert("Hello BOM Window");
  </script>
  ~~~

- confirm()函数：弹出确认框，并且提供用户2个按钮，分别是确认和取消。

  ~~~js
  confirm("您确认删除该记录吗?");
  ~~~

  该函数有一个返回值，当用户点击确认时，返回true，点击取消时，返回false。我们根据返回值来决定是否执行后续操作。修改代码如下：再次运行，可以查看返回值true或者false

  ~~~js
  var flag = confirm("您确认删除该记录吗?");
  alert(flag);
  ~~~

- setInterval(fn,毫秒值)：定时器，用于周期性的执行某个功能，并且是**循环执行**。该函数需要传递2个参数：

  fn:函数，需要周期性执行的功能代码

  毫秒值：间隔时间

  ~~~js
  //定时器 - setInterval -- 周期性的执行某一个函数
  var i = 0;
  setInterval(function(){
       i++;
       console.log("定时器执行了"+i+"次");
  },2000);
  ~~~

   

- setTimeout(fn,毫秒值) ：定时器，只会在一段时间后**执行一次功能**。参数和上述setInterval一致

  ~~~js
  //定时器 - setTimeout -- 延迟指定时间执行一次 
  setTimeout(function(){
  	alert("JS");
  },3000);
  ~~~

  浏览器打开，3s后弹框，关闭弹框，发现再也不会弹框了。



#### 4.2.2 Location对象

location是指代浏览器的地址栏对象，对于这个对象，我们常用的是href属性，用于获取或者设置浏览器的地址信息



### 4.3 DOM对象

#### 4.3.1 DOM介绍

DOM：Document Object Model 文档对象模型。也就是 JavaScript 将 HTML 文档的各个组成部分封装为对象。

- Document：整个文档对象
- Element：元素对象
- Attribute：属性对象
- Text：文本对象
- Comment：注释对象

主要作用如下：

- 改变 HTML 元素的内容
- 改变 HTML 元素的样式（CSS）
- 对 HTML DOM 事件作出反应
- 添加和删除 HTML 元素



#### 4.3.2 获取DOM对象

HTML中的Element对象可以通过Document对象获取，而Document对象是通过window对象获取的。document对象提供的用于获取Element元素对象的api如下表所示：

| 函数                              | 描述                                     |
| --------------------------------- | ---------------------------------------- |
| document.getElementById()         | 根据id属性值获取，返回单个Element对象    |
| document.getElementsByTagName()   | 根据标签名称获取，返回Element对象数组    |
| document.getElementsByName()      | 根据name属性值获取，返回Element对象数组  |
| document.getElementsByClassName() | 根据class属性值获取，返回Element对象数组 |

---