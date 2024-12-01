from logger import LOG
from general import stage, transfer_table, metro

移车台 = [transfer_table(i) for i in range(2)]

进车台位 = [stage(i, "进车台位") for i in range(1)]
粘接预装台位 = [stage(i, "粘接预装台位") for i in range(3)]
自动化粘接台位 = [stage(i, "自动化粘接台位") for i in range(1)]
普通组装1类 = [stage(i, "普通组装1类") for i in range(6)]
模块化组装台位 = [stage(i, "模块化组装台位") for i in range(2)]
A车组装2类 = [stage(i, "A车组装2类") for i in range(6)]
BC车组装2类 = [stage(i, "BC车组装2类") for i in range(12)]
落车台位 = [stage(i, "落车台位") for i in range(2)]

metro_all_sequence = ["A型车", "B型车", "B型车"] * 167 # 一共501节

进车总数 = 0
昨天进车总数 = 0
出车总数 = 0
昨天出车总数 = 0

if __name__ == "__main__":
    day_count = 0
    while True:
        LOG.debug("-" * 20 + "第" + str(int(day_count/16)) + "天第" + str(day_count%16*0.5) + "小时" + "-" * 20)
        day_count += 1
        
        if 出车总数 >= len(metro_all_sequence):
            break
        
        for 台位 in 进车台位:
            if 台位.metro is None and (进车总数 == 0 or int(day_count/进车总数) > 8):
                台位.input_metro(metro(进车总数, metro_all_sequence[进车总数]))
                metro_all_sequence.pop()
                进车总数 += 1
                    
        for 单个移车台 in 移车台:
            if 单个移车台.metro is None:
                for 台位 in 进车台位 + 粘接预装台位 + 自动化粘接台位 + 普通组装1类 + 模块化组装台位 + A车组装2类 + BC车组装2类:
                    if not 台位.metro is None and 台位.can_remove:
                        单个移车台.pack(台位.output_metro(), 台位.type)
                        break
            else:
                if 单个移车台.can_remove:
                    if 单个移车台.last_stage_type == "进车台位":
                        for 台位 in 粘接预装台位:
                            if 台位.metro is None and 台位.can_remove:
                                台位.input_metro(单个移车台.unpack())
                                break
                    elif 单个移车台.last_stage_type == "自动化粘接台位":
                        for 台位 in 普通组装1类:
                            if 台位.metro is None and 台位.can_remove:
                                台位.input_metro(单个移车台.unpack())
                                break
                    elif 单个移车台.last_stage_type == "模块化组装台位":
                        if 单个移车台.metro.type == "A型车":
                            for 台位 in A车组装2类:
                                if 台位.metro is None and 台位.can_remove:
                                    台位.input_metro(单个移车台.unpack())
                                    break
                        elif 单个移车台.metro.type == "B型车":
                            for 台位 in BC车组装2类:
                                if 台位.metro is None and 台位.can_remove:
                                    台位.input_metro(单个移车台.unpack())
                                    break
                    elif 单个移车台.last_stage_type == "粘接预装台位":
                        for 台位 in 自动化粘接台位:
                            if 台位.metro is None and 台位.can_remove:
                                台位.input_metro(单个移车台.unpack())
                                break
                    elif 单个移车台.last_stage_type == "普通组装1类":
                        for 台位 in 模块化组装台位:
                            if 台位.metro is None and 台位.can_remove:
                                台位.input_metro(单个移车台.unpack())
                                break
                    elif 单个移车台.last_stage_type == "A车组装2类" or 单个移车台.last_stage_type == "BC车组装2类":
                        for 台位 in 落车台位:
                            if 台位.metro is None and 台位.can_remove:
                                台位.input_metro(单个移车台.unpack())
                                break

        
        for 台位 in 落车台位:
            if not 台位.metro is None and 台位.can_remove:
                台位.output_metro()
                出车总数 += 1
                
        for 台位 in 进车台位 + 粘接预装台位 + 自动化粘接台位 + 普通组装1类 + 模块化组装台位 + A车组装2类 + BC车组装2类 + 落车台位:
            if not 台位.metro is None and 台位.can_remove:
                LOG.warning(台位.type + "的" + str(台位.index) + "号台位的" + 台位.metro.type + "的" + str(台位.metro.index) + "号已经准备完毕但是无法移动")
                
        for 能动的 in 进车台位 + 粘接预装台位 + 自动化粘接台位 + 普通组装1类 + 模块化组装台位 + A车组装2类 + BC车组装2类 + 落车台位 + 移车台:
            能动的.work()
        
        
        if day_count%16 == 0:
            LOG.error("-" * 40)
            LOG.error("第" + str(int(day_count/16)) + "天一共进车" + str(进车总数 - 昨天进车总数) + "节")
            昨天进车总数 = 进车总数
            LOG.error("第" + str(int(day_count/16)) + "天一共出车" + str(出车总数 - 昨天出车总数) + "节")
            昨天出车总数 = 出车总数
            temp = 0
            for 单个移车台 in 移车台:
                temp += int(单个移车台.all_work_count - 单个移车台.last_all_work_count)
                LOG.error("第" + str(int(day_count/16)) + "天" + str(单个移车台.index) + "号移车台移动了" + str(int(单个移车台.all_work_count - 单个移车台.last_all_work_count)) + "次")
                单个移车台.last_all_work_count = 单个移车台.all_work_count
            LOG.error("第" + str(int(day_count/16)) + "天移车台一共移动了" + str(temp) + "次")
            LOG.error("-" * 40)
        
        # input()
        
        