from math import factorial
from decimal import Decimal, getcontext


SERVICE_RATES = [1.9, 6.3]
ARRIVAL_RATES = [9, 11, 13, 15, 19, 22, 25, 26, 31, 37, 43, \
                 45, 57, 68, 79, 81, 101, 121, 141, 145, 181, \
                 217, 253, 260, 325, 370, 390, 455, 463, 555, 648]


class MMCQueue:

    def __init__(self, arrival_rate: float, service_rate: float, c: int):
        if c * service_rate - arrival_rate < 0:
            raise(ValueError("c * mu must be greater than lambda"))
        self.arrival_rate = Decimal(arrival_rate)
        self.service_rate = Decimal(service_rate)
        self.c = c
        self.rho = self._calculate_utilization_factor()
        self.p0 = self._calculate_p0()
        self.Lq = self._calculate_Lq()
        self.Wq = self._calculate_Wq()

    def to_dict(self):
        return self.__dict__
    
    def _calculate_utilization_factor(self) -> Decimal:
        return Decimal(self.arrival_rate / self.service_rate)
    
    def _calculate_p0(self) -> Decimal:
        s = 1
        for n in range(1, self.c):
            s += self.rho ** n / self._factorial(n)
        x = self.rho ** self.c / self._factorial(self.c)
        y = (self.c * self.service_rate) / (self.c * self.service_rate - self.arrival_rate)
        denom = s + (x * y)
        return 1 / denom

    def _calculate_Lq(self) -> Decimal:
        x = self.rho**self.c / self._factorial(self.c - 1)
        y = self.arrival_rate * self.service_rate / (self.c * self.service_rate - self.arrival_rate)**2
        return x * y * self.p0

    def _calculate_Wq(self) -> Decimal:
        return self.Lq / self.arrival_rate
    
    @staticmethod
    def _factorial(n: int) -> Decimal:
        return Decimal(factorial(n))


if __name__ == '__main__':
    max_Wq = 0.5
    output = {}
    for l in ARRIVAL_RATES:
        for mu in SERVICE_RATES:
            for c in range(1, 100):
                if c * mu - l < 0:
                    continue
                else:
                    q = MMCQueue(l, mu, c)
                    if q.Wq < 0.5:
                        output[(l, mu)] = {'c': c, 'Wq': q.Wq}
                        break
    print(output)
