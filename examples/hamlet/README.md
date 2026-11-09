# Hamlet demo

A tiny public-domain example of the cut format (about 2 minutes, not a full 10-minute piece).

- `source.txt` is the original speech.
- `cut.json` is the cut: exact lines, cues, delivery tags, intro.
- `hamlet-demo-cut.docx` is what `/script-cut` hands you.

Try the checker:

```sh
python skills/script-cut/scripts/build_cut.py check examples/hamlet/source.txt examples/hamlet/cut.json
```

Change one word in a `"src"` line in `cut.json` and run it again. The checker catches it.
