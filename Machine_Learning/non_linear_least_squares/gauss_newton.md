# Gauss–Newton algorithm


## Description

<img src="https://latex.codecogs.com/svg.latex?%7B%5Cdisplaystyle%20%7B%5Cboldsymbol%20%7BX%20%7D%7D_%7B%28n&plus;1%29%7D%3D%7B%5Cboldsymbol%20%7BX%20%7D%7D_%7B%28n%29%7D-%5Cleft%28%5Cmathbf%20%7BJ_%7Br%7D%7D%20%5E%7B%5Cmathsf%20%7BT%7D%7D%5Cmathbf%20%7BJ_%7Br%7D%7D%20%5Cright%29%5E%7B-1%7D%5Cmathbf%20%7BJ_%7Br%7D%7D%20%5E%7B%5Cmathsf%20%7BT%7D%7D%5Cmathbf%20%7Br%7D%20%5Cleft%28%7B%5Cboldsymbol%20%7BX%20%7D%7D_%7B%28n%29%7D%5Cright%29%2C%7D" alt="{\displaystyle {\boldsymbol {X }}_{(n+1)}={\boldsymbol {X }}_{(n)}-\left(\mathbf {J_{r}} ^{\mathsf {T}}\mathbf {J_{r}} \right)^{-1}\mathbf {J_{r}} ^{\mathsf {T}}\mathbf {r} \left({\boldsymbol {X }}_{(n)}\right),}"/>


## Notes

The normal equations are n simultaneous linear equations in the unknown increments 
Δ\Delta . They may be solved in one step, using Cholesky decomposition, or, better, the QR factorization of 


{\displaystyle \mathbf {J_{r}} }. For large systems, an iterative method, such as the conjugate gradient method, may be more efficient. 


### Example



|i     |1      |2      |3      |4     |5     |6     |7        |
|---   |---    |---    |---    |---   |---   |---   |---      |
|[S]   |0.038  |0.194  |0.425  |0.626 |1.253 |2.500 | 	3.740  |
|Rate  |0.050  |0.127  |0.094  |0.2122|0.2729|0.2665|	0.3317 |


<br/>
<br/>


<img src="https://latex.codecogs.com/svg.latex?%7B%5Cdisplaystyle%20%7B%5Ctext%7Brate%7D%7D%3D%7B%5Cfrac%20%7BV_%7B%5Ctext%7Bmax%7D%7D%5Ccdot%20%5BS%5D%7D%7BK_%7BM%7D&plus;%5BS%5D%7D%7D%7D%3D%7B%5Cfrac%20%7Bx_1%5Ccdot%20S%7D%7Bx_%7B2%7D&plus;S%7D%7D" alt="https://latex.codecogs.com/svg.latex?{\displaystyle {\text{rate}}={\frac {V_{\text{max}}\cdot [S]}{K_{M}+[S]}}}={\frac {x_1\cdot S}{x_{2}+S}}" />

<br/>
<br/>

<img src="https://latex.codecogs.com/svg.latex?%7B%5Cdisplaystyle%20r_%7Bi%7D%3Dy_%7Bi%7D-%7B%5Cfrac%20%7Bx_%7B1%7Ds_%7Bi%7D%7D%7Bx_%7B2%7D&plus;s_%7Bi%7D%7D%7D%2C%5Cquad%20%28i%3D1%2C%5Cdots%20%2C7%29%7D" alt="{\displaystyle r_{i}=y_{i}-{\frac {x_{1}s_{i}}{x_{2}+s_{i}}},\quad (i=1,\dots ,7)}"/>

Here the Parameters that we are looking for are <img src="https://latex.codecogs.com/svg.latex?x_1" alt="https://latex.codecogs.com/svg.latex?x_1"/> and <img src="https://latex.codecogs.com/svg.latex?x_1" alt="https://latex.codecogs.com/svg.latex?x_2"/>






The Jacobian <img src="https://latex.codecogs.com/svg.latex?%5Cmathbf%7BJ_r%7D" alt="https://latex.codecogs.com/svg.latex?\mathbf{J_r}" />   of the vector of residuals <img src="https://latex.codecogs.com/svg.latex?r_%7Bi%7D" alt="https://latex.codecogs.com/svg.latex?r_{i}" />  with respect to the unknowns <img src="https://latex.codecogs.com/svg.latex?x_%7Bj%7D" alt="https://latex.codecogs.com/svg.latex?x_{j}" /> is a <img src="https://latex.codecogs.com/svg.latex?%7B%5Cdisplaystyle%207%5Ctimes%202%7D" alt="https://latex.codecogs.com/svg.latex?{\displaystyle 7\times 2}" /> matrix with the i-th row having the entries 









<img src="https://latex.codecogs.com/svg.latex?%7B%5Cdisplaystyle%20%7B%5Cfrac%20%7B%5Cpartial%20r_%7Bi%7D%7D%7B%5Cpartial%20x_%7B1%7D%7D%7D%3D-%7B%5Cfrac%20%7Bs_%7Bi%7D%7D%7Bx_%7B2%7D&plus;s_%7Bi%7D%7D%7D%3B%5Cquad%20%7B%5Cfrac%20%7B%5Cpartial%20r_%7Bi%7D%7D%7B%5Cpartial%20x_%7B2%7D%7D%7D%3D%7B%5Cfrac%20%7Bx_%7B1%7D%5Ccdot%20s_%7Bi%7D%7D%7B%5Cleft%28x_%7B2%7D&plus;s_%7Bi%7D%5Cright%29%5E%7B2%7D%7D%7D.%7D" alt="{\displaystyle {\frac {\partial r_{i}}{\partial x_{1}}}=-{\frac {s_{i}}{x_{2}+s_{i}}};\quad {\frac {\partial r_{i}}{\partial x_{2}}}={\frac {x_{1}\cdot s_{i}}{\left(x_{2}+s_{i}\right)^{2}}}.}" />

<br/>
<br/>

<img src="https://latex.codecogs.com/svg.latex?%5Cmathbf%7BJ_r%7D%3D%5Cbegin%7Bbmatrix%7D%20%7B%5Cfrac%20%7B%5Cpartial%20r_%7B1%7D%7D%7B%5Cpartial%20x_%7B1%7D%7D%7D%3D-%7B%5Cfrac%20%7Bs_%7B1%7D%7D%7Bx_%7B2%7D&plus;s_%7B1%7D%7D%7D%20%26%20%5Cquad%20%7B%5Cfrac%20%7B%5Cpartial%20r_%7B1%7D%7D%7B%5Cpartial%20x_%7B2%7D%7D%7D%3D%7B%5Cfrac%20%7Bx_%7B1%7D%5Ccdot%20s_%7B1%7D%7D%7B%5Cleft%28x_%7B2%7D&plus;s_%7B1%7D%5Cright%29%5E%7B2%7D%7D%7D%5C%5C%20%7B%5Cfrac%20%7B%5Cpartial%20r_%7B2%7D%7D%7B%5Cpartial%20x_%7B1%7D%7D%7D%3D-%7B%5Cfrac%20%7Bs_%7B2%7D%7D%7Bx_%7B2%7D&plus;s_%7B2%7D%7D%7D%20%26%20%5Cquad%20%7B%5Cfrac%20%7B%5Cpartial%20r_%7B2%7D%7D%7B%5Cpartial%20x_%7B2%7D%7D%7D%3D%7B%5Cfrac%20%7Bx_%7B1%7D%5Ccdot%20s_%7B2%7D%7D%7B%5Cleft%28x_%7B2%7D&plus;s_%7B2%7D%5Cright%29%5E%7B2%7D%7D%7D%5C%5C%20%26%20%5C%5C%20%26%20%5C%5C%20%7B%5Cfrac%20%7B%5Cpartial%20r_%7B7%7D%7D%7B%5Cpartial%20x_%7B1%7D%7D%7D%3D-%7B%5Cfrac%20%7Bs_%7B7%7D%7D%7Bx_%7B2%7D&plus;s_%7B7%7D%7D%7D%20%26%20%5Cquad%20%7B%5Cfrac%20%7B%5Cpartial%20r_%7B7%7D%7D%7B%5Cpartial%20x_%7B2%7D%7D%7D%3D%7B%5Cfrac%20%7Bx_%7B1%7D%5Ccdot%20s_%7B7%7D%7D%7B%5Cleft%28x_%7B2%7D&plus;s_%7B7%7D%5Cright%29%5E%7B2%7D%7D%7D%5C%5C%20%5Cend%7Bbmatrix%7D" alt=" \mathbf{J_r}=\begin{bmatrix} {\frac {\partial r_{1}}{\partial x_{1}}}=-{\frac {s_{1}}{x_{2}+s_{1}}} &  \quad {\frac {\partial r_{1}}{\partial x_{2}}}={\frac {x_{1}\cdot s_{1}}{\left(x_{2}+s_{1}\right)^{2}}}\\ {\frac {\partial r_{2}}{\partial x_{1}}}=-{\frac {s_{2}}{x_{2}+s_{2}}} &  \quad {\frac {\partial r_{2}}{\partial x_{2}}}={\frac {x_{1}\cdot s_{2}}{\left(x_{2}+s_{2}\right)^{2}}}\\ " />

## Improved versions

## Wolfe conditions

## Goldstein conditions


