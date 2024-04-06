# 🤖 AFK LLAMA
This repository contains a chatbot created utilising [Textual](https://github.com/textualize/textual/), 
as front-end, and META open source Large Language Model [Llama](https://github.com/meta-llama/llama).

## ⚒️ How to install
To run this code, several steps are necessary.
Your environment should have. In paranthesis I report the versions I used to run my code. 
Other versions may work, but I don't ensure a smooth runtime, should you use different versions.

### 🧰 My Environment

* Linux Environment
* Python (3.10).
* Pytorch (2.2.2).
* NVIDIA GPU (at least 16GB of GPU RAM) with updated drivers (550) and CUDA (12.4).
* Textual (0.55.1) - This is required for the front-end.

### 🦙 Get Llama
[Llama](https://github.com/meta-llama/llama) contains all the necessary explanation to get the code and the AI models.
In a nutshell, you need to:
* Follow the link in their repository to get access to the pretrained model weights.
* Once you receive the email, take node of the provided URL.
* Clone their repository
* Run the `download.sh` script to download the pretrained weights. I used the `llama-2-7b-chat`. It's the smallest you can download
* Install the library and dependencies via `pip` following their instructions.

Through the download script, you will download also the tokenizer. At this point, take note of:
* The path to the folder of the llama model
* The path to the tokenizer (the `.model` file)

### ⌨️ Configure AFK Llama

* Clone this repository
* Search the line of code `async def load_llm(this):`
* Change the path to the model parameters and tokenizer accordingly to what you did in the step before

## 🏃 Run

As llama relies on torch distributed computation, even though you have a single GPU, you still need to use `torchrun`.

`
torchrun afk_llama.py
`

# 📝 Licence Agreement
Llama and Textual are released under their respective licence agreement. The following agreement is restricted to the contect of this repository.

The code in this repository is released under the terms of [GNU GPLv3 Licence Agreement](https://www.gnu.org/licenses/gpl-3.0.html). A summary of this (and other FOSS licences is provided [here](https://en.wikipedia.org/wiki/Comparison_of_free_and_open-source_software_licenses)).

# ⚠️ Disclaimer
The code provided in this repository is provided AS IS and is intended for educational purposes only.

From the MIT License

`THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE`
