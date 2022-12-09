import math
fps = 60
#------------------PRZELICZONE ROZMIARY ELEMENTÓW EKRANU WZGLĘDEM JEGO SZEROKOŚCI-------------------

# wartości wzięte z tła gry

screen_w = 600
screen_h = 800

road_w = 331
road_w_pc = round(road_w/screen_w, 5)

lane_w = 78
lane_w_pc = round(lane_w/screen_w, 5)

strip_w = 7
strip_w_pc = round(strip_w/screen_w, 5)

left_road_border = 134
left_road_border_pc = round(left_road_border/screen_w, 5)
right_road_border = 465
right_road_border_pc = round(right_road_border/screen_w, 5)

first_lane_mostleft = left_road_border
second_lane_mostleft = first_lane_mostleft + lane_w + strip_w
third_lane_mostleft = second_lane_mostleft + lane_w + strip_w
fourth_lane_mostleft = third_lane_mostleft + lane_w + strip_w

lanes_leftmost_list = [first_lane_mostleft, second_lane_mostleft, third_lane_mostleft, fourth_lane_mostleft]
lanes_center_list = [i + lane_w //2 for i in lanes_leftmost_list]

if __name__ == '__main__':
    print(lanes_center_list)