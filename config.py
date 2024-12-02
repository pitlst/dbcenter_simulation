# 是否使用喷砂间
USE_OF_THE_BLASTING_ROOM = False
# 进车数量
NUMBER_OF_METRO_DROP_OFF = 500
# 转运车数量
NUMBER_OF_TRANS_SHIPMENT_VEHICLES = 2
if USE_OF_THE_BLASTING_ROOM:
    # 是否启用转运车在喷砂间和总成分离的模式
    ENABLING_SEPARATION_OF_TRANSFER_VEHICLES = False
    if ENABLING_SEPARATION_OF_TRANSFER_VEHICLES:
        # 喷砂间转运车总数
        NUMBER_OF_TRANSFER_TRUCKS_IN_THE_BLASTING_ROOM = 1
        # 总成转运车总数
        NUMBER_OF_TRANS_SHIPMENT_TRUCKS_IN_ASSEMBLY_HALLS = 1
        assert NUMBER_OF_TRANSFER_TRUCKS_IN_THE_BLASTING_ROOM + NUMBER_OF_TRANS_SHIPMENT_TRUCKS_IN_ASSEMBLY_HALLS <= NUMBER_OF_TRANS_SHIPMENT_VEHICLES, "转运车总数超过规定"

        

if USE_OF_THE_BLASTING_ROOM:
    ALL_STAGE = ["进车台位", 
                "粘接预装台位_1", 
                "粘接预装台位_2", 
                "自动化粘接台位", 
                "普通组装1类" ,
                "模块化组装" ,
                "普通组装2类_A车" ,
                "普通组装2类_BC车" ,
                "落车台位"
                ]
else:
    ALL_STAGE = ["进车台位", 
            "粘接预装台位", 
            "自动化粘接台位", 
            "普通组装1类", 
            "模块化组装" ,
            "普通组装2类_A车" ,
            "普通组装2类_BC车" ,
            "落车台位"
            ]