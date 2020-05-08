import pandas as pd
import numpy as np

from acheron.workflows import supervised_model

# set to 5 for 5 fold cross-validation
k_folds = config['folds']

# if we are cross validating we only need one feature dataframe, otherwise
# we need to check if the other datasets are also ready
features = [] # paths to feature matrices
labels = [] # paths to label matrices
masks = [] # paths to validity masks

# if a dataset has been declared, add it to above paths
for dataset in ['train','test','validation']:
    if config[dataset] != 'None':
        features += ["data/{}/features/{}_matrix.df".format(
            config[dataset],config['type'])]
        labels += ["data/{}/labels/{}.df".format(
            config[dataset],config['label'])]
        masks += ["data/{}/features/masks/{}_{}.df".format(
            config[dataset],config['type'],config['label'])]

splits = [] # path to splits df, for when only train is passed

if config['test'] == 'None' and config['validation'] == 'None':
    for trial in range(config['trials']):
        splits += ["data/{}/masks/split{}_{}_{}.df".format(
            config['train'],trial,config['type'],config['label'])]

columns =

rule all:
    input:
        expand("results/model={}_train={}_test={}_validate={}_feats={}_hyp?={}\
        ".format(config['model'], config['train'], config['test'],
        config['validation'],config['num_features'], config['hyperparam'])+
        '_attribute={atb}.df', atb=columns)

rule mask:
    input:
        labels
    output:
        masks
    run:
        for dataset_num in range(len(labels)):
            label = pd.read_pickle(labels[dataset_num])

            mask = supervised_model.make_mask(label, len(splits))
            mask.to_pickle(output[dataset_num], mask)

# splits will only run when cross validating (i.e. test == None)
rule split_samples:
    input:
        masks
    output:
        splits
    run:
        mask = pd.read_pickle(masks[0])
        for trial in trials#finish this, prob run sequentially to ensure diff seeds
            split = supervised_model.make_split(config['dataset'], config['cv'], trial)


rule build_model:
    input:
        features+splits
    output:
        "results/model={}_train={}_test={}_validate={}_feats={}_hyp?={}".format(
        config['model'], config['train'], config['test'], config['validation'],
        config['num_features'], config['hyperparam'])+'_attribute={atb}.df'
    threads:
        8
