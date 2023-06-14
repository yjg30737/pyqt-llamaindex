# pyqt-llamaindex
Example of use llama-index in Python desktop application

With combination of llama-index and openai, you can pretty much make your personal chatbot, by your input.

Currently this package is only supporting txt files(i don't know about other file type such as .doc works) in the directory. If you want to feed the chatbot to respond what you want to get answer, put txt file inside the "example" directory in this repo and read the instruction below("How to Run" section) to use it. Of course, you can use your own directory other than the directory i mentioned earlier. <b>Remember, the directory has to contain at least one text file</b>.

By default, example folder contains yjg30737.txt and pyqt-openai.txt. It was used for testing so feel free to remove it if you want.

## Requirements
* PyQt5 >= 5.14
* openai
* llama-index

## How to Run
1. git clone ~
2. cd pyqt-llamaindex
3. pip install -r requirements.txt
4. cd pyqt_llamaindex
5. python main.py
6. write your openai api key to the top of the screen and clicking "use" button
7. pressing "set directory" button to import directory which contains text files
8. chat with your personal chatbot

## Preview

![image](https://github.com/yjg30737/pyqt-llamaindex/assets/55078043/67e17c9b-9a49-4f3b-8c3d-05d7c85941fb)

## See Also
* <a href="https://github.com/yjg30737/pyqt-openai">pyqt-openai</a>
