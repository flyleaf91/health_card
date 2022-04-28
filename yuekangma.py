class Yuekangma(Card):
   
    def __init__(self,img_path="粤康码/",result_file="粤康码解码信息.csv"):

        Card.__init__(self,img_path,result_file)
        self.catch_sum = {'img_name':None,
                            'label': None,                         
                            'name': None, 
                            'c': None,
                            't': None, 
                            'cid': None, 
                            'cidtype': None,
                            'text':None}
        self.header = ["图片原文件路径","粤康码","姓名","是否绿码","健康码时间","证件号","证件类型","识别文字"]
        
    def img_process(self):
        reader = zxing.BarCodeReader()
        # 遍历图片
        g = os.walk(self.img_path)
        for path,dir_list,file_list in g:
            #有check.txt标记的同级目录文件不再处理
            if "check.txt" in file_list:
                print("存在check.txt文件，跳过目录：",path)
                continue
            for file_name in file_list:
                img_name = os.path.join(path,file_name)
                barcode = reader.decode(img_name,try_harder=True,possible_formats="QR_CODE",products_only=True)

                print("\r\n识别")
                print(img_name)
                
                #初始化字典
                catch_sum = copy.deepcopy(self.catch_sum)
                
                catch_sum["img_name"] = os.path.abspath(img_name)
                catch_sum["text"] = barcode.parsed
                
                yield catch_sum
                
            self.dir_check(path)
    
    #多线程、进程                
    def img_process_muti(self,out_q):    
        for catch_sum in self.img_process():
            out_q.put(catch_sum)
            
        catch_sum = None
        out_q.put(catch_sum)

    def get_pattern(self,text,try_others=False):
        pattern = []
        if text:
            try:
                pattern = json.loads(text) 
            except:
                print("\033[31m识别错误，text=\033[0m",text)
        return pattern
    
    
    
    def clean_data(self,pattern,catch_sum={"text":None}):  
        try:
            catch_sum.update(pattern)
        except:
            print("\033[31m识别错误，pattern=\033[0m",pattern)
            
        return catch_sum

    def check_data(self,catch_sum={},show_pic=False):         
        bad = False
        if not catch_sum['text']:            
            catch_sum['text'] = "检测不到二维码!请人工检查！"
            print("\033[31m错误！检测不到二维码。\033[0m")
            print("\033[31m错误的文件名为：",catch_sum["img_name"],"\033[0m")
            bad = True
            
        elif catch_sum['label'] != "yss":
            catch_sum['label'] = "非粤康码!请人工检查！"
            print("\033[31m错误！识别结果不正常，可能是非粤康码。\033[0m")
            print(catch_sum["text"])
            bad = True
        else:
            catch_sum['label'] = "粤康码"
        
        if catch_sum["c"] != "G":
            catch_sum['c'] = "非绿卡！请人工检查！"
            bad = True
        else:
            catch_sum['c'] = "绿卡" 
            
        try:
            #是否开启采样时间检查
            if not catch_sum["t"]:
                print("\033[31m时间识别为空值异常",e,"\033[0m")
                catch_sum["t"] = "异常！"
                bad = True
            elif self.time_check and catch_sum['label'] and not self.latest_stamp > catch_sum["t"] > self.early_stamp:
                print("\033[31m日期太早或不正常（超出当前时间）\033[0m")
                catch_sum["t"] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(catch_sum["t"]))
                catch_sum["t"] += "异常！"
                bad = True
            else:
                catch_sum["t"] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(catch_sum["t"]))
                                                  
        except Exception as e:
            print("\033[31m时间比较出错,错误信息：",e,"时间值：",catch_sum["t"],"\033[0m")
            catch_sum["t"] = "异常！"
            bad = True

        #其它非关键内容 None 改 无
        for k,v in catch_sum.items():
            if not v:                 
                catch_sum[k] = "无" 

        if bad and show_pic:
            t = Thread(target=self.show_img,args=(catch_sum["img_name"],))
            t.start()

        return catch_sum
    

 