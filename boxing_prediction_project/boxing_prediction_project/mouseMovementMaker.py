from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
import scipy.interpolate as si

class MouseMoventMaker:

    def __init__(self):
        self.x_i, self.y_i = self.__getMoveMousePoints()

    def moveMouse(self, element):
        action =  ActionChains(self.driver)

        action.move_to_element(element);
        action.perform();

        for mouse_x, mouse_y in zip(self.x_i, self.y_i):
            action.move_by_offset(mouse_x,mouse_y);
            action.perform();
    
    def __getMoveMousePoints(self):
        # Curve base:
        points = [[0, 0], [0, 2], [2, 3], [4, 0], [6, 3], [8, 2], [8, 0]];
        points = np.array(points)

        x = points[:,0]
        y = points[:,1]


        t = range(len(points))
        ipl_t = np.linspace(0.0, len(points) - 1, 25)

        x_tup = si.splrep(t, x, k=3)
        y_tup = si.splrep(t, y, k=3)

        x_list = list(x_tup)
        xl = x.tolist()
        x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

        y_list = list(y_tup)
        yl = y.tolist()
        y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

        x_i = si.splev(ipl_t, x_list) # x interpolate values
        y_i = si.splev(ipl_t, y_list) # y interpolate values
        return x_i, y_i