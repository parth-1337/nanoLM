import torch
import torch.nn as nn
import torch.nn.functional as F

class Decoder(nn.Module):
    def __init__(self, vocab_size, d_model):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)
        self.q_proj = nn.Linear(d_model, d_model, bias=False)
        self.k_proj = nn.Linear(d_model, d_model, bias=False)
        self.v_proj = nn.Linear(d_model, d_model, bias=False)

        # feed forward network setup
        # data pases inorder that its defined in nn.Sequential
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.ReLU(),
            nn.Linear(d_model * 4, d_model)
        )

        self.lm_head = nn.Linear(d_model, vocab_size)

    def forward(self, x):
        # B -> batch , T -> Time/Token Lenght
        B, T = x.shape

        x = self.embed(x)

        q = self.q_proj(x)
        k = self.k_proj(x)
        v = self.v_proj(x)

        # attnetion fomrula and divided by root of dimension
        # so softmax doesnt mess up
        # casual masking lower traingle and setting to -inf

        scores = q @ k.transpose(-2, -1) / (q.size(-1) ** 0.5)
        mask = torch.tril(torch.ones(T, T)).view(1, T, T).to(x.device)
        scores = scores.masked_fill(mask == 0, float('-inf'))

        attn = F.softmax(scores, dim=-1) @ v

        # connection skipping(residual connection)
        # prevents gradient vanishing
        x = x + attn
        x = x + self.ffn(x)

        return self.lm_head(x)
