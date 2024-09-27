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

def sumGeometricSeries(amount: float, commonRatio: float, periods: int) -> float:
    """
    Typical sum of a geometric series.
    """

    ## need to check this as geometric series is undefined for a commonRatio of 1, which here is no growth
    if (commonRatio == 1):
        return amount * periods
    
    return amount * (1 - commonRatio ** periods) / (1 - commonRatio)

def toFutureValueOfContribution(annualRate: float, contributionAmount: int, contributionsPerYear: int, durationYears: int, timing: Literal["start, end"] = "end") -> float:
    """
    Compute the future value of a defined contribution scheme (growth rate, amount, duration, timing of payments within period).
    """

    ratePerPeriod = toEquivalentRate(annualRate, contributionsPerYear, 1) / contributionsPerYear
    totalPeriods = contributionsPerYear * durationYears
    finalValue = sumGeometricSeries(contributionAmount, 1 + ratePerPeriod, totalPeriods)

    ## less commonly, an annuity due (i.e., you make contributions at the start of each period)
    ## i.e., you get extra investment period
    if timing == "start":
        return finalValue * (1 + ratePerPeriod)

    return finalValue


print(toEquivalentRate(.10, 12))
print(toFutureValueOfContribution(.10, 1000, 12, 5))
print(toFutureValueOfContribution(.10, 1000, 12, 5, "start"))