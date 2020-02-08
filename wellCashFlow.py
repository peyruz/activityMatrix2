import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd

def well_moCF(startDate=datetime(2020,1,1), endDate=datetime(2021,1,1), qini=5, decline=0.05, discRate=0.1,
              investment=10000,
              oilPrice=55, NRI=0.875, fixedCost=300):
    """ Monthly cash flow from an oil well
    Recommended use for limited time periods (<3 yrs) since the calculation is a bit simplified and may accrue error
    in the long term."""

    if (endDate-startDate)<timedelta(days=60):
        print('Error: Range of dates should be at least 60 days. Return -1.')
        return -1

    # Monthly exponential decline coef
    k_mo = np.log(1 - decline) / 12

    # Define compounding periods
    dateRange = pd.date_range(startDate, endDate, freq='M')

    CFdf = pd.DataFrame(data={'Date': dateRange, 'CF': np.NaN})

    # Count days in the compounding periods
    dayCount = CFdf['Date'].diff().apply(lambda x: x.days)
    dayCount.iloc[0] = (CFdf['Date'][0] - startDate).days
    # dayCount.iloc[-1] = (endDate - endDate).days

    # time from startDate to midPoint of each compounding period
    midPoints = ( (CFdf['Date']-startDate).apply(lambda x: x.days) - dayCount/2 )
    # Amount produced in each compounding period
    monthlyProd = qini*np.exp(k_mo * midPoints / 30.4) * dayCount

    # Cash flow
    CFdf['CF'] = monthlyProd*oilPrice*NRI-fixedCost
    CFdf.loc[CFdf.index[0], 'CF'] -= investment

    # Discounted Cash Flow
    CFdf['DCF'] = [CFdf['CF'][ii]/(1+discRate/12)**ii for ii in range(len(CFdf['CF']))]

    # Cumulative DCF
    CFdf['Cum DCF'] = CFdf['DCF'].cumsum()

    return CFdf








