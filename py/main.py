
from cli_gui import DirectionView
from gamepad_control import GamePadControler as GPC
 

if __name__ == '__main__':
    print('Hey')
        gpc = GPC()
            dv_left = DirectionView()
                dv_right = DirectionView()
                    while(1):
                                gpc.update(info=0)

#        data = gpc.childs['rightstick'].data
#        data = gpc.btns['LHstick'].data
        left = gpc.btns['leftstick'].fdata
                right = gpc.btns['rightstick'].fdata

                        dv_left.show_direction(left)
                                dv_right.show_direction(right)
                                
