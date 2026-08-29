# Metadata-Loss Ablation Protocol

This test asks a deliberately narrower question than the prior local-model
study: if a flat evidence bundle removes the only record type needed by the
question, does restoring that type through a UAS address change answer choice?

The model gets 24 synthetic, held-out questions across science, safe local
security, and AI evaluation. Every flat bundle has three same-key records with
three different codes but no type labels. Every UAS bundle has the same three
records with stable typed addresses. The question names the desired type. The
answer key is never put in either prompt.

This is an **information-preservation ablation**. A positive result would mean
the local model can use typed addresses when flat retrieval has removed a
necessary discriminator. It would not prove a general reasoning gain, natural
data performance, or a production UAS benefit.

The positive gate is UAS accuracy at least 15 points above flat accuracy and
fewer wrong-domain codes. All outputs and parse failures are saved.
