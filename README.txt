特效红石音乐通用生成器 Demo.2

开发者: zlc_3

运行要求：python 3, 安装了mido库即可，同时须在游戏内安装AnotherColorBlock这一模组,游戏版本1.12.2

使用的第三方库：medit_4的noteMsg和sequence(https://github.com/xuetaolu/python-in-minecraft) 已经在builder文件夹里了;  
               mido(https://mido.readthedocs.io/en/latest/) 需自行下载

文件夹结构：
..
└─functions
    ├─_seq
    ├─added
    │  └─__pycache__
    ├─builder
    │  └─__pycache__
    ├─example
    ├─midi
    └─sc

builder里是程序主要脚本
added里是插件(?)，用于自定义生成粒子线的函数
midi就是放.midi文件的地方
其他的文件夹是放我的世界function文件的
运行main.py进行生成，之后进入游戏运行function sc:begin即可播放
使用一个json文件和一个midi文件来输入
json文件和midi文件的路径和播放速度在config文件中设置
json文件的写法暂时不详细介绍
插件的写法暂时不详细介绍
