import os
import datetime
import numpy as np
import pandas as pd
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
        self.can_remove_stage_type: list[str] = can_remove_stage_type
            
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
                
    def lapse(self):
        '''时间流逝一次'''
        self.time_count += 1      
        '''全体工作一次'''
        for platform_ in self.platform_list + self.moving_vehicles_platform:
            platform_.work()  

    def get_platform_with_name(self, platform_name: str) -> stage:
        '''返回指定名称的台位或移车台'''
        for platform_ in self.platform_list + self.moving_vehicles_platform:
            if platform_.get_name() == platform_name:
                return platform_

    def get_stage_with_type(self, platform_type: str) -> list[stage]:
        '''返回指定类型的台位'''
        temp_stage: list[stage] = []
        for stage_ in self.platform_list:
            if stage_.type in platform_type:
                temp_stage.append(stage_)
        return temp_stage
                
    def get_input_metro(self, time_step: int = -1) -> metro|None:
        '''获取进车的车'''
        if time_step == -1:
            time_step = self.time_count
        if len(self.approach_queue) == 0 or self.approach_queue[0][0] > time_step:
            return None
        return self.approach_queue.pop(0)[1]
        
    def get_real_days(self, time_step: int = -1) -> int:
        '''获取对应循环次数的天数'''
        if time_step == -1:
            time_step = self.time_count
        return int(time_step * self.TIME_STEP / self.DAY_WORK_TIME)
    
    def get_real_hours(self, time_step: int = -1) -> int:
        '''获取对应循环次数当天的小时数'''
        if time_step == -1:
            time_step = self.time_count
        return int(time_step * self.TIME_STEP % self.DAY_WORK_TIME / 60)
    
    def get_real_minutes(self, time_step: int = -1) -> int:
        '''获取对应循环次数当天的小时数'''
        if time_step == -1:
            time_step = self.time_count
        return int(time_step * self.TIME_STEP % self.DAY_WORK_TIME % 60)
    
    def get_trans_time(self, temp_key: str) -> int:
        '''给台位号获取转运的循环次数'''
        for ch in self.ALL_STAGE_CONFIG:
            for ch_ in self.ALL_STAGE_CONFIG[ch]["具体台位"]:
                if ch_["台位号"] == temp_key:
                    return ch_["转运时长"] / self.TIME_STEP
    
    def get_max_wait_metro(self) -> stage|None:
        '''寻找所有可以出车的台位中拥有等待时间最长的车的台位'''
        temp_index = -1
        temp_prioritization = -1
        for index_, platform_ in enumerate(self.platform_list):
            if platform_.can_output() and temp_prioritization < platform_.metro.work_count:
                temp_index = index_
                temp_prioritization = platform_.metro.work_count
        if temp_index == -1:
            return None
        return self.platform_list[temp_index]

    def get_max_wait_metro_with_filter(self, filter_list: list[str]) -> stage|None:
        '''寻找在筛选的类别中可以出车的台位中拥有等待时间最长的车的台位'''
        temp_index = -1
        temp_prioritization = -1
        for index_, platform_ in enumerate(self.platform_list):
            if platform_.can_output() and platform_.type in filter_list and temp_prioritization < platform_.metro.work_count:
                temp_index = index_
                temp_prioritization = platform_.metro.work_count
        if temp_index == -1:
            return None
        return self.platform_list[temp_index]
    
    def get_mv_platform_index(self, platform_: transfer_table) -> int:
        '''给定移车台返回索引'''
        for index_, platform__ in enumerate(self.moving_vehicles_platform):
            if platform__.get_name() == platform_.get_name():
                return index_
    
class data_record:
    '''数据记录与打印'''
    def __init__(self, m_environment: environment):
        self.name = "方案" + str(m_environment.program_index) + "试验记录" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.LOG = logger_make(self.name)
        '''进车总数'''
        self.total_number_of_incoming_vehicles = 0
        self.lastday_number_of_incoming_vehicles = 0
        '''落车总数'''
        self.total_number_of_vehicles_dropped = 0
        self.lastday_number_of_vehicles_dropped = 0
        '''每一个移车台的移动计数'''
        self.total_moving_vehicles_platform_removw_index = [0] * len(m_environment.moving_vehicles_platform)
        self.lastday_moving_vehicles_platform_removw_index = [0] * len(m_environment.moving_vehicles_platform)
        '''所有异常的记录'''
        self.error_record = []
        self.error_record_temp = []
        self.error_day_count = 0
        self.error_platform_count = 0
        '''要记录并保存的数据'''
        self.save_data_ = []
        
    def save_data(self, m_environment: environment) -> None:
        np.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "data", self.name + ".npy"), self.save_data_)
        for ch in self.error_record_temp:
            self.error_record.append(ch + [m_environment.time_count])
        pd.DataFrame(self.error_record, columns=["task", "start", "end"]).to_csv(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "data", self.name + "-error.csv"))

    def event_start(self, m_environment: environment) -> None:
        '''触发循环的开始，更新数据'''
        self.LOG.debug("-" * 20 + "第" + str(m_environment.get_real_days() + 1) + "天 " + str(m_environment.get_real_hours()) + " 时 " + str(m_environment.get_real_minutes()) + " 分" + "-" * 20)
          
    def event_input(self, m_environment: environment) -> None:
        '''触发进车，更新数据'''
        for platform_ in m_environment.platform_list:
            if platform_.type == "进车台位" and platform_.work_count == 0 and not platform_.metro is None:
                self.LOG.debug(platform_.name + "号" + platform_.type + "进了" + str(platform_.metro.index) + "号" + platform_.metro.type + "型车")
                self.total_number_of_incoming_vehicles += 1
        
    def event_output(self, m_environment: environment, output_metro: metro) -> None:
        '''触发落车，更新数据'''
        self.LOG.info(str(output_metro.index) + "号" + output_metro.type + "型车已经落车，在车间中呆了" + str(output_metro.work_count * m_environment.TIME_STEP / 60) + "小时的上班时间")
        self.total_number_of_vehicles_dropped += 1
        
    def event_mv_input(self, m_environment: environment, output_platform: stage, input_platform: transfer_table) -> None:
        '''触发移车台进车，更新数据'''
        self.LOG.debug(input_platform.get_name() + "从" + output_platform.get_name() + "进了" + str(input_platform.metro.index) + "号" + input_platform.metro.type + "型车")
        self.total_moving_vehicles_platform_removw_index[m_environment.get_mv_platform_index(input_platform)] += 1
        
    def event_mv_output(self, m_environment: environment, output_platform: transfer_table, input_platform: stage) -> None:
        '''触发移车台落车，更新数据'''
        self.LOG.debug(input_platform.get_name() + "从" + output_platform.get_name() + "进了" + str(input_platform.metro.index) + "号" + input_platform.metro.type + "型车")
        self.total_moving_vehicles_platform_removw_index[m_environment.get_mv_platform_index(output_platform)] += 1

    def event_work(self, m_environment: environment) -> None:
        '''触发工作，更新数据'''
        for platform_ in m_environment.platform_list + m_environment.moving_vehicles_platform:
            temp_str = platform_.get_status()
            if temp_str != "工作已完成但是车未移走":
                self.LOG.debug(platform_.get_name() + ":" + temp_str)
                for ch in self.error_record_temp:
                    if ch[0] == platform_.get_name():
                        self.error_record.append(ch + [m_environment.time_count])
                        self.error_record_temp.remove(ch)
                        break
            else:
                self.LOG.warning(platform_.get_name() + ":" + temp_str)
                self.error_day_count += 1
                if len(self.error_record_temp) == 0 or platform_.get_name() not in [ch[0] for ch in self.error_record_temp]:
                    self.error_platform_count += 1
                    self.error_record_temp.append([platform_.get_name(), m_environment.time_count])
        # 检测到过了新的一天         
        if m_environment.get_real_days() != 0 and m_environment.get_real_hours() == 0 and m_environment.get_real_minutes() == 0:
            temp_data = []
            self.LOG.debug("-" * 20 + "打印当天状态" + "-" * 20)
            self.LOG.info("-" * 40)
            self.LOG.info("第" + str(m_environment.get_real_days()) + "天一共进车" + str(self.total_number_of_incoming_vehicles - self.lastday_number_of_incoming_vehicles) + "节")
            temp_data.append(self.total_number_of_incoming_vehicles - self.lastday_number_of_incoming_vehicles)
            self.LOG.info("第" + str(m_environment.get_real_days()) + "天一共落车" + str(self.total_number_of_vehicles_dropped - self.lastday_number_of_vehicles_dropped) + "节")
            temp_data.append(self.total_number_of_vehicles_dropped - self.lastday_number_of_vehicles_dropped)
            self.lastday_number_of_incoming_vehicles = self.total_number_of_incoming_vehicles
            self.lastday_number_of_vehicles_dropped = self.total_number_of_vehicles_dropped
            temp_sum = 0
            for mv_index, mv_platform in enumerate(m_environment.moving_vehicles_platform):
                self.LOG.info("第" + str(m_environment.get_real_days()) + "天" + str(mv_platform.name) + "号移车台移动了" + str(int(self.total_moving_vehicles_platform_removw_index[mv_index] - self.lastday_moving_vehicles_platform_removw_index[mv_index])) + "次")
                temp_sum += int(self.total_moving_vehicles_platform_removw_index[mv_index] - self.lastday_moving_vehicles_platform_removw_index[mv_index])
                self.lastday_moving_vehicles_platform_removw_index[mv_index] = self.total_moving_vehicles_platform_removw_index[mv_index]
            self.LOG.info("第" + str(m_environment.get_real_days()) + "天移车台一共移动了" + str(temp_sum) + "次")
            temp_data.append(temp_sum)
            self.LOG.info("第" + str(m_environment.get_real_days()) + "天时一共发生了" + str(self.error_platform_count) + "个异常")
            temp_data.append(self.error_platform_count)
            self.error_platform_count = 0
            self.LOG.info("第" + str(m_environment.get_real_days()) + "天时一共发生" + str(self.error_day_count * 10) + "分钟的异常")
            temp_data.append(self.error_day_count)
            self.error_day_count = 0
            self.LOG.info("第" + str(m_environment.get_real_days()) + "天时一共有" + str(len(self.error_record_temp)) + "个异常正在发生")
            for error_ in self.error_record_temp:
                self.LOG.info("由" + error_[0] + "引发在第" + str(m_environment.get_real_days(error_[1]) + 1) + "天 " + str(m_environment.get_real_hours(error_[1])) + " 时 " + str(m_environment.get_real_minutes(error_[1])) + " 分")
            self.LOG.info("-" * 40)
            self.save_data_.append(temp_data)
