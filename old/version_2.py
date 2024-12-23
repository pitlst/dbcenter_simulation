import numpy as np 
from general.workshop import metro, stage, transfer_table, FANGAN
from utils.logger import logger_make

SAVE_DATA = []

LOG = logger_make("总成车间")

if __name__ == "__main__":
    时间折算标志位 = 6
    if FANGAN == 0:
        all_config = {
            "进车台位":{
                "台位数":1,
                "作业周期":2,
            },
            "粘接预装台位":{
                "台位数":3,
                "作业周期":7.5,
            },
            "自动化粘接台位":{
                "台位数":1,
                "作业周期":2,
            },
            "普通组装1类":{
                "台位数":1,
                "作业周期":22.5,
            },
            "模块化组装台位":{
                "台位数":1,
                "作业周期":7.5,
            },
            "A车组装2类":{
                "台位数":1,
                "作业周期":67.5,
            },
            "BC车组装2类":{
                "台位数":1,
                "作业周期":67.5,
            },
            "落车台位":{
                "台位数":2,
                "作业周期":4,
            },
        }
        移车台 = [transfer_table(str(i) + "号移车台") for i in range(10)]

        进车台位 = [stage("1号", "进车台位", all_config["进车台位"]["作业周期"] * 时间折算标志位)]
        粘接预装台位 = [stage("27号", "粘接预装台位", all_config["粘接预装台位"]["作业周期"] * 时间折算标志位), 
                  stage("29号", "粘接预装台位", all_config["粘接预装台位"]["作业周期"] * 时间折算标志位), 
                  stage("33号", "粘接预装台位", all_config["粘接预装台位"]["作业周期"] * 时间折算标志位)]
        自动化粘接台位 = [stage("32号", "自动化粘接台位", all_config["自动化粘接台位"]["作业周期"] * 时间折算标志位)]
        普通组装1类 = [  stage("11号", "普通组装1类", all_config["普通组装1类"]["作业周期"] * 时间折算标志位),
                        stage("12号", "普通组装1类", all_config["普通组装1类"]["作业周期"] * 时间折算标志位),
                        stage("13号", "普通组装1类", all_config["普通组装1类"]["作业周期"] * 时间折算标志位),
                        stage("14号", "普通组装1类", all_config["普通组装1类"]["作业周期"] * 时间折算标志位),
                        stage("15号", "普通组装1类", all_config["普通组装1类"]["作业周期"] * 时间折算标志位),
                        stage("16号", "普通组装1类", all_config["普通组装1类"]["作业周期"] * 时间折算标志位)
                  ]
        模块化组装台位 = [stage("6号", "模块化组装台位", all_config["模块化组装台位"]["作业周期"] * 时间折算标志位), 
                   stage("7号", "模块化组装台位", all_config["模块化组装台位"]["作业周期"] * 时间折算标志位)]
        A车组装2类 = [   stage("2号", "A车组装2类", all_config["A车组装2类"]["作业周期"] * 时间折算标志位), 
                        stage("3号", "A车组装2类", all_config["A车组装2类"]["作业周期"] * 时间折算标志位),
                        stage("4号", "A车组装2类", all_config["A车组装2类"]["作业周期"] * 时间折算标志位),
                        stage("5号", "A车组装2类", all_config["A车组装2类"]["作业周期"] * 时间折算标志位),
                        stage("17号", "A车组装2类", all_config["A车组装2类"]["作业周期"] * 时间折算标志位),
                        stage("19号", "A车组装2类", all_config["A车组装2类"]["作业周期"] * 时间折算标志位)
                  ]
        BC车组装2类 = [stage("18号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("20号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("21号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("22号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("23号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("24号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("25号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("26号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("34号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("35号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("36号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("37号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位)
                   ]
        落车台位 = [stage("新落车台位", "落车台位", 24), stage("老落车台位", "落车台位", 24)]
        
        进车队列 = ["A型车", "B型车", "B型车"] * 1000
        预计进车总数 = len(进车队列)
        
        被移车台预定台位对应移车台名称的队列 = []
        被移车台预定台位的队列 = []
        
        进车总数 = 0
        昨天进车总数 = 0
        出车总数 = 0
        昨天出车总数 = 0
        
        时间步骤 = 0 # 一次代表10分钟
        while True:
            
            LOG.debug("-" * 20 + "第" + str(int(时间步骤/48)) + "天 " + str(int(时间步骤%48*10/60)) + " 时 " + str(时间步骤%48*10%60) + " 分" + "-" * 20)
            
            时间步骤 += 1
            if 出车总数 == 500:
                break
            
            # LOG.debug("进车")
            # 每天限制进两台车
            for 台位 in 进车台位:
                if 台位.input_test() and (进车总数 == 0 or int(时间步骤/进车总数) > 24) and len(进车队列) != 0:
                    台位.input(metro(进车总数, 进车队列.pop(0)))
                    进车总数 += 1

            有移车台能够移车 = False
            本轮能够从哪个台位移车 = []
            本轮能够移向哪个台位 = []
            # 检查有没有移车台能够移车
            for 单个移车台 in 移车台:
                if 单个移车台.input_test():
                    有移车台能够移车 = True
                    break
            
            if 有移车台能够移车:
                for 台位 in 进车台位 + 粘接预装台位 + 自动化粘接台位 + 普通组装1类 + 模块化组装台位 + A车组装2类 + BC车组装2类:
                    if 台位.output_test() and not 台位 in 本轮能够从哪个台位移车:
                        if 台位.type == "进车台位":
                            for 台位_ in 粘接预装台位:
                                if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                    本轮能够从哪个台位移车.append(台位)
                                    本轮能够移向哪个台位.append(台位_)
                                    break
                        elif 台位.type == "粘接预装台位":
                            for 台位_ in 自动化粘接台位:
                                if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                    本轮能够从哪个台位移车.append(台位)
                                    本轮能够移向哪个台位.append(台位_)
                                    break
                        elif 台位.type == "自动化粘接台位":
                            for 台位_ in 普通组装1类:
                                if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                    本轮能够从哪个台位移车.append(台位)
                                    本轮能够移向哪个台位.append(台位_)
                                    break
                        elif 台位.type == "普通组装1类":
                            for 台位_ in 模块化组装台位:
                                if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                    本轮能够从哪个台位移车.append(台位)
                                    本轮能够移向哪个台位.append(台位_)
                                    break
                        elif 台位.type == "模块化组装台位":
                            if 台位.metro.type == "A型车":
                                for 台位_ in A车组装2类:
                                    if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                        本轮能够从哪个台位移车.append(台位)
                                        本轮能够移向哪个台位.append(台位_)
                                        break
                            else:
                                for 台位_ in BC车组装2类:
                                    if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                        本轮能够从哪个台位移车.append(台位)
                                        本轮能够移向哪个台位.append(台位_)
                                        break
                        elif 台位.type in ["A车组装2类",  "BC车组装2类"]:
                            for 台位_ in 落车台位:
                                if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                    本轮能够从哪个台位移车.append(台位)
                                    本轮能够移向哪个台位.append(台位_)
                                    break

                # 求移车优先级
                for 单个移车台 in 移车台:
                    if 单个移车台.input_test() and len(本轮能够从哪个台位移车) != 0:
                        本轮准备出车的台位的最大优先级 = -1
                        本轮准备出车的台位的索引 = -1
                        for 索引 in range(len(本轮能够从哪个台位移车)):
                            if 本轮能够从哪个台位移车[索引].metro.work_count >= 本轮准备出车的台位的最大优先级:
                                本轮准备出车的台位的最大优先级 = 本轮能够从哪个台位移车[索引].metro.work_count
                                本轮准备出车的台位的索引 = 本轮准备出车的台位的索引
                        print(本轮能够从哪个台位移车[本轮准备出车的台位的索引].type + 本轮能够从哪个台位移车[本轮准备出车的台位的索引].name + "到" + 本轮能够移向哪个台位[本轮准备出车的台位的索引].type + 本轮能够移向哪个台位[本轮准备出车的台位的索引].name + "由" + 单个移车台.name)
                        单个移车台.input(本轮能够从哪个台位移车[本轮准备出车的台位的索引].output(), 本轮能够从哪个台位移车[本轮准备出车的台位的索引].type)
                        被移车台预定台位的队列.append(本轮能够移向哪个台位[本轮准备出车的台位的索引])
                        被移车台预定台位对应移车台名称的队列.append(单个移车台.name)
                        本轮能够从哪个台位移车.pop(本轮准备出车的台位的索引)
                        本轮能够移向哪个台位.pop(本轮准备出车的台位的索引)
                    
            for 单个移车台 in 移车台:
                if 单个移车台.output_test():
                    for 索引, 预定台位的移车台名称 in enumerate(被移车台预定台位对应移车台名称的队列):
                        if 预定台位的移车台名称 == 单个移车台.name:
                            被移车台预定台位的队列[索引].input(单个移车台.output(被移车台预定台位的队列[索引].name))
                            被移车台预定台位对应移车台名称的队列.pop(索引)
                            被移车台预定台位的队列.pop(索引)
                            break
            
            # LOG.debug("落车")     
            for 台位 in 落车台位:
                if 台位.output_test():
                    已完工的车 = 台位.output()
                    LOG.info(str(已完工的车.index) + "号" + 已完工的车.type + "已经落车，在总成车间内呆了" + str(已完工的车.work_count / 6) + "小时的上班时间")
                    出车总数 += 1
            
            for 能动的 in 进车台位 + 粘接预装台位 + 自动化粘接台位 + 普通组装1类 + 模块化组装台位 + A车组装2类 + BC车组装2类 + 落车台位 + 移车台:
                能动的.log_status()   
            
            # LOG.debug("所有台位和移车台工作一次")
            for 能动的 in 进车台位 + 粘接预装台位 + 自动化粘接台位 + 普通组装1类 + 模块化组装台位 + A车组装2类 + BC车组装2类 + 落车台位 + 移车台:
                能动的.work()      


            if 时间步骤%48 == 0:
                temp_save_data = []
                LOG.info("-" * 40)
                temp_save_data.append(进车总数 - 昨天进车总数)
                LOG.info("第" + str(int(时间步骤/48)) + "天一共进车" + str(进车总数 - 昨天进车总数) + "节")
                昨天进车总数 = 进车总数
                temp_save_data.append(出车总数 - 昨天出车总数)
                LOG.info("第" + str(int(时间步骤/48)) + "天一共出车" + str(出车总数 - 昨天出车总数) + "节")
                昨天出车总数 = 出车总数
                temp = 0
                for 单个移车台 in 移车台:
                    temp += int(单个移车台.all_work_count - 单个移车台.last_all_work_count)
                    temp_save_data.append(int(单个移车台.all_work_count - 单个移车台.last_all_work_count))
                    LOG.info("第" + str(int(时间步骤/48)) + "天" + str(单个移车台.name) + "移动了" + str(int(单个移车台.all_work_count - 单个移车台.last_all_work_count)) + "次")
                    单个移车台.last_all_work_count = 单个移车台.all_work_count
                temp_save_data.append(temp)
                LOG.info("第" + str(int(时间步骤/48)) + "天移车台一共移动了" + str(temp) + "次")
                LOG.info("-" * 40)
                SAVE_DATA.append(np.array(temp_save_data))
                # input()
        temp = np.array(SAVE_DATA)     
        np.save("temp_data", temp)
    elif FANGAN == 1:
        all_config = {
            "进车台位":{
                "台位数":1,
                "作业周期":2,
            },
            "粘接预装台位_1":{
                "台位数":1,
                "作业周期":2,
            },
            "粘接预装台位_2":{
                "台位数":1,
                "作业周期":2,
            },
            "粘接预装台位_3":{
                "台位数":1,
                "作业周期":2,
            },
            "自动化粘接台位":{
                "台位数":1,
                "作业周期":2,
            },
            "普通组装1类":{
                "台位数":1,
                "作业周期":22.5,
            },
            "模块化组装台位":{
                "台位数":1,
                "作业周期":7.5,
            },
            "A车组装2类":{
                "台位数":1,
                "作业周期":67.5,
            },
            "BC车组装2类":{
                "台位数":1,
                "作业周期":67.5,
            },
            "落车台位":{
                "台位数":2,
                "作业周期":4,
            },
        }
        
        移车台 = [transfer_table(str(i) + "号移车台") for i in range(10)]

        进车台位 = [stage("1号", "进车台位", all_config["进车台位"]["作业周期"] * 时间折算标志位)]
        粘接预装台位_1 = [stage("_27号", "粘接预装台位_1", all_config["粘接预装台位_1"]["作业周期"] * 时间折算标志位)]
        粘接预装台位_2 = [stage("_29号", "粘接预装台位_2", all_config["粘接预装台位_2"]["作业周期"] * 时间折算标志位)] 
        粘接预装台位_3 = [stage("_33号", "粘接预装台位_3", all_config["粘接预装台位_3"]["作业周期"] * 时间折算标志位)]  
        自动化粘接台位 = [stage("32号", "自动化粘接台位", all_config["自动化粘接台位"]["作业周期"] * 时间折算标志位)]
        普通组装1类 = [  stage("11号", "普通组装1类", all_config["普通组装1类"]["作业周期"] * 时间折算标志位),
                        stage("12号", "普通组装1类", all_config["普通组装1类"]["作业周期"] * 时间折算标志位),
                        stage("13号", "普通组装1类", all_config["普通组装1类"]["作业周期"] * 时间折算标志位),
                        stage("14号", "普通组装1类", all_config["普通组装1类"]["作业周期"] * 时间折算标志位),
                        stage("15号", "普通组装1类", all_config["普通组装1类"]["作业周期"] * 时间折算标志位),
                        stage("16号", "普通组装1类", all_config["普通组装1类"]["作业周期"] * 时间折算标志位)
                  ]
        模块化组装台位 = [stage("6号", "模块化组装台位", all_config["模块化组装台位"]["作业周期"] * 时间折算标志位), 
                   stage("7号", "模块化组装台位", all_config["模块化组装台位"]["作业周期"] * 时间折算标志位)]
        A车组装2类 = [   stage("2号", "A车组装2类", all_config["A车组装2类"]["作业周期"] * 时间折算标志位), 
                        stage("3号", "A车组装2类", all_config["A车组装2类"]["作业周期"] * 时间折算标志位),
                        stage("4号", "A车组装2类", all_config["A车组装2类"]["作业周期"] * 时间折算标志位),
                        stage("5号", "A车组装2类", all_config["A车组装2类"]["作业周期"] * 时间折算标志位),
                        stage("17号", "A车组装2类", all_config["A车组装2类"]["作业周期"] * 时间折算标志位),
                        stage("19号", "A车组装2类", all_config["A车组装2类"]["作业周期"] * 时间折算标志位)
                  ]
        BC车组装2类 = [stage("18号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("20号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("21号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("22号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("23号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("24号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("25号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("26号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("34号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("35号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("36号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位),
                   stage("37号", "BC车组装2类", all_config["BC车组装2类"]["作业周期"] * 时间折算标志位)
                   ]
        落车台位 = [stage("新落车台位", "落车台位", 24), stage("老落车台位", "落车台位", 24)]
        
        进车队列 = ["A型车", "B型车", "B型车"] * 1000
        预计进车总数 = len(进车队列)
        
        被移车台预定台位对应移车台名称的队列 = []
        被移车台预定台位的队列 = []
        
        进车总数 = 0
        昨天进车总数 = 0
        出车总数 = 0
        昨天出车总数 = 0
        
        时间步骤 = 0 # 一次代表10分钟
        while True:
            
            LOG.debug("-" * 20 + "第" + str(int(时间步骤/48)) + "天 " + str(int(时间步骤%48*10/60)) + " 时 " + str(时间步骤%48*10%60) + " 分" + "-" * 20)
            
            时间步骤 += 1
            if 出车总数 == 500:
                break
            
            # LOG.debug("进车")
            # 每天限制进两台车
            for 台位 in 进车台位:
                if 台位.input_test() and (进车总数 == 0 or int(时间步骤/进车总数) > 24) and len(进车队列) != 0:
                    台位.input(metro(进车总数, 进车队列.pop(0)))
                    进车总数 += 1

            有移车台能够移车 = False
            本轮能够从哪个台位移车 = []
            本轮能够移向哪个台位 = []
            # 检查有没有移车台能够移车
            for 单个移车台 in 移车台:
                if 单个移车台.input_test():
                    有移车台能够移车 = True
                    break
            
            if 有移车台能够移车:
                for 台位 in 进车台位 + 粘接预装台位_1 + 粘接预装台位_2 + 粘接预装台位_3 + 自动化粘接台位 + 普通组装1类 + 模块化组装台位 + A车组装2类 + BC车组装2类:
                    if 台位.output_test() and not 台位 in 本轮能够从哪个台位移车:
                        if 台位.type == "进车台位":
                            for 台位_ in 粘接预装台位_1:
                                if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                    本轮能够从哪个台位移车.append(台位)
                                    本轮能够移向哪个台位.append(台位_)
                                    break
                        if 台位.type == "粘接预装台位_1":
                            for 台位_ in 粘接预装台位_2:
                                if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                    本轮能够从哪个台位移车.append(台位)
                                    本轮能够移向哪个台位.append(台位_)
                                    break
                        if 台位.type == "粘接预装台位_2":
                            for 台位_ in 粘接预装台位_3:
                                if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                    本轮能够从哪个台位移车.append(台位)
                                    本轮能够移向哪个台位.append(台位_)
                                    break
                        elif 台位.type == "粘接预装台位_3":
                            for 台位_ in 自动化粘接台位:
                                if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                    本轮能够从哪个台位移车.append(台位)
                                    本轮能够移向哪个台位.append(台位_)
                                    break
                        elif 台位.type == "自动化粘接台位":
                            for 台位_ in 普通组装1类:
                                if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                    本轮能够从哪个台位移车.append(台位)
                                    本轮能够移向哪个台位.append(台位_)
                                    break
                        elif 台位.type == "普通组装1类":
                            for 台位_ in 模块化组装台位:
                                if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                    本轮能够从哪个台位移车.append(台位)
                                    本轮能够移向哪个台位.append(台位_)
                                    break
                        elif 台位.type == "模块化组装台位":
                            if 台位.metro.type == "A型车":
                                for 台位_ in A车组装2类:
                                    if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                        本轮能够从哪个台位移车.append(台位)
                                        本轮能够移向哪个台位.append(台位_)
                                        break
                            else:
                                for 台位_ in BC车组装2类:
                                    if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                        本轮能够从哪个台位移车.append(台位)
                                        本轮能够移向哪个台位.append(台位_)
                                        break
                        elif 台位.type in ["A车组装2类",  "BC车组装2类"]:
                            for 台位_ in 落车台位:
                                if 台位_.input_test() and not 台位_ in 本轮能够移向哪个台位 and not 台位_ in 被移车台预定台位的队列:
                                    本轮能够从哪个台位移车.append(台位)
                                    本轮能够移向哪个台位.append(台位_)
                                    break

                # 求移车优先级
                for 单个移车台 in 移车台:
                    if 单个移车台.input_test() and len(本轮能够从哪个台位移车) != 0:
                        本轮准备出车的台位的最大优先级 = -1
                        本轮准备出车的台位的索引 = -1
                        for 索引 in range(len(本轮能够从哪个台位移车)):
                            if 本轮能够从哪个台位移车[索引].metro.work_count >= 本轮准备出车的台位的最大优先级:
                                本轮准备出车的台位的最大优先级 = 本轮能够从哪个台位移车[索引].metro.work_count
                                本轮准备出车的台位的索引 = 本轮准备出车的台位的索引
                        print(本轮能够从哪个台位移车[本轮准备出车的台位的索引].type + 本轮能够从哪个台位移车[本轮准备出车的台位的索引].name + "到" + 本轮能够移向哪个台位[本轮准备出车的台位的索引].type + 本轮能够移向哪个台位[本轮准备出车的台位的索引].name + "由" + 单个移车台.name)
                        单个移车台.input(本轮能够从哪个台位移车[本轮准备出车的台位的索引].output(), 本轮能够从哪个台位移车[本轮准备出车的台位的索引].type)
                        被移车台预定台位的队列.append(本轮能够移向哪个台位[本轮准备出车的台位的索引])
                        被移车台预定台位对应移车台名称的队列.append(单个移车台.name)
                        本轮能够从哪个台位移车.pop(本轮准备出车的台位的索引)
                        本轮能够移向哪个台位.pop(本轮准备出车的台位的索引)
                    
            for 单个移车台 in 移车台:
                if 单个移车台.output_test():
                    for 索引, 预定台位的移车台名称 in enumerate(被移车台预定台位对应移车台名称的队列):
                        if 预定台位的移车台名称 == 单个移车台.name:
                            被移车台预定台位的队列[索引].input(单个移车台.output(被移车台预定台位的队列[索引].name))
                            被移车台预定台位对应移车台名称的队列.pop(索引)
                            被移车台预定台位的队列.pop(索引)
                            break
            
            # LOG.debug("落车")     
            for 台位 in 落车台位:
                if 台位.output_test():
                    已完工的车 = 台位.output()
                    LOG.info(str(已完工的车.index) + "号" + 已完工的车.type + "已经落车，在总成车间内呆了" + str(已完工的车.work_count / 6) + "小时的上班时间")
                    出车总数 += 1
            
            for 能动的 in 进车台位 + 粘接预装台位_1 + 粘接预装台位_2 + 粘接预装台位_3 + 自动化粘接台位 + 普通组装1类 + 模块化组装台位 + A车组装2类 + BC车组装2类 + 落车台位 + 移车台:
                能动的.log_status()   
            
            # LOG.debug("所有台位和移车台工作一次")
            for 能动的 in 进车台位 + 粘接预装台位_1 + 粘接预装台位_2 + 粘接预装台位_3 + 自动化粘接台位 + 普通组装1类 + 模块化组装台位 + A车组装2类 + BC车组装2类 + 落车台位 + 移车台:
                能动的.work()      


            if 时间步骤%48 == 0:
                temp_save_data = []
                LOG.info("-" * 40)
                temp_save_data.append(进车总数 - 昨天进车总数)
                LOG.info("第" + str(int(时间步骤/48)) + "天一共进车" + str(进车总数 - 昨天进车总数) + "节")
                昨天进车总数 = 进车总数
                temp_save_data.append(出车总数 - 昨天出车总数)
                LOG.info("第" + str(int(时间步骤/48)) + "天一共出车" + str(出车总数 - 昨天出车总数) + "节")
                昨天出车总数 = 出车总数
                temp = 0
                for 单个移车台 in 移车台:
                    temp += int(单个移车台.all_work_count - 单个移车台.last_all_work_count)
                    temp_save_data.append(int(单个移车台.all_work_count - 单个移车台.last_all_work_count))
                    LOG.info("第" + str(int(时间步骤/48)) + "天" + str(单个移车台.name) + "移动了" + str(int(单个移车台.all_work_count - 单个移车台.last_all_work_count)) + "次")
                    单个移车台.last_all_work_count = 单个移车台.all_work_count
                temp_save_data.append(temp)
                LOG.info("第" + str(int(时间步骤/48)) + "天移车台一共移动了" + str(temp) + "次")
                LOG.info("-" * 40)
                SAVE_DATA.append(np.array(temp_save_data))
            # input()
        temp = np.array(SAVE_DATA)     
        np.save("temp_data", temp)