# Data

The course data (1,520 WAV clips + `train.csv`) is for use within the course only
and is **not** committed (see `.gitignore`).

Sources: ASVspoof 5, CodecFake, AILABS-M.

## Expected layout (local only)
```
data/
├── train.csv
├── audio/        # all training WAV files
└── test/         # released only before the presentations; never used for training,
                  # pseudo-labeling, manual labeling, or label lookup
```
