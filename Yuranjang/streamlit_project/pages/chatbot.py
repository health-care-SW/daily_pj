from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel
import torch
import streamlit as st

with st.spinner('로딩 중...'):

    tokenizer = PreTrainedTokenizerFast.from_pretrained('byeongal/Ko-DialoGPT')

    model = GPT2LMHeadModel.from_pretrained('byeongal/Ko-DialoGPT')


past_user_inputs = []
generated_responses = []

with st.form(key='my_test3'):
    user_input = st.text_input(label="챗봇에게 말하기", key='i')
    submitted = st.form_submit_button('물어보기')
    if submitted:
        # if user_input == 'bye':
        #     break
        text_idx = tokenizer.encode(
            user_input + tokenizer.eos_token, return_tensors='pt')
        for i in range(len(generated_responses)-1, len(generated_responses)-3, -1):
            if i < 0:
                break
            encoded_vector = tokenizer.encode(
                generated_responses[i] + tokenizer.eos_token, return_tensors='pt')
            if text_idx.shape[-1] + encoded_vector.shape[-1] < 1000:
                text_idx = torch.cat([encoded_vector, text_idx], dim=-1)
            else:
                break
            encoded_vector = tokenizer.encode(
                past_user_inputs[i] + tokenizer.eos_token, return_tensors='pt')
            if text_idx.shape[-1] + encoded_vector.shape[-1] < 1000:
                text_idx = torch.cat([encoded_vector, text_idx], dim=-1)
            else:
                break
        inference_output = model.generate(
            text_idx,
            max_length=1000,
            num_beams=5,
            top_k=20,
            no_repeat_ngram_size=4,
            length_penalty=0.65,
            repetition_penalty=2.0,
        )
        inference_output = inference_output.tolist()
        bot_response = tokenizer.decode(
            inference_output[0][text_idx.shape[-1]:], skip_special_tokens=True)
        st.write(f"대답:{bot_response}")
        past_user_inputs.append(user_input)
        generated_responses.append(bot_response)
