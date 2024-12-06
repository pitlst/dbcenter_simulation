import datetime
from queue import Queue

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
        
    def get_name(self) -> str:
        '''获取完整名称'''
        return self.type + "型车" + str(self.index) + "号"
        

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
        if not self.metro is None:
            self.metro.work()
        
    def can_input(self) -> bool:
        '''测试是否可以进车'''
        return self.metro is None
            
    def can_output(self) -> bool:
        '''测试是否可以落车'''
        return not self.metro is None and self.work_count >= self.max_work_count
    
    def get_status(self) -> str:
        '''获取当前状态'''
        if self.can_input():
            return "未在工作"
        elif self.can_output():
            return "工作已完成但是车未移走"
        else:
            return "正在工作......"
    
    def input(self, metro_: metro, max_work_count: int):
        '''进车'''
        assert self.can_input(), "不能进车时进车"
        self.metro = metro_
        self.max_work_count = max_work_count
        self.work_count = 0
        return self
    
    def output(self) -> metro:
        '''落车'''
        assert self.can_output(), "不能落车时落车"
        temp = self.metro
        self.metro = None
        self.max_work_count = -1
        self.work_count = 0
        return temp
    

class stage(can_save_metro_object):
    '''台位的抽象'''
    def __init__(self, name_: str, type_: str, max_stage_count: int, max_trans_count: int, next_type: str, can_input_metro_type: list):
        super().__init__()
        # 台位号
        self.name: str = name_
        # 台位类型
        self.type: str = type_
        # 台位的工作周期
        self.max_stage_count: int = max_stage_count
        # 从该台位转出的转运时长
        self.max_trans_count: int = max_trans_count
        # 下一个台位的类型
        self.next_type = next_type
        # 适用的车型
        self.can_input_metro_type = can_input_metro_type
            
    def get_name(self) -> str:
        '''获取完整名称'''
        return self.type + self.name + "号"
    
    def input(self, metro_: metro) -> None:
        assert metro_.type in self.can_input_metro_type, "进车的类型不正确"
        super().input(metro_, self.max_stage_count)
        return self
    
    
class transfer_table(can_save_metro_object):
    '''移车台的抽象'''
    def __init__(self, name_: str, can_remove_stage_type: list):
        super().__init__()
        # 移车台编号
        self.name: str = name_
        # 允许的转运台位类型
        self.can_remove_stage_type: list = can_remove_stage_type
            
    def get_name(self) -> str:
        '''获取完整名称'''
        return "移车台" + self.name + "号"
    
    def input(self, metro_, max_work_count, from_stage: stage):
        assert from_stage.type in self.can_remove_stage_type, "从不允许的台位中转车"
        return super().input(metro_, max_work_count)


class environment:
    '''环境变量'''
    def __init__(self, program_index: int) -> None:
        self.program_index = program_index
        if program_index == 1:
            from program.program_1 import \
                TIME_STEP, \
                DAY_WORK_TIME, \
                USE_OF_THE_BLASTING_ROOM, \
                NUMBER_OF_METRO_DROP_OFF, \
                APPROACH_QUEUE, \
                NUMBER_OF_INCOMING_VEHICLES_PER_DAY, \
                NUMBER_OF_TRANS_SHIPMENT_VEHICLES, \
                ENABLING_SEPARATION_OF_TRANSFER_VEHICLES, \
                STATIONS_SERVICED_BY_TRANSFER_VANS, \
                ALL_STAGE_CONFIG
        elif program_index == 2:
            from program.program_2 import \
                TIME_STEP, \
                DAY_WORK_TIME, \
                USE_OF_THE_BLASTING_ROOM, \
                NUMBER_OF_METRO_DROP_OFF, \
                APPROACH_QUEUE, \
                NUMBER_OF_INCOMING_VEHICLES_PER_DAY, \
                NUMBER_OF_TRANS_SHIPMENT_VEHICLES, \
                ENABLING_SEPARATION_OF_TRANSFER_VEHICLES, \
                STATIONS_SERVICED_BY_TRANSFER_VANS, \
                ALL_STAGE_CONFIG
        elif program_index == 3:
            from program.program_3 import \
                TIME_STEP, \
                DAY_WORK_TIME, \
                USE_OF_THE_BLASTING_ROOM, \
                NUMBER_OF_METRO_DROP_OFF, \
                APPROACH_QUEUE, \
                NUMBER_OF_INCOMING_VEHICLES_PER_DAY, \
                NUMBER_OF_TRANS_SHIPMENT_VEHICLES, \
                ENABLING_SEPARATION_OF_TRANSFER_VEHICLES, \
                STATIONS_SERVICED_BY_TRANSFER_VANS, \
                ALL_STAGE_CONFIG
        elif program_index == 4:
            from program.program_4 import \
                TIME_STEP, \
                DAY_WORK_TIME, \
                USE_OF_THE_BLASTING_ROOM, \
                NUMBER_OF_METRO_DROP_OFF, \
                APPROACH_QUEUE, \
                NUMBER_OF_INCOMING_VEHICLES_PER_DAY, \
                NUMBER_OF_TRANS_SHIPMENT_VEHICLES, \
                ENABLING_SEPARATION_OF_TRANSFER_VEHICLES, \
                STATIONS_SERVICED_BY_TRANSFER_VANS, \
                ALL_STAGE_CONFIG
        elif program_index == 5:
            from program.program_5 import \
                TIME_STEP, \
                DAY_WORK_TIME, \
                USE_OF_THE_BLASTING_ROOM, \
                NUMBER_OF_METRO_DROP_OFF, \
                APPROACH_QUEUE, \
                NUMBER_OF_INCOMING_VEHICLES_PER_DAY, \
                NUMBER_OF_TRANS_SHIPMENT_VEHICLES, \
                ENABLING_SEPARATION_OF_TRANSFER_VEHICLES, \
                STATIONS_SERVICED_BY_TRANSFER_VANS, \
                ALL_STAGE_CONFIG
        elif program_index == 6:
            from program.program_6 import \
                TIME_STEP, \
                DAY_WORK_TIME, \
                USE_OF_THE_BLASTING_ROOM, \
                NUMBER_OF_METRO_DROP_OFF, \
                APPROACH_QUEUE, \
                NUMBER_OF_INCOMING_VEHICLES_PER_DAY, \
                NUMBER_OF_TRANS_SHIPMENT_VEHICLES, \
                ENABLING_SEPARATION_OF_TRANSFER_VEHICLES, \
                STATIONS_SERVICED_BY_TRANSFER_VANS, \
                ALL_STAGE_CONFIG
        else:
            raise ValueError("未知的方案编号")
        self.TIME_STEP = TIME_STEP
        self.DAY_WORK_TIME = DAY_WORK_TIME
        self.USE_OF_THE_BLASTING_ROOM = USE_OF_THE_BLASTING_ROOM
        self.NUMBER_OF_METRO_DROP_OFF = NUMBER_OF_METRO_DROP_OFF
        self.APPROACH_QUEUE = APPROACH_QUEUE
        self.NUMBER_OF_INCOMING_VEHICLES_PER_DAY = NUMBER_OF_INCOMING_VEHICLES_PER_DAY
        self.NUMBER_OF_TRANS_SHIPMENT_VEHICLES = NUMBER_OF_TRANS_SHIPMENT_VEHICLES
        self.ENABLING_SEPARATION_OF_TRANSFER_VEHICLES = ENABLING_SEPARATION_OF_TRANSFER_VEHICLES
        self.STATIONS_SERVICED_BY_TRANSFER_VANS = STATIONS_SERVICED_BY_TRANSFER_VANS
        self.ALL_STAGE_CONFIG = ALL_STAGE_CONFIG
        '''时间计数'''
        self.time_count = 0
        '''进车队列'''
        self.approach_queue = []
        for i, ch in enumerate(APPROACH_QUEUE):
            # 第一个选项存储的是他应当进车的循环次数,可以是浮点数
            self.approach_queue.append([DAY_WORK_TIME/ NUMBER_OF_INCOMING_VEHICLES_PER_DAY / TIME_STEP * i, metro(i, ch)])
        '''移车台'''
        self.moving_vehicles_platform: list[transfer_table] = []
        if USE_OF_THE_BLASTING_ROOM and ENABLING_SEPARATION_OF_TRANSFER_VEHICLES:
            self.moving_vehicles_platform = [transfer_table(str(i), STATIONS_SERVICED_BY_TRANSFER_VANS[i]) for i in range(NUMBER_OF_TRANS_SHIPMENT_VEHICLES)]
        else:
            self.moving_vehicles_platform = [transfer_table(str(i), list(ALL_STAGE_CONFIG.keys())) for i in range(NUMBER_OF_TRANS_SHIPMENT_VEHICLES)]
        '''台位'''
        self.platform_list: list[stage] = []
        for platform_type in ALL_STAGE_CONFIG:
            for platform_ in ALL_STAGE_CONFIG[platform_type]["具体台位"]:
                self.platform_list.append(
                    stage(
                        platform_["台位号"], 
                        platform_type, 
                        int(ALL_STAGE_CONFIG[platform_type]["作业周期"] / TIME_STEP),
                        int(platform_["转运时长"] / TIME_STEP),
                        ALL_STAGE_CONFIG[platform_type]["下一台位类型"],
                        ALL_STAGE_CONFIG[platform_type]["适用车型"],
                    )
                ) 
                
    def work(self):
        '''全体工作一次'''
        for platform_ in self.platform_list + self.moving_vehicles_platform:
            platform_.work()
        
    def lapse(self):
        '''时间流逝一次'''
        self.time_count += 1        

    def get_platform_with_name(self, platform_name: str) -> stage:
        '''返回指定名称的台位或移车台'''
        for platform_ in self.platform_list + self.moving_vehicles_platform:
            if platform_.get_name() == platform_name:
                return platform_

    def get_stage_with_type(self, platform_type) -> list[stage]:
        '''返回指定类型的台位'''
        temp_stage: list[stage] = []
        for stage_ in self.platform_list:
            if stage_.type == platform_type:
                temp_stage.append(stage_)
        return temp_stage
                
    def get_input_metro(self, time_step: int) -> metro|None:
        '''获取进车的车'''
        if len(self.approach_queue) == 0 or self.approach_queue[0][0] > time_step:
            return None
        return self.approach_queue.pop(0)[1]
        
    def get_real_days(self, time_step: int) -> int:
        '''获取对应循环次数的天数'''
        return int(time_step * self.TIME_STEP / self.DAY_WORK_TIME)
    
    def get_real_hours(self, time_step: int) -> int:
        '''获取对应循环次数当天的小时数'''
        return int(time_step * self.TIME_STEP % self.DAY_WORK_TIME / 60)
    
    def get_real_minutes(self, time_step: int) -> int:
        '''获取对应循环次数当天的小时数'''
        return int(time_step * self.TIME_STEP % self.DAY_WORK_TIME % 60)
    
    def get_trans_time(self, temp_key: str) -> int:
        '''给台位号获取转运的循环次数'''
        for ch in self.ALL_STAGE_CONFIG:
            for ch_ in self.ALL_STAGE_CONFIG[ch]["具体台位"]:
                if ch_["台位号"] == temp_key:
                    return ch_["转运时长"] / self.TIME_STEP
    
    @staticmethod
    def get_max_metro(platform_list: list[stage]) -> int:
        '''寻找输入台位中拥有等待时间最长的车的索引'''
        temp_index = -1
        temp_prioritization = -1
        for index_, platform_ in enumerate(platform_list):
            if not platform_.metro is None and temp_prioritization < platform_.metro.work_count:
                temp_index = index_
                temp_prioritization = platform_.metro.work_count
        return temp_index
    
    @staticmethod
    def get_max_metro_with_filter(platform_list: list[stage], filter_list: list[str]) -> int:
        '''寻找输入台位中拥有等待时间最长的车的索引,带上筛选'''
        temp_index = -1
        temp_prioritization = -1
        for index_, platform_ in enumerate(platform_list):
            if not platform_.metro is None and index_ in filter_list and temp_prioritization < platform_.metro.work_count:
                temp_index = index_
                temp_prioritization = platform_.metro.work_count
        return temp_index
    

    
class data_record:
    '''数据记录与打印'''
    def __init__(self, program_index: int):
        self.LOG = logger_make("方案" + str(program_index) + "试验记录，时间" + datetime.datetime.now().strftime("%Y-%m-%d=%H:%M:%S"))
        # 进车
        self.number_of_incoming_vehicles = []
        # 落车
        self.number_of_vehicles_dropped = []
        # 移车台移车相关
        self.moving_vehicles_platform_count = []
        # 异常
        self.error_record = []
        # 当前落车
        self.total_number_of_vehicles_dropped = 0
        
    def event_input(self, m_environment: environment) -> None:
        '''触发进车，更新数据'''
        ...
        
    def event_output(self, m_environment: environment, output_metro: metro) -> None:
        '''触发落车，更新数据'''
        ...
        
    def event_mv_input(self, m_environment: environment) -> None:
        '''触发移车台进车，更新数据'''
        ...
        
    def event_mv_output(self, m_environment: environment) -> None:
        '''触发移车台落车，更新数据'''
        ...

    def event_work(self, m_environment: environment) -> None:
        '''触发工作，更新数据'''
        ...
        
    def event_step(self, m_environment: environment) -> None:
        '''触发时间步进，更新数据'''
        ...