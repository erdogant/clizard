[![Python](https://img.shields.io/pypi/pyversions/clizard)](https://img.shields.io/pypi/pyversions/clizard)
[![Pypi](https://img.shields.io/pypi/v/clizard)](https://pypi.org/project/clizard/)
[![Docs](https://img.shields.io/badge/Sphinx-Docs-Green)](https://erdogant.github.io/clizard/)
[![LOC](https://sloc.xyz/github/erdogant/clizard/?category=code)](https://github.com/erdogant/clizard/)
[![Downloads](https://static.pepy.tech/personalized-badge/clizard?period=month&units=international_system&left_color=grey&right_color=brightgreen&left_text=PyPI%20downloads/month)](https://pepy.tech/project/clizard)
[![Downloads](https://static.pepy.tech/personalized-badge/clizard?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/clizard)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/clizard/blob/master/LICENSE)
[![Forks](https://img.shields.io/github/forks/erdogant/clizard.svg)](https://github.com/erdogant/clizard/network)
[![Issues](https://img.shields.io/github/issues/erdogant/clizard.svg)](https://github.com/erdogant/clizard/issues)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![DOI](https://zenodo.org/badge/231843440.svg)](https://zenodo.org/badge/latestdoi/231843440)
[![Medium](https://img.shields.io/badge/Medium-Blog-black)](https://erdogant.github.io/clizard/pages/html/Documentation.html#medium-blog)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://erdogant.github.io/clizard/pages/html/Documentation.html#colab-notebook)
[![Donate](https://img.shields.io/badge/Support%20this%20project-grey.svg?logo=github%20sponsors)](https://erdogant.github.io/clizard/pages/html/Documentation.html#)

<div>
<a href="https://erdogant.github.io/clizard/">
  <img src="https://raw.githubusercontent.com/erdogant/clizard/master/docs/figs/logo.png"
       width="250"
       align="left" />
</a>
clizard is a Python package for probability density fitting of univariate distributions for random variables.
The clizard library can determine the best fit for over 90 theoretical distributions. The goodness-of-fit test is used to score for the best fit and after finding the best-fitted theoretical distribution, the loc, scale, and arg parameters are returned.
It can be used for parametric, non-parametric, and discrete distributions. ⭐️Star it if you like it⭐️
</div>

---

### Key Features

| Feature | Description |
|--------|-------------|
| [**Parametric Fitting**](https://erdogant.github.io/clizard/pages/html/Parametric.html) | Fit distributions on empirical data X. |
| [**Non-Parametric Fitting**](https://erdogant.github.io/clizard/pages/html/Quantile.html) | Fit distributions on empirical data X using non-parametric approaches (quantile, percentiles). |
| [**Discrete Fitting**](https://erdogant.github.io/clizard/pages/html/Discrete.html) | Fit distributions on empirical data X using binomial distribution. |
| [**Predict**](https://erdogant.github.io/clizard/pages/html/Functions.html#module-clizard.clizard.clizard.predict) | Compute probabilities for response variables y. |
| [**Synthetic Data**](https://erdogant.github.io/clizard/pages/html/Generate.html) |  Generate synthetic data. |
| [**Plots**](https://erdogant.github.io/clizard/pages/html/Plots.html) | Varoius plotting functionalities. |

---

### Resources and Links
- **Example Notebooks:** [Examples](https://erdogant.github.io/clizard/pages/html/Documentation.html)
- **Blog Posts:** [Medium](https://erdogant.github.io/clizard/pages/html/Documentation.html#medium-blog)
- **Documentation:** [Website](https://erdogant.github.io/clizard)
- **Bug Reports and Feature Requests:** [GitHub Issues](https://github.com/erdogant/clizard/issues)

---

### Background

* For the parametric approach, The clizard library can determine the best fit across 89 theoretical distributions.
  To score the fit, one of the scoring statistics for the good-of-fitness test can be used used, such as RSS/SSE, Wasserstein,
  Kolmogorov-Smirnov (KS), or Energy. After finding the best-fitted theoretical distribution, the loc, scale,
  and arg parameters are returned, such as mean and standard deviation for normal distribution.

* For the non-parametric approach, the clizard library contains two methods, the quantile and percentile method.
  Both methods assume that the data does not follow a specific probability distribution. In the case of the quantile method,
  the quantiles of the data are modeled whereas for the percentile method, the percentiles are modeled.

---

### Installation

##### Install clizard from PyPI
```bash
pip install clizard
```

##### Install from Github source
```bash
pip install git+https://github.com/erdogant/clizard
```

##### Imort Library
```python
import clizard
print(clizard.__version__)

# Import library
from clizard import clizard
```

<hr>

### Examples

##### [Example: Quick start to find best fit for your input data](https://erdogant.github.io/clizard/pages/html/Examples.html#)

```python

# [clizard] >INFO> fit
# [clizard] >INFO> transform
# [clizard] >INFO> [norm      ] [0.00 sec] [RSS: 0.00108326] [loc=-0.048 scale=1.997]
# [clizard] >INFO> [expon     ] [0.00 sec] [RSS: 0.404237] [loc=-6.897 scale=6.849]
# [clizard] >INFO> [pareto    ] [0.00 sec] [RSS: 0.404237] [loc=-536870918.897 scale=536870912.000]
# [clizard] >INFO> [dweibull  ] [0.06 sec] [RSS: 0.0115552] [loc=-0.031 scale=1.722]
# [clizard] >INFO> [t         ] [0.59 sec] [RSS: 0.00108349] [loc=-0.048 scale=1.997]
# [clizard] >INFO> [genextreme] [0.17 sec] [RSS: 0.00300806] [loc=-0.806 scale=1.979]
# [clizard] >INFO> [gamma     ] [0.05 sec] [RSS: 0.00108459] [loc=-1862.903 scale=0.002]
# [clizard] >INFO> [lognorm   ] [0.32 sec] [RSS: 0.00121597] [loc=-110.597 scale=110.530]
# [clizard] >INFO> [beta      ] [0.10 sec] [RSS: 0.00105629] [loc=-16.364 scale=32.869]
# [clizard] >INFO> [uniform   ] [0.00 sec] [RSS: 0.287339] [loc=-6.897 scale=14.437]
# [clizard] >INFO> [loggamma  ] [0.12 sec] [RSS: 0.00109042] [loc=-370.746 scale=55.722]
# [clizard] >INFO> Compute confidence intervals [parametric]
# [clizard] >INFO> Compute significance for 9 samples.
# [clizard] >INFO> Multiple test correction method applied: [fdr_bh].
# [clizard] >INFO> Create PDF plot for the parametric method.
# [clizard] >INFO> Mark 5 significant regions
# [clizard] >INFO> Estimated distribution: beta [loc:-16.364265, scale:32.868811]
```

<p align="left">
  <a href="https://erdogant.github.io/clizard/pages/html/Examples.html#make-predictions">
  <img src="https://github.com/erdogant/clizard/blob/master/docs/figs/example_figP4c.png" width="450" />
  </a>
</p>


#

##### [Example: Plot summary of the tested distributions](https://erdogant.github.io/clizard/pages/html/Examples.html#plot-rss)

After we have a fitted model, we can make some predictions using the theoretical distributions.
After making some predictions, we can plot again but now the predictions are automatically included.

<p align="left">
  <a href="https://erdogant.github.io/clizard/pages/html/Examples.html#plot-rss">
  <img src="https://github.com/erdogant/clizard/blob/master/docs/figs/fig1_summary.png" width="450" />
  </a>
</p>

#

<hr>

### Contributors
Setting up and maintaining bnlearn has been possible thanks to users and contributors. Thanks to:

<p align="left">
  <a href="https://github.com/erdogant/clizard/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=erdogant/clizard" />
  </a>
</p>

### Maintainer
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)
* Contributions are welcome.
* Yes! This library is entirely **free** but it runs on coffee! :) Feel free to support with a <a href="https://erdogant.github.io/donate/?currency=USD&amount=5">Coffee</a>.

[![Buy me a coffee](https://img.buymeacoffee.com/button-api/?text=Buy+me+a+coffee&emoji=&slug=erdogant&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/erdogant)
