# **Project Plan: Monte Carlo Retirement Simulation**

## **1\. Project Instruction & Goal**

The primary goal of this project is to build a Monte Carlo simulation model to assess the viability of a specific retirement plan over a 10-year period (from age 50 to 60).

The user plans to retire early in California with a $1M stock portfolio and live by borrowing on margin against it, rather than selling shares for income. The simulation will model the interaction between portfolio growth, living expenses, margin loan interest, quarterly dividends, and an annual tax-gain harvesting strategy.

The final output will show the monthly range of potential net worth (maximum, average, and minimum) across thousands of simulated market scenarios, helping to quantify the risk and potential success of this strategy.

## **2\. Requirements Specification**

### **2.1. Core Methodology**

* The simulation must use the Monte Carlo method, running a user-configurable number of scenarios (e.g., default 200).  
* The simulation must stop and report the month of failure if the **average** net worth across all scenarios drops below zero.

### **2.2. User-Defined Inputs (Variables)**

The model must allow the user to configure the following parameters:

* **Initial Portfolio Value:** e.g., $1,000,000  
* **Initial Cost Basis:** e.g., $700,000  
* **Annual Spending:** e.g., $120,000 ($10,000/month)  
* **Monthly Passive Income:** e.g., $1,000  
* **Portfolio Annual Average Return:** e.g., 10%  
* **Portfolio Annual Standard Deviation:** e.g., 19%  
* **Quarterly Dividend Yield (%):** e.g., 1%  
* **Margin Loan Annual Average Interest Rate:** e.g., 5%  
* **Margin Loan Annual Interest Rate Std. Dev.:** e.g., 1.5%  
* **Brokerage Margin Limit:** e.g., 50% of portfolio value  
* **Federal Tax-Free Gain Limit (Annual):** e.g., $123,250 (This represents the top of the 0% federal bracket after the standard deduction)  
* **Tax Harvesting Profit Threshold (%):** e.g., 30%

### **2.3. Simulation Logic & Rules**

The model must accurately implement the following sequence of operations on a monthly basis for each scenario:

1. **Portfolio Growth:** The portfolio's value must change based on a randomly generated monthly return.  
2. **Dividend Payout (Quarterly):** In months 3, 6, 9, and 12, the simulation must calculate a dividend based on the current portfolio value and use this cash to pay down the margin loan.  
3. **Expense Funding:** Monthly spending needs are met first by passive income, then by borrowing on margin.  
4. **Margin Loan Management:** The loan balance accrues interest monthly. A "sell trigger" forces a sale of stock to pay off the loan if it exceeds the brokerage limit.  
5. **Annual Tax Strategy (every 12th month):**  
   * Tax-gain harvesting is performed only if the **unrealized long-term gain** exceeds the profit threshold.  
   * The model calculates total investment income for the year (dividends \+ any realized gains).  
   * It then harvests *just enough* additional **long-term capital gains** so the total investment income matches the federal tax-free limit.  
   * The cost basis of the harvested shares is "stepped up," and these shares are now considered **short-term holdings**.  
   * California state tax is calculated on the net investment income (dividends \+ gains \- margin interest). This tax bill is added to the margin loan.  
   * A new random margin interest rate is set for the next year.

### **2.4. Outputs**

* The output will be both a **table and a plot/chart** showing the **Maximum, Average, and Minimum Net Worth** for each of the 120 months.  
* Net Worth is defined as: (Current Portfolio Value) \- (Current Margin Loan Balance).

## **3\. Technical Design & Algorithm**

### **3.1. Initialization (Before Loop Starts)**

* Set initial values based on user inputs. **Create two portfolio buckets:**  
  * long\_term\_value \= initial\_portfolio\_value  
  * long\_term\_basis \= initial\_cost\_basis  
  * short\_term\_value \= 0  
  * short\_term\_basis \= 0  
* Initialize arrays to store results.  
* Initialize annual counters: total\_margin\_interest\_paid\_this\_year, gains\_realized\_this\_year, total\_dividend\_income\_this\_year to 0\.  
* Set current\_annual\_margin\_rate for the first year.

### **3.2. Monthly Simulation Loop (from month \= 1 to 120\)**

**Step 1: Asset Aging (Short-Term to Long-Term)**

* (This step moves assets held for 12 months from the short-term bucket to the long-term one. A simple approximation is to move 1/12th of the short-term portfolio each month).  
* aging\_value \= short\_term\_value / 12  
* aging\_basis \= short\_term\_basis / 12  
* short\_term\_value \-= aging\_value; short\_term\_basis \-= aging\_basis  
* long\_term\_value \+= aging\_value; long\_term\_basis \+= aging\_basis

**Step 2: Calculate Market Returns & Update Portfolio**

* Convert annual return/volatility to monthly figures.  
* Generate a random monthly return.  
* Apply the return to both buckets:  
  * long\_term\_value \*= (1 \+ random\_monthly\_return)  
  * short\_term\_value \*= (1 \+ random\_monthly\_return)

**Step 3: Handle Quarterly Dividends**

* total\_portfolio\_value \= long\_term\_value \+ short\_term\_value  
* **If month % 3 \== 0:**  
  * dividend\_payment \= total\_portfolio\_value \* (quarterly\_dividend\_yield / 100\)  
  * margin\_loan \-= dividend\_payment  
  * total\_dividend\_income\_this\_year \+= dividend\_payment

**Step 4: Cover Expenses & Update Margin Loan**

* cash\_shortfall \= monthly\_spending \- monthly\_passive\_income  
* margin\_loan \+= cash\_shortfall  
* Calculate and add monthly margin interest to margin\_loan and total\_margin\_interest\_paid\_this\_year.

**Step 5: Check for Forced Selling (Deleveraging)**

* margin\_limit \= total\_portfolio\_value \* brokerage\_margin\_limit  
* **If margin\_loan \> margin\_limit:**  
  * amount\_to\_sell \= (margin\_loan \- (total\_portfolio\_value \* brokerage\_margin\_limit)) / (1 \- brokerage\_margin\_limit)  
  * **Prioritize selling long-term assets first.** Update values accordingly, reducing long\_term\_value and long\_term\_basis first, then short-term if necessary. Track the gain\_from\_this\_sale.  
  * Update portfolio\_value, cost\_basis, margin\_loan, and gains\_realized\_this\_year.

**Step 6: Execute End-of-Year Tax Strategy**

* **If month % 12 \== 0:**  
  * unrealized\_long\_term\_gain\_percentage \= (long\_term\_value \- long\_term\_basis) / long\_term\_value  
  * **If unrealized\_long\_term\_gain\_percentage \> tax\_harvesting\_profit\_threshold:**  
    * total\_investment\_income\_so\_far \= gains\_realized\_this\_year \+ total\_dividend\_income\_this\_year  
    * gains\_to\_harvest \= federal\_tax\_free\_limit \- total\_investment\_income\_so\_far  
    * **If gains\_to\_harvest \> 0 and unrealized\_long\_term\_gain\_percentage \> 0:**  
      * value\_to\_harvest \= gains\_to\_harvest / unrealized\_long\_term\_gain\_percentage  
      * **Move harvested shares from Long-Term to Short-Term bucket:**  
        * long\_term\_value \-= value\_to\_harvest  
        * long\_term\_basis \-= (value\_to\_harvest \- gains\_to\_harvest) // Remove old basis  
        * short\_term\_value \+= value\_to\_harvest // Add value to ST  
        * short\_term\_basis \+= value\_to\_harvest // New basis is market value  
      * gains\_realized\_this\_year \+= gains\_to\_harvest  
  * **Calculate and "Pay" California Tax:**  
    * total\_investment\_income \= gains\_realized\_this\_year \+ total\_dividend\_income\_this\_year  
    * net\_investment\_income \= total\_investment\_income \- total\_margin\_interest\_paid\_this\_year  
    * ca\_taxable\_income \= net\_investment\_income \+ (passive\_income \* 12\) \- ca\_standard\_deduction  
    * ca\_tax\_due \= calculate\_ca\_tax(ca\_taxable\_income)  
    * margin\_loan \+= ca\_tax\_due  
  * **Set Margin Rate for Next Year & Reset Counters.**

**Step 7: Record Net Worth**

* net\_worth \= (long\_term\_value \+ short\_term\_value) \- margin\_loan  
* Store this result for the current month.

### **3.3. Final Aggregation (After all loops complete)**

* For each month (1-120), calculate the max, average, and min net\_worth from all scenarios.  
* Display these results in a table and a line chart.