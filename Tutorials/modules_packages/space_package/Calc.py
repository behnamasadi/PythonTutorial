def plannet_mass(gravity,radius):
    mass=(gravity*radius**2/6.67*10**-11)
    return mass


def plannet_volume(radius):
    vol=(4*3.14*radius**2)/2
    return vol
