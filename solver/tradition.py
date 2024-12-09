from utils.environment import environment, data_record
    
def simulation(progame_index: int):
    # 初始化环境
    m_environment = environment(progame_index)
    m_record = data_record(m_environment)
    
    # 移车台和预定的移入的台位名称的映射
    reservations_dict: dict[str, str] = {}
        
    # 开始模拟
    while m_record.total_number_of_vehicles_dropped < m_environment.NUMBER_OF_METRO_DROP_OFF:
        m_record.event_start(m_environment)
        # 检查进车
        input_platform = m_environment.get_platform_with_name("进车台位1号")
        if input_platform.can_input():
            temp_metro = m_environment.get_input_metro()
            if not temp_metro is None:
                input_platform.input(temp_metro)
                m_record.event_input(m_environment)
        # 检查落车
        output_platform = m_environment.get_stage_with_type("落车台位")
        for platform_ in output_platform:
            if platform_.can_output():
                m_record.event_output(m_environment, platform_.output())
        # 检查移车台落车
        for platform_ in m_environment.moving_vehicles_platform:
            if platform_.can_output():
                temp_platform = m_environment.get_platform_with_name(reservations_dict[platform_.get_name()])
                temp_platform.input(platform_.output())
                m_record.event_mv_output(m_environment, platform_, temp_platform)
        # 检查移车台进车
        for platform_ in m_environment.moving_vehicles_platform:
            if platform_.can_input():
                # 这个函数会检查是否能够出车
                if m_environment.USE_OF_THE_BLASTING_ROOM and m_environment.ENABLING_SEPARATION_OF_TRANSFER_VEHICLES:
                    temp_stage = m_environment.get_max_wait_metro_with_filter(platform_.can_remove_stage_type)
                else:
                    temp_stage = m_environment.get_max_wait_metro()
                if not temp_stage is None:
                    next_platform = m_environment.get_stage_with_type(temp_stage.next_type)
                    for stage_ in next_platform:
                        if stage_.can_input() and temp_stage.metro.type in stage_.can_input_metro_type:
                            platform_.input(temp_stage.output(), m_environment.get_trans_time(temp_stage.name), temp_stage)
                            reservations_dict[platform_.get_name()] = stage_.get_name()
                            m_record.event_mv_input(m_environment, temp_stage, platform_)
                            break    
        # 开始时间流逝
        m_environment.lapse()
        m_record.event_work(m_environment)
    m_record.save_data(m_environment)