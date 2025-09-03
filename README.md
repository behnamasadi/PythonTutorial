# [Python Snippet Codes](#)

This repository contains my snippet codes for my Python projects. It includes various examples for: Machine Learning, Probability, Probabilistic Graphical Modeling, Signal System, Calculus, and Rerun.


![alt text](https://img.shields.io/badge/license-BSD-blue.svg)
![CI Tests](https://github.com/behnamasadi/PythonTutorial/actions/workflows/ci.yml/badge.svg)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/behnamasadi/PythonTutorial)
![GitHub Release](https://img.shields.io/github/v/release/behnamasadi/PythonTutorial)
![GitHub Repo stars](https://img.shields.io/github/stars/behnamasadi/PythonTutorial)
![GitHub forks](https://img.shields.io/github/forks/behnamasadi/PythonTutorial)


Dependencies:
```
conda create -n PythonTutorial
conda activate PythonTutorial
conda install scipy numpy matplotlib pywavelets scikit-image anaconda::ipython anaconda::sympy
conda install -c conda-forge jupyterlab
conda install -c anaconda networkx
conda install anaconda::pandas
conda install conda-forge::acstools
```
then 
```
cd /home/$USER/workspace/
git clone git@github.com:behnamasadi/PythonTutorial.git
ln -s /home/$USER/workspace/PythonTutorial /home/$USER/anaconda3/envs/PythonTutorial/src
```

If you get `conda: command not found` just add it to the path:

```
export PATH="$HOME/anaconda3/bin:$PATH"
```
then 
```
conda init
```


Enable/ disable auto activate base: you can check this using the following command: 

`conda config --show | grep auto_activate_base`

to set it false: 

`conda config --set auto_activate_base False`


# [Machine Learning](machine_learning/)  
- [Clustering](machine_learning/clustering)
  - [Gaussian Mixture Models (GMM)](machine_learning/clustering/gmm.ipynb)
    * [KL Divergence for GMM Distance](machine_learning/clustering/gmm.ipynb)
  - [K-Means Clustering](machine_learning/clustering/scripts/kmeans_demo.py)
  - [DBSCAN (Density-Based Clustering)](machine_learning/clustering/scripts/dbscan.py)
  - [Hierarchical Clustering](machine_learning/clustering/scripts/hierarchical_clustering_agglomerative_divisive.py)
  - [Cluster Validation Methods](machine_learning/clustering/scripts/)
    * [Silhouette Score Validation](machine_learning/clustering/scripts/cluster_validation_silhouette.py)
    * [C-Index Validation](machine_learning/clustering/scripts/c_index_kmeans.py)
  - [Clustering Algorithms Comparison](machine_learning/clustering/scripts/comparing_clustering_algorithms.py)
  - [Graph-Based Clustering](machine_learning/clustering/scripts/minimum_spanning_tree.py)
- [Dimensionality Reduction, Manifold Learning](machine_learning/dimensionality_reduction_manifold_learning)  
- [Ensembling](machine_learning/ensembling)  
- [Feature Preprocessing](machine_learning/feature_preprocessing)  
- [Feature Selection And Analysis](machine_learning/feature_selection_and_analysis)  
- [Generative and Discriminative Algorithm](machine_learning/generative_and_discriminative_algorithm)  
- [Hidden Markov Model](machine_learning/hidden_markov_model/hmm.ipynb)  
- [Hyperparameter](machine_learning/hyperparameter)  
- [Cohen's Kappa coefficient](machine_learning/kappa_coefficient/index.ipynb)  
- [Entropy](machine_learning/entropy/index.ipynb)   
- [Learning Process Steps Strategy](machine_learning/learning_process_steps_strategy)  
- [Metrics and Scoring For Model Evaluation, Bias Variance Trade off, ROC, AUC, F1, TP, FP, TN, FN](machine_learning/metrics_and_scoring_for_model_evaluation/metrics_and_scoring_methods.ipynb)  
- [Model Diagnostics and Evaluation Techniques](machine_learning/metrics_and_scoring_for_model_evaluation/metrics_and_scoring_methods.ipynb)
- [Reliability Score](machine_learning/reliability_score/index.ipynb)
  * [Cronbach’s Alpha](machine_learning/reliability_score/index.ipynb)  
  * [Intraclass Correlation Coefficient (ICC)](machine_learning/reliability_score/index.ipynb)  
  * [Test-Retest Reliability](machine_learning/reliability_score/index.ipynb)  
  * [Split-Half Reliability](machine_learning/reliability_score/index.ipynb)  
- [Training Validation Test set](machine_learning/training_validation_test/index.ipynb)
- [Model Selection](machine_learning/model_selection/index.ipynb)
  - [Information Criteria (BIC, AIC,DIC)](machine_learning/model_selection/information_criteria.ipynb)
  - [Cross-Validation](machine_learning/model_selection/cross_validation.ipynb)
  - [Model Comparison](machine_learning/model_selection/model_comparison.ipynb)
- [Multi Task Learning](machine_learning/multi_task_learning)    
- [Optimization and Null Space](machine_learning/null_space/index.ipynb)  
- [Constrained Optimization](machine_learning/null_space/index.ipynb#Constrained-Optimization)   
- [Curve Fitting](machine_learning/curve_fitting)  
- [Convex Optimization](machine_learning/convex_optimization)   
- [Ridge Regression, Regularization](machine_learning/regularization)  
- [Non-linear least squares](machine_learning/non_linear_least_squares/non_linear_least_squares.md)  
- [Levenberg–Marquardt algorithm](machine_learning/non_linear_least_squares/levenberg_marquardt_algorithm.md)  
- [Gauss Newton](machine_learning/non_linear_least_squares/gauss_newton.md)    
- [Hypothesis Testing](machine_learning/hypothesis_testing/index.ipynb#Hypothesis-Testing)  
  - [Null Hypothesis and Alternative Hypothesis](machine_learning/hypothesis_testing/index.ipynb#Null-Hypothesis)  
  - [P Values](machine_learning/hypothesis_testing/p-value.ipynb)  
  - [Test Statistic](machine_learning/hypothesis_testing/p-value.ipynb#Technical-way-of-describing-the-p-value)
    * [t-test, T-Score, T-Value](machine_learning/hypothesis_testing/t-test.ipynb)
    * [z-test, Z-Score, Z-Value](machine_learning/hypothesis_testing/z-test.ipynb)
    * [chi-square-test](machine_learning/hypothesis_testing/chi-square-test.ipynb)
    * [likelihood ratio-test](machine_learning/hypothesis_testing/likelihood_ratio-test.ipynb)
    * [ANOVA](machine_learning/hypothesis_testing/ANOVA.ipynb)
- [Kernel Function, Support Vector Machine (SVM)](machine_learning/kernel_function/index.ipynb) 
- [Linear Equation](machine_learning/linear_equation)  
- [Regression Analysis](machine_learning/regression_analysis/regression_analysis.ipynb)  
- [Linear Discriminant Analysis (LDA)](machine_learning/linear_discriminant_analysis_LDA/linear_discriminant_analysis_LDA.ipynb)
- [Gaussian Processes](machine_learning/gaussian_processes/index.ipynb)  
- [Radial Basis Function](machine_learning/radial_basis_function/index.ipynb)  
- [Vector Quantization](machine_learning/vector_quantization/index.ipynb)  
- [Ill-conditioned Problem](machine_learning/linear_equation/ill_conditioned_problem.ipynb)  
- [Solving Linear Equations](machine_learning/linear_equation/solving_linear_equations.ipynb)  

# [Probability](probability/)  
- [Expected Value, Variance, Covariance](probability/covariance_expected_value.ipynb#Expected-Value)  
- [PMF, PDF, CDF, Marginal Probability, Joint Probability](probability/cdf_pmf_pdf_joint_marginal.ipynb)  
  - [Probability Mass Function PMF](probability/cdf_pmf_pdf_joint_marginal.ipynb#1.1.-Discrete-Random-Variable-PMF)  
  - [Continuous Random Variable PDF](probability/cdf_pmf_pdf_joint_marginal.ipynb#1.1.-Discrete-Random-Variable-PMF)  
  - [Cumulative Mass Function CMF](probability/cdf_pmf_pdf_joint_marginal.ipynb#2.1.-Discrete-Random-Variable-c.d.f)  
  - [Cumulative Distribution Function CDF](probability/cdf_pmf_pdf_joint_marginal.ipynb#2.2.-Continuous-Random-Variable)  
- [Joint Probability Distribution](probability/joint_probability_distribution.ipynb)  
- [Marginal Distribution](probability/marginal_distributions.ipynb)  
- [Marginal Distribution vs. Conditional Distribution](probability/marginal_distribution_vs_conditional_distribution.ipynb)  
- [Conditional Distribution of Y Given X](probability/conditional_distribution_of_y_given_x.ipynb)
- [Chain Rule](probability/chain_rule.ipynb)  
- [Correlation Matrix](probability/correlation_matrix.ipynb)  
- [Density Estimation](probability/density_estimation.ipynb)  
- [Important Extensions](probability/important_extensions.ipynb)  
- [KL Divergence](probability/KL_divergence.ipynb)  
- [Jensen's Inequality](probability/jensen_inequality.ipynb)  
- [Likelihood](probability/likelihood.ipynb)  
  - [Log Likelihood](probability/likelihood.ipynb#Log-Likelihood)  
  - [Likelihood ratio](probability/likelihood.ipynb#Likelihood-ratio)  
  - [Log odds](probability/likelihood.ipynb#Log-odds)  
  - [Odds ratio](probability/likelihood.ipynb#Odds-ratio)  
  - [Maximum Likelihood Estimation (MLE)](probability/likelihood.ipynb#Maximum-Likelihood-Estimation-(MLE))  
- [Maximum A Posteriori (MAP) Estimation](probability/maximum_a_posteriori_estimation_MAP/index.ipynb)  
- [Maximum A-Posteriori (MAP) Inference](machine_learning/hidden_markov_model/hmm.ipynb#Maximum-A-Posteriori-(MAP)-Inference)  
- [Minimum Mean Square Error (MMSE)](probability/minimum_mean_square_error_MMSE/index.ipynb)  
- [Probability Distributions](probability/probability_distributions.ipynb)  
  - [Multinomial Distribution](probability/probability_distributions.ipynb#Multinomial-Distribution)  
  - [Bernoulli Distribution](probability/probability_distributions.ipynb#Bernoulli-Distribution)  
  - [Binomial Distribution](probability/probability_distributions.ipynb#Binomial-Distribution)  
  - [Multivariate Normal (Gaussian) Distribution](probability/probability_distributions.ipynb#Multivariate-Normal-(Gaussian)-Distribution)  
  - [Moments Parameterization](probability/probability_distributions.ipynb#Moments-Parameterization)  
  - [Canonical Parameterization](probability/probability_distributions.ipynb#Canonical-Parameterization)  
- [Percentiles and Percentages](probability/percentiles_percentages/index.ipynb)  
  - [Quartiles (25th, 50th, 75th percentiles)](probability/percentiles_percentages/index.ipynb#Quartiles)  
  - [Interquartile Range (IQR)](probability/percentiles_percentages/index.ipynb#Interquartile-Range)  
  - [Deciles and Percentiles](probability/percentiles_percentages/index.ipynb#Deciles-Percentiles)  
  - [Percentage vs Percentile](probability/percentiles_percentages/index.ipynb#Percentage-vs-Percentile)  
  - [Percentile Rank](probability/percentiles_percentages/index.ipynb#Percentile-Rank)  
- [Probability Space, Measure](probability/probability_space_measure.ipynb)  
- [Confidence Interval](machine_learning/confidence_interval/index.ipynb)  

# [Probabilistic Graphical Modeling](probabilistic_graphical_modeling/)  

- [Probabilistic Graphical Models](probabilistic_graphical_modeling/probabilistic_graphical_models.ipynb)  
- [Bayesian Inference](probabilistic_graphical_modeling/bayesian_inference.ipynb)  
- [Bayes Filter](probabilistic_graphical_modeling/bayes_filter.ipynb)
- [Naive Bayes Classifier](machine_learning/naive_bayes_classifier/naive_bayes_classifier.ipynb)
- [Bayesian Network (Bayes Network, Belief Network, or Decision Network)](probabilistic_graphical_modeling/bayesian_network.ipynb)  
- [High Dimensional Probability](https://www.math.uci.edu/~rvershyn/teaching/hdp/hdp.html)  
- [Factor Graph](probabilistic_graphical_modeling/factor_graph.ipynb)  
  - [Message Passing Algorithm](probabilistic_graphical_modeling/factor_graph.ipynb#Message-Passing-Algorithm)  
  - [Belief Propagation](probabilistic_graphical_modeling/factor_graph.ipynb#Belief-Propagation)  
  - [A visual introduction to Gaussian Belief Propagation](probabilistic_graphical_modeling/factor_graph.ipynb#A-visual-introduction-to-Gaussian-Belief-Propagation)  
  - [Variable Elimination](probabilistic_graphical_modeling/factor_graph.ipynb#Variable-Elimination)  

# [Signal System](signal_system/)    

- [convolution](signal_system/convolution.ipynb)  
- [auto correlation](signal_system/autocorrelation.ipynb)
- [wavelets](signal_system/wavelets.ipynb)  
- [continuous wavelet transform CWT, discrete wavelet transform DWT](signal_system/continuous_wavelet_transform_discrete_wavelet_transform.ipynb)
- [white noise Gaussian noise](signal_system/white_noise_gaussian_noise.ipynb)
- [random walk, wiener process, brownian noise](signal_system/random_walk_wiener_process_brownian_noise.ipynb)
- [signal smoothing noise removal reduction](signal_system/signal_smoothing_noise_removal_reduction.ipynb)
- [continuous time state equations](signal_system/continuous_time_state_equations.ipynb)
- [noise spectral density](signal_system/noise_spectral_density.ipynb)
- [non-stationary signal](signal_system/non-stationary_signal.ipynb)
- [signal to noise ratio](signal_system/signal_to_noise_ratio.ipynb)
- [spectral analysis](signal_system/spectral_analysis.ipynb)

# [Calculus](calculus/)    

- [Derivatives](calculus/derivatives.ipynb)  
- [Partial-derivative](calculus/derivatives.ipynb#Partial-derivative)
- [Gradient](calculus/derivatives.ipynb#Gradient)
- [Total Derivative](calculus/derivatives.ipynb#Total-derivative)
- [Directional Derivative](calculus/derivatives.ipynb#Directional-derivative)
- [Scalar, Vector, and Matrix Derivatives](calculus/derivatives.ipynb#Scalar,-Vector-and-Matrix-derivatives)
- [Hessian](calculus/derivatives.ipynb#Hessian)
- [Taylor's theorem for single functions](calculus/taylor's_theorem.ipynb#Taylor's-theorem-for-single-functions)
- [Taylor's theorem for multivariate functions](calculus/taylor's_theorem.ipynb#Taylor's-theorem-for-multivariate-functions)
- [Differentiation](calculus/differentiation.ipynb)  
- [Automatic Differentiation Forward Mode Dual Number](calculus/automatic_differentiation_forward_mode_dual_number.ipynb)



# [Python Tutorials](#)
### [**Python Basics**](#)
[Built-in Types (Lists, Tuples, Sets, Dictionaries) and Functions](python_tutorials/built-in_types_and_functions.ipynb)  
[Mutable and Immutable Types](python_tutorials/mutable_and_immutable_types.ipynb)  
[Numbers Representation in Memory, typing](python_tutorials/numbers_representation_typing.ipynb)  
[Strings and String Formatting](python_tutorials/strings_and_string_formatting.ipynb)  
[Control Flow Structures (if, for, while, match-case)](python_tutorials/control_flow.ipynb)  
[Exception Handling (`try`, `except`, `finally`), Raising Exceptions (`raise`)](python_tutorials/exception_handling.ipynb)  
[Assertions (`assert` statement)](python_tutorials/assertions.ipynb)  
[Doc strings](python_tutorials/docstrings_python.ipynb)

### [**Data Structures**](#)
[Python Data Structures set, dict, heapq, collections.deque](python_tutorials/cpp_data_structure_python.ipynb)  
[Slicing](python_tutorials/slicing.ipynb)  
[ `*args` and `**kwargs`, Packing and Unpacking Arguments](python_tutorials/args_kwargs_packing_and_unpacking.ipynb)  
[Ellipsis (`...`, three dots)](python_tutorials/ellipsis_three_dots.ipynb)  
### [**Functions and Functional Programming**](python_tutorials/)
[Functions, Call by value/ ref](python_tutorials/functions.ipynb)  
[`lambda` Functions (Anonymous functions)](python_tutorials/lambda.ipynb)  
[`yield` and Generators](python_tutorials/generators_yield.ipynb)  
[Decorators (`@decorator_name`)](python_tutorials/decorator.ipynb)  
[`functools` (e.g., `lru_cache`, `partial`)](#)  

### [**Object-Oriented Programming (OOP)**](#)
[Classes and Objects](python_tutorials/)  
[Attributes and Properties](python_tutorials/)  
[Class Methods (`@classmethod`) and Static Methods (`@staticmethod`)](python_tutorials/)  
[Inheritance and Polymorphism](python_tutorials/)  
[Encapsulation and Data Hiding](python_tutorials/)  
[Magic Methods (`__str__`, `__repr__`, `__call__`, etc.)](python_tutorials/class_objet_orinted.ipynb#Class-magic-methods)  

### [**Modules, Packages, and Code Organization**](#)
[Creating and Importing Modules](python_tutorials/)  
[Python Packages and `__init__.py`](python_tutorials/)  
[`__main__` and Executable Scripts](python_tutorials/)  
[Logging (`logging` module)](python_tutorials/logging.ipynb)  

### [**File Handling and Serialization**](#)
[File IO (`open`, `read`, `write`), `with` Statement, Context Managers (`contextlib`)](python_tutorials/file_IO_with_statement_contextlib.ipynb)  
[Reading/ executing files, absolute/ relative path](python_tutorials/reading_executing_files_absolute_relative_path.ipynb)  
[JSON](python_tutorials/json.ipynb)  
[XML](python_tutorials/)  
[YAML](python_tutorials/yaml.ipynb)  
[Pickle](python_tutorials/pickle.ipynb)  
  

### [**Standard Library and Useful Modules**](#)
[Date and Time (`datetime`, `time`)](python_tutorials/datetime_time.ipynb)  
[Regular Expressions (`re`)](python_tutorials/)  
[Command Line Arguments and Flags (`sys.argv`, `argparse`)](python_tutorials/argparse_command_line_arg.ipynb)  
[`tqdm` (Progress Bar)](python_tutorials/progress_bar_tqdm.ipynb)  
[`collections` (`Counter`, `defaultdict`, `namedtuple`)](python_tutorials/)  

### [**Networking and Web Development**](#)
[HTTP Requests (`urllib`, `requests`)](python_tutorials/)  
[Webhooks and APIs](python_tutorials/)  
[Web Scraping (`BeautifulSoup`, `Scrapy`)](python_tutorials/)  
[FastAPI or Flask Basics](python_tutorials/)  

### [**Data Science and Visualization**](#)
[NumPy](python_tutorials/numpy_tutorials.ipynb)  
[Pandas](python_tutorials/pandas.ipynb)  
[Data Visualization (`matplotlib`, `seaborn`, `plotly`)](python_tutorials/matplotlib.ipynb)  
[Graph Processing (`networkx`)](python_tutorials/)  

### [**Testing and Code Quality**](#)
[Unit Testing (`unittest`, `pytest`)](python_tutorials/)  
[Linting and Formatting (`pylint`, `black`, `isort`)](python_tutorials/)  
[Static Code Analysis (`mypy`, `pyflakes`, `pychecker`)](python_tutorials/)  
[PEP8 and Google Python Style Guide](python_tutorials/)  

### [**Advanced Python Topics**](#)
[Concurrency and Parallelism (`threading`, `multiprocessing`, `asyncio`)](python_tutorials/)  
[Metaprogramming (Metaclasses, `type`, `exec`, `eval`)](python_tutorials/)  
[Memory Management and Garbage Collection](python_tutorials/)  
[Cython for Performance Optimization](python_tutorials/)  
[Syntactic sugar](python_tutorials/syntactic_sugar.ipynb)  
[Dataclasses](python_tutorials/dataclasses.ipynb)  
[Context Manager](python_tutorials/context_manager.ipynb)  

### [**Miscellaneous and Tips**](#)
[Python Tips and Tricks](python_tutorials/tips_and_tricks.ipynb)  
[Code Visualization Tools](#)  
[Writing Efficient and Pythonic Code](python_tutorials/writing_efficient_and_pythonic_code.ipynb)  
[Data Structure](data_structure)  
[Jupyter Notebook/ Sympy](Jupyter_Tutorial)  
[Conda and pip](docs/conda_pip.md)  
[GUI with Python QT5](PyQT5)  

---




