# [Generative FrameNet: Scalable and Adaptive Frames for Interpretable Knowledge Storage and Retrieval for LLMs Powered by LLMs](https://github.com/H-TayyarMadabushi/Generative-FrameNet/blob/main/Paper/Generative-FrameNet-COLING_2025.pdf)
[Harish Tayyar Madabushi](https://aclanthology.org/people/h/harish-tayyar-madabushi/), Taylor Pellegrin, [Claire Bonial](https://aclanthology.org/people/c/claire-bonial/), 

This repository contains the program code and prompts associated with the paper [Generative FrameNet: Scalable and Adaptive Frames for Interpretable Knowledge Storage and Retrieval for LLMs Powered by LLMs](https://github.com/H-TayyarMadabushi/Generative-FrameNet/blob/main/Paper/Generative-FrameNet-COLING_2025.pdf) that was presented at The Second COLING Workshop on Bridging Neurons and Symbols for NLP and Knowledge Graph Reasoning (BNS-KGR), at COLING 2025. 

Read the [Paper Here](https://github.com/H-TayyarMadabushi/Generative-FrameNet/blob/main/Paper/Generative-FrameNet-COLING_2025.pdf)

1. The program code for the automatic generation of frames and frame relations is availble [here](https://github.com/H-TayyarMadabushi/Generative-FrameNet/blob/main/src/frameCreator.py)
2. The prompts used in this study are available [here](https://github.com/H-TayyarMadabushi/Generative-FrameNet/blob/main/src/TestTemplates.py). This includes the exploratory prompts. The final prompts used are part of *Template 6*
3. Running these scripts requires an OpenAI API key, which must be stored in a file called .key

## Abstract
Frame semantics provides an explanation for how we make use of conceptual *frames*, which encapsulate background knowledge and associations, to more completely understand the meanings of words within a context. Unfortunately, FrameNet, the only widely available implementation of frame semantics, is limited in both scale and coverage. Therefore, we introduce a novel mechanism for generating task-specific frames using large language models (LLMs), which we call *Generative FrameNet*. We demonstrate its effectiveness on a task that is highly relevant in the current landscape of LLMs: the interpretable storage and retrieval of factual information. Specifically, Generative Frames enable the extension of Retrieval-Augmented Generation (RAG), providing an interpretable framework for reducing inaccuracies in LLMs. We conduct experiments to demonstrate the effectiveness of this method both in terms of retrieval effectiveness as well as the relevance of the automatically generated frames and frame relations. Expert analysis shows that Generative Frames capture a more suitable level of semantic specificity than the frames from FrameNet. Thus, Generative Frames capture a notion of frame semantics that is closer to Fillmore's originally intended definition, and offer potential for providing data-driven insights into Frame Semantics theory. Our results also show that this novel mechanism of Frame Semantic-based interpretable retrieval improves RAG for question answering with LLMs---outperforming a GPT-4 based baseline by up to 8 points. We provide open access to our data, including prompts and Generative FrameNet.

## Citation
If you find yourself building on this work, do consider citing us: 

```
@inproceedings{tayyarmadabushi-etal-2025-generative,
    title = "Generative FrameNet: Scalable and Adaptive Frames for Interpretable Knowledge Storage and Retrieval for LLMs Powered by LLMs",
    author = "Harish Tayyar Madabushi and
      Taylor Pellegrin and
      Claire Bonial",
    editor = "Dong, Tiansi  and
      Hinrichs, Erhard  and
      Han, Zhen  and
      Liu, Kang  and
      Song, Yangqiu  and
      Cao, Yixin  and
      Hempelmann, Christian F.  and
      Sifa, Rafet",
    booktitle = "Proceedings of the Workshop: Bridging Neurons and Symbols for Natural Language Processing and Knowledge Graphs Reasoning (NeusymBridge) @ LREC-COLING-2025",
    month = Jan,
    year = "2025",
    address = "Abu Dhabi, UAE",
    publisher = "ELRA and ICCL",
}```
