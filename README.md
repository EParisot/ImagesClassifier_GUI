# ImagesClassifier_GUI

(This repo isn't maintained anymore, take a look at the Django/web version : https://github.com/EParisot/IC_GUI_web)

Machine Learning Images Classification in Graphical User Interface
* Take pictures
* Labelize them
* Define a Model Design
* Train your model 
* Test your model

### Without any line of code !

![Alt text](/screenshots/model.bmp?raw=true "Model")

![Alt text](/screenshots/train.bmp?raw=true "Training")

## Installation :

#### Windows and MACOS users only : Download and Install Anaconda3 (Python3) for your system :

https://www.continuum.io/downloads

#### Linux users only : Download and Install Python3.5 for your system :

```
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tar.xz
tar -xvf Python-3.5.2.tar.xz
cd Python-3.5.2
./configure
make
make altinstall
```

#### Clone Repo
```
git clone "https://github.com/EParisot/ImagesClassifier_GUI.git"
```

#### Change to repo's folder:

```
cd ImagesClassifier_GUI
```

#### Install for your system (WIN, MACOS, Linux, RPI):

```
./install_???.sh
```
wait for Anaconda to build environnement

#### Start program:

```
./run.sh
```


## Uninstall:

*Windows and MACOS:
```
	conda env remove -n IC_GUI
```

*Linux :
```
	rm -rf IC_GUI
```

