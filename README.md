# Question-Matching-on-Qianyan
- 2024.10.1 - 10.18: 
Machine Learning Practice (2024 Fall), for Baidu"Qianyan Dataset: Question Matching Robustness" Competition.  
- 2024.10.30:
NLP (2024 Fall) Course Lab, adding some new exploration of this project (including dataset, model, training, etc).

## Get Started
### Repo Stucture
```
Github Repo Root
 |---- corrector  # Contains code for text correction
 |---- data      # Contains datasets
 |---- result    # Contains results and logs
 |---- train     # Contains training scripts and configurations
 |---- misc     # New things from NLP course lab

```
## Introduction
This is the **demo implementation (which only includes the core code but not an excutable version, since the competition hasn't ended)** for the technical report "Qianyan Dataset: Technical Report on the Question Matching Robustness Competition", which ranked 6th (until 2024.10.18) in the "Baidu Qianyan: Question Matching Robustness Competition". This is also the assignment 1 of *Machine Learning Practice (2024 fall)*.

<img width="694" alt="{D58410CA-FCF3-4C13-94F6-760F9490A3AD}" src="https://github.com/user-attachments/assets/82e410c4-06a3-4c04-87ed-14318705abbd">

## Performance
Untill 2024.10.18 0:00, ranked 6th in the leader board.
| Rank | score  | OPPO   | DuQM_pos | DuQM_named_entity | DuQM_synonym | DuQM_antonym | DuQM_negation | DuQM_temporal | DuQM_symmetry | DuQM_asymmetry | DuQM_neg_asymmetry | DuQM_voice | DuQM_misspelling | DuQM_discourse_particle(simple) | DuQM_discourse_particle(complex) |
|------|--------|--------|----------|-------------------|--------------|--------------|---------------|---------------|---------------|----------------|--------------------|------------|------------------|---------------------------------|----------------------------------|
| 1    | 90.845 | 88.895 | 76.943   | 95.441            | 89.889       | 99.672       | 95.726        | 84.188        | 94.747        | 83.3           | 87.755             | 85.496     | 97.65            | 96.714                          | 95.42                            |
| 2    | 90.331 | 89.155 | 73.568   | 94.779            | 88.376       | 99.344       | 94.302        | 79.487        | 94.371        | 82.093         | 91.837             | 87.023     | 98.932           | 96.714                          | 94.656                           |
| 3    | 90.31  | 89.48  | 77.966   | 97.206            | 90.287       | 99.672       | 96.011        | 87.607        | 92.308        | 82.294         | 65.306             | 90.84      | 99.359           | 99.061                          | 96.947                           |
| 4    | 90.208 | 89.23  | 78.315   | 96.912            | 89.729       | 99.344       | 94.587        | 86.752        | 93.058        | 82.495         | 65.306             | 92.366     | 99.573           | 99.061                          | 96.183                           |
| 5    | 90.132 | 89.09  | 79.752   | 96.471            | 86.943       | 98.361       | 94.587        | 94.444        | 92.308        | 84.708         | 67.347             | 85.496     | 98.504           | 97.653                          | 96.183                           |
| **6**    | **89.901** | **89.07**  | **80.318**   | **96.912**            | **87.978**       | **99.672**       | **93.732**        | **91.453**        | **91.932**        | **86.72**          | **65.306**             | **81.679**     | **99.359**           | **99.061**                          | **95.42**                            |

## Reference
[Qianyan: Question Matching Robustness Competiton](https://aistudio.baidu.com/competition/detail/130/0/introduction) 
[Competition Baseline](https://github.com/baidu/DuReader/tree/master/DuQM)  
[2021 CCF BDCI Thousand Words - Problem Matching Robustness Review - 12th Place Scheme](https://aistudio.baidu.com/projectdetail/2384565?searchKeyword=%E5%8D%83%E8%A8%80%E9%97%AE%E9%A2%98%E5%8C%B9%E9%85%8D&searchTab=ALL)  
[2021 CCF BDCI Thousand Words - Problem Matching Robustness Review - 5th Place Scheme](https://aistudio.baidu.com/projectdetail/2487202?searchKeyword=%E5%8D%83%E8%A8%80%E9%97%AE%E9%A2%98%E5%8C%B9%E9%85%8D&searchTab=ALL)  
[2021 CCF BDCI Thousand Words - Problem Matching Robustness Review - 1st Place Scheme](https://discussion.datafountain.cn/articles/detail/3813)

## Acknowledgements
We would like to thank the organizers of the Qianyan Question Matching Robustness Competition for providing the dataset and the opportunity to participate in this competition. Also, authors of the blogs in the *Reference* helped me so much (*part of the code in this repo is developed based on their code or idea*). Thanks a lot!

## License
This project is licensed under the MIT License. 


