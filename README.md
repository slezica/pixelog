# pixelog

Print all unique colors from an image with their frequency, hex, RGB, and OKLCH values.

<img width="860" height="307" alt="image" src="https://github.com/user-attachments/assets/c512a7cb-d9bd-4d0c-a846-99b5600f5ceb" />


## Installation

Install using `uv`:

```bash
uv tool install git+https://github.com/slezica/pixelog.git
```

Uninstall with `uv tool uninstall pixelog`.

## Usage

Basic usage:

```bash
pixelog image.png
```

Show all colors including rare ones (< 0.01%):

```bash
pixelog --all image.png
```

Get the 5 most common colors:

```bash
pixelog photo.jpg | head -5
```

## Requirements

- Python 3.13+
- Pillow (image processing)
- colorspacious (OKLCH conversion)


## License

Use this code freely, except for waging war.
