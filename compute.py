import numpy as np
from typing import Literal

def toEquivalentRate(annualRate: float, newCompounding: int, oldCompunding: int = 1) -> float:
    """
    Convert nominal interest rates between different compounding periods.
    Allows projection of investments with different contribution schedules by converting them to equivalent interest rates.

        See: https://www.calculatorsoup.com/calculators/financial/equivalent-interest-rate-calculator.php
    """

    return newCompounding * ((1 + annualRate / oldCompunding) ** (oldCompunding / newCompounding) - 1)

def averageReturnPerPeriod(rate: float, contributionsPerYear: int) -> float:
    """
    Average the returns over the number of contributions per year. 
    e.g., 10% nominal return annually with quarterly contributions is 2.5% nominal per quarter.
    """

    return 1 + rate / contributionsPerYear

def cumulativeGeometricSeries(amount: float, commonRatio: float, periods: int) -> float:
    """
    Typical sum of a geometric series.
    """
    def sumGeometricSeries(p: int):
        ## need to check this as geometric series is undefined for a commonRatio of 1, which here is no growth
        if (commonRatio == 1):
            return amount * p
        
        return amount * (1 - commonRatio ** p) / (1 - commonRatio)

    return np.array([sumGeometricSeries(p) for p in range(1, periods + 1)])

def toFutureValueOfContribution(annualRate: float, contributionAmount: int, contributionsPerYear: int, durationYears: int, timing: Literal["start, end"] = "end") -> float:
    """
    Compute the future value of a defined contribution scheme (growth rate, amount, duration, timing of payments within period).
    """

    ratePerPeriod = toEquivalentRate(annualRate, contributionsPerYear, 1) / contributionsPerYear
    totalPeriods = contributionsPerYear * durationYears
    finalValue = cumulativeGeometricSeries(contributionAmount, 1 + ratePerPeriod, totalPeriods)

    ## less commonly, an annuity due (i.e., you make contributions at the start of each period)
    ## i.e., you get extra investment period
    if timing == "start":
        return np.array([x * (1 + ratePerPeriod) for x in finalValue])

    return finalValue


print(toEquivalentRate(.10, 12))
print(toFutureValueOfContribution(.10, 1000, 12, 5))
print(toFutureValueOfContribution(.10, 1000, 12, 5, "start"))