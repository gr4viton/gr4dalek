from state import State

import shared_globals

class ButtonControl():
    state = None
    def __init__(q):
        
#r d l u
        states_str = \
"""0 0 0 0 0 0 0 0 idle
0 0 0 1 100 100 100 100 front
0 0 1 0 -100 100 -100 100 turn_left
0 1 0 0 -100 -100 -100 -100 reverse 
1 0 0 0 100 -100 100 -100 turn_right
0 0 1 1 100 -100 -100 100 go_left
1 0 0 1 -100 100 100 -100 go_right"""

#r d l u
        states_str_test = \
"""0 0 0 0 0 0 0 0 idle
0 0 0 1 100 0 0 0 RF
0 0 1 0 0 0 100 0 RB
0 1 0 0 0 100 0 0 LF
1 0 0 0 0 0 0 100 LB"""

 #       states_str = states_str_test
        states_list = states_str.split('\n')

        q.states = []
        for state_str in states_list:
            btns_state = []
            vels = []

            state_list = state_str.split()

            for i in range(4):
                btns_state.append(int(state_list[i])==1)
            for i in [4,5,6,7]:
                vels.append(float(state_list[i]))

            name = state_list[-1]

            state = State(btns_state, vels, name)
            print('state', btns_state, vels, name)
            q.states.append(state)
        
        q.state = q.states[0]

    def querry_state(q):
        q.btns_pressed = shared_globals.btns_pressed
        for state in q.states:
            if state.btns_state == q.btns_pressed:
#                print(state.btns_state, '?=', q.btns_pressed)                
                if q.state != state:
                    q.state = state                
                    return state, q.state
        return None

                    



