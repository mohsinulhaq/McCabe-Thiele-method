import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString


def mole_fraction(weight_fraction):
    return (weight_fraction/78)/(weight_fraction/78 + (100 - weight_fraction)/92)


def intersection(x1_array, y1_array, x2_array, y2_array):
    line1 = LineString([i for i in zip(x1_array, y1_array)])
    line2 = LineString([i for i in zip(x2_array, y2_array)])
    x_inter = line1.intersection(line2).x
    y_inter = line1.intersection(line2).y
    return x_inter, y_inter


def line(x_inter, y_inter, slope, length, perp=False):
    if perp:
        x_inter, y_inter = y_inter, x_inter
    x_array = [x_inter - i / 10 for i in range(length)]
    y_array = [y_inter]
    for i in range(1, length):
        y_inter -= slope * 0.1
        y_array.append(y_inter)
    if perp:
        return y_array, x_array
    else:
        return x_array, y_array


x = y = np.arange(0, 1.1, 0.1)
y_curve = [0, 0.21, 0.38, 0.511, 0.627, 0.719, 0.79, 0.853, 0.91, 0.961, 1]
y_straight = x
count = 0

residue_percentage = 100 - float(input('Enter residue composition %: '))
feed_percentage = float(input('Enter feed composition %: '))
distillate_percentage = float(input('Enter distillate composition %: '))
q = eval(input('Enter mole fraction of liquid in feed (q): '))
reflux_ratio = float(input('Enter the reflux ratio (R/Rm): '))

xw = mole_fraction(residue_percentage)
xf = mole_fraction(feed_percentage)
xd = mole_fraction(distillate_percentage)
slope = q/(q-1)

plt.title('McCabe-Thiele method')
plt.xlabel('Mole fraction of lighter component in liquid phase')
plt.ylabel('Mole fraction of lighter component in vapor phase')
plt.plot(x, x, color='black')  # y=x
plt.plot(x, y_curve, color='black')  # curve
plt.plot([xw] * 11, y_straight, color='red', linestyle='dashed')  # xw
plt.plot([xf] * 11, y_straight, color='red', linestyle='dashed')  # xf
plt.plot([xd] * 11, y_straight, color='red', linestyle='dashed')  # xd

plt.text(xf, -0.04, 'xf')
plt.text(xw, -0.04, 'xw')
plt.text(xd, -0.04, 'xd')

# xw line
xw_inter, yw_inter = intersection(x, y, [xw] * 11, y_straight)
# xf line
xf_inter, yf_inter = intersection(x, y, [xf] * 11, y_straight)
# xd line
xd_inter, yd_inter = intersection(x, y, [xd] * 11, y_straight)

x_inter_array, y_inter_array = line(xf_inter, yf_inter, slope, 3)
plt.plot(x_inter_array, y_inter_array, color='blue')

x_inter2, y_inter2 = intersection(x_inter_array, y_inter_array, x, y_curve)
slope2 = (yd_inter - y_inter2)/(xd_inter - x_inter2)
rm = 1/(1 - slope2)
R = rm * reflux_ratio
slope3 = R/(R + 1)
x_inter_array2, y_inter_array2 = line(xd_inter, yd_inter, slope3, 8)
plt.plot(x_inter_array2, y_inter_array2, color='green')

x_inter5, y_inter5 = intersection(x_inter_array2, y_inter_array2, x_inter_array, y_inter_array)
slope4 = (yw_inter - y_inter5)/(xw_inter - x_inter5)
x_inter_array3, y_inter_array3 = line(x_inter5, y_inter5, slope4, 5)
plt.plot(x_inter_array3, y_inter_array3, color='purple')

x_inter_array, y_inter_array = line(xd_inter, yd_inter, 0, 4)
plt.plot(x_inter_array, y_inter_array, color='black')

while True:
    try:
        x_inter, y_inter = intersection(x_inter_array, y_inter_array, x, y_curve)
    except AttributeError:
        break
    x_inter_array, y_inter_array = line(x_inter, y_inter, 0, 4, True)
    plt.plot(x_inter_array, y_inter_array, color='black')
    count += 1

    try:
        x_inter, y_inter = intersection(x_inter_array, y_inter_array, x_inter_array2, y_inter_array2)
        if x_inter < x_inter5:
            break
    except AttributeError:
        break
    x_inter_array, y_inter_array = line(x_inter, y_inter, 0, 4)
    plt.plot(x_inter_array, y_inter_array, color='black')

while True:
    try:
        x_inter, y_inter = intersection(x_inter_array, y_inter_array, x_inter_array3, y_inter_array3)
        if x_inter < xw:
            break
    except AttributeError:
        break
    x_inter_array, y_inter_array = line(x_inter, y_inter, 0, 4)
    plt.plot(x_inter_array, y_inter_array, color='black')

    try:
        x_inter, y_inter = intersection(x_inter_array, y_inter_array, x, y_curve)
    except AttributeError:
        break
    x_inter_array, y_inter_array = line(x_inter, y_inter, 0, 4, True)
    plt.plot(x_inter_array, y_inter_array, color='black')
    count += 1

plt.text(0.4, 1.1, 'Number of trays = ' + str(count - 1))

plt.show()
