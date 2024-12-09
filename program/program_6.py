# 每次循环步进多少分钟
TIME_STEP = 10
# 每天的工作时长（分钟）
DAY_WORK_TIME = 8 * 60
# 是否使用喷砂间
USE_OF_THE_BLASTING_ROOM = True
# 落车数量
NUMBER_OF_METRO_DROP_OFF = 500
# 进车队列
APPROACH_QUEUE = ["A", "B", "B"] * 3000
# 每天进车数量，默认是当天早上进车一辆，中午进车一辆
NUMBER_OF_INCOMING_VEHICLES_PER_DAY = 2
# 转运车数量
NUMBER_OF_TRANS_SHIPMENT_VEHICLES = 3

# 是否启用转运车在喷砂间和总成分离的模式
ENABLING_SEPARATION_OF_TRANSFER_VEHICLES = True
# 各个转运车服务的台位
STATIONS_SERVICED_BY_TRANSFER_VANS = \
[
    ["粘接预装台位(1)", "粘接预装台位(2)"],
    ["进车台位", "自动化粘接台位", "普通组装1类", "模块化组装", "普通组装2类(A车)", "普通组装2类(BC车)", "落车台位"],
    ["进车台位", "自动化粘接台位", "普通组装1类", "模块化组装", "普通组装2类(A车)", "普通组装2类(BC车)", "落车台位"]
]
# 所有的台位
ALL_STAGE_CONFIG = \
{
    "进车台位":
    {
        "作业周期":3.5*60,
        "适用车型":["A", "B"],
        "下一台位类型": ["粘接预装台位(1)"],
        "具体台位":
        [
            {
                "台位号":"1",
                "转运时长":30
            }    
        ]
    },
    "粘接预装台位(1)":
    {
        "作业周期":3.5*60,
        # "作业周期":230,
        "适用车型":["A", "B"],
        "下一台位类型": ["粘接预装台位(2)"],
        "具体台位":
        [
            {
                "台位号":"粘接预装台位(1)",
                "转运时长":10
            }  
        ]
    },
    "粘接预装台位(2)":
    {
        "作业周期":3.5*60,
        # "作业周期":230,
        "适用车型":["A", "B"],
        "下一台位类型": ["自动化粘接台位"],
        "具体台位":
        [
            {
                "台位号":"粘接预装台位(2)",
                "转运时长":10
            }  
        ]
    },
    "自动化粘接台位":
    {
        "作业周期":3.5*60,
        "适用车型":["A", "B"],
        "下一台位类型": ["普通组装1类"],
        "具体台位":
        [
            {
                "台位号":"自动化粘接台位",
                "转运时长":30
            }
        ]
    },
    "普通组装1类":
    {
        "作业周期":23.5*60,
        "适用车型":["A", "B"],
        "下一台位类型": ["模块化组装"],
        "具体台位":
        [
            {
                "台位号":"2",
                "转运时长":30
            },
            {
                "台位号":"3",
                "转运时长":30
            },
            {
                "台位号":"4",
                "转运时长":30
            },
            {
                "台位号":"5",
                "转运时长":30
            },
            {
                "台位号":"27",
                "转运时长":30
            },
            {
                "台位号":"28",
                "转运时长":30
            }
        ]
    },    
    "模块化组装":
    {
        "作业周期":7.5*60,
        "适用车型":["A", "B"],
        "下一台位类型": ["普通组装2类(A车)", "普通组装2类(BC车)"],
        "具体台位":
        [
            {
                "台位号":"7",
                "转运时长":30
            },
            {
                "台位号":"8",
                "转运时长":30
            }
        ]
    }, 
    "普通组装2类(A车)":
    {
        "作业周期":71.5*60,
        "适用车型":["A"],
        "下一台位类型": ["落车台位"],
        "具体台位":
        [
            {
                "台位号":"11",
                "转运时长":30
            },
            {
                "台位号":"13",
                "转运时长":30
            },
            {
                "台位号":"15",
                "转运时长":30
            },
            {
                "台位号":"17",
                "转运时长":30
            },
            {
                "台位号":"19",
                "转运时长":30
            },
            {
                "台位号":"21",
                "转运时长":30
            }
        ]
    }, 
    "普通组装2类(BC车)":
    {
        "作业周期":71.5*60,
        "适用车型":["B"],
        "下一台位类型": ["落车台位"],
        "具体台位":
        [
            {
                "台位号":"12",
                "转运时长":60
            },
            {
                "台位号":"14",
                "转运时长":60
            },
            {
                "台位号":"16",
                "转运时长":60
            },
            {
                "台位号":"18",
                "转运时长":60
            },
            {
                "台位号":"20",
                "转运时长":60
            },
            {
                "台位号":"22",
                "转运时长":60
            },
            {
                "台位号":"23",
                "转运时长":30
            },
            {
                "台位号":"24",
                "转运时长":60
            },
            {
                "台位号":"25",
                "转运时长":30
            },
            {
                "台位号":"26",
                "转运时长":60
            },            
            {
                "台位号":"27",
                "转运时长":30
            },
            {
                "台位号":"28",
                "转运时长":60
            }
        ]
    },
    "落车台位":
    {
        "作业周期":3.5*60,
        "适用车型":["A", "B"],
        "下一台位类型": [],
        "具体台位":
        [
            {
                "台位号":"落车1",
                "转运时长":30
            },
            {
                "台位号":"落车2",
                "转运时长":30
            }
        ]
    }
} 
