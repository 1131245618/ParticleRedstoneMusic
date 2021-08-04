特效红石音乐通用生成器 Demo.2.2

运行要求：python 3, 安装了mido库即可，同时须在游戏内安装AnotherColorBlock和midiout模组，游戏版本1.12

运行方法：把整个文件放入我的世界存档的functions文件夹下。(.minecraft/saves/{Your World}/data/functions/)

使用的第三方库：medit_4的noteMsg和sequence(https://github.com/xuetaolu/python-in-minecraft) 位于xuetaolu文件夹中;  
               mido(https://mido.readthedocs.io/en/latest/) 需自行下载

文件夹结构：
..
└─functions
    ├─_seq
    ├─pulgins
    │  └─__pycache__
    ├─particle
    │  └─__pycache__
    ├─example
    ├─midi
    └─sc

particle里是程序主要脚本
pulgins里是插件(?)，用于自定义生成粒子线的函数
midi就是放.midi文件的地方
其他的文件夹是放我的世界function文件的，这个脚本只直接生成粒子线的效果，粒子线之外的特效需由mcfunction文件实现。
运行main.py进行生成，之后进入游戏运行function sc:begin即可播放
根据json文件计算各个轨道不同时间的粒子效果
json文件和midi文件的路径config文件中设置

mido的安装：控制台输入 pip install mido
