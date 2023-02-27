# SZTU教务系统-全自动检测抢课(Beta)

## 部署此脚本，你需要安装下面这些组件

### Python库

```
Selenium 版本>= 4.0 (老版本的selenium语法不同没有适配)
Schedule
```

您可以通过以下方法安装这些库

1. 使用Pycharm的图形化界面，在解释器面板下载包

2. 使用pip，你可以使用如下命令：

   ```python
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple selenium
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple Schedule
   ```

### 还需要在脚本py文件的同目录下，创建名为chromedriver文件夹，

### 并将与你本地Chrome浏览器版本相应的Chromedriver软件下载

文件夹名 **必须** 为 chromedriver

![Screen Shot 2023-02-27 at 12.50.43 PM](/Users/oplin/Documents/project_in_giithub/SZTU-CatchLesson/Screen Shot 2023-02-27 at 12.50.43 PM.png)

可以通过以下两个网站下载到需要的chromedriver

```
http://chromedriver.storage.googleapis.com/index.html
http://npm.taobao.org/mirrors/chromedriver/
```

在本地Chrome的设置中即可看到自己的Chrome版本

![Screen Shot 2023-02-27 at 12.53.48 PM](/Users/oplin/Documents/project_in_giithub/SZTU-CatchLesson/Screen Shot 2023-02-27 at 12.53.48 PM.png)

最后将压缩包下载到chromedriver文件夹中解压，并将exe文件命名为chromedriver.exe

![Screen Shot 2023-02-27 at 12.54.50 PM](/Users/oplin/Documents/project_in_giithub/SZTU-CatchLesson/Screen Shot 2023-02-27 at 12.54.50 PM.png)

## 到此，环境配置全部完成！