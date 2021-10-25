
def pointsInCircle(r, xm, ym ):
    
    xmin = xm - r
    xmax = xm + r
    ymin = ym - r
    ymax = ym + r
    
    xs = range(xmin, xmax+1)
    ys = range(ymin, ymax+1)
    print("Points in circle (",r,xm, ym,") :")
    pic = set() # set of points in circle
    for x in xs:
        for y in ys:
            if (x-xm)**2 + (y-ym)**2 <= r**2:
                pic.add((x,y))
    print(pic)
    return pic
  
# here put e.g. radio cells ( with radius and their location ).
pic1 = pointsInCircle(3, 1, 2)        
pic2 = pointsInCircle(2, 3, 2) 
intersection = pic1.intersection(pic2)   
print("intersect: ", intersection)
