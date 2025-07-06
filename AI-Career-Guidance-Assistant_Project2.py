import gradio as gr
from ibm_watson_machine_learning.foundation_models import Model

wml_credentials = {
    "apikey": "PGJP9fGCj5N_9rWNMHe3bNElnY_YqRTPY1QiQSL_peu_",
    "url": "https://us-south.ml.cloud.ibm.com"
}

project_id = "84518077-ea6b-4462-b9ff-6aa0f40709ee"
model_id = "ibm/granite-13b-instruct-v2"

model = Model(
    model_id=model_id,
    credentials=wml_credentials,
    project_id=project_id
)

parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 300
}

career_questions = [
    "What subjects do you enjoy the most? (Science, Arts, Commerce, Technology, etc.)",
    "Do you prefer working with people, data, or things?",
    "Would you describe yourself as creative or analytical?",
    "How do you like to solve problems? (Logic, Innovation, Teamwork)",
    "What are your top 3 skills or strengths?",
    "What are your long-term career goals?",
    "Would you prefer a structured 9-5 job or a dynamic work environment?",
    "Do you enjoy learning new technology?",
    "Would you like to travel frequently for work?",
    "Which of the following appeals to you the most? (Helping others, Building systems, Leading teams, Researching)"
]

import json 

def career_guidance(*responses):
    try:
        combined = "\n".join([f"{career_questions[i]} Answer: {responses[i]}" for i in range(len(responses))])

        prompt = f"""
You are a professional career counselor.

Based on the user's answers below, suggest 2 to 3 ideal career options. Keep suggestions short and explain why each fits.

{combined}
"""

        result = model.generate_text(prompt=prompt, params=parameters)

        # Try getting proper response
        if isinstance(result, dict) and "results" in result:
            output = result["results"][0].get("generated_text", "").strip()
            return output if output else "⚠️ The model didn't return a proper answer. Try rephrasing your answers."
        else:
            return "⚠️ Watsonx returned an unexpected response. Please try again later."

    except Exception as e:
        return f"⚠️ Something went wrong: {str(e)}"


with gr.Blocks() as demo:
    gr.Markdown("## 🎯 AI-Powered Career Guidance Assistant (by Kunal Singh Beniwal)")
    with gr.Row():
        with gr.Column():
            inputs = [gr.Textbox(label=q) for q in career_questions]
            submit_btn = gr.Button("Get Career Suggestions")
        with gr.Column():
            output_box = gr.Textbox(label="Suggested Career Paths", lines=12, interactive=False)
    submit_btn.click(fn=career_guidance, inputs=inputs, outputs=output_box)

demo.launch(share=True)
