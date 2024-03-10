"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import asyncio
from rxconfig import config

import reflex as rx
import json
import requests
import httpx

import os
import openai


_client = openai.OpenAI(api_key="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")


# def get_openai_client():
#     global _client
#     if _client is None:
#         _client = openai.OpenAI(api_key="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")

#     return _client



my_tasks = set()
docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"
send_over = {"filename":"ACM"}


class State(rx.State):
    """The app state."""
    form_data: dict = {}
    output_dict: dict = {}
    final_dict:list = []
    print(form_data)
    results_returned = False
    return1:str
    return2:str
    return3:str
    return4:str
    return5:str

    #Dali stuff
    image_url = ""
    image_processing = False
    image_made = False
    error_msg = ""

    def openai_function(self,url):
        question="Write a short description for each of the following resulting pages."
        new_question = f"{question}{url}"
        completion = _client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=new_question,
            max_tokens=30,
        )
        return completion.choices[0].text

   
    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.results_returned=False
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"http://127.0.0.1:5000/read_file",
                    json={"filename":form_data['first_name']},
                )
            print(self.output_dict)
            self.output_dict = response.json()['content']
            print('before')
            test_input = self.openai_function(self.output_dict[0])
            self.return1 = test_input
            self.return2 = self.openai_function(self.output_dict[1])
            self.return3 = self.openai_function(self.output_dict[2])
            self.return4 = self.openai_function(self.output_dict[3])
            self.return5 = self.openai_function(self.output_dict[4])
            print(self.return2)
            print(type(self.return1))

            print(self.return1)
            # for result in self.openai_function(self.output_dict)[0:4]:
            #     print(result)
            # for x in test_input:
            #     self.final_dict.append(x)
            self.results_returned=True
            self.error_msg=""
            # for x in self.output_dict:
            #     self.final_dict.append(self.openai_function(x))

            # self.form_data = self.output_dict['content']
        except:
            print('error')
            self.error_msg="Sorry something went wrong. Please try again"
        print(self.output_dict)
        self.image_made=True

    
# def search_item(search_item)->rx.Component:
#     return rx.table.row(
#         rx.table.row_header_cell(
#             "head"
#         ),
#         rx.table.cell(
#             search_item,
#         ),
#     ),

def index() -> rx.Component:
    return rx.center(
        # rx.theme_panel(),
        rx.heading("Search Project INF141",size="9"),
        rx.vstack(
            rx.form(
                rx.hstack(
                    rx.input(
                        placeholder="enter here",
                        name="first_name",
                        size="3",
                    ),
                    rx.button("Submit", type="submit",size="4"),
                justify_items="center",
                align_items="center",
                ),
                on_submit=State.handle_submit,
                reset_on_submit=True,    
            ),
            rx.divider(),
            rx.heading(State.error_msg),
            # rx.text(State.form_data.to_string()),
            rx.cond(
                State.results_returned,
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Index"),
                            rx.table.column_header_cell("Result"),
                            rx.table.column_header_cell("GPT Summary")
                            
                        ),
                    ),
                    rx.table.body(
                        rx.table.row(
                            rx.table.row_header_cell("Index 1"),
                            rx.table.cell(State.output_dict[0]),
                            rx.cond(
                                State.image_made,
                                rx.table.cell(State.return1),
                                rx.icon(tag="more-horizontal"),
                            ),
                            
                        ),
                        rx.table.row(
                            rx.table.row_header_cell("Index 2"),
                            rx.table.cell(State.output_dict[1]),
                            rx.cond(
                                State.image_made,
                                rx.table.cell(State.return2),
                                rx.icon(tag="more-horizontal"),
                            ),
                        
                        ),
                        rx.table.row(
                            rx.table.row_header_cell("Index 3"),
                            rx.table.cell(State.output_dict[2]),
                            rx.cond(
                                State.image_made,
                                rx.table.cell(State.return3),
                                rx.icon(tag="more-horizontal"),
                            ),
        
                        ),
                        rx.table.row(
                            rx.table.row_header_cell("Index 4"),
                            rx.table.cell(State.output_dict[3]),
                            rx.cond(
                                State.image_made,
                                rx.table.cell(State.return4),
                                rx.icon(tag="more-horizontal"),
                            ),
        
                        ),
                        rx.table.row(
                            rx.table.row_header_cell("Index 5"),
                            rx.table.cell(State.output_dict[4]),
                            rx.cond(
                                State.image_made,
                                rx.table.cell(State.return5),
                                rx.icon(tag="more-horizontal"),
                            ),
        
                        ),
                    ),
                ),
                rx.text(),
            ),
        align="center",
        justify_content="center",
        align_items="center",
        justify="center",
        justify_self="center",
        align_self="center",
        ),
    align="center",
    justify_content="center",
    align_items="center",
    justify="center",
    direction="column",
    justify_self="center",
    align_self="center",
    spacing="9"
)


app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="sky"
    ),
)
app.add_page(index)
