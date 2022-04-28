import os,time,re,json,logging,csv,copy,zxing,shutil
from threading import Thread

class Card:
    def __init__(self,img_path="粤康码/",result_file="解码信息.csv"): 
        self.time_init()        
        self.img_path = img_path
        self.catch_sum = {}
        self.result_file = os.path.abspath(result_file)
            
    def time_init(self):
        self.latest_stamp = time.mktime(time.localtime())
        
        early_time = input("请输入检查报告允许的最早日期（格式：2022-04-25）：")+" 0:0:0"
        early_time = re.sub("\D", "", early_time)   
        try:
            early_time = time.strptime(early_time,'%Y%m%d%H%M%S')
            self.early_stamp = time.mktime(early_time)
            self.time_check = True
        except:
            print("输入的日期格式错误，采用不检查日期的模式")    
            self.early_stamp = 0
            self.time_check = False
       
    
    def show_img(self,img_name):
        img = Image.open(self,img_name)
        img.show()    
        
    def dir_check(self,dst_dir):
        #print("在目录下生成check.txt文件表示已检查")
        if not os.path.exists("check.txt"):
            with open("check.txt", 'w', encoding='utf-8_sig') as f:
                f.write("在目录下生成check.txt文件表示已检查")
            
        file_name = os.path.join(dst_dir,"check.txt")
        Thread(target=shutil.copy, args=['check.txt', file_name]).start()

    def dir_clean(self,clean_path=None):
        print("清空检查记录文件和解码结果")
        if clean_path == None:
            clean_path = self.img_path    
        g = os.walk(clean_path)
        for path,dir_list,file_list in g:
            for file_name in file_list:
                if file_name == "check.txt":
                    os.remove(os.path.join(path,file_name))
        #删除解码结果文件，并复制一份
        if os.path.exists(self.result_file):
            copy_name = os.path.join(os.path.dirname(self.result_file),"copy_"+os.path.basename(self.result_file))
            shutil.copy(self.result_file,copy_name)
            os.remove(self.result_file)
        
    def img_process(self):        
        from paddleocr import paddleocr,PaddleOCR
        paddleocr.logging.disable(logging.DEBUG)        
        
        ocr = PaddleOCR(use_angle_cls=True, lang='ch') 
        # 遍历图片
        g = os.walk(self.img_path)
        for path,dir_list,file_list in g:
            #有check.txt标记的同级目录文件不再处理
            if "check.txt" in file_list:
                print("存在check.txt文件，跳过目录：",path)
                continue
            for file_name in file_list:
                img_name = os.path.join(path,file_name)
                result = ocr.ocr(img_name, cls=True)

                print("\r\n识别")
                print(img_name)
                
                #拼接识别结果
                text = ''
                for line in result:
                    text += line[1][0] 
                    
                catch_sum={}    
                #初始化字典
                catch_sum.update(self.catch_sum)
                
                catch_sum["img_name"] = os.path.abspath(img_name)
                catch_sum["text"] = text
                
                yield catch_sum
                
            self.dir_check(path)
    
    #多线程、进程                
    def img_process_muti(self,out_q):    
        for catch_sum in self.img_process():
            out_q.put(catch_sum)
            
        catch_sum = None
        out_q.put(catch_sum)
            
    def clean_data(self,pattern,catch_sum={"text":None}):    
        #finditer
        matchs = pattern.finditer(catch_sum["text"])  

        for match in matchs:
            for k in match.groupdict():
                #只取第一个有效值
                if match.groupdict()[k] and not catch_sum[k]:
                    catch_sum[k] = match.groupdict()[k]

        return catch_sum
    
    def process_text(self,in_q=None):
        if not os.path.exists(self.result_file):
            with open(self.result_file, 'w', encoding='utf-8_sig',newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(self.header)   
        
        with open(self.result_file, 'a', encoding='utf-8_sig',newline='') as f:
            csv_writer = csv.writer(f)
            
            if in_q:
                while True:
                    catch_sum = in_q.get()
                    if not catch_sum:
                        break
                    print("\r\n提取")
                    print(catch_sum["img_name"])  
                    pattern = self.get_pattern(catch_sum["text"])
                    catch_sum = self.clean_data(pattern,catch_sum)
                    catch_sum = self.check_data(catch_sum)        

                    csv_writer.writerow(list(catch_sum.values()))  
                    f.flush()
            else:
                for catch_sum in self.img_process():
                    print("\r\n提取")
                    print(catch_sum["img_name"]) 
                    
                    pattern = self.get_pattern(catch_sum["text"])
                    catch_sum = self.clean_data(pattern,catch_sum)
                    catch_sum = self.check_data(catch_sum)        

                    csv_writer.writerow(list(catch_sum.values()))  
                    f.flush()               

