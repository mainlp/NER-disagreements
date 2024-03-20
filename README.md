# Different Tastes of Entities: Investigating Human Label Variation in Named Entity Annotations


- This paper studies disagreements in expert-annotated named entity datasets for three languages: English, Danish, and Bavarian. 
- We show that text ambiguity and artificial guideline changes are dominant factors for diverse annotations among high-quality revisions. 
- We survey student annotations on a subset of difficult entities and substantiate the feasibility and necessity of manifold annotations for understanding named entity ambiguities from a distributional perspective.


<p align="center">
<img src="https://github.com/mainlp/NER-disagreements/blob/main/figs/Table1.png" alt="drawing" width="500"/>
</p>


## Some observations in our paper 

### Entity-level Disagreements

- Tag disagreements contribute to most cases among repeatedly developed English corpora;
- Danish and Bavarian contain more Missing disagreements;
- In sum, combining Tag and Missing accounts for 85%+ of disagreements in all comparisons across three languages;
- In other words, entity tagging remains a bigger issue compared to span selection.

<p align="center">
<img src="https://github.com/mainlp/NER-disagreements/blob/main/figs/Figure1.png" alt="drawing" width="600"/>
</p>


- LOC-ORG, O-MISC and ORG-MISC are the most frequently (70%+) disagreed label pairs in English comparisons;
- Most (80%+) of Danish label disagreements concern MISC;
- O-related (i.e., Missing) disagreements donate the majority (70%+) to Bavarian.

<p align="center">
<img src="https://github.com/mainlp/NER-disagreements/blob/main/figs/Figure2.png" alt="drawing" width="600"/>
</p>

### Sources of Disagreements

- Most (80.0%) of disagreements stem from differences in guideline update;
- Ambiguous cases in Danish are either guideline updates (52.5%) or annotator errors (41.5%);
- Annotator error (67.2%) is the highest for Bavarian though some are acceptable under certain English guidelines.


<p align="center">
<img src="https://github.com/mainlp/NER-disagreements/blob/main/figs/Table2.png" alt="drawing" width="600"/>
</p>



## How to use this repository?
- **presentations**: poster and slides of this paper
- **datasets**: token-aligned corpora from three languages: English (**en**), Danish (**da**), and Bavarian German (**bar**).
    - **en-conll2003-original** [Tjong Kim Sang and De Meulder 2003](https://aclanthology.org/W03-0419/)
    - **en-conll2003-conllpp** [Wang et al. 2019](https://aclanthology.org/D19-1519/)
    - **en-conll2003-reiss** [Reiss et al. 2020](https://aclanthology.org/2020.conll-1.16/)
    - **en-conll2003-clean** [Rücker and Akbik 2023](https://aclanthology.org/2023.emnlp-main.533/)
   - **da-ddt-plank** [Plank et al. 2020](https://aclanthology.org/2020.coling-main.583/)
   - **da-ddt-hvingelby** [Hvingelby et al. 2020](https://aclanthology.org/2020.lrec-1.565/) 
    - **bar-barner** [Peng et al. 2024](https://aclanthology.org/2024.unimplicit-1.7/) 
- **disagreement-annotations**: qualitative disagreement analyses between annotation versions:
    - English **clean-vs-original**
    - Danish **plank-vs-hvingelby**
    - Bavarian between two annotators
- **survey-results**: student surveyed annotations (18 BSc and 9 MSc) on difficult English and Bavarian entities
- **utils**: scripts to generate quantitative comparison figures in **figs**
- **figs**: Figures and Tables used in the paper


    




### Paper
https://aclanthology.org/2024.unimplicit-1.7/


#### Reference

    Siyao Peng, Zihang Sun, Sebastian Loftus, and Barbara Plank. 2024. Different Tastes of Entities: Investigating Human Label Variation in Named Entity Annotations. In Proceedings of the Third Workshop on Understanding Implicit and Underspecified Language, pages 73–81, Malta. Association for Computational Linguistics.


#### [ACL Anthology](https://aclanthology.org/2024.unimplicit-1.7/)

    @inproceedings{peng-etal-2024-different,
        title = "Different Tastes of Entities: Investigating Human Label Variation in Named Entity Annotations",
        author = "Peng, Siyao  and
          Sun, Zihang  and
          Loftus, Sebastian  and
          Plank, Barbara",
        editor = "Pyatkin, Valentina  and
          Fried, Daniel  and
          Stengel-Eskin, Elias  and
          Stengel-Eskin, Elias  and
          Liu, Alisa  and
          Pezzelle, Sandro",
        booktitle = "Proceedings of the Third Workshop on Understanding Implicit and Underspecified Language",
        month = mar,
        year = "2024",
        address = "Malta",
        publisher = "Association for Computational Linguistics",
        url = "https://aclanthology.org/2024.unimplicit-1.7",
        pages = "73--81",
    }

### Poster
https://github.com/mainlp/NER-disagreements/presentations/Unimplicit_2024_NER_Poster.pdf


### Slides
https://github.com/mainlp/NER-disagreements/presentations/Unimplicit_2024_NER_Slides.pdf



## Acknowledgement
- This project is supported by ERC Consolidator Grant DIALECT 101043235.