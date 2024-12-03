from utils.logger import logger_make

class metro:
    '''对每一节车的抽象'''
    def __init__(self, index: int, type_name: str):
        assert type_name in ["A", "B", "C"], "节车的类型不正确"
        # 车的索引
        self.index = index
        # 车的类型
        self.type = type_name
        # 车的工作计数
        self.work_count = 0
    
    def work(self):
        self.work_count += 1
        

class can_save_metro_object:
    '''可以承载车辆的单位的基类，也就是可以在车间中拥有班组承载的单位'''
    def __init__(self):
        # 最大工作计数
        self.max_work_count: int = -1
        # 工作计数
        self.work_count: int = 0
        # 承载的节车
        self.metro: metro|None = None
        
    def work(self) -> None:
        '''工作一次'''
        self.work_count += 1 
        
    def can_input(self) -> bool:
        '''测试是否可以进车'''
        return self.metro is None
            
    def can_output(self) -> bool:
        '''测试是否可以落车'''
        return not self.metro is None and self.work_count >= self.max_work_count
    
    def __lshift__(self, metro_: tuple):
        '''进车'''
        assert self.can_input(), "不能进车时进车"
        self.metro = metro_[0]
        self.max_work_count = metro_[1]
        self.work_count = 0
        return self
    
    def __rshift__(self) -> metro:
        '''落车'''
        assert self.can_output(), "不能落车时落车"
        temp = self.metro
        self.metro = None
        self.max_work_count = -1
        self.work_count = 0
        return temp
    

class stage(can_save_metro_object):
    '''台位的抽象'''
    def __init__(self, name: str, type_name: str, max_stage_count: int):
        super().__init__()
        assert type_name in [""], "不允许的台位类型"
        self.name: str = name
        self.type: str = type_name
        self.max_stage_count: int = max_stage_count
        self.LOG = logger_make(self.type + self.name)
    
    def log_status(self) -> None:
        if self.metro is None:
            self.LOG.debug("未在工作")
        elif self.work_count < self.max_stage_count:
            self.LOG.debug("正在工作......")
        else:
            self.LOG.warning("工作已完成但是车未移走")
    
    def __lshift__(self, metro_: metro):
        self.LOG.debug("进了" + metro_.type + "的" + str(metro_.index) + "号")
        super().__lshift__(metro_, self.max_stage_count)
        return self
        
    def output(self) -> metro:
        self.LOG.debug("出了" + self.metro.type + "的" + str(self.metro.index) + "号")
        return super().output()