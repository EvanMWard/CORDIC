import fileinput
import math

# Goal is to minimize error
EPS = 10**-8

# Closed form indefinite integral of pizza radius function
def area(alpha, beta, a, b):
    return 0.5*((alpha**2)/(12*math.pi**2)*(b**3-a**3)+alpha*beta/(2*math.pi)*(b**2-a**2)+(b-a)*beta**2)

# Relative error calculation
def relative_error(ar, slice_area):
    return (slice_area-ar)/slice_area

file = fileinput.input()
line = list(map(float, file.readline().strip().split()))

alpha = line[0]
beta = line[1]
n = line[2]

# Closed form definite integral from 0 to 2*pi of pizza radius function gives total area
total_area = (1/3)*math.pi*(alpha**2) + math.pi*alpha*beta + math.pi*(beta**2)
# Calculate slice area
slice_area = total_area/n

# Goal of this algorithm is to solve the area equation for the upper bound of the definite integral (b), since alpha, beta and a are known
# This is done by guessing a cutoff point and checking its area
# If the area is too small or large, we rotate the cutoff point in a direction such that the area approaches the calculated slice area
# If we overshoot the true cutoff on any rotation (area goes from being too small to too large or vice versa), swap the rotation direction and halve the rotation amount
# Iterate this until absolute and relative area error is within tolerance of EPS

a = 0
slice_count = 0
while slice_count < n-1:
    # Start b at a, rotation direction positive and rotation amount 1 radian
    b = a
    dir = 1
    rot = 1
    # Since b starts at a, initial area will be 0 since integral bounds are the same value
    ar = 0
    while (abs(ar - slice_area) > EPS) or (abs(relative_error(ar, slice_area)) > EPS):
        # Calculate new area (does nothing on first iteration)
        ar = area(alpha, beta, a, b)

        # Rotate in positive direction
        # If area becomes larger than actual value, we have overshot and need to rotate negative next time
        if dir > 0: 
            b += rot
            if ar > slice_area:
                rot /= 2
                dir = -1
        # Rotate in negative direction
        # If area becomes smaller than actual value, we have overshot and need to rotate positive next time 
        else: 
            b -= rot
            if ar < slice_area:
                rot /= 2
                dir = 1
    # Once area values are within EPS, add one to slice count, print cutoff point and start next integral at b
    # Error WILL compound with inaccuracies in b, so it is important to have small EPS (for given problem bounds, 10**-8 passes all cases)
    slice_count += 1
    print(b)
    a = b