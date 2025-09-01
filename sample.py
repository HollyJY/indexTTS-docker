#!/usr/bin/env python3
"""
Minimal standalone IndexTTS CLI.
Usage:
    python sample.py --model_dir checkpoints \
                     --ref data/inputs/ref.wav \
                     --text "Hello, this is a test." \
                     --outdir data/outputs/index-tts
"""

import os
import argparse
from indextts.infer import IndexTTS


def main():

    parser = argparse.ArgumentParser("Minimal IndexTTS CLI")
    parser.add_argument("--model_dir", default=os.environ.get("MODEL_DIR", "checkpoints"),
                        help="Path to model weights (with config.yaml)")
    parser.add_argument("--ref", required=True,
                        help="Reference audio file (wav, mp3, etc.)")
    parser.add_argument("--text", required=True,
                        help="Text to synthesize")
    parser.add_argument("--outdir", default="data/outputs/index-tts",
                        help="Output directory")
    parser.add_argument("--outfile", default=None,
                        help="Optional output filename (default auto)")
    parser.add_argument("--verbose", action="store_true",
                        help="Print extra logs")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    if args.outfile is None:
        import time
        args.outfile = f"tts_{int(time.time())}.wav"
    outpath = os.path.join(args.outdir, args.outfile)

    # Load model
    cfg_path = os.path.join(args.model_dir, "config.yaml")
    tts = IndexTTS(model_dir=args.model_dir, cfg_path=cfg_path)

    # Run inference (batch mode handles longer sentences robustly)
    result = tts.infer_fast(
        args.ref,
        args.text,
        outpath,
        verbose=args.verbose,
        max_text_tokens_per_sentence=120,
        sentences_bucket_max_size=4,
        do_sample=True,
        top_p=0.8,
        top_k=30,
        temperature=1.0,
        length_penalty=0.0,
        num_beams=3,
        repetition_penalty=10.0,
        max_mel_tokens=600,
    )

    print("Generated file:", result)


if __name__ == "__main__":
    main()