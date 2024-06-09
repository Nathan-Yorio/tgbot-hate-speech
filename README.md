# hate-speech-detection-method-for-telegram
Code portion of masters thesis on a machine-learning focused content detection method for Telegram

# Dataset Citations

Dataset: The Pushshift Telegram Dataset  
Author: Baumgartner, Jason; Zannettou, Savvas; Squire, Megan; Blackburn, Jeremy   
Source: Zenodo  
License:  CC BY 4.0  
Date of Publication: Jan 14, 2020  
Version: v1  
Date Accessed: 2024-01-07  
Identifier: 10.5281/zenodo.3607496 @ https://zenodo.org/doi/10.5281/zenodo.3607496  

---

Dataset: Labeled Hate Speech Detection Dataset  
Author: Cooke, Shane (2022)  
Source: Figshare  
License: CC BY 4.0  
Date of Publication: 2022-04-30, 03:25  
Version: v1  
Date Accessed: 2024-01-14  
Identifier: https://doi.org/10.6084/m9.figshare.19686954.v1  

---

Dataset: A Benchmark Dataset for Learning to Intervene in Online Hate Speech  
Author: Qian et al.  
Source: Github, Arxiv  
License: CC BY 4.0  
Date of Publication: Tue, 10 Sep 2019 03:00:58 UTC  
Version: v1  
Date Accessed: 2024-04  
Identifier: https://doi.org/10.48550/arXiv.1909.04251 [Github link](https://github.com/jing-qian/A-Benchmark-Dataset-for-Learning-to-Intervene-in-Online-Hate-Speech)  

---  

Dataset: A Curated Hate Speech Dataset  
Author: Mody et al.  
Source: Mendeley Data  
License: CC BY 4.0  
Date of Publication: 3 Oct 2022  
Version: v1  
Date Accessed: 2024-01 - 2024-04  
Identifier: 10.17632/9sxpkmm8xn.1, https://data.mendeley.com/datasets/9sxpkmm8xn/1, [Article link](https://www.sciencedirect.com/science/article/pii/S2352340922010356)  

---

# Machine Learning Model Citations  

Model: facebook/roberta-hate-speech-dynabench-r4-target  
Author: Vidgen et al.  
Source: [Huggingface](https://huggingface.co/facebook/roberta-hate-speech-dynabench-r4-target)  
Date of Publication: Thu, 31 Dec 2020 17:36:48 UTC  
Version: v1 presumed  
Analysis Software: Python, with PyTorch and Transformers libraries  
Date Accessed: 2024-01 - 2024-04  
Identifier: https://doi.org/10.48550/arXiv.2012.15761  
License: Not including specific license attached on HuggingFace  
Research article simply includes intended use-case and Arxiv citation request if model is used:  
"The approach, dataset and models presented here are intended to support more accurate and robust detection and classification of online hate. We anticipate that the high-quality and fine-grained labels in the dataset will advance research in online hate in other ways, such as enabling multiclass classification of types and targets of online hate." (Vidgen et al., 2020)  

```
@inproceedings{vidgen2021lftw,
  title={Learning from the Worst: Dynamically Generated Datasets to Improve Online Hate Detection},
  author={Bertie Vidgen and Tristan Thrush and Zeerak Waseem and Douwe Kiela},
  booktitle={ACL},
  year={2021}
}
```


---

Model: cardiffnlp/twitter-roberta-base-hate-latest   
Author: Loureiro et al.  
Source: [Huggingface](https://huggingface.co/cardiffnlp/twitter-roberta-base-hate-latest), [v1](https://huggingface.co/cardiffnlp/twitter-roberta-base-2022-154m)  
Date of Publication: Fri, 1 Apr 2022 15:01:53 UTC  
Version: v2  
Analysis Software: Python, with PyTorch and Transformers libraries  
Date Accessed: 2024-01 - 2024-04  
Identifier: https://doi.org/10.48550/arXiv.2202.03829 , https://arxiv.org/pdf/2202.03829  
License: MIT  

```
@inproceedings{antypas-camacho-collados-2023-robust,
    title = "Robust Hate Speech Detection in Social Media: A Cross-Dataset Empirical Evaluation",
    author = "Antypas, Dimosthenis  and
      Camacho-Collados, Jose",
    booktitle = "The 7th Workshop on Online Abuse and Harms (WOAH)",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.woah-1.25",
    pages = "231--242"
}
```

** This one appears to actually be based on two different papers, one for dataset processing and one for model construction  

---

Model: Andrazp/multilingual-hate-speech-robacofi   
Author: Barbieri et al.  
Source: [Huggingface](https://huggingface.co/Andrazp/multilingual-hate-speech-robacofi)  
Date of Publication: Wed, 11 May 2022 08:06:39 UTC  
Version: v2  
Analysis Software: Python, with PyTorch and Transformers libraries  
Date Accessed: 2024-01 - 2024-04  
Identifier: https://doi.org/10.48550/arXiv.2104.12250  
License: MIT  

---  
