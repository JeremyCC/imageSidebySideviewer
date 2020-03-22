'''
COPYRIGHT © 2020 JeremyCC, Github

Distribution is allowed under License
"GNU General Public License v3.0"

'''

import matplotlib.pyplot as plt
import numpy as np
import copy
import time
import gc
import multiprocessing


class comparer(object):

    def defcolormapping(self, colormapping=None):
        if colormapping is not None:
            '''Self define value color mapping: input=pixel color output=plt color code'''
            self.wcolor = colormapping
        else:
            '''Default value color mapping function'''

            def mycolor(pixelvalue, minv=None, maxv=None):
                if pixelvalue.dtype == np.uint8:
                    if isinstance(pixelvalue, np.ndarray):
                        if pixelvalue.mean() > 125:
                            return 'black'
                        else:
                            return 'w'
                    else:
                        if pixelvalue > 125:
                            return 'black'
                        else:
                            return 'w'
                elif pixelvalue.dtype == np.uint16:
                    if isinstance(pixelvalue, np.ndarray):
                        if pixelvalue.mean() > 32765:
                            return 'black'
                        else:
                            return 'w'
                    else:
                        if pixelvalue > 32765:
                            return 'black'
                        else:
                            return 'w'
                else:
                    if isinstance(pixelvalue, np.ndarray):
                        if pixelvalue.mean() > (maxv + minv) / 2:
                            return 'black'
                        else:
                            return 'w'
                    else:
                        if pixelvalue > (maxv + minv) / 2:
                            return 'black'
                        else:
                            return 'w'

            self.wcolor = mycolor

    def showvalue(self, ax, nowrange, image, fontsize):
        box = []

        # Limited showing value's precision of floating point data
        if image.dtype == np.float32 or image.dtype == np.float64:
            if image.shape[-1] == 1 or len(image.shape) == 2:
                minv = image.min()
                maxv = image.max()
                for y in np.arange(max(nowrange[2] - 3, -0.5), min(nowrange[3] + 3, self.limit[1] - 0.500001),
                                   1):  # Bounding inside the image size

                    row = []

                    for x in np.arange(max(nowrange[0] - 3, -0.5), min(nowrange[1] + 3, self.limit[0] - 0.500001), 1):
                        color = self.wcolor(image[int(y + 0.5), int(x + 0.5)], minv, maxv)
                        temp = ax.text(int(x + 0.5) - 0.35, int(y + 0.5) + 0.1,
                                       "%.2f" % image[int(y + 0.5), int(x + 0.5)],
                                       fontsize=fontsize, color=color)
                        temp.set_clip_on(True)  # show value outside the window but hide it
                        row.append(temp)
                    box.append(row)
                    del row


            elif image.shape[-1] == 3:
                minv = [image[:, :, 0].min(), image[:, :, 1].min(), image[:, :, 2].min()]
                maxv = [image[:, :, 0].max(), image[:, :, 1].max(), image[:, :, 2].max()]

                for y in np.arange(max(nowrange[2] - 3, -0.5), min(nowrange[3] + 3, self.limit[1] - 0.500001), 1):
                    row = []

                    for x in np.arange(max(nowrange[0] - 3, -0.5), min(nowrange[1] + 3, self.limit[0] - 0.500001), 1):
                        c = []
                        for idx, ynow in enumerate([-0.18, 0.12, 0.42]):  # show three values at different y location
                            color = self.wcolor(image[int(y + 0.5), int(x + 0.5)], minv[idx], maxv[idx])
                            temp = ax.text(int(x + 0.5) - 0.35, int(y + 0.5) + ynow,
                                           "%.2f" % image[int(y + 0.5), int(x + 0.5), idx], fontsize=fontsize,
                                           color=color)
                            temp.set_clip_on(True)
                            c.append(temp)

                        row.append(c)

                    box.append(row)
        else:
            if image.shape[-1] == 1 or len(image.shape) == 2:
                minv = image.min()
                maxv = image.max()
                for y in np.arange(max(nowrange[2] - 3, -0.5), min(nowrange[3] + 3, self.limit[1] - 0.500001), 1):

                    row = []

                    for x in np.arange(max(nowrange[0] - 3, -0.5), min(nowrange[1] + 3, self.limit[0] - 0.500001), 1):
                        color = self.wcolor(image[int(y + 0.5), int(x + 0.5)], minv, maxv)
                        temp = ax.text(int(x + 0.5) - 0.35, int(y + 0.5) + 0.1, str(image[int(y + 0.5), int(x + 0.5)]),
                                       fontsize=fontsize, color=color)
                        temp.set_clip_on(True)
                        row.append(temp)
                    box.append(row)
                    del row


            elif image.shape[-1] == 3:
                minv = [image[:, :, 0].min(), image[:, :, 1].min(), image[:, :, 2].min()]
                maxv = [image[:, :, 0].max(), image[:, :, 1].max(), image[:, :, 2].max()]

                for y in np.arange(max(nowrange[2] - 3, -0.5), min(nowrange[3] + 3, self.limit[1] - 0.500001), 1):
                    row = []

                    for x in np.arange(max(nowrange[0] - 3, -0.5), min(nowrange[1] + 3, self.limit[0] - 0.500001), 1):
                        c = []
                        for idx, ynow in enumerate([-0.18, 0.12, 0.42]):
                            color = self.wcolor(image[int(y + 0.5), int(x + 0.5)], minv[idx], maxv[idx])
                            temp = ax.text(int(x + 0.5) - 0.35, int(y + 0.5) + ynow,
                                           str(image[int(y + 0.5), int(x + 0.5), idx]), fontsize=fontsize,
                                           color=color)
                            temp.set_clip_on(True)
                            c.append(temp)

                        row.append(c)

                    box.append(row)
            else:
                raise Exception

        return box

    def modifyshowvalue(self, id, nowrange):
        image = self.image[id]
        # Reset the text object for showing value one by one
        if image.shape[-1] == 1 or len(image.shape) == 2:
            minv = image.min()
            maxv = image.max()
            change = True

            if change:
                # present pixels with value printing on the screen
                row = len(self.box[id])
                col = len(self.box[id][0])

                if image.dtype == np.float32 or image.dtype == np.float64:
                    for i, ys in enumerate(range(row)):
                        y = nowrange[2] + ys
                        if (y < -0.5 or y >= self.limit[1] - 0.500001):  # Bounding inside the image size
                            continue

                        for j, xs in enumerate(range(col)):
                            x = xs + nowrange[0]
                            if (x < -0.5 or x >= self.limit[0] - 0.500001):
                                continue
                            color = self.wcolor(image[int(y + 0.5), int(x + 0.5)], minv, maxv)
                            (self.box[id][i][j]).set_x(int(x + 0.5) - 0.35)
                            (self.box[id][i][j]).set_y(int(y + 0.5) + 0.1)
                            (self.box[id][i][j]).set_text("%.2f" % image[int(y + 0.5), int(x + 0.5)])
                            (self.box[id][i][j]).set_color(color)

                else:

                    for i, ys in enumerate(range(row)):
                        y = nowrange[2] + ys

                        if (y < -0.5 or y >= self.limit[1] - 0.500001):
                            continue
                        for j, xs in enumerate(range(col)):
                            x = xs + nowrange[0]
                            if (x < -0.5 or x >= self.limit[0] - 0.500001):
                                continue

                            color = self.wcolor(image[int(y + 0.5), int(x + 0.5)], minv, maxv)
                            (self.box[id][i][j]).set_x(int(x + 0.5) - 0.35)
                            (self.box[id][i][j]).set_y(int(y + 0.5) + 0.1)
                            (self.box[id][i][j]).set_text(str(image[int(y + 0.5), int(x + 0.5)]))
                            (self.box[id][i][j]).set_color(color)
                            self.axall[id].draw_artist(self.box[id][i][j])

        elif image.shape[-1] == 3:
            minv = [image[:, :, 0].min(), image[:, :, 1].min(), image[:, :, 2].min()]
            maxv = [image[:, :, 0].max(), image[:, :, 1].max(), image[:, :, 2].max()]

            row = len(self.box[id])
            col = len(self.box[id][0])

            if image.dtype == np.float32 or image.dtype == np.float64:
                for i, ys in enumerate(range(row)):
                    y = nowrange[2] + ys
                    if (y < -0.5 or y >= self.limit[1] - 0.500001):  # Bounding inside the image size
                        continue

                    for j, xs in enumerate(range(col)):
                        x = xs + nowrange[0]
                        if (x < -0.5 or x >= self.limit[0] - 0.500001):
                            continue
                        for idx, ynow in enumerate([-0.18, 0.12, 0.42]):
                            color = self.wcolor(image[int(y + 0.5), int(x + 0.5), idx], minv[idx], maxv[idx])
                            (self.box[id][i][j][idx]).set_x(int(x + 0.5) - 0.35)
                            (self.box[id][i][j][idx]).set_y(int(y + 0.5) + ynow)
                            (self.box[id][i][j][idx]).set_text("%.2f" % image[int(y + 0.5), int(x + 0.5), idx])
                            (self.box[id][i][j][idx]).set_color(color)

            else:

                for i, ys in enumerate(range(row)):
                    y = nowrange[2] + ys

                    if (y < -0.5 or y >= self.limit[1] - 0.500001):
                        continue
                    for j, xs in enumerate(range(col)):
                        x = xs + nowrange[0]
                        if (x < -0.5 or x >= self.limit[0] - 0.500001):
                            continue
                        for idx, ynow in enumerate([-0.18, 0.12, 0.42]):
                            color = self.wcolor(image[int(y + 0.5), int(x + 0.5), idx], minv[idx], maxv[idx])
                            (self.box[id][i][j][idx]).set_x(int(x + 0.5) - 0.35)
                            (self.box[id][i][j][idx]).set_y(int(y + 0.5) + ynow)
                            (self.box[id][i][j][idx]).set_text(str(image[int(y + 0.5), int(x + 0.5), idx]))
                            (self.box[id][i][j][idx]).set_color(color)

    def changesize(self, center, range):
        '''

        :param center: [x,y]
        :param range: [xleft,xright,yup,ydown]
        :param limit :[wlimit,hlimit]
        :return:
        '''
        xmin = center[0] - (range[0])
        xmax = center[0] + (range[1])

        # Prevent acquiring the range outside the image's size
        if xmin < 0:
            diff = -xmin
            xmin += diff
            xmax += diff
        if xmax > self.limit[0] - 1:
            diff = self.limit[0] - 1 - xmax
            xmin += diff
            xmax += diff

        ymin = center[1] - (range[2])
        ymax = center[1] + (range[3])

        if ymin < 0:
            diff = -ymin
            ymin += diff
            ymax += diff
        if ymax > self.limit[1] - 1:
            diff = self.limit[1] - 1 - ymax
            ymin += diff
            ymax += diff

        return [xmin, xmax, ymin, ymax]

    def params2(self, xdata, ydata, scroll, last):
        # Calculate the new zooming range
        # return the center and rectangle's xy limit w.r.t center
        w = self.limit[0]
        h = self.limit[1]

        limit = (h if h < w else w) // 2  # left/right/up/down limit

        x = xdata
        y = ydata
        xloc = int(round(x + 0.5))
        yloc = int(round(y + 0.5))

        center = [xloc, yloc]

        range = 2 * limit * (0.5 ** scroll)  # shortest edge's  length after zooming
        # X and Y 's length after zooming
        xrangefull = range * (w / 2) / limit  # if w is shorter than h --> xrangefull = shortest edge
        yrangefull = range * (h / 2) / limit  # if w is shorter than h--> yrangefull>xrangefull
        xleftratio = (xloc - last[0]) / float(last[1] - last[0])
        # center-(old left edge):(old right edge-old left edge)= center-(new leftedge):(new rightedge-new leftedge)
        # (new rightedge-new leftedge)=xrangefull = new zooming width
        xleft = xrangefull * xleftratio  # |-----[---C---]-------------| -> [---C---]:[--- = |-----[--- : |-----[---C---]-------------|
        xright = xrangefull - xleft

        yupratio = (yloc - last[2]) / float(last[3] - last[2])
        yup = yrangefull * yupratio
        ydown = yrangefull - yup
        xyrange = [xleft, xright, yup, ydown]

        return center, xyrange

    def zoom(self, event):
        if not event.inaxes:
            return
        assert self.zoomstate == 'max' or self.zoomstate == 'min' or self.zoomstate == 'zoom'
        x, y = event.xdata, event.ydata

        # Use state machine to control the process, 3 stages: max:original size min:largest zooming size, value will be displayed under this state
        # zoom: state between max and min
        if self.zoomstate == 'max':
            if event.button == 'down':
                # Not zoom out under max state
                return
            elif event.button == 'up':

                if self.help:
                    self.statetext.set_text("Present state: Zooming in, please wait.....")
                    self.statetext.set_color('r')
                    self.stateax.figure.canvas.draw()
                    plt.pause(0.0001)
                self.scroll += 1  # use scroll to count the zooming steps
                self.zoomstate = 'zoom'
                center, xyrange = self.params2(x, y, self.scroll, self.last)
                newsize = self.changesize(center, xyrange)

                for id, ax in enumerate(self.axall):
                    ax.set_xlim([newsize[0], newsize[1]])
                    ax.set_ylim([newsize[3], newsize[2]])

                self.last = copy.copy(newsize)

        elif self.zoomstate == 'min':
            if event.button == 'up':
                # Not zoom in under min state
                return
            elif event.button == 'down':
                if self.help:
                    self.statetext.set_text("Present state: Zooming out, please wait.....")
                    self.statetext.set_color('r')
                    self.stateax.figure.canvas.draw()
                    plt.pause(0.0002)
                if self.box:
                    # zoom out from min state --> clear the showing pixel value
                    for box in self.box:
                        if isinstance(box[0][0], list):
                            for roltext in box:
                                for coltext in roltext:
                                    for c in coltext:
                                        c.remove()
                        else:
                            for roltext in box:
                                for coltext in roltext:
                                    coltext.remove()
                    del self.box

                    for ax in self.axall:
                        ax.set_xticks([], minor=True)
                        ax.set_yticks([], minor=True)
                        ax.grid(b=None, which='minor')

                self.scroll -= 1
                self.zoomstate = 'zoom'
                center, xyrange = self.params2(x, y, self.scroll, self.last)
                newsize = self.changesize(center, xyrange)

                self.last = copy.copy(newsize)
                for ax in self.axall:
                    ax.set_xlim([newsize[0], newsize[1]])
                    ax.set_ylim([newsize[3], newsize[2]])


        elif self.zoomstate == 'zoom':
            if event.button == 'up':  # zoom in
                self.scroll += 1
                if self.help:
                    self.statetext.set_text("Present state: Zooming in, please wait.....")
                    self.statetext.set_color('r')
                    self.stateax.figure.canvas.draw()
                    plt.pause(0.0001)
            elif event.button == 'down':  # zoom out
                if self.help:
                    self.statetext.set_text("Present state: Zooming out, please wait.....")
                    self.statetext.set_color('r')
                    self.stateax.figure.canvas.draw()
                    plt.pause(0.0001)
                self.scroll -= 1
            center, xyrange = self.params2(x, y, self.scroll, self.last)
            newsize = self.changesize(center, xyrange)

            if self.scroll == 0:
                self.zoomstate = 'max'

            elif xyrange[1] + xyrange[0] < 12 or xyrange[2] + xyrange[
                3] < 12:  # Hard control for the largest zooming range
                # (condition to get in min state and pixel showing mode)

                self.zoomstate = 'min'
                self.box = []
                if self.help:
                    self.statetext.set_text("Present state: Showing value, please wait.....")
                    self.statetext.set_color('r')
                    self.stateax.figure.canvas.draw()
                    plt.pause(0.0001)
                for ax, im, fz in zip(self.axall, self.image, self.fontsize):
                    ax.set_xticks(np.arange(int(round(newsize[0] - 2)) + 0.5, int(round(newsize[1] + 2)) + 0.5, 1),
                                  minor=True)
                    ax.set_yticks(np.arange(int(round(newsize[2] - 2)) + 0.5, int(round(newsize[3] + 2)) + 0.5, 1),
                                  minor=True)
                    ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

                    self.box.append(self.showvalue(ax, newsize, im, fz))

            for ax in self.axall:
                ax.set_xlim([newsize[0], newsize[1]])
                ax.set_ylim([newsize[3], newsize[2]])
            self.last = copy.copy(newsize)

        if self.help:
            self.statetext.set_text("Present state: Zoom-in state " + str(self.scroll) + "/" + str(self.scrolllimit))
            self.statetext.set_color('b')
            self.stateax.figure.canvas.draw()

        for id, (ax, lx, ly) in enumerate(zip(self.axall, self.lxall, self.lyall)):
            # need to close the cursor before buffering the displaying image
            lx.set_visible(False)
            ly.set_visible(False)

            ax.figure.canvas.draw()
            # Buffer the displaying image
            self.backgroundcache[id] = ax.figure.canvas.copy_from_bbox(ax.bbox)
            lx.set_visible(True)
            ly.set_visible(True)

            ax.draw_artist(lx)
            ax.draw_artist(ly)

            ax.figure.canvas.draw()

    def dragstart(self, event):
        # 'Draging event'
        assert self.dragstate == 'move' or self.dragstate == 'stop'
        if not event.inaxes:
            return
        if event.button == 1:
            if self.zoomstate == 'max':
                return
            # Draging state machine: move: Moving displaying area stop:Stop moving
            self.dragstate = 'move'
            x, y = event.xdata, event.ydata
            xloc = int(round(x + 0.5))
            yloc = int(round(y + 0.5))
            self.mouseloc = [xloc, yloc]

    def release(self, event):
        # 'button_release_event'

        if event.button == 1:
            assert self.dragstate == 'move' or self.dragstate == 'stop'
            self.dragstate = 'stop'

        if event.button == 2:
            self.wait = False

    def drag(self, event):
        # 'motion_notify_event'

        # Cursor moving event
        if (not event.inaxes) or self.cursor_lock:
            pass

        elif self.dragstate != 'move':
            x, y = event.xdata, event.ydata
            #
            for lx, ly, ax, background in zip(self.lxall, self.lyall, self.axall, self.backgroundcache):
                ax.figure.canvas.restore_region(background)

                lx.set_ydata(y)
                ly.set_xdata(x)

        # Dragging event

        for lx, ly, ax, background in zip(self.lxall, self.lyall, self.axall, self.backgroundcache):
            ax.draw_artist(lx)
            ax.draw_artist(ly)
            ax.figure.canvas.blit(ax.bbox)
        if not event.inaxes or self.dragstate != 'move':
            return

        x, y = event.xdata, event.ydata
        xloc = x
        yloc = y

        xdelta = -(xloc - self.mouseloc[0])
        ydelta = -(yloc - self.mouseloc[1])
        self.mouseloc = [xloc, yloc]

        newxleft = self.last[0] + xdelta

        newxright = self.last[1] + xdelta

        # Bounding conditions
        if newxright > self.limit[0] - 0.5:
            over = newxright - (self.limit[0] - 0.5)
            newxright = self.limit[0] - 0.5
            newxleft -= over

        if newxleft < -0.5:
            over = -0.5 - newxleft
            newxleft = -0.5
            newxright += over

        newyup = self.last[2] + ydelta

        newydown = self.last[3] + ydelta
        if newydown > self.limit[1] - 0.5:
            over = newydown - (self.limit[1] - 0.5)
            newydown = self.limit[1] - 0.5
            newyup -= over

        if newyup < -0.5:
            over = -0.5 - newyup
            newyup = -0.5
            newydown += over
        newposition = [newxleft, newxright, newyup, newydown]

        if self.zoomstate == 'min':
            for ax in self.axall:
                ax.set_xticks(np.arange(int(round(newposition[0] - 2)) + 0.5, int(round(newposition[1] + 2)) + 0.5, 1),
                              minor=True)
                ax.set_yticks(np.arange(int(round(newposition[2] - 2)) + 0.5, int(round(newposition[3] + 2)) + 0.5, 1),
                              minor=True)
                ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

            for idx, (ax, im) in enumerate(zip(self.axall, self.image)):
                self.modifyshowvalue(idx, newposition)

        for id, (ax, lx, ly) in enumerate(zip(self.axall, self.lxall, self.lyall)):
            ax.set_xlim([newxleft, newxright])

            ax.set_ylim([newydown, newyup])

        for id, (ax, lx, ly) in enumerate(zip(self.axall, self.lxall, self.lyall)):
            lx.set_visible(False)
            ly.set_visible(False)

            # Redraw everything after draging the image
            ax.figure.canvas.draw()

            self.backgroundcache[id] = ax.figure.canvas.copy_from_bbox(ax.bbox)
            lx.set_visible(True)
            ly.set_visible(True)
            ax.draw_artist(lx)
            ax.draw_artist(ly)

            ax.figure.canvas.blit()

        self.last = [newxleft, newxright, newyup, newydown]
        self.mouseloc = [xloc + xdelta, yloc + ydelta]

    def mouse_move(self, event):

        if (not event.inaxes) or self.cursor_lock:
            return

        x, y = event.xdata, event.ydata

        for lx, ly, ax, background in zip(self.lxall, self.lyall, self.axall, self.backgroundcache):
            # Restore the clean image without cursor, then draw a new cursor
            ax.figure.canvas.restore_region(background)

            lx.set_ydata(y)
            ly.set_xdata(x)
            ax.draw_artist(lx)
            ax.draw_artist(ly)

            ax.figure.canvas.blit(ax.bbox)

    def press(self, event):

        if not event.inaxes:
            return

        if event.button == 2:
            starttime = time.time()
            self.wait = True
            state = -1
            while (True):
                endtime = time.time()
                if (endtime - starttime > 0.7):
                    state = 0
                    break
                if (self.wait is False):
                    if (endtime - starttime > 0.7):
                        state = 0
                        break
                    else:
                        state = 1
                        break

                plt.pause(0.001)

            if state == 0:  # Original size
                if self.zoomstate == 'max': return

                if self.zoomstate == 'min':
                    # zoom out from min state --> clear the showing pixel value
                    for box in self.box:
                        if isinstance(box[0][0], list):
                            for roltext in box:
                                for coltext in roltext:
                                    for c in coltext:
                                        c.remove()
                        else:
                            for roltext in box:
                                for coltext in roltext:
                                    coltext.remove()
                    del self.box

                    for ax in self.axall:
                        ax.set_xticks([], minor=True)
                        ax.set_yticks([], minor=True)
                        ax.grid(b=None, which='minor')
                self.scroll = 0
                self.zoomstate = 'max'
                self.last = [0, self.limit[0] - 1, 0, self.limit[1] - 1]
                for ax in self.axall:
                    ax.set_xlim([self.last[0], self.last[1]])
                    ax.set_ylim([self.last[3], self.last[2]])
                for id, (ax, lx, ly) in enumerate(zip(self.axall, self.lxall, self.lyall)):
                    # need to close the cursor before buffering the displaying image
                    lx.set_visible(False)
                    ly.set_visible(False)

                    ax.figure.canvas.draw()
                    # Buffer the displaying image
                    self.backgroundcache[id] = ax.figure.canvas.copy_from_bbox(ax.bbox)
                    lx.set_visible(True)
                    ly.set_visible(True)

                    ax.draw_artist(lx)
                    ax.draw_artist(ly)

                    ax.figure.canvas.draw()
                if self.help:
                    self.statetext.set_text(
                        "Present state: Zoom-in state " + str(self.scroll) + "/" + str(self.scrolllimit))

                    self.statetext.set_color('b')
                    self.stateax.figure.canvas.draw()

            elif state == 1:  # Showing value
                if self.zoomstate == 'min': return
                if self.help:
                    self.statetext.set_text("Present state: Showing value, please wait.....")
                    self.statetext.set_color('r')
                    self.stateax.figure.canvas.draw()
                    plt.pause(0.0001)

                x, y = event.xdata, event.ydata
                center, xyrange = self.params2(x, y, self.scrolllimit, self.last)
                newsize = self.changesize(center, xyrange)
                self.scroll = copy.copy(self.scrolllimit)
                self.zoomstate = 'min'
                self.box = []

                for ax, im, fz in zip(self.axall, self.image, self.fontsize):
                    ax.set_xticks(np.arange(int(round(newsize[0] - 2)) + 0.5, int(round(newsize[1] + 2)) + 0.5, 1),
                                  minor=True)
                    ax.set_yticks(np.arange(int(round(newsize[2] - 2)) + 0.5, int(round(newsize[3] + 2)) + 0.5, 1),
                                  minor=True)
                    ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

                    self.box.append(self.showvalue(ax, newsize, im, fz))

                for ax in self.axall:
                    ax.set_xlim([newsize[0], newsize[1]])
                    ax.set_ylim([newsize[3], newsize[2]])
                self.last = copy.copy(newsize)

                for id, (ax, lx, ly) in enumerate(zip(self.axall, self.lxall, self.lyall)):
                    # need to close the cursor before buffering the displaying image
                    lx.set_visible(False)
                    ly.set_visible(False)

                    ax.figure.canvas.draw()
                    # Buffer the displaying image
                    self.backgroundcache[id] = ax.figure.canvas.copy_from_bbox(ax.bbox)
                    lx.set_visible(True)
                    ly.set_visible(True)

                    ax.draw_artist(lx)
                    ax.draw_artist(ly)

                    ax.figure.canvas.draw()

                if self.help:
                    self.statetext.set_text(
                        "Present state: Zoom-in state " + str(self.scroll) + "/" + str(self.scrolllimit))
                    self.statetext.set_color('b')
                    self.stateax.figure.canvas.draw()

        if event.button == 3:
            nowpic = [i for i, ax in enumerate(self.axall) if ax == event.inaxes]

            self.diff.append([self.image[nowpic[0]], nowpic[0]])
            if len(self.diff) == 2:
                if self.diff[0][0].shape != self.diff[1][0].shape:
                    print("Image shape not match, please select another image")
                    self.diff.pop()

                else:
                    # "imshow" function only support uint or float, to compromise negative number, we use floating point
                    comp = self.diff[0][0].astype(np.float32) - self.diff[1][0].astype(np.float32)
                    fig, ax = plt.subplots()

                    plt.draw()
                    plt.pause(0.1)
                    if comp.shape[-1] == 3:
                        ax.imshow(comp)
                    else:
                        ax.imshow(comp, cmap='gray')

                    name1 = (self.axall[self.diff[0][1]]).title._text
                    name2 = (self.axall[self.diff[1][1]]).title._text
                    ax.title.set_text(name1 + '-' + name2)
                    self.axall.append(ax)

                    self.diff.clear()

                    self.figall.append(fig)

                    self.image.append(comp)
                    self.shape.append(comp.shape)

                    self.figsize.append([fig.get_figheight(), fig.get_figwidth()])
                    fontsize = 8 if comp.dtype == np.float32 or comp.dtype == np.float64 else 10
                    self.fontsizeoriginal.append(fontsize)
                    fontsize = fontsize * fig.get_figwidth() / 7.0
                    self.fontsize.append(fontsize)

                    if self.zoomstate == 'min':

                        if self.help:
                            self.statetext.set_text("Present state: Showing value, please wait.....")
                            self.statetext.set_color('r')
                            self.stateax.figure.canvas.draw()
                            plt.pause(0.0001)
                        ax.set_xticks(
                            np.arange(int(round(self.last[0] - 2)) + 0.5, int(round(self.last[1] + 2)) + 0.5, 1),
                            minor=True)
                        ax.set_yticks(
                            np.arange(int(round(self.last[2] - 2)) + 0.5, int(round(self.last[3] + 2)) + 0.5, 1),
                            minor=True)
                        ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

                        self.box.append(self.showvalue(ax, self.last, comp, fontsize))
                    ax.set_xlim([self.last[0], self.last[1]])
                    ax.set_ylim([self.last[3], self.last[2]])
                    ax.figure.canvas.draw()
                    self.backgroundcache.append(ax.figure.canvas.copy_from_bbox(ax.bbox))
                    self.lxall.append(ax.axhline(color='r', alpha=0.5))  # the horiz line
                    self.lyall.append(ax.axvline(color='r', alpha=0.5))  # the vert line
                    ax.draw_artist(self.lxall[-1])
                    ax.draw_artist(self.lyall[-1])

                    ax.figure.canvas.draw()

                    fig.canvas.mpl_connect('close_event', self.close)
                    fig.canvas.mpl_connect('scroll_event', self.zoom)
                    fig.canvas.mpl_connect('button_press_event', self.dragstart)
                    fig.canvas.mpl_connect('button_release_event', self.release)
                    fig.canvas.mpl_connect('motion_notify_event', self.drag)
                    fig.canvas.mpl_connect('button_press_event', self.press)
                    fig.canvas.mpl_connect('resize_event', self.Resizefordiff)
                    fig = None
                    ax = None
                    comp = None
                    gc.collect()
                    if self.help:

                        self.statetext.set_text(
                            "Present state: Zoom-in state " + str(self.scroll) + "/" + str(self.scrolllimit))
                        self.statetext.set_color('b')
                        self.statetext2.set_text("")
                        self.stateax.figure.canvas.draw()

            else:
                if self.help:
                    self.statetext2.set_text("Select another image for comparison")
                    self.statetext2.set_color('r')
                    self.stateax.figure.canvas.draw()
        if event.button == 1 and event.dblclick:
            self.cursor_lock = not self.cursor_lock
            self.mouse_move(event)  # Move cursor when releasing lock

    def close(self, event):
        findfig = [ss for ss, f in enumerate(self.figall) if f == event.canvas.figure]
        id = findfig[0]

        totalnum = len(self.figall)

        self.axall[id].clear()

        self.figall[id].clear()
        plt.close(self.figall[id])
        del self.axall[id]
        del self.figall[id]
        del self.backgroundcache[id]
        del self.figsize[id]
        del self.fontsize[id]
        del self.fontsizeoriginal[id]
        del self.image[id]
        del self.lxall[id]
        del self.lyall[id]
        del self.shape[id]

        if (len(self.box)) == totalnum:
            del self.box[id]
            assert len(self.box) == totalnum - 1

        assert len(self.axall) == totalnum - 1
        assert len(self.figall) == totalnum - 1
        assert len(self.backgroundcache) == totalnum - 1
        assert len(self.figsize) == totalnum - 1
        assert len(self.fontsize) == totalnum - 1
        assert len(self.fontsizeoriginal) == totalnum - 1
        assert len(self.image) == totalnum - 1
        assert len(self.lxall) == totalnum - 1
        assert len(self.lyall) == totalnum - 1
        assert len(self.shape) == totalnum - 1
        gc.collect()

    def Resizefordiff(self, event):
        if self.help:
            self.statetext.set_text("Present state: Resizing, please wait...")
            self.statetext.set_color('r')
            self.stateax.figure.canvas.draw()
            plt.pause(0.001)

        findfig = [ss for ss, f in enumerate(self.figall) if f == event.canvas.figure]

        newheight = self.figall[findfig[0]].get_figheight()
        newwid = self.figall[findfig[0]].get_figwidth()
        ratio = newwid / (8.0)

        self.figsize[findfig[0]] = [newheight, newwid]

        self.fontsize[findfig[0]] = self.fontsizeoriginal[findfig[0]] * ratio

        if self.zoomstate == 'min':  # Resize font size showing on the pics
            for id, box in enumerate(self.box):
                if id != findfig[0]: continue
                if isinstance(box[0][0], list):
                    for roltext in box:
                        for coltext in roltext:
                            for c in coltext:
                                c.set_fontsize(self.fontsize[findfig[0]])
                else:
                    for roltext in box:
                        for coltext in roltext:
                            coltext.set_fontsize(self.fontsize[findfig[0]])
                break

        for id, (ax, im, lx, ly) in enumerate(zip(self.axall, self.image, self.lxall, self.lyall)):
            if id != findfig[0]: continue

            lx.set_visible(False)
            ly.set_visible(False)

            ax.figure.canvas.draw()
            self.backgroundcache[id] = ax.figure.canvas.copy_from_bbox(ax.bbox)
            lx.set_visible(True)
            ly.set_visible(True)
            ax.draw_artist(lx)
            ax.draw_artist(ly)

            break

        if self.help:
            self.statetext.set_text(
                "Present state: Zoom-in state " + str(self.scroll) + "/" + str(self.scrolllimit))
            self.statetext.set_color('b')
            self.stateax.figure.canvas.draw()

    def Resize(self, event):
        if self.help:
            self.statetext.set_text("Present state: Resizing, please wait...")
            self.statetext.set_color('r')
            self.stateax.figure.canvas.draw()
            plt.pause(0.001)

        if self.mode == 0:
            findfig = [ss for ss, f in enumerate(self.figall) if f == event.canvas.figure]

            newheight = self.figall[findfig[0]].get_figheight()
            newwid = self.figall[findfig[0]].get_figwidth()
            ratio = newwid / (8.0)

            self.figsize[findfig[0]] = [newheight, newwid]

            self.fontsize[findfig[0]] = self.fontsizeoriginal[findfig[0]] * ratio

            if self.zoomstate == 'min':  # Resize font size showing on the pics
                for id, box in enumerate(self.box):
                    if id != findfig[0]: continue
                    if isinstance(box[0][0], list):
                        for roltext in box:
                            for coltext in roltext:
                                for c in coltext:
                                    c.set_fontsize(self.fontsize[findfig[0]])
                    else:
                        for roltext in box:
                            for coltext in roltext:
                                coltext.set_fontsize(self.fontsize[findfig[0]])
                    break

            for id, (ax, im, lx, ly) in enumerate(zip(self.axall, self.image, self.lxall, self.lyall)):
                if id != findfig[0]: continue

                lx.set_visible(False)
                ly.set_visible(False)

                ax.figure.canvas.draw()
                self.backgroundcache[id] = ax.figure.canvas.copy_from_bbox(ax.bbox)
                lx.set_visible(True)
                ly.set_visible(True)
                ax.draw_artist(lx)
                ax.draw_artist(ly)

                break
        else:

            newheight = self.figall[0].get_figheight()
            newwid = self.figall[0].get_figwidth()
            ratio = newwid / 7.0
            for s in range(self.picnum):
                self.figsize[s] = [newheight, newwid]

                self.fontsize[s] = self.fontsizeoriginal[s] * ratio

            if self.zoomstate == 'min':  # Resize font size showing on the pics
                for id, box in enumerate(self.box):
                    if id >= self.picnum: continue
                    if isinstance(box[0][0], list):
                        for roltext in box:
                            for coltext in roltext:
                                for c in coltext:
                                    c.set_fontsize(self.fontsize[id])
                    else:
                        for roltext in box:
                            for coltext in roltext:
                                coltext.set_fontsize(self.fontsize[id])

            for id, (ax, im, lx, ly) in enumerate(zip(self.axall, self.image, self.lxall, self.lyall)):
                # if id != findfig[0]: continue
                if id >= self.picnum: break
                lx.set_visible(False)
                ly.set_visible(False)

                ax.figure.canvas.draw()
                self.backgroundcache[id] = ax.figure.canvas.copy_from_bbox(ax.bbox)
                lx.set_visible(True)
                ly.set_visible(True)
                ax.draw_artist(lx)
                ax.draw_artist(ly)

        if self.help:

            self.statetext.set_text("Present state: Zoom-in state " + str(self.scroll) + "/" + str(self.scrolllimit))
            self.statetext.set_color('b')
            self.stateax.figure.canvas.draw()

    def __call__(self, images, name=None, contrastminmax=None, mode=0, showhelp=True, colormapping=None):
        self.help = showhelp
        self.defcolormapping(colormapping)
        if showhelp:
            mainfig, mainax = plt.subplots()
            mainax.axis("off")

            mainfig.gca().invert_yaxis()
            mainax.text(0.05, 0.1, "*Single click and hold the left button to drag the image", fontsize=12)
            mainax.text(0.05, 0.2, "*Double press left button: Cursor Lock/Unlock", fontsize=12)
            mainax.text(0.05, 0.3, "*Press right button: Image difference mode (select two images)", fontsize=12)
            mainax.text(0.05, 0.4, "*Scroll the mouse wheel to zoom in/out", fontsize=12)
            mainax.text(0.05, 0.5, "*Single click the mouse wheel to show pixel value", fontsize=12)
            mainax.text(0.05, 0.55, " (might take a few seconds)", fontsize=12)
            mainax.text(0.05, 0.65, "*Single click and hold the mouse wheel to back", fontsize=12)
            mainax.text(0.05, 0.7, " to original size", fontsize=12)

            mainax.text(0.05, 0.8, "--------------------------------------------------------------")
            mainax.text(0.05, 0.95, "--------------------------------------------------------------")

            self.statetext2 = mainax.text(0.05, 0.925, "", fontsize=10, color='b')
            self.stateax = mainax

        if len(images) == 1:
            mode = 0
        self.mode = mode
        if name is None:
            name = ['fig_' + str(i) for i in range(len(images))]

        if len(name) < len(images):
            for i in range(len(images)):
                if i >= len(name):
                    name.append('fig_' + str(i))

        if contrastminmax is None:
            contrastminmax = [None for k in range(len(images))]

        if len(contrastminmax) < len(images):

            for i in range(len(images)):
                if i >= len(contrastminmax):
                    contrastminmax.append(None)

        self.picnum = len(images)
        self.backgroundcache = []

        self.figall = []
        self.axall = []
        self.image = []
        self.shape = []
        self.lxall = []
        self.lyall = []
        self.figsize = []
        self.fontsize = []
        self.fontsizeoriginal = []
        if mode == 1:
            h = int((len(images)) ** 0.5)
            w = int(np.ceil(len(images) / h))
            fig, axall = plt.subplots(h, w)
            self.axgrid = [h, w]

        for idx, im in enumerate(images):
            if mode == 0:
                fig, ax = plt.subplots()


            elif mode == 1:
                if h == 1:
                    ax = axall[idx]
                else:
                    ax = axall[idx // w][idx - w * (idx // w)]
            else:
                raise Exception
            self.figall.append(fig)
            ax.title.set_text(name[idx])
            self.axall.append(ax)
            self.image.append(im)
            self.shape.append(im.shape)

            if im.shape[-1] == 3:
                if contrastminmax[idx] is None:
                    ax.imshow(im)
                else:
                    print("***** Showing Image id:{}  'Min/Max bounding  is not supported for color image'".format(idx))
                    ax.imshow(im)
            else:
                if contrastminmax[idx] is None:
                    ax.imshow(im, cmap='gray')
                else:
                    ax.imshow(im, cmap='gray', vmin=contrastminmax[idx][0], vmax=contrastminmax[idx][1])
            fig.canvas.draw()
            self.backgroundcache.append(ax.figure.canvas.copy_from_bbox(ax.bbox))
            self.figsize.append([fig.get_figheight(), fig.get_figwidth()])
            fontsize = 8 if im.dtype == np.float32 or im.dtype == np.float64 else 10
            if mode == 0:
                self.fontsizeoriginal.append(fontsize)
            fontsize = fontsize * fig.get_figwidth() / 7.0

            if mode == 1:
                fontsize /= self.axgrid[1]
                self.fontsizeoriginal.append(fontsize)

            self.fontsize.append(fontsize)
            self.lxall.append(ax.axhline(color='r', alpha=0.5))  # the horiz line
            self.lyall.append(ax.axvline(color='r', alpha=0.5))  # the vert line

        self.dragprocessing = False
        h = self.shape[0][0]
        w = self.shape[0][1]

        limit = min(h, w)
        c = 0
        while (True):
            limit /= 2
            c += 1

            if limit < 12:
                break
        self.scrolllimit = copy.copy(c)
        self.wait = False
        self.limit = [w, h]
        self.scroll = 0
        self.cursor_lock = False
        self.cursorxy = [0, 0]
        self.diff = []
        self.extraax = []
        self.zoomstate = 'max'
        self.last = [0, w - 1, 0, h - 1]
        self.dragstate = 'stop'
        self.forcezoom = False
        if self.help:
            self.statetext = mainax.text(0.05, 0.875, "Present state: Zoom-in state " + str(self.scroll) + "/" + str(
                self.scrolllimit), fontsize=16, color='b')

        for fig in self.figall:
            fig.canvas.mpl_connect('scroll_event', self.zoom)
            fig.canvas.mpl_connect('button_press_event', self.dragstart)
            fig.canvas.mpl_connect('button_release_event', self.release)
            fig.canvas.mpl_connect('motion_notify_event', self.drag)
            fig.canvas.mpl_connect('button_press_event', self.press)
            fig.canvas.mpl_connect('resize_event', self.Resize)

        plt.show()


def func(images, name, contrastminmax, mode, showhelp, colormapping):
    newobj = comparer()
    newobj(images, name, contrastminmax, mode, showhelp, colormapping)


def compare(images, name=None, contrastminmax=None, mode=0, showhelp=True, colormapping=None):
    process = multiprocessing.Process(target=func, args=(images, name, contrastminmax, mode, showhelp, colormapping))
    process.start()

