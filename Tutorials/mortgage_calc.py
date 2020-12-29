#https://en.wikipedia.org/wiki/Compound_interest
#https://www.maa.org/sites/default/files/Peyman_Milanfar45123.pdf
#https://twitter.com/docmilanfar/status/1254535220491022336/photo/1
#https://byjus.com/maths/compound-interest/
#https://www.mathsisfun.com/money/compound-interest-derivation.html
# Continuous compounding
# Monthly amortized loan or mortgage payments
eigen_capital=0
#House Price
House_Price=200000


#Total loan
P=House_Price-eigen_capital

#Yearly Interest year
R=0.0145
#Total number of month
numer_of_years=15
N=numer_of_years*12
r=R/12

monthly_payment=(r*((1+r)**N)*P)/((1+r)**N-1)


estimate_monthly_payment=(P+0.5*P*N*r)/N

print(monthly_payment)
print(estimate_monthly_payment)


from mortgage import Loan
loan = Loan(principal=P, interest=R, term=numer_of_years)
loan.summarize
