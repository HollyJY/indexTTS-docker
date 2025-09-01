From IndexTTS, https://indextts.io

Only adding dockerfile, and a runnable sample.py

# running with docker

## building image

```bash
docker build -t indextts:latest .
```

## running in a container

```bash
docker run --gpus all -it \
  --entrypoint /bin/bash \
  -v $PWD/checkpoints:/app/checkpoints \
  -v $PWD/data:/app/data \
  -v $PWD/tests:/app/tests \
  indextts:lastest
```

## download the weights into checkpoints/
```bash
huggingface-cli download IndexTeam/IndexTTS-1.5 \
  config.yaml bigvgan_discriminator.pth bigvgan_generator.pth bpe.model dvae.pth gpt.pth unigram_12000.vocab \
  --local-dir checkpoints
```

## running a test
```bash
python3 sample.py --model_dir checkpoints \
                  --ref tests/sample_prompt.wav \
                  --text "Hello, this is a test." \
                  --outdir app/data/outputs/index-tts
```