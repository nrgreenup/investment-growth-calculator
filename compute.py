import numpy as np

def toEquivalentRate(annualRate: float, newCompounding: int, oldCompunding: int = 1):
    """
    What: 
    Convert nominal interest rates of a given compounding period to an equivalent interest rate given a different compounding period.
    
    Why:
    We normally think of returns in annual terms (e.g., the S&P500 returns about 10.5% annually, on average).
    But, people invest at differing schedules (monthly, quarterly, semi-annually, annually... or commonly a combination of them).
    So, we need to be able to move between effective interest rates based on contribution frequency.

    Ref: 
    See for explanation and formula: https://www.calculatorsoup.com/calculators/financial/equivalent-interest-rate-calculator.php
    """
    return newCompounding * ((1 + annualRate / oldCompunding) ** (oldCompunding / newCompounding) - 1)

def averageReturnPerPeriod(rate: float, contributionsPerYear: int):
    """
    What:
    Average the returns over the number of contributions per year. 

    Why:
    If we return 6% per year, we need to break that over the contribution frequency. If we contribute 12 times a year, we then assume .5% for each contribution per month.
    Assumes uniformity month-over-month, which of course isn't the case, but is a decent approximator absent getting into much more complex approaches.
    """
    return 1 + rate / contributionsPerYear

def toFutureValueOfContribution(annualRate: float, amount: int, contributionsPerYear: int, durationYears: int):
    growthFactor = averageReturnPerPeriod(toEquivalentRate(annualRate, contributionsPerYear, 1), contributionsPerYear)
    totalContributions = contributionsPerYear * durationYears
    return amount * (1 - pow(growthFactor, totalContributions)) / (1 - growthFactor)

print(toEquivalentRate(.10, 12))
print(toFutureValueOfContribution(.10, 1000, 12, 5))