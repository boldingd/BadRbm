#! /usr/bin/python3

import numpy
import random

import badrbm

training_set = list()
for i in range(5):
    cur = numpy.zeros((5, 1))
    cur[i] = 1.0

    training_set.append(cur)

# append an all-on vector to the training set
#training_set.append( numpy.ones((5,1)) )

r = badrbm.rbm(5, 6, 0.1, p=0.1)

count = 0
while count < 10 ** 6:
    cur = random.choice(training_set)
    r.apply_update(cur)

    count += 1

print("trained")

# it seems to get stuck repeating one sample, which /kind of/ makes sense
# so, run multiple trials, make sure it will at least get stuck in any training sample that shows up

def demented_energy_guess(rbm, v, samples=20):
    energies = []
    while len(energies) < samples:
        cur_h = rbm.get_h(v)
        cur_e = rbm.get_energy(v, cur_h)
        energies.append(cur_e)

    energy = sum(energies) / len(energies)

    return energy

def get_random_sample(prob=0.5):
    r = numpy.random.rand(5,1)
    for i in range(len(r)):
        if r[i] < prob:
            r[i] = 1.0
        else:
            r[i] = 0.0

    return r

with open("samples.dat", "w") as ofile:
    #earlies = []

    trial = 0
    while trial < 100:
        ofile.write("trial {}\n".format(trial))

        samples = r.get_samples(20)
        #earlies.append(samples[1])

        for sample in samples:
            ofile.write(str(sample.T) + "\n")

        ofile.write("\n\n")

        trial += 1

    ofile.write("energies:\n")

    for s in training_set:
        e = demented_energy_guess(r, s)
        ofile.write("{}  {}\n".format(s.T, e))

#    for s in earlies:
#        e = demented_energy_guess(r, s)
#        ofile.write("{}  {}\n".format(s.T, e))

    for _ in range(20):
        s = get_random_sample()
        e = demented_energy_guess(r, s)
        ofile.write("{}  {}\n".format(s.T, e))


    ofile.write("\n\nW:\n{}\n\na:\n{}\n\nb:\n{}\n".format(r.W, r.a, r.b))
    
