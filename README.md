# Instructions
### Please read OC-README.pdf for a better understanding of the program.

There are a few installs required for the program to run. If you are on macOS:

```
pip3 install numpy
pip3 install Pillow
```

Otherwise, if you are on Windows:

```
pip install numpy
pip install Pillow
```
Then run the program. If your command line interpreter doesn't understand a module that is being imported, it is likely fixed by pip-installing the module.

Why do we need numpy and Pillow? Well, we make use of numpy's random function to iterate towards a fixed point. We use PIL's image saving service to save an image of the bifurcation diagram to the desktop.
