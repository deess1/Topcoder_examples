# Alarmed
# https://arena.topcoder.com/#/u/practiceCode/1798/6714/7479/1/1798

# 1)
#{1,99}
#{50,50}
#{1,1}
#Returns: 2400.9999999999995

# 2)
#{3,11,2,62,91}
#{90,10,75,25,50}
#{5,4,3,2,1}
#Returns: 1537.9999999999998

#3)
#{ 1,99}
#{ 50,50}
#{ 1, 2}
#Returns: 3295.5717878751793

import math

class Alarmed:
    alarms = None
    deltaE = 1.0E-14
    corners = ({'x': 50,  'y':   0},
               {'x':  0,  'y':   0},
               {'x':  0,  'y': 100},
               {'x': 50,  'y': 100},
               {'x': 100, 'y': 100},
               {'x': 100, 'y':   0},
               {'x': 50,  'y':   0}                                                        
               )

    # minimal value of noise for specified point
    def min_noise_pt(self, x, y):
        minA = None
        for a in self.alarms:
            A = a['t']*((x-a['x'])**2 + (y-a['y'])**2)
            if A<minA or not minA:
                minA = A
        return minA

    # find cross point from current point on wall-line to nearest alarm circle
    def line_to_circle(self, pos, N):
        if self.corners[pos.iWall]['x']==self.corners[pos.iWall+1]['x']:
            x = self.corners[pos.iWall]['x']
            y = -1
            y1 = min(pos.y, self.corners[pos.iWall+1]['y'])
            y2 = max(pos.y, self.corners[pos.iWall+1]['y'])
            if pos.y>self.corners[pos.iWall+1]['y']:
                dy = -1
            else:
                dy = 1
            start = pos.y
        elif self.corners[pos.iWall]['y']==self.corners[pos.iWall+1]['y']:
            x = -1
            y = self.corners[pos.iWall]['y']
            x1 = min(pos.x, self.corners[pos.iWall+1]['x'])
            x2 = max(pos.x, self.corners[pos.iWall+1]['x'])            
            if pos.x>self.corners[pos.iWall+1]['x']:
                dx = -1
            else:
                dx = 1
            start = pos.x
            print 'x1=%f, x2=%f, dx=%f, start=%f' % (x1,x2,dx,start)

        circle = None
        for a in self.alarms:

            if x==-1 and N/a['t']>(y-a['y'])**2:
                c = -dx*(N/a['t'] - (y-a['y'])**2)**0.5 + a['x']
                if c>=x1 and c<=x2:
                    if (c>start and dx>0) or (c<start and dx<0):
                        start = c
                        circle = a
            elif y==-1 and N/a['t']>(x-a['x'])**2:
                c = -dy*(N/a['t'] - (x-a['x'])**2)**0.5 + a['y']
                if c>=y1 and c<=y2:
                    if (c>start and dy>0) or (c<start and dy<0):
                        start = c
                        circle = a
                
        if circle:
            pos.fig = 'a'
            pos.alarm = circle
            if x==-1:
                pos.x = start
                pos.y = y
            elif y==-1:
                pos.x = x
                pos.y = start

            print 'line %d->circle: %.10f,%.10f' % (pos.iWall, pos.x,pos.y)
            return True

    def get_angle(self, x, y, x0, y0, r):
        k = math.atan2(y-y0,x-x0)
        if k<0:
            k = 2*math.pi + k
        return k

    # clockwise angle between a0 -> a1
    def angle_diff(self, a0, a1):
        if a1-a0<0:
            return 2*math.pi+(a1-a0)
        else:
            return a1-a0
    
    # clockwise direction: find crossing point to the nearest circle or line
    def circle_to_circle_line(self, pos, N):
        r1 = (N/pos.alarm['t'])**0.5
        # start angle for entry point on circle
        a0 = self.get_angle(pos.x, pos.y, pos.alarm['x'], pos.alarm['y'], r1)
        
        amin = 10
        circle = None
        # the first check circle
        for a in self.alarms:
            if pos.alarm==a: continue
            # skip if sum of radiuses higher than distance between centers
            r2 = (N/a['t'])**0.5
            center_dist = ((a['x']-pos.alarm['x'])**2+(a['y']-pos.alarm['y'])**2)**0.5
            # skip if circle inside other and no intersection
            if center_dist + min(r1,r2)<=max(r1,r2): continue
            if center_dist > r1+r2: continue
            k = (r1**2-r2**2 + center_dist**2)/(2*center_dist)
            h = (r1**2-k**2)**0.5
            x0 = pos.alarm['x'] + k*(a['x']-pos.alarm['x'])/center_dist
            y0 = pos.alarm['y'] + k*(a['y']-pos.alarm['y'])/center_dist
            # first point of intersection and corresponded angle
            x1 = x0 + h*(a['y']-pos.alarm['y']) / center_dist;
            y1 = y0 - h*(a['x']-pos.alarm['x']) / center_dist;
            a1 = self.get_angle(x1, y1, pos.alarm['x'], pos.alarm['y'], r1)
            # second point of intersection and corresponded angle
            x2 = x0 - h*(a['y']-pos.alarm['y']) / center_dist;
            y2 = y0 + h*(a['x']-pos.alarm['x']) / center_dist;
            a2 = self.get_angle(x2, y2, pos.alarm['x'], pos.alarm['y'], r1)
            if self.angle_diff(a0, a1)<self.angle_diff(a0, a2) and abs(a0-a1)>self.deltaE and self.angle_diff(a0, a1)<amin:
                amin = self.angle_diff(a0, a1)
                xmin = x1
                ymin = y1
                circle = a
            elif self.angle_diff(a0, a2)<self.angle_diff(a0, a1) and abs(a0-a2)>self.deltaE and self.angle_diff(a0, a2)<amin:
                amin = self.angle_diff(a0, a2)
                xmin = x2
                ymin = y2
                circle = a

        if circle:
            print 'circle found. amin=%f, x=%f, y=%f' % (amin,xmin,ymin)
            
        # the second check line (borders)
        iWall = None
        for i in range(0,6):
            a1 = None
            a2 = None
            
            if self.corners[i]['y']==self.corners[i+1]['y'] and r1>abs(self.corners[i]['y']-pos.alarm['y']):
                x1 = pos.alarm['x'] + (r1**2-(self.corners[i]['y']-pos.alarm['y'])**2)**0.5
                x2 = pos.alarm['x'] - (r1**2-(self.corners[i]['y']-pos.alarm['y'])**2)**0.5                      
                y1 = self.corners[i]['y']
                y2 = self.corners[i]['y']
                if x1>=min(self.corners[i]['x'],self.corners[i+1]['x']) and x1<max(self.corners[i]['x'],self.corners[i+1]['x']):
                    a1 = self.get_angle(x1, y1, pos.alarm['x'], pos.alarm['y'], r1)
                if x2>=min(self.corners[i]['x'],self.corners[i+1]['x']) and x2<max(self.corners[i]['x'],self.corners[i+1]['x']):
                    a2 = self.get_angle(x2, y2, pos.alarm['x'], pos.alarm['y'], r1)

            if self.corners[i]['x']==self.corners[i+1]['x'] and r1>abs(self.corners[i]['x']-pos.alarm['x']):
                x1 = self.corners[i]['x']
                x2 = self.corners[i]['x']
                y1 = pos.alarm['y'] + (r1**2-(self.corners[i]['x']-pos.alarm['x'])**2)**0.5
                y2 = pos.alarm['y'] - (r1**2-(self.corners[i]['x']-pos.alarm['x'])**2)**0.5
                if y1>=min(self.corners[i]['y'],self.corners[i+1]['y']) and y1<max(self.corners[i]['y'],self.corners[i+1]['y']):
                    a1 = self.get_angle(x1, y1, pos.alarm['x'], pos.alarm['y'], r1)
                if y2>=min(self.corners[i]['y'],self.corners[i+1]['y']) and y2<max(self.corners[i]['y'],self.corners[i+1]['y']):
                    a2 = self.get_angle(x2, y2, pos.alarm['x'], pos.alarm['y'], r1)         
                    
            if a1 and abs(a0-a1)<self.deltaE: a1 = None
            if a2 and abs(a0-a2)<self.deltaE: a2 = None
            
            if a1 and a2 and self.angle_diff(a0, a1)<self.angle_diff(a0, a2) and self.angle_diff(a0, a1)<amin:
                amin = self.angle_diff(a0, a1)
                xmin = x1
                ymin = y1
                iWall = i
                print '1. xmin=%f, ymin=%f, amin=%f, wall=%d' % (xmin, ymin, amin, iWall)
            elif a1 and a2 and self.angle_diff(a0, a2)<self.angle_diff(a0, a1) and self.angle_diff(a0, a2)<amin:
                print '%f' % self.angle_diff(a0, a1)    
                amin = self.angle_diff(a0, a2)
                xmin = x2
                ymin = y2
                iWall = i
                print '2. xmin=%f, ymin=%f, amin=%f, wall=%d' % (xmin, ymin, amin, iWall)                
            elif a1 and a2==None and self.angle_diff(a0, a1)<amin:
                amin = self.angle_diff(a0, a1)
                xmin = x1
                ymin = y1
                iWall = i
                print '3. xmin=%f, ymin=%f, amin=%f, wall=%d' % (xmin, ymin, amin, iWall)         
            elif a2 and a1==None and self.angle_diff(a0, a2)<amin:                
                amin = self.angle_diff(a0, a2)
                xmin = x2
                ymin = y2
                iWall = i
                print '4. xmin=%f, ymin=%f, wall=%d' % (xmin, ymin, iWall)     


        if iWall:
            if iWall>2:
                return False
            pos.fig = 'w'
            pos.iWall = iWall
            pos.x = xmin
            pos.y = ymin
            print 'circle->line %d: a=%f;  x=%.10f, y=%.10f' % (iWall, amin, pos.x,pos.y)
            return True
        
        if circle and abs(pos.x-xmin)>self.deltaE and abs(pos.y-ymin)>self.deltaE:
            pos.fig = 'a'
            pos.alarm = circle
            pos.x = xmin
            pos.y = ymin
            print 'circle->circle: angle=%f; x=%.10f,y=%.10f' % (amin, pos.x,pos.y)
            return True
        
    
    def find_next(self, pos, N):
        if pos.fig=='w':
            if self.line_to_circle(pos, N):
                return True
            else:
                # pass corner or exit
                pos.iWall += 1
                if pos.iWall>=len(self.corners): pos.iWall = 0
                pos.x = self.corners[pos.iWall]['x']
                pos.y = self.corners[pos.iWall]['y']
                return True
        elif pos.fig=='a':
            return self.circle_to_circle_line(pos, N)
        

    # check if path from enter to exit is free for specified noise level N
    def PathPassed(self, N):
        print "start check path N=%f" % N
        # start way round from first wall
        class TPos:
            x = 50
            y = 0
            iWall = 0
            fig = 'w' # current figure: w - wall, a - circle of alarm detection

        pos = TPos()

        while self.find_next(pos, N):
            if pos.iWall>2:
                break
        print "check end %s, wall=%d, x=%f, y=%f" % (pos.fig, pos.iWall, pos.x, pos.y)
        # check if we reach the exit
        return pos.fig=='w' and pos.iWall==3 and pos.x==50 and pos.y==100
    
    def noise(self, x, y, threshold):
        self.alarms = [{'x': x[i], 'y': y[i], 't': threshold[i]} for i in range(len(x))]
        # get minimal and maximum value of noise of whole system
        # minimal value near maximum sensitive alarm
        minN = max(threshold)
        # get maximum value noise between enter and exit
        maxN = min(self.min_noise_pt(50,0), self.min_noise_pt(50,100)) - 1.0E-9
        if maxN<minN: return
        print 'minN=%.14f, maxN=%.14f' % (minN, maxN)
        N = maxN
        if self.PathPassed(N):
            return N

        prevN = 0
        N = (maxN - minN)/2
        while abs(N-prevN)>self.deltaE:
            if self.PathPassed(N):
                print 'passed N=%.14f' % N
                minN = N
            else:
                print 'not passed N=%.14f' % N
                maxN = N
            prevN = N
            N = minN + (maxN - minN)/2

        return minN    
            

A = Alarmed()
#print '%.14f' % A.noise((50,),(2,), (87,))
#print '%.14f' % A.noise((1,99),(50,50), (1,1))
#print '%.14f' % A.noise((3,11,2,62,91),(90,10,75,25,50), (5,4,3,2,1))
#print '%.14f' % A.noise((1,99),(50,50), (1,2))
#print '%.14f' % A.noise((11, 32, 50, 69, 30, 49, 72, 91, 9, 31, 52, 70),(24, 26, 25, 23, 51, 52, 50, 49, 77, 75, 74, 76),(105, 97, 100, 106, 96, 103, 99, 102, 95, 101, 104, 98))
print '%.14f' % A.noise((20, 35, 50, 65, 80),(10, 20, 30, 20, 10),(5, 5, 5, 5, 5))
#{3,11,2,62,91}
#{90,10,75,25,50}
#{5,4,3,2,1}
