# Evaluation
This page concerns sentence similarity evaluation results in low-resource languages and English regarding different encoding models and translation API.

## Method

The method we used here for evaluation is the following: Given $n$ English and low-resource language sentences pairs of $\[\[x_1,y_1\], \[x_2,y_2\],\dots, \[x_n,y_n\]\]$, we use a pre-trained model $f$ to map each sentence into a representation with dimension size $d$. Each sentence pair has the same semantic meaning but is displayed in different languages. After processing by model $f$, all English sentences and low-resource sentences are mapped into two corresponding matrices $\mathbf{X}$ and $\mathbf{Y}$, all with size $m\times d$. The row vectors in $\mathbf{X}$ and $\mathbf{Y}$ with the same row index is a sentence pair.

Then, we calculate cosine similarity through spearman correlation which takes the relevant rank distance rather than actual values similarity to measure similarity. In particularly, given one paired high-dimensional representations $\mathbf{x}$ and $\mathbf{y}$ with dimension $d$, we rank vector value with rank index $D_i\in \[0,1,\dots,d\]$ and  replace real value $\mathbf{x}_i$ and $\mathbf{y}_i$ by $D_i$. Then using the following formula to compute correlations

$$
  \uprho = 1 - \frac{3\sum{(D_{\mathbf{x}_i} - D_{\mathbf{y}_i})^2}}{d(d^2-1)}
$$

We return $\uprho$ as the correlation scores. $\uprho$ is in the range $[0,1]$, where $0$ denotes opposite, $1$ means identical, and $0.5$ implies unrelated.


