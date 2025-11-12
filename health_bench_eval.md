# 🩺 Reproduce HealthBench using MynaBot

This repository reproduces the HealthBench evaluation pipeline using responses generated from the **MynaBot** model. It includes both response generation and rubric-based evaluation using the SRH dataset extracted from the original HealthBench data.

## 📂 Dataset

**Path**: [`data/srh_healthbench_data_structured.json`](data/srh_healthbench_data_structured.json)

This structured JSON dataset contains prompts and evaluation rubrics. Each entry follows this schema:

```json
{
  "prompt": "<user prompt>",
  "prompt_id": "<unique id>",
  "conversation_turns": "<conversation_turns>",
  "theme": "<health theme/topic>",
  "rubrics": {
    ...
  }
}
```
- conversation_turns includes single or multi-turn dialogues.
- Prompts always end with a user question to which MynaBot should respond.

## 🧠 Step 1: Response Generation with MynaBot
The HealthBench prompts include both single-turn and multi-turn conversations. Each ends with a user question, and the task is to generate the assistant's final response using the MynaBot model.

You may follow or adapt these scripts from the OpenAI simple-evals repository:
1. chat_completion_sampler: https://github.com/openai/simple-evals/blob/main/sampler/chat_completion_sampler.py 
2. responses_sampler: https://github.com/openai/simple-evals/blob/main/sampler/responses_sampler.py

✅ Customization: Regardless of the number of turns, only the assistant's generate responses to the final user message.

## 📏 Step 2: Evaluate the Responses (HealthBench Criteria)

Based on the generated answer you need to evaluate bot reponse based on healthbench criteria. 
Use the following scripts from OpenAI’s evaluation suite:
1. healthbench_eval: https://github.com/openai/simple-evals/blob/main/healthbench_eval.py
2. healthbench_eval_test: https://github.com/openai/simple-evals/blob/main/healthbench_eval_test.py
3. healthbench_meta_eval: https://github.com/openai/simple-evals/blob/main/healthbench_meta_eval.py


# 📊 SRH Extracted Question Visualization

To see the srh question structed we made an app, where you can see overall SRH analysis and download the data as Excel and Json format 

To explore the structured SRH questions, we created an interactive web app where you can:

- ✅ View SRH data summaries and analytics  
- 📥 Download the dataset in **Excel** or **JSON** formats


# 📚 References
- [OpenAI HealthBench Repo](https://github.com/openai/simple-evals)
- [OpenAI Evals Documentation](https://platform.openai.com/docs/guides/evals)
- [OpenAI Chat Completions](https://platform.openai.com/docs/api-reference/chat/create)
- [Paper](https://arxiv.org/pdf/2505.08775v1)