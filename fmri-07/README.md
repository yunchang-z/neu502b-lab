# Brainiak Tutorials

## Seed-based Functional Connectivity

Here are some ways to run this notebook:
- [Run on Google Colab (online)](https://colab.research.google.com/github/brainiak/brainiak-tutorials/blob/master/tutorials/08-connectivity.ipynb)
- To set up locally, see [Installation Instructions](https://brainiak.org/tutorials/#detailed-installation-instructions). Basically, check out the [tutorials repo](https://github.com/brainiak/brainiak-tutorials), then run the below setup block.

If you're using Google Colab, run this as a new code cell:
```
%%bash
git clone https://github.com/brainiak/brainiak-tutorials.git
cd brainiak-tutorials/tutorials/
cp -r 07-searchlight 09-fcma 13-real-time utils.py setup_environment.sh /content/
```

If you're using Google Colab or are set up locally, run this as a new code cell:
```
%%bash
pip install deepdish ipython matplotlib nilearn notebook pandas seaborn watchdog
pip install pip\<10
pip install brainiak
mkdir ~/brainiak_datasets
cd ~/brainiak_datasets
wget -q --show-progress --no-check-certificate -r 'https://drive.google.com/uc?export=download&confirm=jj9P&id=1iX5nLZvQsWuM5AmKeiBNoP8QkZjlOY7T' -O 'latatt.zip'
unzip latatt.zip
```
