# initial position setting  ------------------------------------------------

initial_pos = [-11.79, -19.07, 103.95, 3.90, 3.63, -3.97]

# Picking in mode           ------------------------------------------------

""" cabinet 0 planning [PICK IN]"""
caninet_0_pickin_0 = [0.66, -9.33, 88.23, 3.46, 6.13, -3.96]
caninet_0_pickin_1 = [0.66, -0.25, 78.89, 2.70, 7.55, -3.96]
caninet_0_pickin_2 = [0.53, 22.24, 53.23, 2.69, 7.54, -3.96]
caninet_0_pickin_3 = [0.56, 22.19, 53.36, 2.68, 4.72, -3.96]
caninet_0_pickin_4 = [0.57, -30.98, 105.44, 2.68, 4.74, -3.96]

""" cabinet 1 planning [PICK IN]"""

""" cabinet 2 planning [PICK IN]"""

""" cabinet 3 planning [PICK IN]"""

# entrance - gazett - 도킹 - 들어올리기 - 빼내기
caninet_3_pickin_0 = [-19.27, -9.46, 89.87, 3.90, 3.65, -3.96]  
caninet_3_pickin_1 = [-19.61, 1.74, 78.65, 3.90, 3.66, -3.95]
caninet_3_pickin_2 = [-19.97, 20.14, 56.05, 3.93, 7.19, -3.95]
caninet_3_pickin_3 = [-19.97, 18.58, 56.08, 3.93, 7.21, -3.95]
caninet_3_pickin_4 = [-19.97, -26.80, 99.28, 4.12, 9.02, -3.95]


""" cabinet 4 planning [PICK IN]"""

# entrance - gazett - 도킹 - 들어올리기 - 빼내기
caninet_4_pickin_0 = [-18.46, -8.70, 109.96, -1.18, -16.30, 1.04]
caninet_4_pickin_1 = [-19.93, -0.12, 101.61, -1.18, -16.30, 1.04]
caninet_4_pickin_2 = [-19.93, 21.43, 76.65, -1.18, -15.61, 1.04]
caninet_4_pickin_3 = [-19.93, 19.30, 76.87, -1.19, -15.60, 1.04]
caninet_4_pickin_4 = [-20.42, -29.81, 124.91, -1.18, -15.59, 1.04]

""" cabinet 5 planning [PICK IN]"""
caninet_5_pickin_0 = [-19.61, 2.87, 119.58, -0.24, -34.49, -3.95]
caninet_5_pickin_1 = [-19.50, 8.21, 114.19, -0.24, -34.49, -3.95]
caninet_5_pickin_2 = [-19.63, 28.39, 89.09, -0.24, -34.49, -3.95]
caninet_5_pickin_3 = [-19.63, 28.37, 90.14, -0.29, -37.69, -3.95]
caninet_5_pickin_4 = [-19.65, -21.33, 141.39, -0.28, -42.33, -3.95]

""" go to client [COMMON] """
goto_client_0 = [-94.89, -19.11, 103.95, 3.90, 3.64, -3.96]


""" path planning """
cabinet_0_planning = [caninet_0_pickin_0, caninet_0_pickin_1, caninet_0_pickin_2, caninet_0_pickin_3, caninet_0_pickin_4]
cabinet_1_planning = []
cabinet_2_planning = []
cabinet_3_planning = [caninet_3_pickin_0, caninet_3_pickin_1, caninet_3_pickin_2, caninet_3_pickin_3, caninet_3_pickin_4]
cabinet_4_planning = [caninet_4_pickin_0, caninet_4_pickin_1, caninet_4_pickin_2, caninet_4_pickin_3, caninet_4_pickin_4]
cabinet_5_planning = [caninet_5_pickin_0, caninet_5_pickin_1, caninet_5_pickin_2, caninet_5_pickin_3, caninet_5_pickin_4]