import math as m


# https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html
mu = 0.00490*10**6 *10**9  # m3 s-2
r = 1738.1*10**3  # m
h = 100*10**3  # m

print(mu)
print(r)

hdiff = 1*10**3

ac = r + h
alower = (2*(r + h) - hdiff)/2
ahigher = (2*(r + h) + hdiff)/2

vc = m.sqrt(mu/ac)
vlower = m.sqrt(mu*(2/ac - 1/alower))
vhigher = m.sqrt(mu*(2/ac - 1/ahigher))

print(vc)
print(vlower)
print(vhigher)

dv = 10  # m s-1

rlower = -1/((vc - dv)**2/mu - 2/ac)
rhigher = -1/((vc + dv)**2/mu - 2/ac)

print(ac)
print(rlower)
print(rhigher)

burnend = 2759.424635848819
wetmass = 4.7e3
drymass = 2.25e3

fuelstart = wetmass - drymass
fuelend = burnend - drymass
fuelconsumed = fuelstart - fuelend

print(fuelconsumed, fuelstart - fuelconsumed, fuelconsumed/fuelstart)