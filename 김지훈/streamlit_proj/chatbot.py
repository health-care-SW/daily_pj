import torch
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast

model = torch.load(".\model\model20")
model = model.cpu()

Q_TKN = "<usr>"
A_TKN = "<sys>"
BOS = '</s>'
EOS = '</s>'
MASK = '<unused0>'
SENT = '<unused1>'
PAD = '<pad>'

koGPT2_TOKENIZER = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
            bos_token=BOS, eos_token=EOS, unk_token='<unk>',
            pad_token=PAD, mask_token=MASK) 


def chat(q):
    with torch.no_grad():
        q = q.strip()
        if q == "quit":
            return q
        a = ""
        while 1:
            input_ids = torch.LongTensor(koGPT2_TOKENIZER.encode(Q_TKN + q + SENT + A_TKN + a)).unsqueeze(dim=0)
            pred = model(input_ids)
            pred = pred.logits
            gen = koGPT2_TOKENIZER.convert_ids_to_tokens(torch.argmax(pred, dim=-1).squeeze().numpy().tolist())[-1]
            if gen == EOS:
                break
            a += gen.replace("▁", " ")
        return a.strip()
        #print("Chatbot > {}".format(a.strip()))

if __name__ == "__main__":
    
    while True:
        input_ = input('user > ')
        output_ = chat(input_)
        if output_ == "quit":
            break
        print(f'chatbot > {output_}')
