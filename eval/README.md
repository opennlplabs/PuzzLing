# Evaluation
This page is about sentences similarity evaluation result on low-resource languages and english regarding different encoding models and translation API.

## Method

The method we used here for evaluation is the following: Given $n$ english and low-reousrce language sentences pairs of ${{x_1,y_1}, {x_2,y_2},\dots, {x_n,y_n}}$, we use a pre-trained model $f$ to map each sentence into a representation with dimension size $d$. Each sentence pair has the same semantic meaning, but displayed in different languages. After processed by model $f$, all english sentences and low-resource sentences are mapped into two corresponding matrixs $\mathbf{X}$ and $\mathbf{Y}$, all with size $m\times d$. The row vectors in $\mathbf{X}$ and $\mathbf{Y}$ with the same row index is a sentence pair.

Then, we calculate cosine similarity through spearman correlation which takes the rank rather than actual values to measure similarity. In particularly, given paired encoded representations $\mathbf{x}$ and $\mathbf{y}$ with dimension $d$, we rank vector value with rank index $D_i\in {0,1,\dots,d}$ and  replace real value $\mathbf{x}_i$ and $\mathbf{y}_i$ by $D_i$. Then using the following formula to compute correlation

$$
  \uprho = 1 - \frac{3\sum{(D_{\mathbf{x}_i} - D_{\mathbf{y}_i})^2}}{d(d^2-1)}
$$

We return $\uprho$ as the correlation scores. $\uprho$ is in the range $[0,1]$, where $0$ denotes opposite, $1$ means identical and $0.5$ implys unrelevant.


