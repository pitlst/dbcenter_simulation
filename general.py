import abc
from logger import logger_make

# 走一步半小时
metro_all_type = ["A型车", "B型车"]
stage_all_type = ["进车台位", "粘接预装台位", "自动化粘接台位", "普通组装1类", "模块化组装台位", "A车组装2类", "BC车组装2类", "落车台位"]
# 模拟的方案标志位
FANGAN = 0

# 节车
class metro:
    def __init__(self, index: int, type_name: str):
        assert type_name in metro_all_type, "车型信息不正确"
        self.index = index
        self.type = type_name
        self.work_count = 0
    
    def work(self):
        self.work_count += 1
        

# 所有能动的，拥有班组的单位的单位的抽象
class moving_object(abc.ABC):
    def __init__(self) -> None:
        self.max_work_count = -1
        self.work_count = 0
        self.metro = None
    
    def work(self) -> None:
        self.work_count += 1
        if not self.metro is None:
            self.metro.work()
        
    def input_test(self) -> bool:
        '''测试当前能否进车'''
        if self.metro is None:
            return True
        return False
        
    def output_test(self) -> bool:
        '''测试当前能否出车'''
        if self.metro is None:
            return False
        if self.work_count < self.max_work_count:
            return False
        return True
        
    def input(self, input_metro: metro, max_work_count: int = -1) -> None:
        '''进车'''
        if not self.metro is None:
            raise ValueError("在有车的状态下进车")
        self.work_count = 0
        self.metro = input_metro
        self.max_work_count = max_work_count
        
    def output(self) -> metro:
        '''出车'''
        if self.metro is None:
            raise ValueError("在无车的状态下出车")
        if self.work_count < self.max_work_count:
            raise ValueError("在工作未完成的情况下出车")
        temp_metro = self.metro
        # 重置状态
        self.metro = None
        self.work_count = 0
        return temp_metro
    
    
# 台位的抽象
class stage(moving_object):
    def __init__(self, name: str, type_name: str, max_work_count: int):
        super().__init__()
        self.name = name
        self.type = type_name
        self.max_work_count = max_work_count
        self.LOG = logger_make(self.type + self.name)
    
    def log_status(self) -> None:
        if self.metro is None:
            self.LOG.debug("未在工作")
        elif self.work_count < self.max_work_count:
            self.LOG.debug("正在工作......")
        else:
            self.LOG.warning("工作已完成但是车未移走")
    
    def input(self, metro_: metro) -> None:
        self.LOG.debug("进了" + metro_.type + "的" + str(metro_.index) + "号")
        super().input(metro_, self.max_work_count)
        
    def output(self) -> metro:
        self.LOG.debug("出了" + self.metro.type + "的" + str(self.metro.index) + "号")
        return super().output()
            
            
# 移车台的抽象
class transfer_table(moving_object):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.LOG = logger_make(self.name)
        self.last_all_work_count = 0
        self.all_work_count = 0

    def log_status(self) -> None:
        if self.metro is None:
            self.LOG.debug("移车台为空")
        elif self.work_count < self.max_work_count:
                self.LOG.debug("正在工作......")
        else:
            self.LOG.warning("移车台不为空但是已到达目标台位")
            
            
    def input(self, metro_: metro, from_stage_name: str) -> None:
        self.LOG.debug("从" + from_stage_name + "进了" + metro_.type + "的" + str(metro_.index) + "号")
        max_work_count = -1
        if FANGAN == 0 :
            max_work_count = 3
        elif FANGAN == 1:
            if from_stage_name in ["进车台位", "粘接预装台位-1", "粘接预装台位-2", "粘接预装台位-3" ,"自动化粘接台位"]:
                max_work_count = 1
            else:
                max_work_count = 3
        super().input(metro_, max_work_count)
        
    def output(self, to_stage_name: str) -> metro:
        self.LOG.debug("出了" + self.metro.type + "的" + str(self.metro.index) + "号到" + to_stage_name)
        self.all_work_count += 1
        return super().output()
        
    