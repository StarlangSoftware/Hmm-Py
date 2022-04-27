Hidden Markov Models
============

Video Lectures
============

[<img src="https://github.com/StarlangSoftware/Hmm/blob/master/video1.jpg" width="50%">](https://youtu.be/zHj5mK3jcyk)[<img src="https://github.com/StarlangSoftware/Hmm/blob/master/video2.jpg" width="50%">](https://youtu.be/LM0ld3UKCEs)

For Developers
============

You can also see [Cython](https://github.com/starlangsoftware/Hmm-Cy), [Java](https://github.com/starlangsoftware/Hmm), [C++](https://github.com/starlangsoftware/Hmm-CPP), [Swift](https://github.com/starlangsoftware/Hmm-Swift), [Js](https://github.com/starlangsoftware/Hmm-Js), or [C#](https://github.com/starlangsoftware/Hmm-CS) repository.

## Requirements

* [Python 3.7 or higher](#python)
* [Git](#git)

### Python 

To check if you have a compatible version of Python installed, use the following command:

    python -V
    
You can find the latest version of Python [here](https://www.python.org/downloads/).

### Git

Install the [latest version of Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

## Pip Install

	pip3 install NlpToolkit-Hmm
	
## Download Code

In order to work on code, create a fork from GitHub page. 
Use Git for cloning the code to your local or below line for Ubuntu:

	git clone <your-fork-git-link>

A directory called Hmm will be created. Or you can use below link for exploring the code:

	git clone https://github.com/starlangsoftware/Hmm-Py.git

## Open project with Pycharm IDE

Steps for opening the cloned project:

* Start IDE
* Select **File | Open** from main menu
* Choose `Hmm-PY` file
* Select open as project option
* Couple of seconds, dependencies will be downloaded. 

Detailed Description
============

+ [Hmm](#hmm)

## Hmm

Hmm modelini üretmek için

	Hmm(self, states: set, observations: list, emittedSymbols: list)


Viterbi algoritması ile en olası State listesini elde etmek için

	viterbi(self, s: list) -> list
