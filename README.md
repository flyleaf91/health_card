# 健康码截图检查
本程序支持对 粤康码，行程卡，核酸结果 的结果进行识别，减少人工检查的机械工作

# 免责声明
本程序仅用于学习交流，不对健康码进行真伪检测，也不保证识别结果的可靠性，
若使用本程序导致防疫检查工作疏漏，本人概不负责

# 效果
对截图文字进行识别，整理至表格，减少人工检查的工作量：

核酸结果解码信息:
![核酸结果解码信息](图片说明\核酸结果解码信息.png)

行程卡解码信息:
![行程卡解码信息](图片说明\行程卡解码信息.png)

粤康码解码信息:
![粤康码解码信息](图片说明\粤康码解码信息.png)


# 使用方法

把截图文件按文件夹保存至代码目录，如： 核酸结果，行程卡，粤康码 文件夹，各文件夹下为对应的截图.

使用示例，命令行：

`
python health_card.py --test yuekangma
`

提示输入检查日期时，可直接按回车跳过，若输入日期，则程序会检查截图日期，核酸结果日期是否符合要求

生成的解码结果文件后缀为csv，可直接用excel打开。

命令行帮助：

```
python health_card.py --help

Options:
  -t, --test [yuekangma|粤康码|xingchengka|行程卡|heshuan|核酸]
                                  要检查截图的类型:[粤康码，行程卡，核酸]，默认为[粤康码]
  -p, --image_path TEXT           对应检查的截图目录，默认目录为:[粤康码测试,行程卡测试,核酸结果测试]
  -f, --result_file TEXT          检查结果文件名，默认为:[粤康码解码信息.csv,行程卡解码信息.csv,核酸结果解码信
                                  息.csv]
  -c, --clean                     清除检查结果文件以及check.txt标记
  --help                          Show this message and exit.
```

按提示操作就好，

-t：支持输入 [yuekangma|粤康码|xingchengka|行程卡|heshuan|核酸]，进行指定的类型检测，输入拼音或中文均可
-p：指定检查的截图目录

-f：指定结果保存到的文件

-c：清除检查结果，并备份到“copy_xxx”文件中，还会清除check.txt文件标记
    程序执行一遍后，若文件夹中的所有图片已检查，（不包含子目录），会在目录下保存一个check.txt文件。

check.txt机制主要是为了在使用时，图片是一个目录一个目录添加的，这样重新执行程序检查可以跳过已检查的内容。
    
    
执行 -c 操作后，会清除对应的check.txt标记，下次重新执行程序会重新检查所有图片。
    
  


# 程序安装
本程序为python脚本，使用前需要安装较多内容，后期我会考虑打包成exe。

## python解释器

python版本3.9，下载：https://www.python.org/

## python包
本程序依赖的python包已记录到requirements文件，使用如下命令安装：
`
pip install -r requirements.txt
`
### zxing二维码库
其中zxing二维码库默认不支持gbk编码，参考如下链接进行修改：
https://www.cnblogs.com/hyyx/p/14292703.html

使用时若提示找不到java程序之类的，请安装JDK：
https://docs.microsoft.com/zh-cn/java/openjdk/download

### paddle文字识别库
使用到paddle文字识别库，安装依赖包时好像需要安装Visual Studio，我忘记具体内容了，大家看提示操作吧


## 最后

希望大家用不上这个程序，希望疫情能够结束，世界和平，身体健康

有兴趣可以参与进行修改本程序，有空可能我也会继续优化





