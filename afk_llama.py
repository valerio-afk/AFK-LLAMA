from datetime import datetime
from rich.text import Text
from textual import work
from textual.reactive import reactive
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, TextArea, Button, Static, Label, MarkdownViewer
from llama import Llama, Dialog
from llama.generation import Message
from typing import Optional

import asyncio
import torch


class LLM:

    def __init__(this,model_path, tokenkizer_path):
        assert torch.cuda.is_available(), "No GPU Found"

        this._model = Llama.build(
        ckpt_dir=model_path,
        tokenizer_path=tokenkizer_path,
        max_seq_len=4096,
        max_batch_size=1,
    )

    def generate(this,dialog:Dialog):
        return this._model.chat_completion([dialog],
                                           max_gen_len=4096,
                                           temperature=0.6,
                                           top_p=0.9)[0]['generation']

class PromptArea(Static):

    BINDINGS = [Binding("ctrl+q", "submit", "Submit prompt")]

    def __init__(this, *args, **kwargs):
        super().__init__(*args,**kwargs)

        this.prompt_area = TextArea(id="prompt")
        this.prompt_area.show_line_numbers = False

        this.submit_prompt_button = Button("Submit",id="submit",variant="success")

    def compose(this) -> ComposeResult:
        yield this.prompt_area
        yield this.submit_prompt_button

    async def action_submit(this):
        this.submit_prompt_button.press()


class StatusBar(Static):
    def __init__(this,*args,**kwargs):
        super().__init__(*args,**kwargs)

        this._label = Label()

    def compose(this) -> ComposeResult:
        yield this._label

    def _remove_classes(this):
        this.remove_class("success")
        this.remove_class("warning")

    def show_warning(this,text:str):
        this._remove_classes()

        this.add_class("warning")
        this._label.update(Text.from_markup(text))

    def show_success(this, text: str):
        this._remove_classes()

        this.add_class("success")
        this._label.update(Text.from_markup(text))

class AFKLlama(App):

    BINDINGS = [("ctrl+s","save_chat","Save Chat"),("ctrl+r","clear_chat","Clear Chat")]
    CSS_PATH = "app.tcss"

    llm = reactive(None)
    chat = []

    chat_info = {"time":datetime.now(),"content":""}


    def __init__(this):
        super().__init__()
        this._chat_area = MarkdownViewer(show_table_of_contents=False,id="chat_area")
        this._chat_area.show_line_numbers = False

        this._status_bar = StatusBar(id="status-bar",classes="success")
        this._prompt_area = PromptArea(id="prompt_area")

        this.enable_prompt_area(False)

        this.chat_info["time"] = datetime.now()


    async def on_load(this):
        this.load_llm()

    def compose(this) -> ComposeResult:
        yield Header()
        yield this._status_bar
        yield this._chat_area
        yield this._prompt_area
        yield Footer()



    @work(exclusive=True,thread=True,name="load_llm")
    async def load_llm(this):
        if (this.llm is None):
            this._status_bar.show_warning("Loading AI Model")

            this.llm = LLM("<YOUR_PATH>/llama-2-7b-chat",
                            "<YOUR_PATH>/tokenizer.model")

    @work(exclusive=True,name="thinking")
    async def ask_llm(this,prompt:str):
        this.enable_prompt_area(False)
        this._status_bar.show_warning("Thinking")

        await this.add_interaction({"role":"user","content":prompt})

        await asyncio.sleep(0.1)

        result = this.llm.generate(this.chat)

        await this.add_interaction(result)

        this._status_bar.show_success("Ready...")
        this.enable_prompt_area(True)


    def watch_llm(this, old:Optional[LLM], new:Optional[LLM]):
        if (new is not None):
            this._status_bar.show_success("Ready...")
            this.enable_prompt_area(True)

    async def add_interaction(this, msg:Message):
        this.chat.append(msg)
        await this.show_chat()

    def action_save_chat(this):
        fname = f"{this.chat_info['time'].strftime('%Y%m%d_%H%M%S')}.md"

        with open(fname,"w") as h:
            h.write(this.chat_info['content'])

        this._status_bar.show_success(f"Chat saved in [b]{fname}[/b]")

    async def show_chat(this):

        final_dialog = ""
        await this._chat_area.document.update(final_dialog)

        n = len(this.chat) - 1

        for i,interaction in enumerate(this.chat):
            match (interaction['role']):
                case 'user':
                    role = "You"
                case "assistant":
                    role ="AFKLlama"
                case _:
                    continue

            final_dialog += f"## {role}:\n"

            if (role == "AFKLlama") and (i==n):
                m = len(interaction['content'])-1
                for j,c in enumerate(interaction['content']):
                    final_dialog+=c

                    if (j<m):
                        chat = final_dialog + "\u2588"
                    else:
                        chat = final_dialog

                    await this._chat_area.document.update(chat)
                    await asyncio.sleep(0.001)
                    this._chat_area.scroll_end()
            else:
                final_dialog+=f"{interaction['content']}\n"
                await this._chat_area.document.update(final_dialog)
                this._chat_area.scroll_end()

        this.chat_info["content"] = final_dialog


    def on_button_pressed(this, event:Button.Pressed):
        prompt = this._prompt_area.prompt_area.text.strip()
        this._prompt_area.prompt_area.text = ""

        if (len(prompt) > 0):
            this.ask_llm(prompt)



    def enable_prompt_area(this,enabled:bool):
        this._prompt_area.prompt_area.disabled = not enabled
        this._prompt_area.submit_prompt_button.disabled = not enabled

        if enabled:
            this._prompt_area.prompt_area.focus()

    async def action_clear_chat(this):
        busy = False

        for w in this.workers:
            if w.name == "thinking":
                busy = True

        if not busy:
            this.chat = []
            this.chat_info["time"] = datetime.now()
            await this.show_chat()




def main():

    app = AFKLlama()



    app.run()

if __name__ == "__main__":
    main()