# Evaluation
This page is about sentences similarity evaluation result on low-resource languages and english regarding different encoding models and translation API.

## Method

The method we used here for evaluation is the following: Given $n$ english and low-reousrce language sentences pairs of ${{x_1,y_1}, {x_2,y_2},\dots, {x_n,y_n}}$, we use a pre-trained model $f$ to map each sentence into a representation with dimension size $d$. Each sentence pair has the same semantic meaning, but displayed in different languages. After processed by model $f$, all english sentences and low-resource sentences are mapped into two corresponding matrixs $\mathbf{X}$ and $\mathbf{Y}$, all with size $m\times d$. The row vectors in $\mathbf{X}$ and $\mathbf{Y}$ with the same row index is a sentence pair.

Then, we calculate cosine similarity $\textbf{H} = \text{sim}(\mathbf{X},\mathbf{Y})$ among $\mathbf{X}$ and $\mathbf{Y}$ through formula 

$$
  h_{ij} = \text{sim}(\mathbf{x}_i,\mathbf{y}_j) = \frac{\mathbf{x}_i\mathbf{y}{_j^\top}}{\parallel\mathbf{x}_i\parallel \cdot \parallel\mathbf{y}_j\parallel}
$$

