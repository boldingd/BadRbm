#! /usr/bin/python3

import numpy
import scipy.special # for expit (a quick numpy-array-aware sigmoid)

# consider http://stackoverflow.com/questions/3985619/how-to-calculate-a-logistic-sigmoid-function-in-python

class RbmError(Exception):
    pass

class rbm:
    def __init__(self, i, j, rate, p=None): # i = |v|, j = |h|, p -> momentum
        if i < 1:
            raise RbmError("There must be at least one visible unit")

        if j < 1:
            raise RbmError("There must be at least one hidden unit")

        if p is not None:
            if p > 0.5:
                raise RbmError("Momentum greater than 0.5 doesn't make sense.")
            elif p <= 0.0:
                raise RbmError("Zero-or-less momentum doesn't make sense (use momentum=None to turn momentum off).")

        self.i = i # record |v| for error-checking
        self.j = j # record |h| for error-checking

        self.a = numpy.random.rand(i, 1) # visible biases
        self.b = numpy.random.rand(j, 1) # hidden viases

        self.W = numpy.random.rand(i,j)

        self.rate = rate

        self.p = p
        self.last_dW = None

    def get_json(self):
        pass

    def set(self, json_string):
        pass

    def get_energy(self, v, h):
        if v.shape != (self.i, 1):
            raise RbmError("wrong shape for v, should be (i, 1).")

        if h.shape != (self.j, 1):
            raise RbmError("wrong shape for h, should be (j, 1).")

        E = -1.0 * self.a.T @ v
        E -= self.b.T @ h
        E -= v.T @ self.W @ h

        return E

    def get_v(self, h):
        v_probs = scipy.special.expit(self.a + (self.W @ h))
        v_vals = numpy.random.rand(self.i, 1)

        # there has to be some craftier way to do this
        # possibly using numpy.vectorize?
        v_res = numpy.zeros((self.i, 1))
        for i in range(self.i):
            if v_vals[i] <= v_probs[i]:
                v_res[i] = 1.0

        return v_res

    def get_h(self, v):
        h_probs = scipy.special.expit(self.b + (self.W.T @ v))
        #h_probs = scipy.special.expit(self.b + (v.T @ self.W).T) # trying to avoid an expensive matrix invert
        h_vals = numpy.random.rand(self.j, 1)

        h_res = numpy.zeros((self.j, 1))
        for i in range(self.j):
            if h_vals[i] < h_probs[i]:
                h_res[i] = 1.0

        return h_res

#    def get_weight_update(self, v):
#        # https://en.wikipedia.org/wiki/Restricted_Boltzmann_machine
#        h = self.get_h(v)
#        positive = v @ h.T
#
#        vprime = self.get_v(h)
#        hprime = self.get_h(vprime)
#        negative = vprime @ hprime.T
#
#        return positive - negative
#
#    def get_bias_updates(self, v):
#        # random "seems reasonable" guess (not spelled out in paper or wikipedia)
#        # /should/ be folded into get_weight_update
#        
#        h = self.get_h(v)
#        vprime = self.get_v(h)
#        hprime = self.get_h(vprime)
#
#        return v - vprime, h - hprime

    def get_updates(self, v):
        h = self.get_h(v)
        vprime = self.get_v(h)
        hprime = self.get_h(vprime)

        w_update = (v @ h.T) - (vprime @ hprime.T)
        a_update = v - vprime
        b_update = h - hprime

        return w_update, a_update, b_update

    def apply_update(self, v, rate=None):
        if rate is None:
            rate = self.rate

        w_update, a_update, b_update = self.get_updates(v)

        if self.p is not None:
            self.W += (1.0 - self.p) * w_update * rate
            if self.last_dW is not None:
                self.W += self.p * self.last_dW * rate
            self.last_dW = w_update
        else:
            self.W += w_update * rate

        self.a += a_update * rate
        self.b += b_update * rate

    def get_samples(self, count, initial_visible=None):
        samples = []

        if initial_visible is None:
            current_v = numpy.random.rand(self.i, 1)
        else:
            current_v = initial_visible

        generated = 0;
        while generated < count:
            #print(str(current_v))

            current_h = self.get_h(current_v)
            current_v = self.get_v(current_h)

            samples.append( current_v )

            generated += 1

        return samples


# I determined that W.T @ v = v @ W in the lasiest and dumbest way possible
# I asked my brother, who is a methematician
# with one proviso: at least in numpy, v.T @ w produces a row-vector, and w.T @ v produces a column vector.
# simple test shows that it's actually faster with the matrix transpose?  It is a small matrix in the test, hmm.

