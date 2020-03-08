sudo apt install curl
sudo apt-get install git

#download anaconda:
curl https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh --output anaconda.sh
sudo chmod 777 anaconda.sh

./anaconda.sh


cd Desktop
git clone https://github.com/AlexEMG/DeepLabCut

# YOU NEED TO RESTART TERMINAL... 
## An environment for CPU on Ubuntu 18.04
conda create -n DLC python=3.6
conda activate DLC
pip install deeplabcut
pip install https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04/wxPython-4.0.3-cp36-cp36m-linux_x86_64.whl
pip install tensorflow
pip install ipython spyder
