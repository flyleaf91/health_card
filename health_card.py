import time,click
#import click
#import heshuan,xingchengka,yuekangma
from heshuan import Heshuan
from xingchengka import Xingchengka
from yuekangma import Yuekangma


@click.command()
@click.option("--test","-t", 
              type=click.Choice(['yuekangma','粤康码','xingchengka','行程卡','heshuan','核酸']),
              default="yuekangma",
              prompt="请输入要检查的截图类型：",
              help="要检查截图的类型:[粤康码，行程卡，核酸]，默认为[粤康码]")

@click.option("--image_path","-p", default=None, 
              help="对应检查的截图目录，默认目录为:[粤康码测试,行程卡测试,核酸结果测试]")
@click.option("--result_file","-f", default=None, 
              help="检查结果文件名，默认为:[粤康码解码信息.csv,行程卡解码信息.csv,核酸结果解码信息.csv]")
@click.option("--clean","clean","-c", flag_value="clean",default=False, help="清除检查结果文件以及check.txt标记")
def health_card(test,image_path,result_file,clean):
    
    """本程序用于检查粤康码、行程卡、核酸结果截图的程序，
       仅用于测试学习，不检测截图真伪，不保证解码结果可信，
       若使用本程序导致防疫检查疏漏，本人概不负责！"""   
    
    if test in ['yuekangma','粤康码']:        
        #默认路径与文件
        image_path = image_path if image_path else "粤康码测试/"
        result_file = result_file if result_file else "粤康码解码信息.csv"  
        
        decode = Yuekangma(image_path,result_file)  
        if clean:
            print("""即将复位检查结果文件以及check.txt标记，
                  检查结果文件会备份到[copy_xxx]""")
            print("清除check.txt标记路径：",image_path)
            print("清除文件：",result_file)
            decode.dir_clean()
            return
        
        print("即将进行检测：",test)
        print("检查路径：",image_path)
        print("检查结果将保存至：",result_file)
        
        start = time.time()
        decode.process_text()
        end = time.time()
        print("time:",end-start)
       
    if test in ['xingchengka','行程卡']:
        #默认路径与文件
        image_path = image_path if image_path else "行程卡测试/"
        result_file = result_file if result_file else "行程卡解码信息.csv"  
        
        decode = Xingchengka(image_path,result_file)  
        if clean:
            print("""即将复位检查结果文件以及check.txt标记，
                  检查结果文件会备份到[copy_xxx]""")
            print("清除check.txt标记路径：",image_path)
            print("清除文件：",result_file)
            decode.dir_clean()
            return
        
        print("即将进行检测：",test)
        print("检查路径：",image_path)
        print("检查结果将保存至：",result_file)
        
        start = time.time()
        decode.process_text()
        end = time.time()
        print("time:",end-start)
        
    if test in ['heshuan','核酸']:
        #默认路径与文件
        image_path = image_path if image_path else "核酸结果测试/"
        result_file = result_file if result_file else "核酸结果解码信息.csv"  
        
        decode = Heshuan(image_path,result_file)  
        if clean:
            print("""即将复位检查结果文件以及check.txt标记，
                  检查结果文件会备份到[copy_xxx]""")
            print("清除check.txt标记路径：",image_path)
            print("清除文件：",result_file)
            decode.dir_clean()
            return
        
        print("即将进行检测：",test)
        print("检查路径：",image_path)
        print("检查结果将保存至：",result_file)
        
        start = time.time()
        decode.process_text()
        end = time.time()
        print("time:",end-start)

if __name__ == '__main__':
    health_card()
