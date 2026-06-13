# Adding a Custom Plotter

Upload a `.py` file with the desired function into this folder. PostFOAM will discover it automatically, just remember to add it to your config.yaml :D

## Minimal template

```python
from __future__ import annotations
from pathlib import Path
from base import PostStage
import matplotlib.pyplot as plt

class MyFunction(PostStage):
    name = "my_function"   # this name must be matched in config.yaml exactly, so in this case "my_function"

    def run(self) -> list[Path]:
        # Read your file
        file_path = self.case_dir / self.config.get("file", "path/to/default") # Add your folder here

        # Your code here...
        #...
        #...

        # Save and return, ReportBuilder picks up everything you return
        out = self.out_dir / "my_plot.png"
        fig.savefig(out, dpi=150)
        plt.close(fig)
        self.log(f"Saved {out.name}")
        return [out]  # return a list: you can return multiple images
```

## config.yaml entry

```yaml
- type: my_function        # must match name = "my_function" in your class
  file: postProcessing/myData/0/myfile.dat # Where the file will be saved in OpenFOAM
  section: "My Section"  # section title in the PDF report
```

## Rules

- **`name`** must be unique across all plotters and match `type` in the config exactly
- **`run()`** must return a `list[Path]` of generated images, all of them will appear in the report
- **`self.case_dir`** is the OpenFOAM case root
- **`self.out_dir`** is where you should save output files
- **`self.config`** is the raw YAML entry for this plot, access any field with `self.config.get("field")`
- **`self.log("A message")`** prints a formatted log message (e.g. function xyz was plotted)

## Available context

| Attribute | Type | Description |
|---|---|---|
| `self.case_dir` | `Path` | OpenFOAM case root directory |
| `self.out_dir` | `Path` | Output directory for generated files |
| `self.config` | `dict` | The full YAML entry for this plot |
| `self.log(msg)` | method | Formatted logging |

## Dependencies

Standard library + whatever is in `requirements.txt` (`matplotlib`, `pandas`,
`numpy`). If your plotter needs something extra, add it to `requirements.txt`
and mention it in a comment at the top of your file.