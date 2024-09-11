# Finetuning open source models.

Plan
  - May be start with HF llama. Do some inferencing in 8 or 4 bit, then follow the meta repo and then do some lora tuning locally + finetuning. 
  - Then move to running on mac.
  - Then move to reflection


Documentation:

- LLAMA documentation: 
  - Meta llama repo: https://github.com/meta-llama/llama-models/blob/main/README.md
  - Meta thorough documentation: https://llama.meta.com/docs/model-cards-and-prompt-formats/llama3_1
  - [Unique download url](https://llama3-1.llamameta.net/*?Policy=eyJTdGF0ZW1lbnQiOlt7InVuaXF1ZV9oYXNoIjoibTNxZ2dmb3JyZHd6bmpxYmF5ZnhvcG1pIiwiUmVzb3VyY2UiOiJodHRwczpcL1wvbGxhbWEzLTEubGxhbWFtZXRhLm5ldFwvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTcyNjEyNDQzNH19fV19&Signature=mHdZc-dPstMPOAdRDwUmXDsqo%7E%7EdPXxviW7YwY-YEa0IE2dgkQ80lfTClhBtMWNuO-wdUjC4Ic9ifqYxFOQSwiGdu1m0HgZJMA-6qaN3qZJY0s93ao0C5b8TZha-pMFpN3I6V6pG9Kq3Czpj0xM0YW1S-sE2UHoutaOF9ylQ6heipmgU5qGwomfQuZl2BxjuY1y8kVZBvD-sIIvJnHoUcAcUjXNz%7Ebi-97HD6-W0dqZyt8MZ-VPADmiR6i5zEOxtLpvBrp6s7e%7EwA9D-Zbunlw8FrDLX-0Q-cROONPyDLAaUvEJ%7ElvpA9UfdwUzxG-glkV3TDflMiaOOO7a%7E8Kpwpw__&Key-Pair-Id=K15QRJLYKIFSLZ&Download-Request-ID=1059749259122513)
  - Huggingface: https://huggingface.co/meta-llama
- Reflection Llama-3.1 70B: 
  - (currently) the world's top open-source LLM, trained with a new technique called Reflection-Tuning that teaches a LLM to detect mistakes in its reasoning and correct course.
  - https://huggingface.co/mattshumer/Reflection-Llama-3.1-70B
- Running on mac
  - https://llama.meta.com/docs/llama-everywhere/running-meta-llama-on-mac/ (uses a library called ollama)
  - https://github.com/ml-explore/mlx-examples?tab=readme-ov-file - seems to support only llama1 and 2. 3.1 is latest. Hence avoid using this first