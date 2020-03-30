# Brainiak Tutorials

## Seed-based Functional Connectivity

Here are some ways to run/look at this notebook:
- [See an already-run version](https://brainiak.org/tutorials/08-connectivity/).
- [Run on Google Colab (online)](https://colab.research.google.com/github/brainiak/brainiak-tutorials/blob/master/tutorials/08-connectivity.ipynb).
- To set up locally, see [Installation Instructions](https://brainiak.org/tutorials/#detailed-installation-instructions). Basically, check out the [tutorials repo](https://github.com/brainiak/brainiak-tutorials), start Jupyter, then run the below setup blocks in `tutorials/08-connectivity.ipynb`.

If you're using **Google Colab**, run this as a new code cell:
```bash
%%bash
git clone https://github.com/brainiak/brainiak-tutorials.git
cd brainiak-tutorials/tutorials/
cp -r 07-searchlight 09-fcma 13-real-time utils.py setup_environment.sh /content/
```

If you're using **Google Colab** or are running this **locally**, run this as a new code cell:
```bash
%%bash
pip install deepdish ipython matplotlib nilearn notebook pandas seaborn watchdog
pip install --no-use-pep517 brainiak
mkdir ~/brainiak_datasets
cd ~/brainiak_datasets
wget -q -r 'https://drive.google.com/uc?export=download&confirm=jj9P&id=1iX5nLZvQsWuM5AmKeiBNoP8QkZjlOY7T' -O 'latatt.zip'
unzip latatt.zip
```

Coordinates for Exercise 2 (necessary to run remaining code)
```python
coords_lPPA = [(-27, -39, -24)]
coords_rPPA = [(30, -39, -15)]
```

## Classification

Here are some ways to run/look at this notebook:
- [See an already-run version](https://brainiak.org/tutorials/03-classification/).
- [Run on Google Colab (online)](https://colab.research.google.com/github/brainiak/brainiak-tutorials/blob/master/tutorials/03-classification.ipynb).
- To set up locally, see [Installation Instructions](https://brainiak.org/tutorials/#detailed-installation-instructions). Basically, check out the [tutorials repo](https://github.com/brainiak/brainiak-tutorials), start Jupyter, then run the below setup blocks in `tutorials/03-classification.ipynb`.

If you're using **Google Colab**, run this as a new code cell:
```bash
%%bash
git clone https://github.com/brainiak/brainiak-tutorials.git
cd brainiak-tutorials/tutorials/
cp -r 07-searchlight 09-fcma 13-real-time utils.py setup_environment.sh /content/
```

If you're using **Google Colab** or are running this **locally**, run this as a new code cell:
```bash
%%bash
pip install deepdish ipython matplotlib nilearn notebook pandas seaborn watchdog
pip install --no-use-pep517 brainiak
mkdir ~/brainiak_datasets
cd ~/brainiak_datasets
URL='https://docs.google.com/uc?export=download&id=18V_vMG9gP381VZ8sHuPqTza-6tOwS18Q'
CONFIRM=$(curl -sL -c cookies.txt $URL | perl -n -e '/confirm=(.*?)&/ && print $1')
curl -L -b cookies.txt -o vdc.zip "$URL&confirm=$CONFIRM"
rm cookies.txt
unzip vdc.zip
mv vdc-small vdc
```
