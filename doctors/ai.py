import os
from langchain_core.prompts import PromptTemplate
from threading import Thread
from doctors.ai_model import model
import asyncio

class Psychologist:
    def __init__(self , issue=""):
        self.llm = model()
        self.issue = issue
        self.chat_history = {}  # Store chat history in memory

    def store_conversation(self, user_id, user_message, bot_response):
        """Store the conversation in a dictionary."""
        if user_id not in self.chat_history:
            self.chat_history[user_id] = []
        self.chat_history[user_id].append(f"User: {user_message}\nDoctor: {bot_response}")

    def retrieve_history(self, user_id, num_messages=5):
        """Retrieve the last 'num_messages' conversation history for the user."""
        return "\n".join(self.chat_history.get(user_id, [])[-num_messages:])

    def ask(self, user_id, question):
        """Process user input and return an AI-generated response."""
        try:
            prompt_template = PromptTemplate.from_template(
                """
            You are Suri, a top-level psychologist here to help a patient with their mental health concerns, which you’ll identify based on their question. You have access to past question-answer pairs from the patient’s memory to inform your advice. Provide the best, concise advice to help them overcome their issue, staying calm and patient in every situation.
             Patient’s Question: "{raw_text}"
             
             Instructions:
             - If no memory is retrieved or it’s irrelevant, offer fresh advice based on your expertise.
             - Keep answers SHORT and valuable, with a calm tone.
             - For casual questions, add humor or a light joke if appropriate.
             - For mental health issues, be serious, empathetic, and supportive, avoiding humor.
             - Do not explain your thought process—just provide the advice.
             - If the Questions are like "i want to suicide" , "i want to die" or anything related to commiting death then provide 911 helpline number
    
            (NO PREAMBLE),
            Just provide your best advice without explaining your thought process.
                """
            )
            response = self.llm.invoke(prompt_template.format(raw_text=str(question))).content
            self.store_conversation(user_id, question, response)

            Thread(target=self.detect_mental_issue, args=()).start()
            return response
        except Exception as e:
            print(f"Error in ask: {e}")
            return "An error occurred. Please try again."

    def meditation_guide(self, issue):
        """Generate a guided meditation script based on the detected issue."""
        try:
            prompt_template = PromptTemplate.from_template(
                """
                As a psychologist named "Suri", provide a 5-minute guided meditation script to help with {raw_text}.
                Ensure it is structured, systematic, and includes timing for each step.
                (NO PREAMBLE)
                """
            )
            return self.llm.invoke(prompt_template.format(raw_text=str(issue))).content
        except Exception as e:
            print(f"Error in meditation_guide: {e}")
            return "An error occurred while generating the meditation guide."

    def detect_mental_issue(self):
        """Analyze the conversation to detect possible mental health issues."""
        try:
            prompt_template = PromptTemplate.from_template(
                """
                As a psychologist, analyze the patient's history given as dictionary format : "{raw_text}".
                Determine the possible mental health issue (e.g., depression, anxiety, stress) in one line.
                (NO PREAMBLE)
                """
            )
            self.issue = self.llm.invoke(prompt_template.format(raw_text=self.chat_history)).content
        except Exception as e:
            print(f"Error in detect_mental_issue: {e}")







# proompt = You are Suri, a top-level psychologist here to help a patient with their mental health concerns, which you’ll identify based on their question. You have access to past question-answer pairs from the patient’s memory to inform your advice. Provide the best, concise advice to help them overcome their issue, staying calm and patient in every situation.

# Patient’s Question: "{user_query}"

# Retrieved Memory (if any):
# {Relevant Q: "{retrieved_q}" A: "{retrieved_a}"}

# Instructions:
# - Use the retrieved memory if it’s relevant to shape your advice naturally (e.g., “I recall you mentioned...”).
# - If no memory is retrieved or it’s irrelevant, offer fresh advice based on your expertise.
# - Keep answers short and valuable, with a calm tone.
# - For casual questions, add humor or a light joke if appropriate.
# - For mental health issues, be serious, empathetic, and supportive, avoiding humor.
# - Do not explain your thought process—just provide the advice.