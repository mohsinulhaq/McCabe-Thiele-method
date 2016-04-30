import matplotlib.pyplot as plt
from shapely.geometry import LineString


def mole_fraction(weight_fraction):
    return (weight_fraction/78)/(weight_fraction/78 + (100 - weight_fraction)/92)

x = [i/10 for i in range(11)]
y_curve = [0, 0.21, 0.38, 0.511, 0.627, 0.719, 0.79, 0.853, 0.91, 0.961, 1]
y_straight = x

weight_percentage = float(input('Enter feed weight %: '))
distillate_percentage = float(input('Enter distillate weight %: '))
residue_percentage = 100 - float(input('Enter residue weight %: '))
q = eval(input('Enter q: '))

xf = mole_fraction(weight_percentage)
xd = mole_fraction(distillate_percentage)
xw = mole_fraction(residue_percentage)
slope = abs(q/(q-1))

plt.plot(x, x)  # y=x
plt.plot(x, y_curve)  # curve
plt.plot([xf] * 11, y_straight, linestyle='dashed')  #xf
plt.plot([xd] * 11, y_straight, linestyle='dashed')  #xd
plt.plot([xw] * 11, y_straight, linestyle='dashed')  #xw

line1 = LineString([i for i in zip(x, x)])
line2 = LineString([i for i in zip([xf] * 11, y_straight)])

x_inter = line1.intersection(line2).x
y_inter = line1.intersection(line2).y

x_inter_array = [x_inter - i/10 for i in range(0, 4)]
y_inter_array = [y_inter]
for i in range(1, 4):
    y_inter += slope * 0.1
    y_inter_array.append(y_inter)

line3 = LineString([i for i in zip(x_inter_array, y_inter_array)])
line4 = LineString([i for i in zip(x, y_curve)])
x_inter2 = line3.intersection(line4).x
y_inter2 = line3.intersection(line4).y

plt.plot(x_inter_array, y_inter_array, 'r')

# xd wala
line5 = LineString([i for i in zip(x, x)])
line6 = LineString([i for i in zip([xd] * 11, y_straight)])
x_inter3 = line5.intersection(line6).x
y_inter3 = line5.intersection(line6).y

# xw wala
line7 = LineString([i for i in zip(x, x)])
line8 = LineString([i for i in zip([xw] * 11, y_straight)])
x_inter4 = line7.intersection(line8).x
y_inter4 = line7.intersection(line8).y

slope2 = (y_inter3 - y_inter2)/(x_inter3 - x_inter2)

rm = 1/(1 - slope2)
R = rm * 1.5
slope3 = R/(R + 1)

x_inter_array2 = [x_inter3 - i/10 for i in range(0, 8)]
y_inter_array2 = [y_inter3]
for i in range(1, 8):
    y_inter3 -= slope3 * 0.1
    y_inter_array2.append(y_inter3)

plt.plot(x_inter_array2, y_inter_array2, 'g')

line9 = LineString([i for i in zip(x_inter_array2, y_inter_array2)])
line10 = LineString([i for i in zip(x_inter_array, y_inter_array)])
print(line9, line10)
x_inter5 = line9.intersection(line10).x
y_inter5 = line9.intersection(line10).y

slope4 = (y_inter4 - y_inter5)/(x_inter4 - x_inter5)
x_inter_array3 = [x_inter5 - i/10 for i in range(0, 4)]
y_inter_array3 = [y_inter5]
for i in range(1, 4):
    y_inter5 -= slope4 * 0.1
    y_inter_array3.append(y_inter5)

plt.plot(x_inter_array3, y_inter_array3, 'b')

plt.text(xf, -0.05, 'xf')
plt.text(xw, -0.05, 'xw')
plt.text(xd, -0.05, 'xd')
plt.show()
