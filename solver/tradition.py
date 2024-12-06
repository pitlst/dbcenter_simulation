from utils.environment import metro, stage, transfer_table, environment, data_record
    
def simulation_once(progame_index: int):
    # 初始化环境
    m_environment = environment(progame_index)
    m_record = data_record(progame_index)
    
    # 移车台和预定的移入的台位名称的映射
    reservations_dict: dict[str, str] = {}
        
    # 开始模拟
    while m_record.total_number_of_vehicles_dropped < m_environment.NUMBER_OF_METRO_DROP_OFF:
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
                m_record.event_mv_output(m_environment)
        # 检查移车台进车
        for platform_ in m_environment.moving_vehicles_platform:
            if platform_.can_input():
                ...
                m_record.event_mv_input(m_environment)
                
        # 开始工作
        m_environment.work()
        m_record.event_work(m_environment)
        # 开始时间流逝
        m_environment.lapse()
        m_record.event_step(m_environment)