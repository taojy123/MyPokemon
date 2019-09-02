"""
     普  格  飞  毒  地  岩  虫  鬼  火  水  草  电  超  冰  龙
普  1.0 1.0 1.0 1.0 1.0 0.5 1.0 0.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0
格  2.0 1.0 0.5 0.5 1.0 2.0 0.5 0.0 1.0 1.0 1.0 1.0 0.5 2.0 1.0
飞  1.0 2.0 1.0 1.0 1.0 0.5 2.0 1.0 1.0 1.0 2.0 0.5 1.0 1.0 1.0
毒  1.0 1.0 1.0 0.5 0.5 0.5 2.0 0.5 1.0 1.0 2.0 1.0 1.0 1.0 1.0
地  1.0 1.0 0.0 2.0 1.0 2.0 0.5 1.0 2.0 1.0 0.5 2.0 1.0 1.0 1.0
岩  1.0 0.5 2.0 1.0 0.5 1.0 2.0 1.0 2.0 1.0 1.0 1.0 1.0 2.0 1.0
虫  1.0 0.5 0.5 2.0 1.0 1.0 1.0 0.5 0.5 1.0 2.0 1.0 2.0 1.0 1.0
鬼  0.0 1.0 1.0 1.0 1.0 1.0 1.0 2.0 1.0 1.0 1.0 1.0 0.0 1.0 1.0
火  1.0 1.0 1.0 1.0 1.0 0.5 2.0 1.0 0.5 0.5 2.0 1.0 1.0 2.0 0.5
水  1.0 1.0 1.0 1.0 2.0 2.0 1.0 1.0 2.0 0.5 0.5 1.0 1.0 1.0 0.5
草  1.0 1.0 0.5 0.5 2.0 2.0 0.5 1.0 0.5 2.0 0.5 1.0 1.0 1.0 0.5
电  1.0 1.0 2.0 1.0 0.0 1.0 1.0 1.0 1.0 2.0 0.5 0.5 1.0 1.0 0.5
超  1.0 2.0 1.0 2.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 0.5 1.0 1.0
冰  1.0 1.0 2.0 1.0 2.0 1.0 1.0 1.0 1.0 0.5 2.0 1.0 1.0 0.5 2.0
龙  1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 2.0
"""

SYSTEM_MAP = {
    '普': {
        '普': 1, '格': 1, '飞': 1, '毒': 1, '地': 1, '岩': 0.5, '虫': 1, '鬼': 0, '火': 1, '水': 1, '草': 1, '电': 1, '超': 1, '冰': 1, '龙': 1,
    },
    '格': {
        '普': 2, '格': 1, '飞': 0.5, '毒': 0.5, '地': 1, '岩': 2, '虫': 0.5, '鬼': 0, '火': 1, '水': 1, '草': 1, '电': 1, '超': 0.5, '冰': 2, '龙': 1,
    },
    '飞': {
        '普': 1, '格': 2, '飞': 1, '毒': 1, '地': 1, '岩': 0.5, '虫': 2, '鬼': 1, '火': 1, '水': 1, '草': 2, '电': 0.5, '超': 1, '冰': 1, '龙': 1,
    },
    '毒': {
        '普': 1, '格': 1, '飞': 1, '毒': 0.5, '地': 0.5, '岩': 0.5, '虫': 2, '鬼': 0.5, '火': 1, '水': 1, '草': 2, '电': 1, '超': 1, '冰': 1, '龙': 1,
    },
    '地': {
        '普': 1, '格': 1, '飞': 0, '毒': 2, '地': 1, '岩': 2, '虫': 0.5, '鬼': 1, '火': 2, '水': 1, '草': 0.5, '电': 2, '超': 1, '冰': 1, '龙': 1,
    },
    '岩': {
        '普': 1, '格': 0.5, '飞': 2, '毒': 1, '地': 0.5, '岩': 1, '虫': 2, '鬼': 1, '火': 2, '水': 1, '草': 1, '电': 1, '超': 1, '冰': 2, '龙': 1,
    },
    '虫': {
        '普': 1, '格': 0.5, '飞': 0.5, '毒': 2, '地': 1, '岩': 1, '虫': 1, '鬼': 0.5, '火': 0.5, '水': 1, '草': 2, '电': 1, '超': 2, '冰': 1, '龙': 1,
    },
    '鬼': {
        '普': 0, '格': 1, '飞': 1, '毒': 1, '地': 1, '岩': 1, '虫': 1, '鬼': 2, '火': 1, '水': 1, '草': 1, '电': 1, '超': 0, '冰': 1, '龙': 1,
    },
    '火': {
        '普': 1, '格': 1, '飞': 1, '毒': 1, '地': 1, '岩': 0.5, '虫': 2, '鬼': 1, '火': 0.5, '水': 0.5, '草': 2, '电': 1, '超': 1, '冰': 2, '龙': 0.5,
    },
    '水': {
        '普': 1, '格': 1, '飞': 1, '毒': 1, '地': 2, '岩': 2, '虫': 1, '鬼': 1, '火': 2, '水': 0.5, '草': 0.5, '电': 1, '超': 1, '冰': 1, '龙': 0.5,
    },
    '草': {
        '普': 1, '格': 1, '飞': 0.5, '毒': 0.5, '地': 2, '岩': 2, '虫': 0.5, '鬼': 1, '火': 0.5, '水': 2, '草': 0.5, '电': 1, '超': 1, '冰': 1, '龙': 0.5,
    },
    '电': {
        '普': 1, '格': 1, '飞': 2, '毒': 1, '地': 0, '岩': 1, '虫': 1, '鬼': 1, '火': 1, '水': 2, '草': 0.5, '电': 0.5, '超': 1, '冰': 1, '龙': 0.5,
    },
    '超': {
        '普': 1, '格': 2, '飞': 1, '毒': 2, '地': 1, '岩': 1, '虫': 1, '鬼': 1, '火': 1, '水': 1, '草': 1, '电': 1, '超': 0.5, '冰': 1, '龙': 1,
    },
    '冰': {
        '普': 1, '格': 1, '飞': 2, '毒': 1, '地': 2, '岩': 1, '虫': 1, '鬼': 1, '火': 1, '水': 0.5, '草': 2, '电': 1, '超': 1, '冰': 0.5, '龙': 2,
    },
    '龙': {
        '普': 1, '格': 1, '飞': 1, '毒': 1, '地': 1, '岩': 1, '虫': 1, '鬼': 1, '火': 1, '水': 1, '草': 1, '电': 1, '超': 1, '冰': 1, '龙': 2,
    },
}
