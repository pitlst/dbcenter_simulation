import pandas as pd
import numpy as np
import os
from utils.logger import logger_make
from utils.workspace import metro, stage, transfer_table, can_save_metro_object

# 每循环并计数一次代表10分钟
time_step_factor = 10
# 每天工作8小时
work_time = 8 * 60
    
def get_trans_time(temp_dict: dict, temp_key: str) -> int:
    '''给台位号获取转运时长'''
    for ch in temp_dict:
        for ch_ in temp_dict[ch]["具体台位"]:
            if ch_["台位号"] == temp_key:
                return ch_["转运时长"] / time_step_factor
            
def get_max_metro(platform_list: list[metro]) -> int:
    '''寻找输入台位中拥有等待时间最长的车的索引'''
    temp_index = -1
    temp_prioritization = -1
    for index_, platform_ in enumerate(platform_list):
        if not platform_.metro is None and temp_prioritization < platform_.metro.work_count:
            temp_index = index_
            temp_prioritization = platform_.metro.work_count
    return temp_index

def get_max_metro_with_filter(platform_list: list[metro], filter_list: list[str]) -> int:
    '''寻找输入台位中拥有等待时间最长的车的索引,带上筛选'''
    temp_index = -1
    temp_prioritization = -1
    for index_, platform_ in enumerate(platform_list):
        if not platform_.metro is None and index_ in filter_list and temp_prioritization < platform_.metro.work_count:
            temp_index = index_
            temp_prioritization = platform_.metro.work_count
    return temp_index

def filter_platform(input_platform_list: list[stage], filter_list: list[str]) -> list[int]:
    '''筛选移车台中符合要求的，返回在列表中的索引'''
    temp_list = []
    for index_, platform_ in enumerate(input_platform_list):
        if platform_.type in filter_list:
            temp_list.append(index_)
    return temp_list

def find_index(input_list: list, request_ch) -> int:
    '''寻找对应的索引'''
    for i, ch in enumerate(input_list):
        if ch == request_ch:
            return i
        
def get_platform_name(_platform: can_save_metro_object) -> str:
    '''获取名称'''
    if isinstance(_platform, stage):
        return _platform.type + _platform.name  + "号"
    elif isinstance(_platform, transfer_table):
        return _platform.name  + "号"
    return None

def transit_logic(
    USE_OF_THE_BLASTING_ROOM: bool,
    NUMBER_OF_METRO_DROP_OFF: int,
    APPROACH_QUEUE: list[str],
    NUMBER_OF_INCOMING_VEHICLES_PER_DAY: int,
    NUMBER_OF_TRANS_SHIPMENT_VEHICLES: int, 
    ENABLING_SEPARATION_OF_TRANSFER_VEHICLES: bool,
    STATIONS_SERVICED_BY_TRANSFER_VANS: list[list[str]],
    ALL_STAGE_CONFIG: dict[str, dict]
    ) -> None:
    # 初始化日志
    TIME_LOG = logger_make("时间记录")
    STATE_LOG = logger_make("状态记录")
    
    # 按照规则初始化车间资源
    '''移车台'''
    moving_vehicles_platform = [transfer_table(str(i)) for i in range(NUMBER_OF_TRANS_SHIPMENT_VEHICLES)]
    '''台位'''
    platform_list: list[stage] = []
    for platform_type in ALL_STAGE_CONFIG:
        for platform_ in ALL_STAGE_CONFIG[platform_type]["具体台位"]:
            platform_list.append(stage(platform_["台位号"], platform_type, int(ALL_STAGE_CONFIG[platform_type]["作业周期"] / time_step_factor)))
    '''时间计数'''
    time_step = 0
    '''进车总数'''
    total_number_of_incoming_vehicles = 0
    lastday_number_of_incoming_vehicles = 0
    '''落车总数'''
    total_number_of_vehicles_dropped = 0
    lastday_number_of_vehicles_dropped = 0
    '''被移车台预定移入的台位'''
    reservations_list = []
    reservations_moving_vehicles_list = []
    '''每一个移车台的移动计数'''
    total_moving_vehicles_platform_removw_index = [0] * len(moving_vehicles_platform)
    lastday_moving_vehicles_platform_removw_index = [0] * len(moving_vehicles_platform)
    '''所有异常的记录'''
    error_record = []
    error_record_temp = []
    '''要记录并保存的数据'''
    save_data = []
    
    
    # 开始模拟
    while total_number_of_vehicles_dropped < NUMBER_OF_METRO_DROP_OFF:
        TIME_LOG.debug("-" * 20 + "第" + str(int(time_step * time_step_factor / work_time) + 1) + "天 " + str(int(time_step * time_step_factor % work_time / 60)) + " 时 " + str(int(time_step * time_step_factor % work_time % 60)) + " 分" + "-" * 20)
        
        TIME_LOG.debug("-" * 20 + "开始进车" + "-" * 20 )
        for platform_ in platform_list:
            if platform_.type == "进车台位" and platform_.can_input() and len(APPROACH_QUEUE) != 0 and time_step * time_step_factor % work_time in [0, int(work_time / NUMBER_OF_INCOMING_VEHICLES_PER_DAY)]:
                platform_.input(metro(total_number_of_incoming_vehicles, APPROACH_QUEUE.pop(0)))
                total_number_of_incoming_vehicles += 1
                STATE_LOG.debug(platform_.name + "号" + platform_.type + "进了" + str(platform_.metro.index) + "号" + platform_.metro.type + "型车")

        TIME_LOG.debug("-" * 20 + "开始移车台进车" + "-" * 20)
        can_move = False
        '''本轮准备从这些台位移出车'''
        platform_from = []
        '''本轮准备移到这些台位'''
        platform_to = []
        
        for moving_vehicles in moving_vehicles_platform:
            if moving_vehicles.can_input():
                can_move = True
                break
        if can_move:
            # 启用转运车在喷砂间和总成分离的模式
            if USE_OF_THE_BLASTING_ROOM and ENABLING_SEPARATION_OF_TRANSFER_VEHICLES:
                for platform_ in platform_list:
                    if platform_.can_output() and not platform_ in platform_from:
                        for platform__ in platform_list:
                            if platform__.can_input() and platform__.type in ALL_STAGE_CONFIG[platform_.type]["下一台位类型"] and platform_.metro.type in ALL_STAGE_CONFIG[platform__.type]["适用车型"] and not platform__ in platform_to and not platform__ in reservations_list:
                                platform_from.append(platform_)
                                platform_to.append(platform__)
                                break
                for mv_index, mv_platform in enumerate(moving_vehicles_platform):
                    temp_platform_from_index = filter_platform(platform_from, STATIONS_SERVICED_BY_TRANSFER_VANS[mv_index])
                    if mv_platform.can_input() and len(temp_platform_from_index) != 0:
                        index_ = get_max_metro_with_filter(platform_from, temp_platform_from_index)
                        # 确定有对应的台位
                        if index_ != -1:
                            # print(platform_from[index_].type + platform_from[index_].name + "号到" + platform_to[index_].type + platform_to[index_].name + "号由" + mv_platform.name + "号移车台移动")
                            mv_platform.input(platform_from[index_].output(), get_trans_time(ALL_STAGE_CONFIG, platform_from[index_].name))
                            total_moving_vehicles_platform_removw_index[mv_index] += 1
                            # 预定将要驶入的台位和正在转运的车
                            reservations_list.append(platform_to[index_])
                            reservations_moving_vehicles_list.append(mv_platform.name)
                            # 去除记录的移车需求
                            platform_from.pop(index_)
                            platform_to.pop(index_)
                        
            else:
                for platform_ in platform_list:
                    if platform_.can_output() and not platform_ in platform_from:
                        for platform__ in platform_list:
                            if platform__.can_input() and platform__.type in ALL_STAGE_CONFIG[platform_.type]["下一台位类型"] and platform_.metro.type in ALL_STAGE_CONFIG[platform__.type]["适用车型"] and not platform__ in platform_to and not platform__ in reservations_list:
                                platform_from.append(platform_)
                                platform_to.append(platform__)
                                break
                # 求移车优先级
                for mv_index, mv_platform in enumerate(moving_vehicles_platform):
                    if mv_platform.can_input() and len(platform_from) != 0:
                        index_ = get_max_metro(platform_from)
                        # print(platform_from[index_].type + platform_from[index_].name + "号到" + platform_to[index_].type + platform_to[index_].name + "号由" + mv_platform.name + "号移车台移动")
                        # 移车
                        mv_platform.input(platform_from[index_].output(), get_trans_time(ALL_STAGE_CONFIG, platform_from[index_].name))
                        total_moving_vehicles_platform_removw_index[mv_index] += 1
                        # 预定将要驶入的台位和正在转运的车
                        reservations_list.append(platform_to[index_])
                        reservations_moving_vehicles_list.append(mv_platform.name)
                        # 去除记录的移车需求
                        platform_from.pop(index_)
                        platform_to.pop(index_)

        
        TIME_LOG.debug("-" * 20 + "开始移车台出车" + "-" * 20)
        for mv_index, mv_platform in enumerate(moving_vehicles_platform):
            if mv_platform.can_output():
                index_ = find_index(reservations_moving_vehicles_list, mv_platform.name)
                if index_ != -1:
                    reservations_list[index_].input(mv_platform.output())
                    reservations_moving_vehicles_list.pop(index_)
                    reservations_list.pop(index_)
                    
        TIME_LOG.debug("-" * 20 + "开始落车" + "-" * 20)
        for platform_ in platform_list:
            if platform_.type == "落车台位" and platform_.can_output():
                worked_stage = platform_.output()
                total_number_of_vehicles_dropped += 1
                STATE_LOG.info(str(worked_stage.index) + "号" + worked_stage.type + "型车已经落车，在车间中呆了" + str(worked_stage.work_count * time_step_factor / 60) + "小时的上班时间")
                
        TIME_LOG.debug("-" * 20 + "打印各个单位状态" + "-" * 20)
        for platform_ in platform_list + moving_vehicles_platform:
            platform_.log_status()
            if platform_.get_status() == "工作已完成但是车未移走":
                if len(error_record_temp) == 0 or get_platform_name(platform_) not in [ch[0] for ch in error_record_temp]:
                    error_record_temp.append([get_platform_name(platform_), time_step])
            else:
                for ch in error_record_temp:
                    if ch[0] == get_platform_name(platform_):
                        error_record.append(ch + [time_step])
                        error_record_temp.remove(ch)
                        break
            
        TIME_LOG.debug("-" * 20 + "开始工作" + "-" * 20)
        for platform_ in platform_list + moving_vehicles_platform:
            platform_.work()
        
        time_step += 1
        if time_step != 0  and time_step % (work_time / time_step_factor) == 0:
            temp_data = []
            TIME_LOG.debug("-" * 20 + "打印当天状态" + "-" * 20)
            STATE_LOG.info("-" * 40)
            STATE_LOG.info("第" + str(int(time_step * time_step_factor / work_time)) + "天一共进车" + str(total_number_of_incoming_vehicles - lastday_number_of_incoming_vehicles) + "节")
            temp_data.append(total_number_of_incoming_vehicles - lastday_number_of_incoming_vehicles)
            STATE_LOG.info("第" + str(int(time_step * time_step_factor / work_time)) + "天一共落车" + str(total_number_of_vehicles_dropped - lastday_number_of_vehicles_dropped) + "节")
            temp_data.append(total_number_of_vehicles_dropped - lastday_number_of_vehicles_dropped)
            lastday_number_of_incoming_vehicles = total_number_of_incoming_vehicles
            lastday_number_of_vehicles_dropped = total_number_of_vehicles_dropped
            temp_sum = 0
            for mv_index, mv_platform in enumerate(moving_vehicles_platform):
                STATE_LOG.info("第" + str(int(time_step * time_step_factor / work_time)) + "天" + str(mv_platform.name) + "号移车台移动了" + str(int(total_moving_vehicles_platform_removw_index[mv_index] - lastday_moving_vehicles_platform_removw_index[mv_index])) + "次")
                temp_sum += int(total_moving_vehicles_platform_removw_index[mv_index] - lastday_moving_vehicles_platform_removw_index[mv_index])
                lastday_moving_vehicles_platform_removw_index[mv_index] = total_moving_vehicles_platform_removw_index[mv_index]
            STATE_LOG.info("第" + str(int(time_step * time_step_factor / work_time)) + "天移车台一共移动了" + str(temp_sum) + "次")
            temp_data.append(temp_sum)
            STATE_LOG.info("第" + str(int(time_step * time_step_factor / work_time)) + "天时一共有" + str(len(error_record_temp)) + "个异常正在发生")
            for error_ in error_record_temp:
                STATE_LOG.info("由" + error_[0] + "引发在第" + str(int(error_[1] * time_step_factor / work_time) + 1) + "天 " + str(int(error_[1] * time_step_factor % work_time / 60)) + " 时 " + str(int(error_[1] * time_step_factor % work_time % 60)) + " 分")
            STATE_LOG.info("-" * 40)
            
            save_data.append(temp_data)
            
            # input()
        

    np.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "analyze", "temp.npy"), save_data)
    for ch in error_record_temp:
        error_record.append(ch + [time_step])
    pd.DataFrame(error_record, columns=["task", "start", "end"]).to_csv(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "analyze", "error.csv"))
        