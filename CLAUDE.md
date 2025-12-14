# CLAUDE.md - AI Assistant Guide for EE-presentation

## Repository Overview

This repository contains research materials for studying **Exploitation-Exploration (E/E) dynamics** in semantic verbal fluency tasks. The project analyzes how humans navigate semantic memory during verbal fluency tests (e.g., "name all animals you can think of in 60 seconds").

**Repository**: `dlchihade/EE-presentation`

## Codebase Structure

```
EE-presentation/
├── CLAUDE.md                              # This file
├── README.md                              # Basic repository description
├── index.html                             # Main semantic verbal fluency visualization
├── MEDIATION_WITH_NEW_SCORES_10_16.ipynb  # Latest mediation analysis (primary notebook)
├── MEDIATION_WITH_NEW_SCORES_08_01.ipynb  # Earlier version of analysis
├── mediation_changes                      # Python code export from notebook
├── semantic-navigation-fixed.html         # MVT vs Softmax interactive visualization
├── semantic-navigation-fixed (1-3).html   # Variant versions
├── semantic-visualization.html            # Simple semantic space visualization
└── S1364661314002332.html                 # Reference research paper (Hills et al.)
```

## Key Concepts

### Research Domain
- **Semantic Verbal Fluency**: Cognitive task where participants name items from a category
- **Exploitation**: Continuing to search within a semantic cluster (e.g., farm animals)
- **Exploration**: Switching to a new semantic cluster (e.g., from farm animals to marine life)
- **E/E Tradeoff**: Balance between staying in a productive patch vs. exploring new areas

### Theoretical Models
1. **BEAGLE Model**: Word vector embeddings for semantic similarity
2. **Marginal Value Theorem (MVT)**: Optimal foraging theory applied to memory search
3. **Softmax Decision Making**: Probabilistic model for word selection based on similarity
4. **Mediation Analysis**: Statistical method to understand causal pathways

## Technology Stack

### Python Data Analysis (Jupyter Notebooks)
```python
# Core dependencies
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.cluster import AgglomerativeClustering
import spacy  # Word vectors (en_core_web_md)

# Additional packages
# pip install git+https://github.com/AusterweilLab/snafu-py
# pip install wordfreq
```

### JavaScript Visualizations (HTML files)
- **D3.js v7.8.5**: Interactive data visualization
- **Math.js v11.8.0**: Mathematical operations

## Development Workflows

### Running Jupyter Notebooks
1. Notebooks are designed for **Google Colab** execution
2. Open via Colab badge in notebook header
3. Run cells sequentially - setup installs dependencies automatically:
   ```bash
   !pip install git+https://github.com/AusterweilLab/snafu-py
   !python -m spacy download en_core_web_md
   !pip install wordfreq
   ```

### Viewing HTML Visualizations
- `index.html` - Open directly in browser for verbal fluency visualization
- Visualizations use CDN-loaded D3.js/Math.js (no build step required)
- Features interactive participant selection and multiple chart types

### Key Notebook Sections (MEDIATION_WITH_NEW_SCORES_10_16.ipynb)
1. **Setup environment** - Install dependencies, load spaCy model
2. **Load Data** - Import participant verbal fluency data
3. **Word Frequency Analysis** - Using wordfreq library for top 50k English words
4. **Verbal fluency basic analysis** - Identify exploitation/exploration phases
5. **t-SNE Visualization** - Project word vectors to 2D
6. **Clustering Analysis** - Agglomerative clustering of word responses
7. **Model Implementation** - Traditional, Softmax, and MVT models
8. **Mediation Analysis** - Statistical mediation for causal inference

## Code Conventions

### Python (Notebooks)
- Use `ggplot` style for matplotlib: `plt.style.use('ggplot')`
- Set seaborn context for presentations: `sns.set_context("talk")`
- Standard figure size: `(12, 8)`
- SVG fonts: `plt.rcParams['svg.fonttype'] = 'none'`

### JavaScript (HTML Visualizations)
- D3.js for all data visualization
- Color scheme:
  - Exploitation: `#2ecc71` (green)
  - Exploration: `#e74c3c` (red)
  - Links/lines: `#3498db` (blue), `#95a5a6` (gray)
- Responsive design with CSS Grid
- Tooltip pattern for interactive elements

## Data Structures

### Participant Data (JavaScript)
```javascript
{
    id: "PD00020",
    items: ["lion", "tiger", "sheep", ...],  // Word sequence
    similarities: [0.82, 0.43, ...],         // Cosine similarities between consecutive words
    phases: [
        { type: "Exploitation", start: 0, end: 2 },
        { type: "Exploration", start: 2, end: 5 },
        ...
    ],
    metrics: {
        exploitationPercentage: 65.0,
        explorationPercentage: 35.0,
        avgSimilarity: 0.52,
        numPhases: 7,
        eeTradeoff: 2.86,
        noveltyRatio: 0.70
    }
}
```

### Key Metrics
- **Exploitation %**: Percentage of items in exploitation phases
- **Exploration %**: Percentage of items in exploration phases
- **Average Similarity**: Mean cosine similarity between consecutive words
- **Number of Phases**: Count of distinct E/E phases
- **E/E Tradeoff**: Ratio metric for exploitation vs exploration balance
- **Novelty Ratio**: Proportion of unique (non-repeated) items

## Important Notes for AI Assistants

1. **Notebook Execution**: These notebooks require Google Colab or a Python environment with GPU support for efficient spaCy model loading

2. **Data Source**: The `snafu-py` package from AusterweilLab provides verbal fluency analysis tools

3. **File Naming**: Files with spaces (e.g., `semantic-navigation-fixed (1).html`) are variant versions, not primary files

4. **Research Context**: This is academic research on cognitive science - maintain scientific accuracy in any modifications

5. **Visualization Updates**: When modifying HTML visualizations, ensure D3.js compatibility and maintain the color scheme for consistency

## Common Tasks

### Adding a New Participant
1. Add participant object to `participantData` array in `index.html`
2. Include: id, items array, similarities array, phases array, metrics object

### Modifying Visualizations
- Word sequence: `createWordSequenceVisualization()`
- E/E chart: `createExploitationExplorationChart()`
- Similarity graph: `createSimilarityGraph()`
- Softmax/MVT: `createSoftmaxMVTVisualization()`

### Running Analysis
```bash
# For local Python execution
pip install matplotlib seaborn numpy pandas scikit-learn spacy wordfreq
pip install git+https://github.com/AusterweilLab/snafu-py
python -m spacy download en_core_web_md
```

## Git Workflow

- Main development happens in feature branches
- Notebooks are versioned with date suffixes (e.g., `_08_01`, `_10_16`)
- HTML visualizations may have numbered variants during iteration
